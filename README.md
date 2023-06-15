
## Modmail Auto-Responder Bot

This script creates a Reddit bot that auto-responds to Modmail messages that contain specific keywords in the message subject or body. It utilizes the Python Reddit API Wrapper (PRAW) to interact with Reddit's API.

### Features

The bot operates on a specific list of subreddits.
It responds to Modmail messages containing any of the keywords defined in a list.
The bot archives the conversation after sending the response.
It records which Modmail conversations it has replied to, to avoid sending multiple responses to the same conversation.
If a Modmail message comes from an admin, the bot will send a private message to every moderator of the subreddit, notifying them of the admin Modmail.

### Requirements

* Python 3

Alternatively, you can use the Dockerfile to build an image and run the script in a container. See the Docker subsectionin the Usage section below for more information.

### Usage

Clone the repository:

    git clone https://github.com/yourusername/auto_respond.git
    cd auto_respond

#### Running Locally
To install the script's module requirements, set up a virtual environment (`python3 -m venv ./venv`), activate it (`source ./venv/bin/activate`), and run the following command:
    ```shell
    pip install -r requirements.txt
    ```

Once the requirements are installed, create an .env file in the script directory. You can use the included env.example file as a base.

Run the script:

    python3 auto_respond.py

#### Docker
Build the image:

    docker build -t auto_respond .

Configuring the script is done with environment variables. You can use the included env.example file as a base. To pass the environment variables, you can pass them in the `docker run` invocation, or you can create an .env file in the script directory and pass it with the `--env-file` flag.  

Run the container:

    # with an env file
    docker run -d --env-file .env --name auto_respond auto_respond
    # without an env file, use a series of -e flags to pass the environment variables. Example below
    docker run -d -e "key=value" --name auto_respond auto_respond

### Configuring the Bot

You can customize the bot's behavior by setting the following environment variables:

* `REDDIT_API_CLIENT_ID` - String: Client ID for the Reddit app you have configured in the Reddit API portal. Required.
* `REDDIT_API_CLIENT_SECRET` - String: Client secret for the Reddit app you have configured in the Reddit API portal. Required.
* `REDDIT_API_REFRESH_TOKEN` - String: Refresh token for the Reddit app you have configured in the Reddit API portal. Required.
* `ALLOWED_SUBREDDITS` - List: Subreddits the bot will operate on. Required.
* `MAIN_RESPONSE_MESSAGE` - String: Message the bot will send in response to a Modmail message. Required.
* `USER_AGENT` - String: User agent to use when interacting with Reddit's API. Optional, default: "modmail_auto_responder_v0.1 by u/buckrowdy"

# Contributing

We appreciate your contributions! Please fork this repository, make your changes, and submit a pull request. If you have any questions or need help, feel free to open an issue.

# Disclaimer

This bot should be used responsibly and in accordance with Reddit's API Terms of Service. The creator of this bot is not responsible for any misuse or damage caused by this bot.

Remember to replace "yourusername" with your actual GitHub username in the "Clone the repository" step, and feel free to customize this README to better suit your project.
