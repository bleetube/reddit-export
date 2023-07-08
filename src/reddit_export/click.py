import click
import logging
from .fetcher import RedditExport

# console logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

fetcher = RedditExport(log_level=logger.getEffectiveLevel())

@click.group()
def cli():
    pass

#@click.command()
#@click.argument('myarg')
#@click.option('--myflag', help='', is_flag=True)
#def check_group(group_name, add_missing=False, fix_names=False):

@click.command()
def saved():
    fetcher.get_saved()

@click.command()
def upvotes():
    fetcher.get_upvotes()

cli.add_command(upvotes)
cli.add_command(saved)