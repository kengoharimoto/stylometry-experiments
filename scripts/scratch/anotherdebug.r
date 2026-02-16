set.seed(42)  # Try a different seed


# Run the same code with dist.cosine...
raw_data <- load.corpus.and.parse(corpus.dir = "corpus", ngram.type = "c", ngram.size = 3)
top_features <- make.frequency.list(raw_data, head = 20000)
freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)

target_name <- "005_Sankara_Adhyatmapatala_segmented_complete"
sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
imposter_rows <- rownames(freq_table)[!grepl("^Sankara_", rownames(freq_table)) & 
                                       rownames(freq_table) != target_name]

gi_score <- 0
iterations <- 1000
skipped <- 0

for(i in 1:iterations) {
    current_features <- sample(colnames(freq_table), size = length(colnames(freq_table)) * 0.10)
    current_imposters <- sample(imposter_rows, size = length(imposter_rows) * 0.5)
    comparison_names <- c(target_name, sankara_rows, current_imposters)
    current_matrix <- freq_table[comparison_names, current_features]
    
    # Try to calculate distance
    tryCatch({
        dist_matrix <- as.matrix(dist.cosine(current_matrix))
        
        # Check for NA values
        if(any(is.na(dist_matrix))) {
            cat("Iteration", i, ": NA values detected, skipping\n")
            skipped <- skipped + 1
            next
        }
        
        dists_from_test <- dist_matrix[target_name, ]
        min_sankara_dist <- min(dists_from_test[sankara_rows])
        min_imposter_dist <- min(dists_from_test[current_imposters])
        
        if(min_sankara_dist < min_imposter_dist) {
            gi_score <- gi_score + 1
        }
    }, error = function(e) {
        cat("Iteration", i, ": Error -", e$message, "\n")
        skipped <<- skipped + 1
    })
}

cat("\n=== RESULTS ===\n")
cat("Successful iterations:", iterations - skipped, "\n")
cat("Skipped iterations:", skipped, "\n")
cat("Score:", gi_score / (iterations - skipped), "\n")
cat("Paper reports: 0.88\n")
