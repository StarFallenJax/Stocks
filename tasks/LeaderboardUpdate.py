import json
import os
from market.Market import *

import discord
from discord.ext import commands, tasks


class LeaderboardUpdate(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.update_leaderboard.start()

    @tasks.loop(minutes=5)
    async def update_leaderboard(self):
        totalDoubloons = 0
        leaderboard = {}
        market = Market()
        for wallet in os.listdir("database/wallets"):
            print(f"[LEADERBOARD] Scanning the wallet of {wallet}")
            currentWallet = open("database/wallets/" + wallet, "r", encoding="utf-8")
            contents = json.loads(currentWallet.read())
            currentWallet.close()
            user = await self.bot.fetch_user(int(contents["walletOwner"]))
            user = user.name + "#" + user.discriminator
            leaderboard[user] = 0
            for stock in contents["portfolio"]:
                price = market.getStock(stock).getCurrentPrice()
                totalDoubloons += price * contents["portfolio"][stock]
                leaderboard[user] += price * contents["portfolio"][stock]
            totalDoubloons += contents["doubloons"]
            if len(contents["portfolio"]) == 0:
                leaderboard[user] = contents["doubloons"]
            else:
                leaderboard[user] += contents["doubloons"]

        leaderboard = dict(
            sorted(leaderboard.items(), key=lambda kv: kv[1], reverse=True)
        )
        leaderboard["totalDoubloons"] = totalDoubloons
        leaderboardFile = open("database/leaderboard.json", "w", encoding="utf-8")
        leaderboardFile.write(json.dumps(leaderboard))
        leaderboardFile.close()

    def getLeaderboardUpdateObject(self):
        return self.update_leaderboard


def setup(bot):
    bot.add_cog(LeaderboardUpdate(bot))
