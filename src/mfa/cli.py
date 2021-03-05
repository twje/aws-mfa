"""
Command Line Interface 
"""
import click
from . import app


@click.group()
@click.option('--verbose', default='info', help='log level')
def cli(verbose):
    app.setup_logger(verbose)


@cli.command('create-session')
@click.option('--profile-name', '-pn', required=True, help='AWS MFA profile in .aws/config')
@click.option('--temporary-profile-name', '-tpn', required=True, help='Temporary AWS profile associated with the MFA session')
@click.option('--duration', '-d', default=3600, show_default=True, type=click.IntRange(900, 3600, clamp=True), help='Duration in seconds the temporary profile is valid for')
def create_session_cmd(profile_name, temporary_profile_name, duration):
    """Generate a temporary AWS profile with an MFA session that persists for duration"""
    app.create_session(profile_name, temporary_profile_name, duration)
    print("AWS MFA session tied to profile '{temporary_profile_name}'")


def main():
    cli()


if __name__ == '__main__':
    exit(main())
