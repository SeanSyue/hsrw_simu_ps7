import codecs
import re


with codecs.open('./JaneEyre.txt', "r", encoding="utf-8") as f:
    text_JE = f.read()

result = re.sub(r"\d+", "", text_JE)

with codecs.open('./JaneEyre-num_removed.txt', "w", encoding="utf-8") as f:
    f.write(result)
