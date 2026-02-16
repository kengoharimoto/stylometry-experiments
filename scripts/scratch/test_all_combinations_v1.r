#!/usr/bin/env Rscript
# Comprehensive GI Authorship Verification Test
# Tests all combinations of n-gram types and distance metrics

library(stylo)

# Set seed for reproducibility
set.seed(123)

# Configuration
CORPUS_DIR <- "corpus"
TARGET_NAME <- "bsbh_unsandhied"
ITERATIONS <- 100
FEATURE_COUNT <- 20000
FEATURE_SAMPLE_RATE <- 0.10
IMPOSTER_SAMPLE_RATE <- 0.50

# Function to run a single GI test
run_gi_test <- function(ngram_type, ngram_size, distance_func, setup_name) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("================================================\n")
    
    # Load and process corpus
    cat("Loading corpus...\n")
    raw_data <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, 
                                      ngram.type = ngram_type, 
                                      ngram.size = ngram_size)
    
    cat("Making frequency list...\n")
    top_features <- make.frequency.list(raw_data, head = FEATURE_COUNT)
    
    cat("Creating frequency table...\n")
    freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)
    
    # Define test sets
    sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
    imposter_rows <- rownames(freq_table)[!grepl("^Sankara_", rownames(freq_table)) & 
                                           rownames(freq_table) != TARGET_NAME]
    
    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", TARGET_NAME, "\n")
    cat("  Sankara candidates:", length(sankara_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")
    
    # Safety checks
    if(length(sankara_rows) == 0) stop("No Sankara files found.")
    if(length(imposter_rows) == 0) stop("No Imposter files found.")
    if(!(TARGET_NAME %in% rownames(freq_table))) stop("Target text not found in corpus!")
    if(TARGET_NAME %in% sankara_rows) stop("Target text is in Sankara candidate set!")
    
    # Run GI iterations
    gi_score <- 0
    skipped <- 0
    
    cat("Running", ITERATIONS, "iterations...\n")
    
    for(i in 1:ITERATIONS) {
        if(i %% 20 == 0) {
            cat("  Progress:", i, "/", ITERATIONS, "\n")
        }
        
        # Sample features and imposters
        current_features <- sample(colnames(freq_table), 
                                   size = floor(length(colnames(freq_table)) * FEATURE_SAMPLE_RATE))
        current_imposters <- sample(imposter_rows, 
                                    size = floor(length(imposter_rows) * IMPOSTER_SAMPLE_RATE))
        
        # Build comparison matrix
        comparison_names <- c(TARGET_NAME, sankara_rows, current_imposters)
        current_matrix <- freq_table[comparison_names, current_features]
        
        # Calculate distances with error handling
        tryCatch({
            dist_matrix <- as.matrix(distance_func(current_matrix))
            
            # Check for NA or Inf values
            if(any(is.na(dist_matrix)) || any(is.infinite(dist_matrix))) {
                skipped <- skipped + 1
                next
            }
            
            # Get distances from test text
            dists_from_test <- dist_matrix[TARGET_NAME, ]
            
            # Find minimum distances
            min_sankara_dist <- min(dists_from_test[sankara_rows], na.rm = TRUE)
            min_imposter_dist <- min(dists_from_test[current_imposters], na.rm = TRUE)
            
            # Print diagnostics for first iteration
            if(i == 1) {
                cat("\n  First iteration diagnostics:\n")
                cat("    Matrix dimensions:", nrow(current_matrix), "x", ncol(current_matrix), "\n")
                cat("    Matrix min:", min(current_matrix), "\n")
                cat("    Matrix max:", max(current_matrix), "\n")
                cat("    Distance matrix max:", max(dist_matrix), "\n")
                cat("    Min Sankara distance:", min_sankara_dist, "\n")
                cat("    Min Imposter distance:", min_imposter_dist, "\n\n")
            }
            
            # Score
            if(!is.na(min_sankara_dist) && !is.na(min_imposter_dist)) {
                if(min_sankara_dist < min_imposter_dist) {
                    gi_score <- gi_score + 1
                }
            } else {
                skipped <- skipped + 1
            }
            
        }, error = function(e) {
            if(i == 1) {
                cat("  Error in iteration", i, ":", e$message, "\n")
            }
            skipped <<- skipped + 1
        })
    }
    
    # Calculate final probability
    successful_iterations <- ITERATIONS - skipped
    final_probability <- if(successful_iterations > 0) {
        gi_score / successful_iterations
    } else {
        NA
    }
    
    # Print results
    cat("\n--- RESULTS ---\n")
    cat("Successful iterations:", successful_iterations, "\n")
    cat("Skipped iterations:", skipped, "\n")
    cat("GI Score:", gi_score, "\n")
    cat("Final Probability:", final_probability, "\n")
    cat("Interpretation:\n")
    cat("  >= 0.66 = Authentic (likely by Sankara)\n")
    cat("  <= 0.34 = Not authentic\n")
    cat("  0.34-0.66 = Uncertain (grey zone)\n")
    
    return(list(
        setup = setup_name,
        score = final_probability,
        successful = successful_iterations,
        skipped = skipped,
        total = ITERATIONS
    ))
}

# ================================================
# MAIN EXECUTION
# ================================================

cat("\n")
cat("========================================\n")
cat("GI AUTHORSHIP VERIFICATION TEST SUITE\n")
cat("========================================\n")
cat("Target text:", TARGET_NAME, "\n")
cat("Iterations per test:", ITERATIONS, "\n")
cat("Feature count:", FEATURE_COUNT, "\n")
cat("Feature sample rate:", FEATURE_SAMPLE_RATE * 100, "%\n")
cat("Imposter sample rate:", IMPOSTER_SAMPLE_RATE * 100, "%\n")
cat("\n")

# Store results
all_results <- list()

# Test 1: Trigrams + MinMax
all_results[[1]] <- run_gi_test("c", 3, dist.minmax, "Trigrams + MinMax")

# Test 2: Trigrams + Cosine
all_results[[2]] <- run_gi_test("c", 3, dist.cosine, "Trigrams + Cosine")

# Test 3: Trigrams + Wurzburg (Cosine Delta)
all_results[[3]] <- run_gi_test("c", 3, dist.wurzburg, "Trigrams + Wurzburg (Cosine Delta)")

# Test 4: Unigrams + MinMax
all_results[[4]] <- run_gi_test("w", 1, dist.minmax, "Unigrams + MinMax")

# Test 5: Unigrams + Cosine
all_results[[5]] <- run_gi_test("w", 1, dist.cosine, "Unigrams + Cosine")

# Test 6: Unigrams + Wurzburg (Cosine Delta)
all_results[[6]] <- run_gi_test("w", 1, dist.wurzburg, "Unigrams + Wurzburg (Cosine Delta)")

# ================================================
# SUMMARY TABLE
# ================================================

cat("\n\n")
cat("========================================\n")
cat("SUMMARY OF ALL RESULTS\n")
cat("========================================\n\n")

# Create summary table
summary_df <- data.frame(
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) sprintf("%.3f", x$score)),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    stringsAsFactors = FALSE
)

