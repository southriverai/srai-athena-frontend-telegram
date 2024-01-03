# srai-telegram-frontend
Telegram frontend for srai services

## deploy dev
srai-deploy deployment_dev.json
## deploy pro



## github
import os

username = os.environ.get("GITHUB_USERNAME")
token = os.environ.get("GITHUB_TOKEN")
command = f"git clone https://{username}:{token}@github.com/southriverai/srai-telegram-frontend.git"
print(command)
# git@github.com:southriverai/srai-telegram-frontend.git
