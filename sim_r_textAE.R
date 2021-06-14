# sim_r_textAE.R

# Install and download packages
pacman::p_load(pacman, tm, SnowballC, dplyr, wordcloud, RColorBrewer)

# Import data
# Don't need to specify file path if files are in the same directory or folder as R script. 
# The text files must be without metadata.
# Set the working directory where you saved your files.
# setwd("D:/ddoc/DLEARN/Simulation-KL/PSs/PS6")

# "Sense and Sensibility" by Jane Austen, published 1811
bookAE <- readLines('austen-emma.txt')

###################################################################################
# Corpus for Sense and Sensibility
corpusAE <- Corpus(VectorSource(bookAE)) %>%
  tm_map(removePunctuation) %>%
  tm_map(removeNumbers) %>%
  tm_map(content_transformer(tolower)) %>%
  tm_map(removeWords, stopwords("english")) %>%
  tm_map(stripWhitespace) %>%
  tm_map(stemDocument)

# Create term-document matrices and remove sparse terms
tdmAE <- DocumentTermMatrix(corpusAE) %>%
  removeSparseTerms(1 -(5/length(corpusAE)))

# Calculate and sort by word frequencies
word.freqAE <- sort(colSums(as.matrix(tdmAE)), decreasing = T)


# Create frequency table
tableAE <- data.frame(word = names(word.freqAE),
                      absolute.frequency = word.freqAE,
                      relative.frequency = word.freqAE/length(word.freqAE))

# Remove the words from the row names
row.names(tableAE) <- NULL

#Show the 15 most common words
head(tableAE, 15)

# Show the histogram of the frequency of the most common 6 words
barplot(data.matrix(tableAE[-1]), names= tableAE$word[1:6], height=tableAE$absolute.frequency[1:6],beside=TRUE)

# Export the 1000 most common words in csv file
write.csv(tableAE[1:1000, ], "AE_1000.csv")

################################################################################
set.seed(42)
# Limit words by specifying min frequency
wordcloud(names(word.freqAE),word.freqAE, min.freq=70)

# Add color
wordcloud(names(word.freqAE),word.freqAE,min.freq=100,colors=brewer.pal(8,"Dark2"))

################################################################################

# Clear workspace
rm(list = ls())






