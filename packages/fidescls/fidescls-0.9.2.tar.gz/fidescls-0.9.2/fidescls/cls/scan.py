"""
Utility functionality to support the scanning of a database for PII
"""

from collections import defaultdict
from typing import Callable, Dict, List, Union
import warnings

import click
import pandas as pd
from sqlalchemy.engine.base import Engine
from tqdm import tqdm

from fidescls.cls import content, context, aggregation, models as _cls_models
from fidescls.utils import databases as _db

try:
    from fideslang import default_taxonomy
except ModuleNotFoundError:
    raise click.ClickException("Unable to find fideslang, please install!")


def nested_default_dict() -> defaultdict[defaultdict]:  # type: ignore
    """
    Create an infinitely nestable dictionary
    """
    return defaultdict(nested_default_dict)


def db_context_classify(
    metadata_df: pd.DataFrame,
    context_method: Callable = context.classify,
    method_params: Dict = {},
    hide_progress: bool = False,
) -> defaultdict:
    """
    Perform context classification given a database's schema metadata
    Args:
        metadata_df: dataframe containing database metadata
        context_method: method to use when performing context classification
        method_params: context classification method kwargs
        hide_progress: flag to disable displaying of progress bars

    Returns:
        Nested dictionary containing schema:table:column = [classification results]
    """
    if not hide_progress:
        click.secho("Classifying database context...", fg="white")

    if not method_params.get("possible_targets"):
        taxonomy = default_taxonomy.DEFAULT_TAXONOMY
        method_params["possible_targets"] = [
            i.fides_key for i in taxonomy.data_category
        ]

    context_labels = nested_default_dict()
    for _, row in tqdm(
        metadata_df.iterrows(),
        total=metadata_df.shape[0],
        disable=hide_progress,
        desc="Tables",
        position=0,
    ):
        for column in tqdm(
            row["columns"],
            disable=hide_progress,
            desc="Columns",
            leave=False,
            position=1,
        ):
            context_labels[row["schema"]][row["table"]][column] = list(
                context_method(
                    f"{row['schema']}.{row['table']}.{column}",
                    method_name="similarity",
                    method_params=method_params,
                )
            )
    return context_labels


def db_content_classify(
    db_engine: Engine,
    metadata_df: pd.DataFrame,
    num_samples: int = 1,
    content_method: Callable = content.classify,
    method_params: dict = {},
    hide_progress: bool = False,
) -> defaultdict[defaultdict]:  # type: ignore
    """
    Perform content classification on a sample dataset taken from tables in a database
    Args:
        db_engine: sqlalchemy database engine
        metadata_df: dataframe containing database metadata
        num_samples: number of samples to take from each table
        content_method: method to use when performing content classification
        method_params: content classification method kwargs
        hide_progress: flag to disable displaying of progress bars

    Returns:
        Nested dictionary containing schema:table:column = [classification results]
    """
    if not hide_progress:
        click.secho(
            f"Classifying database content using {num_samples} sample(s)..", fg="white"
        )

    data_samples_cls = nested_default_dict()
    for _, row in tqdm(
        metadata_df.iterrows(),
        total=metadata_df.shape[0],
        disable=hide_progress,
        desc="Samples",
        position=0,
    ):
        table_samples = _db.get_table_samples(
            db_engine,
            schema_name=row["schema"],
            table_name=row["table"],
            num_samples=num_samples,
        )
        if table_samples:
            data_samples_cls[row["schema"]][row["table"]] = content_method(
                table_samples, **method_params
            )
        else:
            # no samples were returned from the query to the table
            data_samples_cls[row["schema"]][row["table"]] = {
                k: [_cls_models.MethodClassification(input="", labels=[])]
                for k in row["columns"]
            }
    return data_samples_cls


def db_aggregate_system(
    scan_output: Dict,
    aggregation_method: str,
    aggregation_params: Dict,
    hide_progress: bool = False,
    structure_source: str = "context",
) -> defaultdict:
    """
    Perform system level aggregation on the database scanning and classification output
    Args:
        scan_output: The classification output from a database scan
        aggregation_method: The method by which to aggregate (default: weighted)
        aggregation_params: The kwargs to be passed onto the aggregation method
        hide_progress: Flag to high processing progress bars
        structure_source: classification paradigm name to use when traversing db structure

    Returns:
        The aggregated database classification
    """

    if not hide_progress:
        click.secho(
            "Aggregating context and content classification output..", fg="white"
        )
    aggregated_output = nested_default_dict()
    for schema_name, schema in tqdm(
        scan_output[structure_source].items(),
        total=len(scan_output["context"]),
        disable=hide_progress,
        desc="Schema",
        position=0,
    ):
        for table_name, table in tqdm(
            schema.items(),
            total=len(schema),
            disable=hide_progress,
            desc="Tables",
            position=1,
            leave=False,
        ):
            for column_name, _ in tqdm(
                table.items(),
                total=len(table),
                disable=hide_progress,
                desc="Columns",
                position=2,
                leave=False,
            ):
                aggregated_output[schema_name][table_name][
                    column_name
                ] = aggregation.aggregate_system(
                    scan_output["context"][schema_name][table_name][column_name],
                    check_column_continuity(
                        scan_output, schema_name, table_name, column_name
                    ),
                    aggregation_method=aggregation_method,
                    aggregation_params=aggregation_params,
                )
    return aggregated_output


