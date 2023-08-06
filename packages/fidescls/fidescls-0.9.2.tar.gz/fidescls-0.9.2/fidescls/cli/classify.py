"""
CLI command wrappers for classify functionality
"""

import pprint
from typing import cast
import click

from fidescls.cli import options as _opt

from fidescls.cls import models as _cls_models


@click.group(name="classify")
def classify() -> None:
    """
    A CLI command group focused on PII classification methods
    """
    ...


@classify.command(name="content")
@click.pass_context
@_opt.language
@_opt.model
@_opt.decision_method
@click.argument("data", type=str)
def content(
    ctx: click.Context, data: str, language: str, model: str, decision_method: str
) -> None:
    """
    Detect and classify PII content

    DATA: data string to be processed (comma separated)
    """
    from fidescls.cls import content as _content

    cls_output = _content.classify(
        [i.strip() for i in data.split(",")],
        language=language,
        model=model,
        decision_method=decision_method,
    )
    click.secho(
        pprint.pformat(
            [cast(_cls_models.MethodClassification, i).dict() for i in cls_output]
        ),
        fg="white",
    )


@classify.command(name="context")
@click.pass_context
@_opt.top_n
@_opt.possible_targets
@_opt.remove_stop_words
@_opt.pii_threshold
@click.argument("data", type=str)
def context(
    ctx: click.Context,
    data: str,
    top_n: int,
    possible_targets: str,
    remove_stop_words: bool,
    pii_threshold: float,
) -> None:
    """
    PII context classification

    DATA: data string to be processed (comma separated)
    """
    from fidescls.cls import context as _context

    if not possible_targets:
        raise click.BadArgumentUsage(
            "No possible targets were provided! They are required for context classification."
        )
    cls_output = _context.classify(
        [i.strip() for i in data.split(",")],
        method_name="similarity",
        method_params={
            possible_targets: [i.strip() for i in possible_targets.split(",")],
            top_n: top_n,
            remove_stop_words: remove_stop_words,
            pii_threshold: pii_threshold,
        },
    )
    click.secho(pprint.pformat([i.dict() for i in cls_output]), fg="white")
