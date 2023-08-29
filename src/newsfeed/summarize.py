import argparse
import os
import tempfile
from pathlib import Path

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


def main():
    path_article_dir = Path("data/data_warehouse/mit/articles")
    path_summary_dir = Path("data/data_warehouse/mit/summerized_articles")
    path_summary_dir.mkdir(parents=True, exist_ok=True)

    already_summerized = set(os.listdir(path_summary_dir))

    file_list = os.listdir(path_article_dir)

    for file_name in file_list:
        summary_filename_check = f"Summary_of_{file_name}"
        print(summary_filename_check)

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

        # Ignore this for now, will remove soon.
        # Wanted to keep this to learn from.
        """  with open(path_article_dir / file_name, "r") as f:
            blog_post = f.read()

        with tempfile.NamedTemporaryFile(delete=False, mode="w+") as temp:
            temp.write(blog_post["blog_text"])
            current_article_path = temp.name

        try:
            summary_text = summarize_text(current_article_path)
            print(f"Generated summary for {file_name}")

            blog_summary = BlogSummary(
                unique_id=f"summary_{file_name}",
                title=f"Summary of {file_name}",
                text=summary_text,
            )
            summary_filename = blog_summary.get_filename()

            with open(path_summary_dir / summary_filename, "w") as f:
                f.write(blog_summary.json())
            already_summerized.add(summary_filename)
        finally:
            print(f"Failed to summerize text, {current_article_path}")
            os.remove(current_article_path)
        """


# summary = summarize_text(path_article_dir / file_list[blog_post_index])
# print(summary)


# def parse_args():
#    parser = argparse.ArgumentParser()
# add argument for index of article in file_list (arbitrary order)
#    parser.add_argument("--ix", type=int)
#   return parser.parse_args()


if __name__ == "__main__":
    # args = parse_args()
    main()
