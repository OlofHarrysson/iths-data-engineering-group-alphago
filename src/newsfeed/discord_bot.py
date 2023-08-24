import asyncio

import aiohttp
import discord
from discord import Webhook


async def anything(url, desc):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(description=desc)
        await webhook.send(embed=embed, username="SummaryBot")


if __name__ == "__main__":
    url = "https://discord.com/api/webhooks/1143948372546428928/3GiXGLSs3DfqjeMAXvBNPrx_Ywe8XEZR_diBqEuxNp_vMEHNW1_MaI5EphupAE0L04lr"
    desc = """**Group Name**: iths-data-engineering-group-alphago
    **Blog Title**: Test Blog title
    **Summary**:
    This is a summary
    **Additional information**: link
    """

    loop = asyncio.new_event_loop()
    loop.run_until_complete(anything(url, desc))
    loop.close()
