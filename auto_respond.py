import praw
import time
import environs

env = environs.Env()
if env.bool("READ_DOTENV", default=True):
    # Read .env 
    env.read_env(False)


# Create a Reddit instance
reddit = praw.Reddit(
	client_id = env.str("REDDIT_API_CLIENT_ID"),
	client_secret = env.str("REDDIT_API_CLIENT_SECRET"),
	user_agent=env.str("USER_AGENT", Default="modmail_auto_responder_v0.1 by u/buckrowdy"),
	refresh_token = env.str("REDDIT_API_REFRESH_TOKEN"),
)

# Define the list you want this to operate on.  A modmail conversation stream fetches ALL subreddits
if(env.list("ALLOWED_SUBREDDITS", Default=list()) == []):
    print("No subreddits defined in ALLOWED_SUBREDDITS. Please define this variable in your environment or .env file.")
    exit(1)
allowed_subreddits = env.list("ALLOWED_SUBREDDITS", Default=list())

# Define the list of keywords for the auto-respond trigger
keywords = ['request to join','let me in', 'access', 'member', 'private', 'blackout', 'dark', 'closed', 'join', 'shutdown,']

# Define the auto-response
if env.str("MAIN_RESPONSE_MESSAGE", default="") == "":
    print("No response message defined in MAIN_RESPONSE_MESSAGE. Please define this variable in your environment or .env file.")
    exit(1)
main_response_message = env.str("MAIN_RESPONSE_MESSAGE")

# Read the list of processed modmails from a file so we don't reply to the same one twice.
try:
    with open('processed_modmails.txt', 'r') as f:
        processed_mail = f.read().splitlines()
except FileNotFoundError:
    processed_mail = []
    # Create the file if it doesn't exist
    with open('processed_modmails.txt', 'w') as f:
        f.write('')
        f.close()

# Begin the mnain function of the bot.  The bot will need to be interrupted manually
while True:
    try:
        # Print something to the terminal so you know it's working.
        print(f"Logged in as {reddit.user.me()}...")
        print("Fetching modmail conversations...")
        for conv in reddit.subreddit('all').mod.stream.modmail_conversations(skip_existing=True):
            # Check if the conversation owner is in the list of allowed subreddits
            if conv.owner not in allowed_subreddits:
                continue  # If not, skip the rest of this loop and move to the next conversation
        
            # This specific condition will send a PM top every mod on the team if an admin modmail is sent so you don't miss it.
            if len([author for author in conv.authors if author.is_admin]) > 0:
                # Utilize u/mod_mailer, a mail relay bot.
                reddit.redditor("mod_mailer").message(subject=f"{conv.owner}", message =f"New Admin modmail in r/{conv.owner}\n\n---\n\nNew modmail message from admins https://mod.reddit.com/mail/all/{conv.id}\n\nSubject: {conv.subject}")
                conv.archive()

            # Check if we've already processed this modmail.
            if conv.id not in processed_mail:
                # Grab the subject of the first message in the conversation.
                modmail_subject = conv.subject.lower()

                # Check if the conversation only has the original message so the bot doesn't reply to messages further in the chain.
                if len(conv.messages) != 1:
                    continue

                # Get the body of theoriginal message
                original_message = conv.messages[0].body_markdown.lower()

                # Check for keywords in the message subject or body.
                if any(keyword in original_message for keyword in keywords) or any(keyword in modmail_subject for keyword in keywords):
                    print(f"Found modmail in r/{conv.owner}  > {keyword} < in message from user {conv.user.name}")
                    # Reply and archive the message with the preset response, hide the username of the sender.
                    conv.reply(body=main_response_message, author_hidden=True)
                    conv.archive()
                    # Add the id of the conversation to a list so it won't be checked again.
                    processed_mail.append(conv.id)
                    # Append the id of the conversation to a file so it won't be checked again.
                    with open('processed_modmails.txt', 'a') as f:
                        f.write(f"{conv.id}\n")
                    print(f"Replied to message ID {conv.id} from user {conv.user.name} with the preset response\n")
                
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Sleeping for 60 seconds before retrying...")
        time.sleep(60)
