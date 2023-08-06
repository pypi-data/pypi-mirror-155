from pathlib import Path
import typer
import xml.dom.minidom


app = typer.Typer()


def main():
    app()


@app.command()
def run(
    fp: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        help="Path to the XML file that should be prettified.",
    )
):
    with open(fp, "r") as f:
        dom = xml.dom.minidom.parse(f)
        pretty = dom.toprettyxml()
    print(pretty)


if __name__ == "__main__":
    app()
