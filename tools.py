"""
Command Line Interface 
"""
from pathlib import Path
import os
import click

ROOT = Path(__file__).expanduser().resolve().parent

@click.group()
def cli():
    pass

@cli.command('generate-requirements')
def cmd_generate_requirements():
    """Generate requirements file for development"""    
    
    for env in ('dev', 'test'):
        source = Path(ROOT, "requirements", f"{env}.txt")
        target = Path(ROOT, "requirements", f"{env}.in")
        os.system(f"pip-compile --output-file={source} {target}")


@cli.command('generate-requirements')
def cmd_generate_requirements():
    """Generate requirements file for development"""    
    
    for env in ('dev', 'test'):
        source = Path(ROOT, "requirements", f"{env}.txt")
        target = Path(ROOT, "requirements", f"{env}.in")
        os.system(f"pip-compile --output-file={source} {target}")


def main():
    cli()


if __name__ == '__main__':
    exit(main())
