#!/usr/bin/env Rscript
# GI Authorship Verification - Test All Disputed Texts
# Tests all files starting with "Disputed_" against:
#   - Primary candidates: files matching CANDIDATE_PATTERN
#   - Imposters: all other files except disputed texts

library(stylo)

# Set seed for reproducibility
set.seed(123)

# Start logging to file
log_file <- paste0("gi_results_log_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".txt")
sink(log_file, split = TRUE)  # split=TRUE means output goes to both console AND file

# ================================================
# CONFIGURATION
# ================================================

CORPUS_DIR <- "corpus/main"
# Adjust this to the filename pattern used for your primary candidate group.
CANDIDATE_PATTERN <- "^Candidate_"
ITERATIONS <- 100
FEATURE_COUNT <- 2000
# FEATURE_COUNT <- NULL
FEATURE_SAMPLE_RATE <- 0.50
IMPOSTER_SAMPLE_RATE <- 0.50

# ================================================
# FUNCTIONS
# ================================================

# Function to run a single GI test
run_gi_test <- function(freq_table, target_name, distance_func, setup_name) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("Target:", target_name, "\n")
    cat("================================================\n")
    
    # Define test sets
    # Primary candidates: files matching the configured candidate pattern
    candidate_rows <- grep(CANDIDATE_PATTERN, rownames(freq_table), value = TRUE)
    
    # Imposters: everything except disputed texts and primary candidates
    imposter_rows <- rownames(freq_table)[!grepl(CANDIDATE_PATTERN, rownames(freq_table)) & 
                                           !grepl("^Disputed_", rownames(freq_table))]
    
    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", target_name, "\n")
    cat("  Primary candidates:", length(candidate_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")
    
    # Safety checks
    if(length(candidate_rows) == 0) {
        warning("No primary candidate files found.")
        return(NULL)
    }
    if(length(imposter_rows) == 0) {
        warning("No imposter files found.")
        return(NULL)
    }
    if(!(target_name %in% rownames(freq_table))) {
        warning("Target text not found in corpus!")
        return(NULL)
    }
    
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
    
    for(i in 1:ITERATIONS) {
        if(i %% 20 == 0) {
            cat("  Progress:", i, "/", ITERATIONS, "\n")
        }
        
        # Sample features and imposters
        current_features <- sample(colnames(freq_table), 
                                   size = floor(ncol(freq_table) * FEATURE_SAMPLE_RATE))
        current_imposters <- sample(imposter_rows, 
                                    size = floor(length(imposter_rows) * IMPOSTER_SAMPLE_RATE))
        
        # Build comparison matrix
        comparison_names <- c(target_name, candidate_rows, current_imposters)
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
            dists_from_test <- dist_matrix[target_name, ]
            
            # Find minimum distances
            candidate_dists <- dists_from_test[candidate_rows]
            imposter_dists <- dists_from_test[current_imposters]
            
            min_candidate_dist <- min(candidate_dists, na.rm = TRUE)
            min_imposter_dist <- min(imposter_dists, na.rm = TRUE)
            
            closest_candidate <- names(which.min(candidate_dists))
            closest_imposter <- names(which.min(imposter_dists))
            
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
                
                if(winner == "CANDIDATE") {
                    gi_score <- gi_score + 1
                }
            } else {
                skipped <- skipped + 1
            }
            
        }, error = function(e) {
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
    cat("Final Probability:", sprintf("%.3f", final_probability), "\n")
    
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
        cat("  Candidate group:", sprintf("%.4f", mean(iteration_log$candidate_dist, na.rm = TRUE)), "\n")
        cat("  Imposter:", sprintf("%.4f", mean(iteration_log$imposter_dist, na.rm = TRUE)), "\n")
        
        cat("\nMost frequently closest candidate text:\n")
        candidate_freq <- table(iteration_log$closest_candidate)
        candidate_top <- head(sort(candidate_freq, decreasing = TRUE), 3)
        for(j in seq_along(candidate_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       j, names(candidate_top)[j], candidate_top[j],
                       100 * candidate_top[j] / nrow(iteration_log)))
        }
        
        cat("\nMost frequently closest Imposter:\n")
        imposter_freq <- table(iteration_log$closest_imposter)
        imposter_top <- head(sort(imposter_freq, decreasing = TRUE), 5)
        for(j in seq_along(imposter_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       j, names(imposter_top)[j], imposter_top[j],
                       100 * imposter_top[j] / nrow(iteration_log)))
        }
        
        # cat("\nWhen Imposter wins, who wins most often:\n")
#         imposter_winner_log <- iteration_log[iteration_log$winner == "IMPOSTER", ]
#         if(nrow(imposter_winner_log) > 0) {
#             imposter_winner_freq <- table(imposter_winner_log$closest_imposter)
#             imposter_winner_top <- head(sort(imposter_winner_freq, decreasing = TRUE), 5)
#             for(j in seq_along(imposter_winner_top)) {
#                 cat(sprintf("  %d. %s (%d times, %.1f%% of imposter wins)\n",
#                            j, names(imposter_winner_top)[j], imposter_winner_top[j],
#                            100 * imposter_winner_top[j] / nrow(imposter_winner_log)))
#             }
#         } else {
#             cat("  (Imposter never won)\n")
#         }
    }
    
    return(list(
        target = target_name,
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
cat("ALL DISPUTED TEXTS\n")
cat("========================================\n")
cat("Corpus directory:", CORPUS_DIR, "\n")
cat("Iterations per test:", ITERATIONS, "\n")
cat("Feature count:", FEATURE_COUNT, "\n")
cat("Feature sample rate:", FEATURE_SAMPLE_RATE * 100, "%\n")
cat("Imposter sample rate:", IMPOSTER_SAMPLE_RATE * 100, "%\n")
cat("\n")

# Load and parse corpus ONCE (to save time)
cat("Loading trigram corpus (this may take a while)...\n")
raw_data_trigrams_full <- load.corpus.and.parse(
    corpus.dir = CORPUS_DIR, 
    ngram.type = "c", 
    ngram.size = 3
)

# Remove disputed texts from raw data for frequency list construction
cat("Excluding disputed texts from frequency list construction...\n")
disputed_pattern <- "^Disputed_"
non_disputed_indices <- !grepl(disputed_pattern, names(raw_data_trigrams_full))
raw_data_trigrams <- raw_data_trigrams_full[non_disputed_indices]

cat("Making trigram frequency list (based on", length(raw_data_trigrams), "non-disputed texts)...\n")
top_features_trigrams <- make.frequency.list(raw_data_trigrams, head = FEATURE_COUNT)

cat("Creating trigram frequency table (including all texts)...\n")
freq_table_trigrams <- make.table.of.frequencies(
    corpus = raw_data_trigrams_full, 
    features = top_features_trigrams
)

cat("\nLoading unigram corpus...\n")
raw_data_unigrams_full <- load.corpus.and.parse(
    corpus.dir = CORPUS_DIR, 
    ngram.type = "w", 
    ngram.size = 1
)

# Remove disputed texts from raw data for frequency list construction
cat("Excluding disputed texts from frequency list construction...\n")
non_disputed_indices <- !grepl(disputed_pattern, names(raw_data_unigrams_full))
raw_data_unigrams <- raw_data_unigrams_full[non_disputed_indices]

cat("Making unigram frequency list (based on", length(raw_data_unigrams), "non-disputed texts)...\n")
top_features_unigrams <- make.frequency.list(raw_data_unigrams, head = FEATURE_COUNT)

cat("Creating unigram frequency table (including all texts)...\n")
freq_table_unigrams <- make.table.of.frequencies(
    corpus = raw_data_unigrams_full, 
    features = top_features_unigrams
)

cat("\nLoading word bigram corpus...\n")
raw_data_bigrams_full <- load.corpus.and.parse(
    corpus.dir = CORPUS_DIR, 
    ngram.type = "w", 
    ngram.size = 2
)

# Remove disputed texts from raw data for frequency list construction
cat("Excluding disputed texts from frequency list construction...\n")
non_disputed_indices <- !grepl(disputed_pattern, names(raw_data_bigrams_full))
raw_data_bigrams <- raw_data_bigrams_full[non_disputed_indices]

cat("Making word bigram frequency list (based on", length(raw_data_bigrams), "non-disputed texts)...\n")
top_features_bigrams <- make.frequency.list(raw_data_bigrams, head = FEATURE_COUNT)

cat("Creating word bigram frequency table (including all texts)...\n")
freq_table_bigrams <- make.table.of.frequencies(
    corpus = raw_data_bigrams_full, 
    features = top_features_bigrams
)

# Get list of all disputed texts (files that start with "Disputed_")
all_texts <- rownames(freq_table_trigrams)
disputed_texts <- grep("^Disputed_", all_texts, value = TRUE)
candidate_texts <- grep(CANDIDATE_PATTERN, all_texts, value = TRUE)
imposter_texts <- all_texts[!grepl(CANDIDATE_PATTERN, all_texts) & !grepl("^Disputed_", all_texts)]

cat("\n========================================\n")
cat("CORPUS BREAKDOWN:\n")
cat("========================================\n")
cat("Disputed texts (to be tested):", length(disputed_texts), "\n")
cat("Primary candidates:", length(candidate_texts), "\n")
cat("Imposter texts:", length(imposter_texts), "\n")
cat("Total texts:", length(all_texts), "\n\n")

if(length(disputed_texts) == 0) {
    stop("No files starting with 'Disputed_' found in corpus!")
}

cat("Disputed texts to test:\n")
for(i in seq_along(disputed_texts)) {
    cat("  ", i, ".", disputed_texts[i], "\n")
}
cat("========================================\n\n")

# Store all results
all_results <- list()
result_counter <- 1

# Test configurations to run
test_configs <- list(
    # list(name = "Trigrams + Classic Delta", ngram = "trigrams", dist_func = dist.delta),
    list(name = "Trigrams + MinMax", ngram = "trigrams", dist_func = dist.minmax),
    list(name = "Trigrams + Cosine", ngram = "trigrams", dist_func = dist.cosine),
    list(name = "Trigrams + Wurzburg", ngram = "trigrams", dist_func = dist.wurzburg),
    # list(name = "Word Bigrams + Classic Delta", ngram = "bigrams", dist_func = dist.delta),
    list(name = "Word Bigrams + MinMax", ngram = "bigrams", dist_func = dist.minmax),
    list(name = "Word Bigrams + Cosine", ngram = "bigrams", dist_func = dist.cosine),
    list(name = "Word Bigrams + Wurzburg", ngram = "bigrams", dist_func = dist.wurzburg),
    # list(name = "Unigrams + Classic Delta", ngram = "unigrams", dist_func = dist.delta),
    list(name = "Unigrams + MinMax", ngram = "unigrams", dist_func = dist.minmax),
    list(name = "Unigrams + Cosine", ngram = "unigrams", dist_func = dist.cosine),
    list(name = "Unigrams + Wurzburg", ngram = "unigrams", dist_func = dist.wurzburg)
)

# Loop through each disputed text
for(target_text in disputed_texts) {
    cat("\n\n")
    cat("########################################\n")
    cat("TESTING TARGET:", target_text, "\n")
    cat("########################################\n")
    
    # Run all test configurations for this target
    for(config in test_configs) {
        # Select appropriate frequency table
        freq_table <- if(config$ngram == "trigrams") {
            freq_table_trigrams
        } else if(config$ngram == "bigrams") {
            freq_table_bigrams
        } else {
            freq_table_unigrams
        }
        
        result <- run_gi_test(
            freq_table = freq_table,
            target_name = target_text,
            distance_func = config$dist_func,
            setup_name = config$name
        )
        
        if(!is.null(result)) {
            all_results[[result_counter]] <- result
            result_counter <- result_counter + 1
        }
    }
}

# ================================================
# FINAL SUMMARY
# ================================================

cat("\n\n")
cat("========================================\n")
cat("FINAL SUMMARY - ALL DISPUTED TEXTS\n")
cat("========================================\n\n")

# Create comprehensive summary table
summary_df <- data.frame(
    Target = sapply(all_results, function(x) x$target),
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) sprintf("%.3f", x$score)),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    stringsAsFactors = FALSE
)

