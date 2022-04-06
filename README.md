# The Godis Fan Club Stock Market
### Requirements:
* Python 2.9.2+
* An editor, preferably [Visual Studio Code](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/download/#section=windows) (*but  it does not really matter*)

#### Install dependencies
`pip install -r requirements.txt`

#### [Create a discord bot](https://discord.com/developers/applications "Create a discord bot")
The actual bot has the following scopes:
* bot
* application.commands
And the following permissions:
* Manage Roles
* Read Messages/View Channels
* Send Messages
* Embed Links
* Attach Files
* Use External Emojis
* Use External Stickers (not used)
* Add Reactions
* Use Slash Commands

The bot also has all the Privileged Gateway Intents, however most are not used.


**The following fields from the bot will need to be replaced:**

**TGFCSM.py** / line 31 *(with your own bot token)*

**embeds.py** / line 7 *(with your own emoji)*

### Formatting
The Godis Fan Club (very serious organization lol) uses [Black](https://github.com/psf/black "Black") to format the code.

### Database
The data-storing system is pretty stupid, stupid and stupid again. As this project has literally no budget, we have no other database systems
