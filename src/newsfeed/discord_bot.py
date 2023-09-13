import argparse
import asyncio
import json
import os
from pathlib import Path

import aiohttp
import discord
from discord import Webhook

from newsfeed import summarize
from newsfeed.download_blogs_from_rss import LINK_TO_XML_FILE


async def send_webhook(url, desc):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(description=desc)
        await webhook.send(embed=embed, username="SummaryBot")


def send_to_webhook(info, summary, sum_type):
    desc = f"""**Group Name**: alphago

    **Blog Title**: {info['title']}

    **Summary**:
    {summary}

    **Additional information**: {info["link"]}
    """

    url_dict = {
        "tech": "https://discord.com/api/webhooks/1143948372546428928/3GiXGLSs3DfqjeMAXvBNPrx_Ywe8XEZR_diBqEuxNp_vMEHNW1_MaI5EphupAE0L04lr",
        "ntech": "https://discord.com/api/webhooks/1148897197706981419/V5u8mBP0gFzeTjfWLMPdkqwATaip_3FewbYEII93tYA_yTW6MAj05t-Q9qqHHvPWuwHL",
        "swe": "https://discord.com/api/webhooks/1148897850126782565/B1Wqpcw8vXWP5oppsorb9aoqStDgOibuNfssKRB7sjyg5QzLjmI72xI10KqNCmsW_u8J",
    }

    url = url_dict[sum_type]

    loop = asyncio.new_event_loop()
    loop.run_until_complete(send_webhook(url, desc))
    loop.close()


def main(source, articles=None, local_model=None, sum_type="tech"):
    if not source:
        print("Please use --source argument to specify the blog you want articles from")
        return

    path_article_dir = Path(f"data/data_warehouse/{source}/articles")
    file_list = os.listdir(path_article_dir)

    if articles == None:
        print(f"Please use --articles argument to specify a list of articles from {source}:\n")
        for i, j in enumerate(file_list):
            print(i, j)
        return

    path_summary_dir = Path(f"data/data_warehouse/{source}/summarized_articles")

    if local_model:
        path_summary_dir = path_summary_dir / local_model
    else:
        path_summary_dir = path_summary_dir / sum_type

    for article in articles:
        path_summary_file = path_summary_dir / f"Summary_of_{article}"

        if path_summary_file.exists():
            with open(path_summary_file, "r") as json_file:
                summary = json.load(json_file)["text"]
        else:
            summary = summarize.summarize_text(
                path_article_dir / article, local_model=local_model, sum_type=sum_type
            )

        with open(path_article_dir / article, "r") as json_file:
            article_info = json.load(json_file)

        send_to_webhook(article_info, summary, sum_type)


blog_names = ["mit", "aws", "openai"]

# make parse_args util function?


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--articles",
        type=list,
        help=f"Run without --articles argument to see list of articles",
    )
    parser.add_argument(
        "--source",
        type=str,
        choices=blog_names,
        default="mit",
        help=f"Blog source to summarize, allowed arguments are: {blog_names}.",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=["t5", "gpt2"],
        # default="",
        help=f"Use local model for summarization",
    )
    parser.add_argument(
        "--stype",
        type=str,
        choices=["tech", "ntech", "swe"],
        default="tech",
        help=f"What type of summarization do you want (techincal 'tech', non-technical 'ntech', or swedish 'swe')",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(source=args.source, articles=args.articles, local_model=args.model, sum_type=args.stype)
