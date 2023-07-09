import click
import logging
from .fetcher import RedditExport

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

fetcher = RedditExport(log_level=logger.getEffectiveLevel())

@click.group()
def cli():
    pass

@click.command()
def saved():
    fetcher.get_items('saved')

@click.command()
def upvoted():
    fetcher.get_items('upvoted')

@click.command()
def content():
    fetcher.capture_content()

cli.add_command(content)
cli.add_command(upvoted)
cli.add_command(saved)