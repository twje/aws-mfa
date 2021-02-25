"""
Command Line Interface 
"""
import click
import requests

def setup_logger(level):    
    logging.basicConfig(
        format="time: %(asctime)s, module: %(name)s, line: %(lineno)s, level: %(levelname)s, Msg: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logger, level.upper())
    )

@click.group()
@click.option('--verbose', default='info', help='log level')
def cli(verbose):
    app.setup_logger(verbose)


def main():
    cli()


if __name__ == '__main__':
    exit(main())
