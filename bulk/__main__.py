import pathlib

import typer
from bokeh.server.server import Server
from bokeh.util.browser import view
from tornado.ioloop import IOLoop

from bulk.text import bulk_text
from bulk.vision import bulk_vision
from bulk.util import app as util_app

app = typer.Typer(
    name="bulk",
    add_completion=False,
    help="Tools for bulk labelling.",
    no_args_is_help=True,
)
app.add_typer(util_app, name="util")



@app.command("version")
def version():
    """Prints the version."""
    print("0.1.0")


@app.command("text")
def text(path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
         keywords: str = typer.Option(None, help="Keywords to highlight")):
    """Bulk Labelling for Text"""
    if keywords:
        keywords = keywords.split(",")
    server = Server({"/": bulk_text(path, keywords=keywords)}, io_loop=IOLoop())
    server.start()
    host = "http://localhost:5006/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


@app.command("vision")
def vision(path: pathlib.Path = typer.Argument(..., help="Path to .csv file", exists=True),
           port: int = typer.Argument(5006, help="Port number")):
    """Bulk Labelling for Images"""
    server = Server({"/": bulk_vision(path)}, io_loop=IOLoop())
    server.start()
    host = f"http://localhost:{port}/"
    print(f"About to serve `bulk` over at {host}.")
    server.io_loop.add_callback(view, host)
    server.io_loop.start()


if __name__ == '__main__':
    app()