print(summary_df, row.names = FALSE)

cat("\n")
cat("Paper's reported scores:\n")
cat("  Trigrams + Cosine Delta: 0.xx\n")
cat("  Unigrams + Cosine Delta: 0.xx\n")
cat("\n")

# Interpretation
cat("INTERPRETATION:\n")
cat("  >= 0.66 = Text authenticated as Sankara's work\n")
cat("  <= 0.34 = Text NOT authenticated\n")
cat("  0.34-0.66 = Grey zone (uncertain)\n")
cat("\n")

# Determine overall verdict
authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score >= 0.66))
not_authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score <= 0.34))
uncertain_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score > 0.34 && x$score < 0.66))

cat("OVERALL VERDICT:\n")
cat("Target text:", TARGET_NAME, "\n")
cat("  Authenticated:", authenticated_count, "/ 6 tests\n")
cat("  Not authenticated:", not_authenticated_count, "/ 6 tests\n")
cat("  Uncertain:", uncertain_count, "/ 6 tests\n")
cat("\n")

if(authenticated_count >= 4) {
    cat("CONCLUSION: Strong evidence for Sankara authorship\n")
} else if(authenticated_count >= 2) {
    cat("CONCLUSION: Moderate evidence for Sankara authorship\n")
} else if(not_authenticated_count >= 4) {
    cat("CONCLUSION: Strong evidence AGAINST Sankara authorship\n")
} else {
    cat("CONCLUSION: Inconclusive results\n")
}

cat("\n========================================\n")
cat("Test completed!\n")
cat("========================================\n")