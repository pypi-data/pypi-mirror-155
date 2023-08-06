import os

import click
from sbml2dae.dae_model import DaeModel
from sbml2dae.matlab import Matlab


@click.group()
def cli():
    """SBML2Dae Command Line Interface (sbml2dae)."""


@cli.command(short_help="Export model")
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-o", "--output", type=click.Path(exists=True), help="Set the output path to export files."
)
def export(input_file, output):
    """Export the INPUT_FILE sbml model to Matlab."""

    # Get the filename (without extension) and the extension.
    base = os.path.basename(input_file)
    (filename, extension) = os.path.splitext(base)

    # Default value of output is './build/'
    if output is None:
        output = "./build"

    # Create build dir if it doesn't exist.
    if not os.path.isdir(output):
        os.mkdir(output)
        print(f'Created dir "{output}"')

    output = os.path.abspath(output)

    # Check if output dir doesn't exists.
    if not os.path.isdir(output):
        print(f'Created output directory "{output}".')
        os.mkdir(output)

    sbml2matlab(input_file, output)


def sbml2matlab(sbml_filename, output):
    """Convert a sbml file into matlab."""
    print("### Convert sbml into matlab ###")

    # Generate dae model representaion.
    dae = DaeModel(sbml_filename)
    print("\tExtract DAE model from sbml model.")

    # Export into matlab files.
    matlab = Matlab(dae, output)

    filepath = matlab.export_example()
    print(f"\tGenerated {filepath}")

    filepath = matlab.export_class()
    print(f"\tGenerated {filepath}")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