def check_column_continuity(
    scan_output: Dict,
    schema_name: str,
    table_name: str,
    column_name: str,
    paradigm_to_check: str = "content",
) -> List:
    """
    Ensure that a column is present in both the content and context database scanning output.
    If not, add said column with an empty classification output.
    Args:
        scan_output: The output from a database scanning operation
        schema_name: The schema to check for parity
        table_name: The table to check for parity
        column_name: The column to check for parity
        paradigm_to_check: The paradigm (content, context) on which to check parity

    Returns:
        The list of classifications for a given column with any missing columns
        given an empty classification using the structure_source as the ground truth
    """
    try:
        return scan_output[paradigm_to_check][schema_name][table_name][column_name]
    except KeyError:
        warnings.warn(
            f"Mismatch in column parity for {'.'.join([schema_name, table_name, column_name])}! "
            f"Inferring no {paradigm_to_check} classification"
        )
        return [
            _cls_models.AggregatedMethodClassification(
                input="",
                labels=[
                    _cls_models.AggregatedMethodLabel(
                        classification_paradigm="inferred"
                    )
                ],
                aggregation_method="inferred",
            )
        ]


def label_database(
    connection_string: str,
    classify_context: bool = False,
    classify_content: bool = False,
    aggregate_output: bool = False,
    context_method: Callable = context.classify,
    content_method: Callable = content.classify,
    aggregation_method: Union[None, str] = "weighted",
    context_method_params: Dict = {},
    content_method_params: Dict = {
        "decision_method": "direct-mapping",
        "aggregation_method": "mean",
    },
    aggregation_params: Dict = {"top_n": 3},
    num_samples: int = 10,
    hide_progress: bool = False,
) -> Union[Dict[str, Dict], defaultdict]:
    """
    Perform context and/or content classification on a mysql or postgres database
    Args:
        connection_string:  sqlalchemy compatible database connection string
        classify_context: flag to perform context classification (default: False)
        classify_content: flag to perform content classification (default: False)
        aggregate_output: flag to perform system level classification aggregation (default: False)
        context_method: method to use when performing context classification
        content_method: kwargs to pass to the context classification method
        aggregation_method: method used to perform system aggregation
        context_method_params: method kwargs to pass to the context classification method
        content_method_params: method kwargs to pass to the context classification method
        aggregation_params: method kwargs to pass to the system aggregation method
        num_samples: number of samples to use when collecting data for content classification
        hide_progress: flag to disable progress bars and feedback

    Returns:
        Dictionary containing the results for content and/or context classification
        for each column in each table of the database
    """
    # check to see that any inspection is happening
    if not classify_context and not classify_content:
        raise click.exceptions.ClickException("No classification method selected!")

    db_engine = _db.get_engine(connection_string, verbose=True)
    db_metadata = _db.scan_database_metadata(
        connection_string, hide_progress=hide_progress
    )
    metadata_df = _db.metadata_to_dataframe(db_metadata)

    dataset_labels = {}
    if classify_context and context_method:
        context_cls_results = db_context_classify(
            metadata_df,
            context_method=context_method,
            method_params=context_method_params,
            hide_progress=hide_progress,
        )
        dataset_labels["context"] = context_cls_results

    if classify_content and content_method:
        content_cls_results = db_content_classify(
            db_engine,
            metadata_df,
            num_samples=num_samples,
            content_method=content_method,
            method_params=content_method_params,
            hide_progress=hide_progress,
        )
        dataset_labels["content"] = content_cls_results
    if aggregate_output and aggregation_method:
        if not {"context", "content"}.issubset(dataset_labels.keys()):
            raise ValueError(
                "System aggregation only available when both content and context classification are specified!"
            )
        return db_aggregate_system(
            dataset_labels,
            aggregation_method=aggregation_method,
            aggregation_params=aggregation_params,
            hide_progress=hide_progress,
        )
    return dataset_labels  # type: ignore
