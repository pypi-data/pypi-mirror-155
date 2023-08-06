# dis-uniter
This creates a simple website to go with your discord.py bot on https://replit.com so it can be kept alive. If your bot does not have intents that reveal private data (message content, presences, members), it also includes a logger.
## Usage
With a secret environment variable `DISCORD_TOKEN` which contains your token:
```
from disuniter import keepAlive
from discord.ext import commands
bot = commands.Bot()
keepAlive(bot)
```
Yep, that's right, this package forces you to store your token in a secret `DISCORD_TOKEN` to ensure you aren't exposing your token.
## Why is it called dis-uniter?
I am keeping Discord bots alive. Discord = disagreement. I am dis-uniting by keeping disagreements alive.