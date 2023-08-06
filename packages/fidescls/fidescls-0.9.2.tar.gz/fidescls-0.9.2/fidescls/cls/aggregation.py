"""
Classification output aggregation functionality
"""

# pylint: disable=invalid-name

import collections
from typing import Dict, List, Tuple, Union
import warnings
import numpy as np
from fidescls.cls import models as _cls_models

AGGREGATION_METHODS = {"mean": np.nanmean, "max": np.nanmax, "median": np.nanmedian}

CLS_OUTPUT_TYPE = Union[
    List[_cls_models.MethodClassification],
    Dict[str, List[_cls_models.MethodClassification]],
]
AGG_CLS_OUTPUT_TYPE = Union[
    List[_cls_models.AggregatedMethodClassification],
    Dict[str, List[_cls_models.AggregatedMethodClassification]],
]


def validate_aggregation_method(method: str) -> None:
    """
    Check to see if the specified aggregation method is supported
    Args:
        method: the name of the aggregation method

    Raises:
        ValueError: if the provided aggregation method is not supported
    """
    if method not in AGGREGATION_METHODS.keys():
        raise ValueError(
            f"{method} is not a valid aggregation method!"
            f'Must be one of [{", ".join(AGGREGATION_METHODS.keys())}]'
        )


def aggregate_scores(
    cls_outputs: List[_cls_models.MethodClassification],
    aggregation_method: str,
    infer_not_pii: bool = True,
    paradigm: str = "content",
) -> List[_cls_models.AggregatedMethodLabel]:
    """

    Args:
        cls_outputs:
        aggregation_method:
        infer_not_pii: infer the presence of pii as a percentage of not pii labels to number of samples
        paradigm: classification paradigm from which the label was derived

    Returns:
        a list of the aggregated scores grouped by classification label
    """
    validate_aggregation_method(aggregation_method)

    grouped_results = collections.defaultdict(list)
    not_pii_count = 0

    for output in cls_outputs:
        if not output.labels:
            not_pii_count += 1
            continue
        for label in output.labels:
            grouped_results[label.label].append(label.score)

    aggregated_scores = []
    for label, scores in grouped_results.items():
        aggregated_scores.append(
            _cls_models.AggregatedMethodLabel(
                label=label,
                score=AGGREGATION_METHODS[aggregation_method](scores),  # type: ignore
                classification_paradigm=paradigm,
            )
        )
    if infer_not_pii and not_pii_count > 0:
        aggregated_scores.append(
            _cls_models.AggregatedMethodLabel(
                label=None,
                score=np.clip(
                    np.round(not_pii_count / len(cls_outputs), decimals=3), 0, 1
                ),
                classification_paradigm=paradigm,
            )
        )
    return aggregated_scores


def aggregate_classification(
    cls_output: CLS_OUTPUT_TYPE,
    aggregation_method: str,
    infer_not_pii: bool = True,
    paradigm: str = "content",
) -> AGG_CLS_OUTPUT_TYPE:
    """
    Aggregate classification output using the specified aggregation method
    Args:
        cls_output: classification output
        aggregation_method: aggregation method name
        infer_not_pii: flag to infer not pii class label score if classification
        method does not have such a class label
        paradigm: classification paradigm from which the label was derived

    Returns:

    """

    validate_aggregation_method(aggregation_method)

    aggregated_output: Union[
        List[_cls_models.AggregatedMethodClassification],
        Dict[str, List[_cls_models.AggregatedMethodClassification]],
    ]

    if isinstance(cls_output, dict):
        aggregated_output = {}
        for key, cls_results in cls_output.items():
            aggregated_output[key] = [
                _cls_models.AggregatedMethodClassification(
                    input=[i.input for i in cls_results],
                    labels=aggregate_scores(
                        cls_results,
                        aggregation_method=aggregation_method,
                        infer_not_pii=infer_not_pii,
                        paradigm=paradigm,
                    ),  # need to unpack/extend a list of lists i forget the function
                    aggregation_method=aggregation_method,
                )
            ]
    else:
        aggregated_output = []
        aggregated_output.append(
            _cls_models.AggregatedMethodClassification(
                input=[i.input for i in cls_output],
                labels=aggregate_scores(
                    cls_output,
                    aggregation_method=aggregation_method,
                    infer_not_pii=infer_not_pii,
                    paradigm=paradigm,
                ),  # need to unpack/extend a list of lists i forget the function
                aggregation_method=aggregation_method,
            )
        )
    return aggregated_output


