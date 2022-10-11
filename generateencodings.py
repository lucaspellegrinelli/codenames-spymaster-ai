import json
import argparse
from gensim.models import KeyedVectors
from nltk.corpus import stopwords

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True, help="Path to word2vec model")
parser.add_argument("--words", type=str, required=True, help="Path to file that contains the words")
parser.add_argument("--output", type=str, required=True, help="Path to output file")
args = parser.parse_args()

stopwords = stopwords.words("portuguese")

all_words = []
with open(args.words, "r", encoding="utf-8") as words_f:
    for line in words_f:
        if len(line) > 2 and line not in stopwords:
            all_words.append(line.strip())

model = KeyedVectors.load_word2vec_format(args.model, binary=False)

all_reprs = {}
for word in all_words:
    if word in model:
        all_reprs[word] = [float(x) for x in model[word]]

with open(args.output, "w+") as f:
    json.dump(all_reprs, f)