# reddit-export

Captures the external URLs of Reddit submissions that you have upvoted or saved.

## Authentication

Use the PRAW [Password Flow](https://praw.readthedocs.io/en/latest/getting_started/authentication.html) and place the secrets in a `.env` file in the directory where you'll run `reddit-export`:

```
export REDDIT_CLIENT_ID=
export REDDIT_CLIENT_SECRET=
export REDDIT_USERAGENT=
export REDDIT_USERNAME=
export REDDIT_PASSWORD=
```

Alternatively you can source them separately using your favorite secret store. `env`
is included as an example of using GNU pass.

## Usage

```
$ reddit-export upvoted
$ reddit-export saved
$ reddit-export content
```

The `content` arg can resume downloads, for example if you get rate limited by a CDN you can just run it again later. Be aware that `upvoted` and `saved` will overwrite the csv files, removing the scripts awareness of download progress resulting in downloading everything again. So only run the first two commands once!

## Development

Clone the repo and install dependencies into a local virtual environment:

```bash
pip install --upgrade pip
pip install --editable .
reddit-export --help
```

## Resources

* [Reddit API docs](https://old.reddit.com/dev/api)
* [Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/index.html) - [repo](https://github.com/praw-dev/praw)

## Bugs

* no pagination yet, so results get cut off at some point (TODO)