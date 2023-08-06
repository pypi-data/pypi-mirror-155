"""
High level functionality around performing PII classification
"""
import logging
from typing import cast, List, Dict, Union
import numpy as np

from presidio_analyzer import RecognizerResult

from fidescls.cls import (
    decision,
    classifiers,
    config as _cls_config,
    models as _cls_models,
    aggregation as _cls_agg,
    entity_map as _cls_entities,
)

logger = logging.getLogger(__name__)


def format_method_labels(
    method_result: Union[None, RecognizerResult]
) -> _cls_models.MethodLabel:
    """
    Standardized the format of the recognizer results
    Args:
        method_result: A recognizer result
    """
    if method_result:
        return _cls_models.MethodLabel(
            label=method_result.entity_type,
            score=np.round(method_result.score, decimals=4),
            position_start=method_result.start,
            position_end=method_result.end,
        )
    return _cls_models.MethodLabel()


def format_cls_output(
    input_data: Union[List[str], Dict[str, List]],
    cls_output: List[Union[List[RecognizerResult], Dict[str, List[RecognizerResult]]]],
) -> Union[
    List[_cls_models.MethodClassification],
    Dict[str, List[_cls_models.MethodClassification]],
]:
    """
    Format the content classifier's output to meet the spec
    Args:
        input_data: The data that was classified
        cls_output: The output of the classifier

    Returns:
        Formatted classification output to conform to the spec
    """
    formatted_output: Union[
        List[_cls_models.MethodClassification],
        Dict[str, List[_cls_models.MethodClassification]],
    ]
    labels: Union[None, _cls_models.MethodLabel, List[_cls_models.MethodLabel]]

    if isinstance(cls_output, list) and isinstance(cls_output[0], list):
        formatted_output = []
        for i, input_value in enumerate(input_data):
            labels = [format_method_labels(cls_out) for cls_out in cls_output[i]]
            formatted_output.append(
                _cls_models.MethodClassification(input=input_value, labels=labels)
            )
    else:
        formatted_output = {}
        for cls_out in cls_output:
            cls_out_casted = cast(
                Dict[str, Union[str, List[RecognizerResult]]], cls_out
            )
            cls_out_result = cast(
                List[RecognizerResult], cls_out_casted["recognizer_results"]
            )
            cls_out_key = cast(str, cls_out_casted["key"])
            parsed_output = []
            for i, input_value in enumerate(cls_out_casted["value"]):
                if cls_out_result[i]:
                    labels = [
                        format_method_labels(j)
                        if cls_out_result[i]
                        else _cls_models.MethodLabel()
                        for j in cls_out_result[i]
                    ]
                else:
                    labels = []
                parsed_output.append(
                    _cls_models.MethodClassification(input=input_value, labels=labels)
                )
            formatted_output[cls_out_key] = parsed_output
    return formatted_output


def classify(
    data: Union[str, List[str], Dict[str, List]],
    language: str = _cls_config.LANGUAGE,
    model: str = None,
    decision_method: str = "direct-mapping",
    aggregation_method: Union[str, None] = None,
    infer_not_pii: bool = True,
) -> Union[
    List[_cls_models.MethodClassification],
    Dict[str, List[_cls_models.MethodClassification]],
]:
    """
    Perform a PII classification on data using the specified model and decision method
    Args:
        data: Data to be classified (list or dictionary)
        language: language for text model purposes. supported: ['en']
        model: specify which model to use. Default (None, "") is the BaseTextClassifier
        decision_method: specify which decision method to use. supported:
            'pass-through': direct pass-through of results from the model
            'direct-mapping': the mapped value described by an entity map
        aggregation_method: the method to use when aggregating the classification output
        infer_not_pii: flag to infer not pii score based on occurrence if a not-pii label is not a class label
    Returns:
        The output from the classifier in the format dependent on the chosen `decision_method`

    """
    if isinstance(data, str):
        data = [data]
    logger.debug(f"Classifying {data} using decision: {decision_method}")
    if not model:
        cls = classifiers.BaseTextClassifier()
    else:
        raise NotImplementedError("Only default model supported currently!")

    # perform the classification
    cls_label = cls.classify(
        data, language=language, entities=list(_cls_entities.ENTITIES.keys())
    )

    # format the classification output
    cls_label = format_cls_output(data, cls_label)

    # aggregate the classification output
    if aggregation_method:
        cls_label = _cls_agg.aggregate_classification(
            cls_label,
            aggregation_method=aggregation_method,
            infer_not_pii=infer_not_pii,
        )
    # implement any decision based on return if requested
    decision_result = decision.decide(cls_label, decision_method)
    return decision.rank_classification_results(decision_result)
