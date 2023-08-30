import argparse
import os
import tempfile
from pathlib import Path

from download_blogs_from_rss import LINK_TO_XML_FILE
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate

from newsfeed.datatypes import BlogInfo, BlogSummary


def summarize_text(blog_post_path):
    # loading text as langchain document
    loader = TextLoader(blog_post_path)
    blog_post = loader.load()

    # define prompt
    prompt_template = """Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # define what LLM to use
    # using OpenAI chat LLM API requires env variable OPEN_AI_KEY to be set with API key
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # create a "chain" object for running queries against a specified LLM, with customizable prompt
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # send document to the llm_chain
    # StuffDocumentsChain "stuffs" list of documents + prompt into single call
    # MapReduceChain splits it into several combines and then combines output
    # document_variable_name can be used to customize where in the prompt the documents are inserted?
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    summary = stuff_chain.run(blog_post)

    return summary



# main takes the argument --source aws, or --source mit
def main():
    args = parse_args()
    source = args.source
    path_article_dir = Path(f"data/data_warehouse/{source}/articles")
    path_summary_dir = Path(f"data/data_warehouse/{source}/summerized_articles")
    path_summary_dir.mkdir(parents=True, exist_ok=True)

    already_summerized = set(os.listdir(path_summary_dir))

    file_list = os.listdir(path_article_dir)

    for file_name in file_list:
        summary_filename_check = f"Summary_of_{file_name}"

        if summary_filename_check in already_summerized:
            print(f"Skipping already summerized article: {file_name}")
            continue
        # file path for the article that's being summerized/looked at
        current_article_path = path_article_dir / file_name
        summary_text = summarize_text(current_article_path)
        print(f"Generated summary for {file_name}")


        blog_summary = BlogSummary(
            unique_id=f"summary_{file_name}",
            title=f"Summary of {Path(file_name).stem}",
            text=summary_text,
        )
        # gets the name of the article
        summary_filename = blog_summary.get_filename()

        with open(path_summary_dir / summary_filename, "w") as f:
            f.write(blog_summary.json())
        already_summerized.add(summary_filename)

blog_names = list(LINK_TO_XML_FILE)
# run python summarize.py --source mit OR aws
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=str,
        choices=blog_names,
        default="mit",
        help=f"Blog source to summarize, allowed arguments are: {blog_names}.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()

