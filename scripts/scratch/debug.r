library(stylo)
set.seed(123)

# Function to test one setup
test_setup <- function(ngram_type, ngram_size, distance_func, setup_name) {
    cat("\n=== TESTING:", setup_name, "===\n")
    
    raw_data <- load.corpus.and.parse(corpus.dir = "corpus", 
                                      ngram.type = ngram_type, 
                                      ngram.size = ngram_size)
    top_features <- make.frequency.list(raw_data, head = 20000)
    # freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)
    freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features, culling = 50)  # Only features in 50%+ of texts
    target_name <- "005_Sankara_Adhyatmapatala_segmented_complete"
    sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
    imposter_rows <- rownames(freq_table)[!grepl("^Sankara_", rownames(freq_table)) & 
                                           rownames(freq_table) != target_name]
    
    gi_score <- 0
    iterations <- 100  # Use 100 like the paper for comparison
    
    for(i in 1:iterations) {
        current_features <- sample(colnames(freq_table), size = length(colnames(freq_table)) * 0.10)
        current_imposters <- sample(imposter_rows, size = length(imposter_rows) * 0.5)
        comparison_names <- c(target_name, sankara_rows, current_imposters)
        current_matrix <- freq_table[comparison_names, current_features]
		# After creating current_matrix, before calculating distance
		if(i == 1) {
		    cat("\n=== MATRIX DIAGNOSTICS ===\n")
		    cat("Matrix dimensions:", nrow(current_matrix), "x", ncol(current_matrix), "\n")
		    cat("Matrix min value:", min(current_matrix), "\n")
		    cat("Matrix max value:", max(current_matrix), "\n")
		    cat("Any NA values?:", any(is.na(current_matrix)), "\n")
		    cat("Any Inf values?:", any(is.infinite(current_matrix)), "\n")
		}
        dist_matrix <- as.matrix(distance_func(current_matrix))
        dists_from_test <- dist_matrix[target_name, ]
        
        min_sankara_dist <- min(dists_from_test[sankara_rows])
        min_imposter_dist <- min(dists_from_test[current_imposters])
        
        if(min_sankara_dist < min_imposter_dist) {
            gi_score <- gi_score + 1
        }
    }
    
    final_probability <- gi_score / iterations
    cat("RESULT:", final_probability, "\n")
    return(final_probability)
}

# Test all 4 setups from the paper
results <- list()
results$trigram_minmax <- test_setup("c", 3, dist.minmax, "Trigrams + MinMax")
results$trigram_cosine <- test_setup("c", 3, dist.wurzburg, "Trigrams + Cosine Delta")
results$unigram_minmax <- test_setup("w", 1, dist.minmax, "Unigrams + MinMax")
results$unigram_cosine <- test_setup("w", 1, dist.wurzburg, "Unigrams + Cosine Delta")

# Summary
cat("\n=== SUMMARY ===\n")
cat("Trigrams + MinMax:      ", results$trigram_minmax, "\n")
cat("Trigrams + Cosine Delta:", results$trigram_cosine, "(paper reports: 0.88)\n")
cat("Unigrams + MinMax:      ", results$unigram_minmax, "\n")
cat("Unigrams + Cosine Delta:", results$unigram_cosine, "(paper reports: 0.84)\n")
