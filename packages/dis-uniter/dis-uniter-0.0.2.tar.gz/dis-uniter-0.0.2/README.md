# dis-uniter
This creates a simple website to go with your discord.py bot on https://replit.com so it can be kept alive. If your bot does not have intents that reveal private data (message content, presences, members), it also includes a logger.
## Usage 
```
from disuniter import keepAlive
from discord.ext import commands
bot = commands.Bot()
keepAlive(bot)
bot.run()
```
## Why is it called dis-uniter?
I am keeping Discord bots alive. Discord = disagreement. I am dis-uniting by keeping disagreements alive.