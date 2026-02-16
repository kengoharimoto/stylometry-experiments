library(stylo)

# Run the analysis using Character 3-grams
results <- stylo(gui = FALSE,
                 corpus.dir = "corpus",
                 ngram.type = "c",   # "c" = characters
                 ngram.size = 3)     # 3 = 3-grams
# Let's view the distance between the texts
# Save the distance table to a file named "distances.csv"
write.csv(results$distance.table, "distances.csv")
