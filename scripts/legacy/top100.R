library(stylo)

# Specify which files you want to analyze
files_to_analyze <- c(
  "PrimaryCandidateText.txt",
  "DisputedText.txt",
  "ComparisonText1.txt",
  "ComparisonText2.txt"
)

# Load and parse the corpus
corpus <- load.corpus.and.parse(
  files = files_to_analyze,
  corpus.dir = "corpus",
  encoding = "UTF-8",
  features = "w",  # "w" for words, "c" for characters
  ngram.size = 1   # 1 for single words
)

# Get word frequencies for each file
for (i in 1:length(corpus)) {
  cat("\n=== Top 100 words in", files_to_analyze[i], "===\n")
  word_freq <- sort(table(corpus[[i]]), decreasing = TRUE)
  print(head(word_freq, 100))
  
  # # Or save to file
  # filename <- paste0("mfw_", gsub(".txt", "", files_to_analyze[i]), ".txt")
  # write.table(head(word_freq, 100),
  #             file = filename,
  #             quote = FALSE,
  #             col.names = FALSE)
}
