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
    fetcher.get_items('saved')

@click.command()
def upvoted():
    fetcher.get_items('upvoted')

cli.add_command(upvoted)
cli.add_command(saved)