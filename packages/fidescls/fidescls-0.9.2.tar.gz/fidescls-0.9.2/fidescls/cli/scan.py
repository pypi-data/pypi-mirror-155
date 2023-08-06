"""
CLI command wrappers for database scanning and classification functionality
"""
import pprint
import json
import click

from fastapi.encoders import jsonable_encoder

from fidescls.cli import options as _opt


@click.group(name="db")
def db() -> None:
    """
    A CLI command group focused on database scanning for classification
    """
    # pylint: disable=invalid-name
    ...


@db.command(name="classify")
@click.pass_context
@_opt.num_samples
@_opt.use_context
@_opt.use_content
@_opt.use_aggregation
@_opt.aggregation_method
@click.argument("connection_string", type=str)
@click.option(
    "-f",
    "--filename",
    "file_name",
    type=str,
    nargs=1,
    default="",
    help="filename to save database classification output json",
)
@click.option(
    "-q",
    "--quiet",
    "quiet",
    type=bool,
    default=False,
    help="Disable progress bars and feedback",
)
@click.option(
    "-e",
    "--exclude-none",
    "exclude_none",
    type=bool,
    is_flag=True,
    default=False,
    help="Exclude null objects from classification output",
)
def classify(
    ctx: click.Context,
    connection_string: str,
    file_name: str,
    use_context: bool,
    use_content: bool,
    use_aggregation: bool,
    aggregation_method: str,
    num_samples: int,
    quiet: bool,
    exclude_none: bool,
) -> None:
    """
    Classify PII in each column of each table of a database
    """
    from fidescls.cls import scan as _scan

    db_cls_output = _scan.label_database(
        connection_string,
        classify_context=use_context,
        classify_content=use_content,
        aggregate_output=use_aggregation,
        aggregation_method=aggregation_method,
        num_samples=num_samples,
        hide_progress=quiet,
    )
    if file_name:
        with open(file_name, "w", encoding="utf-8") as output_file:
            json.dump(
                jsonable_encoder(db_cls_output, exclude_none=exclude_none), output_file
            )
        click.secho(f"Classification output saved to: {file_name}")
    else:
        click.secho(
            pprint.pformat(jsonable_encoder(db_cls_output, exclude_none=exclude_none)),
            fg="white",
        )
