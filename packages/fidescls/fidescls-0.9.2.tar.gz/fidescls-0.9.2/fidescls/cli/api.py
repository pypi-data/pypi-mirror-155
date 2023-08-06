"""
CLI command wrappers for spinning up the Fidecsl API
"""
import subprocess as sp
import click


@click.group(name="api")
def api() -> None:
    """
    A CLI command group focused on database scanning for classification
    """
    # pylint: disable=invalid-name
    ...


@api.command(name="start")
@click.pass_context
@click.option(
    "-h", "--host", "host", type=str, default="0.0.0.0", help="host to run the api on"
)
@click.option(
    "-p", "--port", "port", type=int, default=8765, help="port number the api will use"
)
def start(ctx: click.Context, host: str, port: int) -> None:
    """
    Start the fidescls api server
    """
    sp.check_call(
        f"uvicorn --host {host} --port {port} --reload fidescls.api.main:app",
        shell=True,
    )