print(summary_df, row.names = FALSE)

# Create summary by target text
cat("\n\n========================================\n")
cat("SUMMARY BY TARGET TEXT\n")
cat("========================================\n\n")

for(target_text in disputed_texts) {
    cat("\n", target_text, ":\n", sep = "")
    target_results <- all_results[sapply(all_results, function(x) x$target == target_text)]
    
    if(length(target_results) > 0) {
        authenticated_count <- sum(sapply(target_results, function(x) {
            !is.na(x$score) && x$score >= 0.66
        }))
        not_authenticated_count <- sum(sapply(target_results, function(x) {
            !is.na(x$score) && x$score <= 0.34
        }))
        uncertain_count <- sum(sapply(target_results, function(x) {
            !is.na(x$score) && x$score > 0.34 && x$score < 0.66
        }))
        
        cat("  Authenticated (>=0.66):", authenticated_count, "/ 9 tests\n")
        cat("  Not authenticated (<=0.34):", not_authenticated_count, "/ 9 tests\n")
        cat("  Uncertain (0.34-0.66):", uncertain_count, "/ 9 tests\n")
        
        avg_score <- mean(sapply(target_results, function(x) x$score), na.rm = TRUE)
        cat("  Average score:", sprintf("%.3f", avg_score), "\n")
        
        if(authenticated_count >= 7) {
            cat("  VERDICT: Strong evidence for the primary candidate group\n")
        } else if(authenticated_count >= 5) {
            cat("  VERDICT: Moderate evidence for the primary candidate group\n")
        } else if(not_authenticated_count >= 7) {
            cat("  VERDICT: Strong evidence against the primary candidate group\n")
        } else {
            cat("  VERDICT: Inconclusive results\n")
        }
    }
}

cat("\n========================================\n")
cat("All tests completed!\n")
cat("========================================\n")

# Save results to CSV for later analysis
results_csv <- data.frame(
    Target = sapply(all_results, function(x) x$target),
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) x$score),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    Total = sapply(all_results, function(x) x$total),
    stringsAsFactors = FALSE
)

output_file <- paste0("gi_results_all_disputed_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".csv")
write.csv(results_csv, output_file, row.names = FALSE)
cat("\nResults saved to:", output_file, "\n")
