import argparse
import asyncio
import json
import os
from pathlib import Path

import aiohttp
import discord
from discord import Webhook

from newsfeed import summarize


async def anything(url, desc):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(description=desc)
        await webhook.send(embed=embed, username="SummaryBot")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ix", type=int)
    return parser.parse_args()


if __name__ == "__main__":
    # url = "https://discord.com/api/webhooks/1143948372546428928/3GiXGLSs3DfqjeMAXvBNPrx_Ywe8XEZR_diBqEuxNp_vMEHNW1_MaI5EphupAE0L04lr"
    url = "https://discord.com/api/webhooks/1131522847509069874/Lwk1yVc4w623xpRPkKYu9faFdMNvV5HTZ3TCcL5DgsIgeqhEvo9tBookvuh2S4IWysTt"
    path_article_dir = Path("data/data_warehouse/mit/articles")
    file_list = os.listdir(path_article_dir)
    ix = parse_args().ix
    file_path = path_article_dir / file_list[ix]

    with open(file_path, "r") as json_file:
        blog_post = json.load(json_file)

    summary = summarize.summarize_text(file_path)

    desc = f"""**Group Name**: alphago

    **Blog Title**: {blog_post['title']}

    **Summary**:
    {summary}

    **Additional information**: {blog_post["link"]}
    """

    loop = asyncio.new_event_loop()
    loop.run_until_complete(anything(url, desc))
    loop.close()