def validate_system_aggregation_weights(
    context_weight: float = 0.55,
    content_weight: float = 0.45,
    prefer_context: bool = True,
    **kwargs: Dict,
) -> Tuple[float, float]:
    """
    Validate and/or set the system aggregation weights for
    context and content classification aggregation
    Args:
        context_weight: classification score multiplication factor
        content_weight: classification score multiplication factor
        prefer_context: boolean to prefer the weight associated with
        context if there's a conflict

    Returns:
        validated set of weights (context, content)

    """
    min_weight = 0.0
    max_weight = 1.0
    if (
        not min_weight < context_weight < max_weight
        or not min_weight < content_weight < max_weight
    ):
        raise ValueError(
            f"System aggregation weights must be [0.0, 1.0], {context_weight} and {content_weight} provided!"
        )
    if context_weight + content_weight != 1.0:
        warnings.warn(
            f"System aggregation weights ({context_weight} and {content_weight}) do not sum to 1.0."
            f'Using preferred weight: {"context" if prefer_context else "content"}'
        )
        if prefer_context:
            precision = str(context_weight)[::-1].find(".")
            content_weight = np.round(1.0 - context_weight, decimals=precision)
        else:
            precision = str(content_weight)[::-1].find(".")
            context_weight = np.round(1.0 - content_weight, decimals=precision)
    return context_weight, content_weight


def adjust_scores_by_weight(cls_output: List, weight: float) -> List:
    """
    Adjust classification scores by the specified weight
    Args:
        cls_output: the classification output to be adjusted
        weight: the weight by which to adjust the classification score

    Returns:
        The classification output with a new weighted score attribute
    """
    for classification in cls_output:
        for label in classification.labels:
            if label.score:
                label.aggregated_score = np.round(label.score * weight, decimals=4)
            else:
                label.aggregated_score = 0.0
    return cls_output


def merge_classifications(
    context_classification: List,
    content_classification: List,
    aggregation_method: str,
    aggregation_params: Dict,
    sort_attribute: str = "aggregated_score",
    desc: bool = True,
) -> _cls_models.AggregatedSystemClassification:
    """
    Merge content and context classification results together in a system aggregation data model
    Args:
        context_classification: results from a context classification
        content_classification: results from a content classification
        aggregation_method: name of the method by which to aggregate
        aggregation_params: parameters to be passed into the aggregation method
        sort_attribute:  data model attribute by which to sort classification labels
        desc: flag to set ordering direction

    Returns:

    """
    merged_classifications = _cls_models.AggregatedSystemClassification()
    merged_classifications.aggregation_method = aggregation_method
    merged_classifications.aggregation_params = aggregation_params

    context_inputs = []
    content_inputs = []
    for classification in context_classification:
        context_inputs.extend(
            classification.input
            if isinstance(classification.input, list)
            else [classification.input]
        )
        merged_classifications.aggregated_labels.extend(
            [
                _cls_models.AggregatedMethodLabel(
                    label=i.label,
                    score=i.score,
                    aggregated_score=i.aggregated_score,
                    classification_paradigm="context",
                )
                for i in classification.labels
            ]
        )
    merged_classifications.context_input = context_inputs
    for classification in content_classification:
        content_inputs.extend(
            classification.input
            if isinstance(classification.input, list)
            else [classification.input]
        )
        merged_classifications.aggregated_labels.extend(classification.labels)
    merged_classifications.content_input = content_inputs
    # score the labels by their weighted scores
    merged_classifications.aggregated_labels.sort(
        key=lambda x: (getattr(x, sort_attribute) is None, getattr(x, sort_attribute)),
        reverse=desc,
    )
    # perform de-duplication after sorting and keep the first occurrence of a label
    return merged_classifications


def deduplicate_aggregated_labels(
    labels: List[_cls_models.AggregatedMethodLabel],
) -> List[_cls_models.AggregatedMethodLabel]:
    """
    Remove duplicated labels in an aggregated set of classification labels; retaining
    the first occurrence
    Args:
        labels: list of labels to deduplicate

    Returns:

    """
    unique_labels: List = []
    for label in labels:
        if label.label not in {i.label for i in unique_labels}:
            unique_labels.append(label)
    return unique_labels


def aggregate_system(
    context_classification: List,
    content_classification: List,
    aggregation_method: str = "weighted",
    aggregation_params: Dict = {},
) -> _cls_models.AggregatedSystemClassification:
    """
    Aggregate context and content classification results
    Args:
        context_classification: results from a context classification
        content_classification: results from a content classification
        aggregation_method: name of the method by which to aggregate [default: 'weighted']
        aggregation_params: parameters to be passed into the aggregation method

    Returns:

    """
    # weighted aggregation is the only implementation, currently
    # when more methods get added, this will have to be abstracted
    if aggregation_method != "weighted":
        raise ValueError(f"Aggregation method, {aggregation_method}, not supported!")

    # get the aggregation weights
    context_weight, content_weight = validate_system_aggregation_weights(
        **aggregation_params
    )

    # adjust scores by weight factor
    adjust_scores_by_weight(context_classification, context_weight)
    adjust_scores_by_weight(content_classification, content_weight)

    aggregated_classifications = merge_classifications(
        context_classification,
        content_classification,
        aggregation_method,
        aggregation_params,
    )

    # return top n labels removing duplicated labels
    aggregated_classifications.aggregated_labels = deduplicate_aggregated_labels(
        aggregated_classifications.aggregated_labels
    )[: aggregation_params.get("top_n", 1)]

    return aggregated_classifications
