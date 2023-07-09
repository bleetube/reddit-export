from os import environ, getcwd, path, makedirs
from csv import DictReader, DictWriter
import subprocess
import logging, json
import praw
import re
import requests
from time import sleep
from pprint import pprint

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
# https://praw.readthedocs.io/en/latest/code_overview/models/redditor.html
print([item.id for item in reddit.user.me().upvoted(limit=10)])
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

    def capture_content(self):
        """Read the csv files, call yt-dlp to download the content, and update the csv files with the local path"""

        yt_dlp_domains = [
            'v.redd.it',
            'redgifs.com',
        ]
        image_extensions = [
            'jpg',
            'jpeg',
            'png',
            'gif',
            'gifv',
        ]

        for item_type in ['saved', 'upvoted']:
            csv_file = f"{self.data_dir}/{item_type}.csv"
            with open(csv_file, 'r') as file:
                csv_reader = DictReader(file)
                rows = list(csv_reader)
            output_dir = f"{self.data_dir}/{item_type}"
            makedirs(output_dir, exist_ok=True)
            for row in rows:
                if row.get('destination'):
                    logging.debug("Skipping {url} because it has already been downloaded as {destination}".format(**row))
                    continue
                url = row['url'].replace('^http:', 'https:').replace('gfycat.com', 'redgifs.com/watch')
                row_index = rows.index(row)

                # Save images
                if any(url.endswith(ext) for ext in image_extensions):
                    destination = f"{row['id']}.{url.split('.')[-1]}"
                    logging.info(f"Downloading {url} to {item_type}/{destination}")

                    try:
                        response = requests.get(url)
                        with open(f"{output_dir}/{destination}", 'wb') as f:
                            f.write(response.content)
                        rows[row_index]['destination'] = destination
                    except Exception as e:
                        logging.warning(f"Failed to download {url}: {e}")
#                       rows[row_index]['destination'] = ''
                        pass
                        continue

                # Call yt-dlp on videos
                if any(domain in url for domain in yt_dlp_domains):
                    try:
                        result = subprocess.run(['yt-dlp', url], check=True, cwd=output_dir, stdout=subprocess.PIPE)
                        output = result.stdout.decode('utf-8')
                        logging.info(output)
                        match = re.search(r'\[download\] Destination: (.*)', output)
                        destination = match.group(1) if match else ''
                        rows[row_index]['destination'] = destination
                        logging.info(f"Downloaded {url} to {output_dir}/{destination}")
                    except Exception as e:
#                       rows[row_index]['destination'] = ''
                        logging.warning(f"Failed to download {url}: {e}")
                        pass
                        continue

                with open(csv_file, 'w') as file:
                    csv_writer = DictWriter(file, fieldnames=['id', 'url', 'destination'])
                    csv_writer.writeheader()
                    csv_writer.writerows(rows)
                sleep(1)


    def get_items(self, item_type):
        items = dict()
        for item in getattr(self.reddit.user.me(), item_type)(limit=1000):
            try:
                items[item.id] = item.url
                logging.debug(f"{item.id}: {item.url}")
            except Exception as e:
                logging.debug(e)
                pass

        csv_file = f"{self.data_dir}/{item_type}.csv"
        logging.info(f"Exporting {item_type} items to {csv_file}")
        with open(csv_file, 'w') as file:
            csv_writer = DictWriter(file, fieldnames=['id', 'url','destination'])
            csv_writer.writeheader()
            for key, value in items.items():
                csv_writer.writerow({'id': key, 'url': value, 'destination': ''})

    """Trying to figure out how to paginate:
    def get_items(self, item_type):
        items = dict()
        after = None
        while True:
#           results = getattr(self.reddit.user.me(), item_type)(limit=100, after=after)
            for item in results:
                try:
                    items[item.id] = item.url
                    logging.debug(f"{item.id}: {item.url}")
                except Exception as e:
                    logging.debug(e)
                    pass
            if len(results) < 100:
                break
            after = results[-1].id

        csv_file = f"{self.data_dir}/{item_type}.csv"
        logging.info(f"Exporting {item_type} items to {csv_file}")
        with open(csv_file, 'w') as file:
            csv_writer = DictWriter(file, fieldnames=['id', 'url'])
            csv_writer.writeheader()
            for key, value in items.items():
                csv_writer.writerow({'id': key, 'url': value})
    """

"""does a file exist:
    if not path.exists(device_cache) or time() - path.getmtime(device_cache) > cache_age_sec:
        servicenow_devices = servicenow_api.get_devices_by_company_sys_id(group_sys_ids[group_name])
        with open(device_cache, 'w') as file:
            logging.info(f"Writing {device_cache}")
            file.write(json.dumps(servicenow_devices))
        return servicenow_devices
"""