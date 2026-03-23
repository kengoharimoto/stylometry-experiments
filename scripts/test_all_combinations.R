#!/usr/bin/env Rscript
# Comprehensive GI Authorship Verification Test
# Tests all combinations of n-gram types and distance metrics

library(stylo)

# Set seed for reproducibility
set.seed(123)

# Configuration
CORPUS_DIR <- "corpus/main"
# Adjust these placeholders to match your corpus naming.
CANDIDATE_PATTERN <- "^Candidate_"
TARGET_NAME <- "Target_Text_Name"
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
    candidate_rows <- grep(CANDIDATE_PATTERN, rownames(freq_table), value = TRUE)
    imposter_rows <- rownames(freq_table)[!grepl(CANDIDATE_PATTERN, rownames(freq_table)) & 
                                           rownames(freq_table) != TARGET_NAME]
    
    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", TARGET_NAME, "\n")
    cat("  Primary candidates:", length(candidate_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")
    
    # Safety checks
    if(length(candidate_rows) == 0) stop("No primary candidate files found.")
    if(length(imposter_rows) == 0) stop("No Imposter files found.")
    if(!(TARGET_NAME %in% rownames(freq_table))) stop("Target text not found in corpus!")
    if(TARGET_NAME %in% candidate_rows) stop("Target text is in the primary candidate set!")
    
    # Run GI iterations
    gi_score <- 0
    skipped <- 0
    
    # Store iteration details for analysis
    iteration_log <- data.frame(
        iteration = integer(),
        winner = character(),
        candidate_dist = numeric(),
        imposter_dist = numeric(),
        closest_candidate = character(),
        closest_imposter = character(),
        stringsAsFactors = FALSE
    )
    
    cat("Running", ITERATIONS, "iterations...\n")
    cat("(Showing details for first 10 and last 10 iterations)\n\n")
    
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
        comparison_names <- c(TARGET_NAME, candidate_rows, current_imposters)
        current_matrix <- freq_table[comparison_names, current_features]
        
        # Calculate distances with error handling
        tryCatch({
            dist_matrix <- as.matrix(distance_func(current_matrix))
            
            # Check for NA or Inf values
            if(any(is.na(dist_matrix)) || any(is.infinite(dist_matrix))) {
                skipped <- skipped + 1
                if(i <= 10 || i > ITERATIONS - 10) {
                    cat("  Iteration", i, ": SKIPPED (NA/Inf values)\n")
                }
                next
            }
            
            # Get distances from test text
            dists_from_test <- dist_matrix[TARGET_NAME, ]
            
            # Find minimum distances and which texts they came from
            candidate_dists <- dists_from_test[candidate_rows]
            imposter_dists <- dists_from_test[current_imposters]
            
            min_candidate_dist <- min(candidate_dists, na.rm = TRUE)
            min_imposter_dist <- min(imposter_dists, na.rm = TRUE)
            
            closest_candidate <- names(which.min(candidate_dists))
            closest_imposter <- names(which.min(imposter_dists))
            
            # Print diagnostics for first iteration
            if(i == 1) {
                cat("\n  First iteration diagnostics:\n")
                cat("    Matrix dimensions:", nrow(current_matrix), "x", ncol(current_matrix), "\n")
                cat("    Matrix min:", min(current_matrix), "\n")
                cat("    Matrix max:", max(current_matrix), "\n")
                cat("    Distance matrix max:", max(dist_matrix), "\n\n")
            }
            
            # Determine winner and score
            if(!is.na(min_candidate_dist) && !is.na(min_imposter_dist)) {
                winner <- if(min_candidate_dist < min_imposter_dist) "CANDIDATE" else "IMPOSTER"
                
                # Log the iteration
                iteration_log <- rbind(iteration_log, data.frame(
                    iteration = i,
                    winner = winner,
                    candidate_dist = min_candidate_dist,
                    imposter_dist = min_imposter_dist,
                    closest_candidate = closest_candidate,
                    closest_imposter = closest_imposter,
                    stringsAsFactors = FALSE
                ))
                
                # Print details for first 10 and last 10 iterations
                if(i <= 10 || i > ITERATIONS - 10) {
                    cat(sprintf("  Iter %3d: %s wins | Candidate: %.4f (%s) | Imposter: %.4f (%s)\n",
                               i, 
                               winner,
                               min_candidate_dist,
                               substr(closest_candidate, 1, 30),
                               min_imposter_dist,
                               substr(closest_imposter, 1, 30)))
                }
                
                if(winner == "CANDIDATE") {
                    gi_score <- gi_score + 1
                }
            } else {
                skipped <- skipped + 1
                if(i <= 10 || i > ITERATIONS - 10) {
                    cat("  Iteration", i, ": SKIPPED (NA distances)\n")
                }
            }
            
        }, error = function(e) {
            if(i == 1) {
                cat("  Error in iteration", i, ":", e$message, "\n")
            }
            skipped <<- skipped + 1
            if(i <= 10 || i > ITERATIONS - 10) {
                cat("  Iteration", i, ": ERROR -", e$message, "\n")
            }
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
    cat("  >= 0.66 = Strong support for the primary candidate group\n")
    cat("  <= 0.34 = Not authentic\n")
    cat("  0.34-0.66 = Uncertain (grey zone)\n")
    
    # Analyze iteration log
    if(nrow(iteration_log) > 0) {
        cat("\n--- ITERATION ANALYSIS ---\n")
        candidate_wins <- sum(iteration_log$winner == "CANDIDATE")
        imposter_wins <- sum(iteration_log$winner == "IMPOSTER")
        cat("Candidate wins:", candidate_wins, "/", nrow(iteration_log), 
            sprintf("(%.1f%%)\n", 100 * candidate_wins / nrow(iteration_log)))
        cat("Imposter wins:", imposter_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * imposter_wins / nrow(iteration_log)))
        
        cat("\nAverage distances:\n")
        cat("  Candidate group:", sprintf("%.4f", mean(iteration_log$candidate_dist, na.rm=TRUE)), "\n")
        cat("  Imposter:", sprintf("%.4f", mean(iteration_log$imposter_dist, na.rm=TRUE)), "\n")
        
        cat("\nMost frequently closest candidate text:\n")
        candidate_freq <- table(iteration_log$closest_candidate)
        candidate_top <- head(sort(candidate_freq, decreasing=TRUE), 3)
        for(i in seq_along(candidate_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       i, names(candidate_top)[i], candidate_top[i],
                       100 * candidate_top[i] / nrow(iteration_log)))
        }
        
        cat("\nMost frequently closest Imposter:\n")
        imposter_freq <- table(iteration_log$closest_imposter)
        imposter_top <- head(sort(imposter_freq, decreasing=TRUE), 5)
        for(i in seq_along(imposter_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       i, names(imposter_top)[i], imposter_top[i],
                       100 * imposter_top[i] / nrow(iteration_log)))
        }
        
        cat("\nWhen Imposter wins, who wins most often:\n")
        imposter_winner_log <- iteration_log[iteration_log$winner == "IMPOSTER", ]
        if(nrow(imposter_winner_log) > 0) {
            imposter_winner_freq <- table(imposter_winner_log$closest_imposter)
            imposter_winner_top <- head(sort(imposter_winner_freq, decreasing=TRUE), 5)
            for(i in seq_along(imposter_winner_top)) {
                cat(sprintf("  %d. %s (%d times, %.1f%% of imposter wins)\n", 
                           i, names(imposter_winner_top)[i], imposter_winner_top[i],
                           100 * imposter_winner_top[i] / nrow(imposter_winner_log)))
            }
        }
    }
    
    return(list(
        setup = setup_name,
        score = final_probability,
        successful = successful_iterations,
        skipped = skipped,
        total = ITERATIONS,
        iteration_log = iteration_log
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

# Interpretation
cat("INTERPRETATION:\n")
cat("  >= 0.66 = Strong support for the primary candidate group\n")
cat("  <= 0.34 = Text NOT authenticated\n")
cat("  0.34-0.66 = Grey zone (uncertain)\n")
cat("\n")

# Determine overall verdict
authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score >= 0.66))
not_authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score <= 0.34))
uncertain_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score > 0.34 && x$score < 0.66))

cat("OVERALL VERDICT:\n")
cat("  Authenticated:", authenticated_count, "/ 6 tests\n")
cat("  Not authenticated:", not_authenticated_count, "/ 6 tests\n")
cat("  Uncertain:", uncertain_count, "/ 6 tests\n")
cat("\n")

if(authenticated_count >= 4) {
    cat("CONCLUSION: Strong evidence for the primary candidate group\n")
} else if(authenticated_count >= 2) {
    cat("CONCLUSION: Moderate evidence for the primary candidate group\n")
} else if(not_authenticated_count >= 4) {
    cat("CONCLUSION: Strong evidence against the primary candidate group\n")
} else {
    cat("CONCLUSION: Inconclusive results\n")
}

cat("\n========================================\n")
cat("Test completed!\n")
cat("========================================\n")
