import argparse
import os
from pathlib import Path

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.prompts import PromptTemplate


def summarize_text(blog_post):
    # loading text as langchain document
    loader = TextLoader(blog_post)
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


def main(blog_post_index, blog_name):
    path_article_dir = Path(f"data/data_warehouse/{blog_name}/articles")
    file_list = os.listdir(path_article_dir)
    summary = summarize_text(path_article_dir / file_list[blog_post_index])
    print(summary)


def parse_args():
    parser = argparse.ArgumentParser()
    # add argument for which blog to summarize from, only accepted arguments are aws and mit
    parser.add_argument("--blog", type=str, help="Name of blog to summarize article from")
    # add argument for index of article in file_list (arbitrary order)
    parser.add_argument("--ix", type=int, help="Index of article in file_list")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_post_index=args.ix, blog_name=args.blog)
