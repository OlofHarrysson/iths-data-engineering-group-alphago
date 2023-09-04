import json
import os
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPT2Model,
    GPT2Tokenizer,
    GPT2TokenizerFast,
    pipeline,
)

from newsfeed import summarize

# use gpu if available (need to add .to(torch_device) after model)
torch_device = "cuda" if torch.cuda.is_available() else "cpu"

# get article
blog = "mit"
path_article_dir = Path(f"data/data_warehouse/{blog}/articles")
file_list = os.listdir(path_article_dir)
file_path = path_article_dir / file_list[0]

with open(file_path, "r") as json_file:
    blog_post = dict(json.load(json_file))
sample_text = blog_post["blog_text"]


# ------------------------------------------------------------
#                  GPT - pipeline modelling
# ------------------------------------------------------------
# decoder only model, summarization using prompt engineernig (zero-shot learning)

# checkpoint_gpt = "distilgpt2"
checkpoint_gpt = "gpt2"

tokenizer_gpt = AutoTokenizer.from_pretrained(checkpoint_gpt)  # this selects GPT2TokenizerFast
# tokenizer = GPT2Tokenizer.from_pretrained(checkpoint)

# max tokens length is 1024
# limit input tokens to allow enough space for generation
tokens_gpt_text = tokenizer.tokenize(sample_text)
tokens_gpt_tldr = tokenizer.tokenize("\n\nTL;DR:\n")
tokens_gpt = tokens_text[:512] + tokens_tldr

# alternatively add "Summarize:\n\n" to the top of gpt_query instead and do:
# tokens_gpt = tokenizer(gpt_query, truncation=True, max_length=512)

# Or maybe I should combine the two for easier prompt customization:
# gpt_query = (
#     "Summarize the following text for a non-technical reader:\n\n"
#     + sample_text + "\n\nSummary:\n"
# )

# convert back to string for pipeline
gpt_query = tokenizer.convert_tokens_to_string(tokens_gpt)
# len(tokenizer(gpt_query)['input_ids'])
# print(gpt_query)

# pipeline uses tokenizer GPT2TokenizerFast and model GPT2LMHeadModel
pipe_gpt = pipeline(
    "text-generation", model=checkpoint_gpt, max_new_tokens=(1024 - len(tokens_gpt))
)
pipe_gpt_out = pipe_gpt(gpt_query)

# check the output
print(pipe_gpt_out[0]["generated_text"])
print(pipe_gpt_out[0]["generated_text"][len(gpt_query) :])


# ------------------------------------------------------------
#                  GPT - manual selection of models
# ------------------------------------------------------------
# more uneven than pipeline for some reason, even though I've chosen the same tokeniser and model

ids_gpt = tokenizer.convert_tokens_to_ids(tokens_gpt)
# model expects batch of inputs, so needs [ids]
encoded_input_gpt = tokenizer_gpt.prepare_for_model([ids_gpt], return_tensors="pt")

# simpler alternative using string input to tokenizer (the tokenizer's __call__ method I think):
# encoded_input_gpt = tokenizer_gpt(gpt_query, return_tensors='pt')

# model_gpt = GPT2Model.from_pretrained(checkpoint_gpt)  # no head and only outputs last_hidden_state
model_gpt = GPT2LMHeadModel.from_pretrained(checkpoint_gpt)
# model_gpt = AutoModelForCausalLM.from_pretrained(checkpoint_gpt)  # equivalent

# what is the output here exactly?
# output_gpt = model_gpt(**encoded_input_gpt)

# very uneven results
# - with low temp always generates "<|endoftext|>" ... why?
# - without high repetition_penalty the output is a single sentence repeated over and over... why?
model_gpt_out = model_gpt.generate(
    **encoded_input_gpt,
    max_new_tokens=(1024 - len(tokens_gpt)),
    do_sample=True,  # samples from the output distribution instead of using argmax (needed for temperature to have an effect)
    temperature=1.5,  # higher value softens output distribution (reducing confidence in predictions, adding more randomness)
    # temperature=0.1,
    repetition_penalty=1.4,  # values over 1.0 decrease likelihood of repeating the same tokens
    early_stopping=False,  # stop when predicing end of sequence?
)
print(tokenizer_gpt.decode(model_gpt_out[0])[len(gpt_query) :])


# ------------------------------------------------------------
#                        T5 - pipeline modelling
# ------------------------------------------------------------
# seq2seq (encoder-decoder model)

# get tokenizer
tokenizer_t5 = AutoTokenizer.from_pretrained("t5-small")

# maximum sequence length for model is 512
# - for some reason I need to remove 3 more tokens than 512.. why?
tokens_t5 = tokenizer_t5.tokenize(sample_text)[: (512 - 3)]
t5_query = tokenizer_t5.convert_tokens_to_string(tokens_t5)

pipe_t5 = pipeline("summarization", model="t5-small", temperature=1.5, do_sample=True)
pipe_t5_out = pipe_t5(t5_query)
print(pipe_t5_out[0]["summary_text"])
