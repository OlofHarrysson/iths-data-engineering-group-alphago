import os
from pathlib import Path

from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader

path_article_dir = Path("data/data_warehouse/mit/articles")
file_list = os.listdir(path_article_dir)

# test check article
with open(path_article_dir / file_list[0], "r") as article:
    print(article.read())

# loading as langchain document
loader = TextLoader(path_article_dir / file_list[0])
blog_post = loader.load()

# fix api key
# echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.bash_profile

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
chain = load_summarize_chain(llm, chain_type="stuff")

# summarize a blog post
chain.run(blog_post)


def summarize_text(blog_text):
    summary = ...  # Your code goes here

    return summary
