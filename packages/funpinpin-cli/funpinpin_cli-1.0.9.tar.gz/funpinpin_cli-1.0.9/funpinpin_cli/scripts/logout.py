import click

from funpinpin_cli.core.logout import Logout


@click.command("logout")
def logout():
    """
    \b
    \033[96mlogout\033[0m: Log out of an authenticated partner organization and store, or clear invalid credentials
      Usage: \033[96mfunpinpin logout\033[0m
    """
    logout = Logout()
    logout.run()
    click.echo("Successfully logged out of your account")
