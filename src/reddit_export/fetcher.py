from os import environ, getcwd, path
from csv import DictReader, DictWriter
import logging, json
import praw
import pprint

"""Testing PRAW:
from os import environ
import praw
reddit = praw.Reddit(
    client_id = environ.get("REDDIT_CLIENT_ID"),
    client_secret = environ.get("REDDIT_CLIENT_SECRET"),
    user_agent = environ.get("REDDIT_USERAGENT"),
    username = environ.get("REDDIT_USERNAME"),
    password = environ.get("REDDIT_PASSWORD"),
)
reddit.user.me()
"""

class RedditExport():
    """RedditExport class"""

    def __init__(self, log_level=logging.INFO) -> None:
        """Instantiate an instance of PRAW using credentials for a script-type OAuth application"""

        # https://praw.readthedocs.io/en/stable/getting_started/authentication.html
        # Password Flow
        self.reddit = praw.Reddit(
            client_id = environ.get("REDDIT_CLIENT_ID"),
            client_secret = environ.get("REDDIT_CLIENT_SECRET"),
            password = environ.get("REDDIT_PASSWORD"),
            user_agent = environ.get("REDDIT_USERAGENT"),
            username = environ.get("REDDIT_USERNAME"),
        )
        self.data_dir = environ.get("DATA_DIR", getcwd())
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

    def get_items(self, item_type):
        items = dict()
        for item in getattr(self.reddit.user.me(), item_type)():
            try:
                items[item.id] = item.url
                logging.debug(f"{item.id}: {item.url}")
            except Exception as e:
                logging.debug(e)
                pass

        csv_file = f"{self.data_dir}/{item_type}.csv"
        logging.info(f"Exporting {item_type} items to {csv_file}")
        with open(csv_file, 'w') as file:
            csv_writer = DictWriter(file, fieldnames=['id', 'url'])
            csv_writer.writeheader()
            for key, value in items.items():
                csv_writer.writerow({'id': key, 'url': value})

"""does a file exist:
    if not path.exists(device_cache) or time() - path.getmtime(device_cache) > cache_age_sec:
        servicenow_devices = servicenow_api.get_devices_by_company_sys_id(group_sys_ids[group_name])
        with open(device_cache, 'w') as file:
            logging.info(f"Writing {device_cache}")
            file.write(json.dumps(servicenow_devices))
        return servicenow_devices
"""