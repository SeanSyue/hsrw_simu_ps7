import codecs
import re
import collections

import numpy as np
import pandas as pd

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.corpus import state_union

nltk.download('stopwords')
nltk.download('state_union')


def get_text_counter(text):
    """ token counter function """
    tokens = WordPunctTokenizer().tokenize(PorterStemmer().stem(text))
    tokens = list(map(lambda x: x.lower(), tokens))
    
    word_pattern = re.compile("^\w+$")
    esw = stopwords.words('english')
    esw.append("would")
    
    tokens = [token for token in tokens if re.match(word_pattern, token) and token not in esw]
    return collections.Counter(tokens), len(tokens)

def make_df(counter, size):
    """ calculate the absolute frequency of the most commen words """
    abs_freq = np.array([el[1] for el in counter])
    rel_freq = abs_freq / size
    index = [el[0] for el in counter]
    df = pd.DataFrame(data=np.array([abs_freq, rel_freq]).T, index=index, columns=["Absolute frequency", "Relative frequency"])
    df.index.name = "Most common words"
    return df


with codecs.open('./1945-Truman.txt', "r", encoding="utf-8") as f:
    text_TM = f.read()
with codecs.open('./2002-GWBush.txt', "r", encoding="utf-8") as f:
    text_GB = f.read()


# Calculate the most common words of 1945-Truman and display the 15 most common.
tm_counter, tm_size = get_text_counter(text_TM)
tm_df = make_df(tm_counter.most_common(1000), tm_size)

# Save the 1000 most common words of 1945-Truman to .csv
tm_df.to_csv("TM2_1000.csv")


# Calculate the most common words of 2002-GWBush
gb_counter, gb_size = get_text_counter(text_GB)
gb_df = make_df(gb_counter.most_common(1000), gb_size)

# Save the 1000 most common words of 2002-GWBush to .csv
gb_df.to_csv("GB2_1000.csv")

######
# Compare texts
#####

# Find the most common words acrotm the two documents.
all_counter = gb_counter + tm_counter
all_df = make_df(gb_counter.most_common(1000), 1)
most_common_words = all_df.index.values

# Create a data frame with the differences in word frequency
df_data = []
for word in most_common_words:
    tm_c = tm_counter.get(word, 0) / tm_size
    gb_c = gb_counter.get(word, 0) / gb_size
    d = abs(tm_c - gb_c)
    df_data.append([tm_c, gb_c, d])

diff_df = pd.DataFrame(data=df_data, index=most_common_words,
                          columns=["TM relative frequency", "GB relative frequency", "Differences in relative frequency"])
diff_df.index.name = "Most common words"
diff_df.sort_values("Differences in relative frequency", ascending=False, inplace=True)

# Save the full list of distinctive words to a file
diff_df.to_csv("dist_TMGB.csv")

# Count the usage of the words "man", "women" or "people" in every annual US presidential addresses
cfd = nltk.ConditionalFreqDist((target, fileid[:4]) for fileid in state_union.fileids() for w in state_union.words (fileid) for target in [ 'men' , 'women','people' ] if w.lower().startswith(target))
print(cfd['men'].items())
# Plot the trend of the usage of the words "man", "women" or "people" in different years
cfd.plot()