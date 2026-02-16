#!/usr/bin/env Rscript
# GI Authorship Verification - Test All Disputed Texts
# Tests all files starting with "Disputed_" against:
#   - Candidates: Files starting with "Sankara_"
#   - Imposters: All other files (not Disputed_, not Sankara_)
#
# Tests: 12 configurations total (4 n-gram types × 3 distance metrics)
#   - Character trigrams: MinMax, Cosine, Wurzburg
#   - Word trigrams: MinMax, Cosine, Wurzburg
#   - Word bigrams: MinMax, Cosine, Wurzburg
#   - Word unigrams: MinMax, Cosine, Wurzburg

library(stylo)

# Set seed for reproducibility
set.seed(123)

# Start logging to file (on.exit ensures sink is closed even on error)
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
log_file <- file.path(OUTPUT_DIR, paste0("gi_results_log_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".txt"))
sink(log_file, split = TRUE)  # split=TRUE means output goes to both console AND file
on.exit(sink(), add = TRUE)

# ================================================
# CONFIGURATION
# ================================================

CORPUS_DIR <- "corpus/main"
OUTPUT_DIR <- "results"
ITERATIONS <- 100
FEATURE_COUNT <- 2000
FEATURE_SAMPLE_RATE <- 0.50
IMPOSTER_SAMPLE_RATE <- 0.50
DISPUTED_PATTERN <- "^Disputed_"

# ================================================
# FUNCTIONS
# ================================================

# Load n-gram corpus, build frequency list (excluding disputed from feature selection), return frequency table
load_ngram_freq_table <- function(ngram_type, ngram_size, label) {
    cat("\nLoading", label, "corpus...\n")
    raw_full <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, ngram.type = ngram_type, ngram.size = ngram_size)
    non_disputed <- raw_full[!grepl(DISPUTED_PATTERN, names(raw_full))]
    cat("Excluding disputed texts from frequency list construction...\n")
    cat("Making", label, "frequency list (based on", length(non_disputed), "non-disputed texts)...\n")
    top_features <- make.frequency.list(non_disputed, head = FEATURE_COUNT)
    cat("Creating", label, "frequency table (including all texts)...\n")
    make.table.of.frequencies(corpus = raw_full, features = top_features)
}

# Function to run a single GI test
run_gi_test <- function(freq_table, target_name, distance_func, setup_name) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("Target:", target_name, "\n")
    cat("================================================\n")
    
    # Define test sets
    # Candidates: Files starting with "Sankara_"
    sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
    
    # Imposters: Everything except Disputed_ and Sankara_
    imposter_rows <- rownames(freq_table)[!grepl("^Sankara_", rownames(freq_table)) & 
                                           !grepl("^Disputed_", rownames(freq_table))]
    
    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", target_name, "\n")
    cat("  Sankara candidates:", length(sankara_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")
    
    # Safety checks
    if(length(sankara_rows) == 0) {
        warning("No Sankara candidate files found.")
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
    
    # Store iteration details for analysis (preallocate list to avoid slow rbind in loop)
    iteration_log_list <- vector("list", ITERATIONS)
    log_idx <- 0L
    
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
        comparison_names <- c(target_name, sankara_rows, current_imposters)
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
            sankara_dists <- dists_from_test[sankara_rows]
            imposter_dists <- dists_from_test[current_imposters]
            
            min_sankara_dist <- min(sankara_dists, na.rm = TRUE)
            min_imposter_dist <- min(imposter_dists, na.rm = TRUE)
            
            closest_sankara <- names(which.min(sankara_dists))
            closest_imposter <- names(which.min(imposter_dists))
            
            # Determine winner and score
            if(!is.na(min_sankara_dist) && !is.na(min_imposter_dist)) {
                winner <- if(min_sankara_dist < min_imposter_dist) "SANKARA" else "IMPOSTER"
                
                # Log the iteration (append to list)
                log_idx <- log_idx + 1L
                iteration_log_list[[log_idx]] <- data.frame(
                    iteration = i,
                    winner = winner,
                    sankara_dist = min_sankara_dist,
                    imposter_dist = min_imposter_dist,
                    closest_sankara = closest_sankara,
                    closest_imposter = closest_imposter,
                    stringsAsFactors = FALSE
                )
                
                if(winner == "SANKARA") {
                    gi_score <- gi_score + 1
                }
            } else {
                skipped <- skipped + 1
            }
            
        }, error = function(e) {
            skipped <<- skipped + 1
        })
    }
    
    # Combine iteration log entries into data frame
    iteration_log <- if(log_idx > 0) {
        do.call(rbind, iteration_log_list[seq_len(log_idx)])
    } else {
        data.frame(
            iteration = integer(), winner = character(),
            sankara_dist = numeric(), imposter_dist = numeric(),
            closest_sankara = character(), closest_imposter = character(),
            stringsAsFactors = FALSE
        )
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
        sankara_wins <- sum(iteration_log$winner == "SANKARA")
        imposter_wins <- sum(iteration_log$winner == "IMPOSTER")
        cat("Sankara wins:", sankara_wins, "/", nrow(iteration_log), 
            sprintf("(%.1f%%)\n", 100 * sankara_wins / nrow(iteration_log)))
        cat("Imposter wins:", imposter_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * imposter_wins / nrow(iteration_log)))
        
        cat("\nAverage distances:\n")
        cat("  Sankara:", sprintf("%.4f", mean(iteration_log$sankara_dist, na.rm = TRUE)), "\n")
        cat("  Imposter:", sprintf("%.4f", mean(iteration_log$imposter_dist, na.rm = TRUE)), "\n")
        
        cat("\nMost frequently closest Sankara text:\n")
        sankara_freq <- table(iteration_log$closest_sankara)
        sankara_top <- head(sort(sankara_freq, decreasing = TRUE), 3)
        for(j in seq_along(sankara_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       j, names(sankara_top)[j], sankara_top[j],
                       100 * sankara_top[j] / nrow(iteration_log)))
        }
        
        cat("\nMost frequently closest Imposter:\n")
        imposter_freq <- table(iteration_log$closest_imposter)
        imposter_top <- head(sort(imposter_freq, decreasing = TRUE), 5)
        for(j in seq_along(imposter_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n", 
                       j, names(imposter_top)[j], imposter_top[j],
                       100 * imposter_top[j] / nrow(iteration_log)))
        }
        
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
cat("Output directory:", OUTPUT_DIR, "\n")
cat("Iterations per test:", ITERATIONS, "\n")
cat("Feature count:", FEATURE_COUNT, "\n")
cat("Feature sample rate:", FEATURE_SAMPLE_RATE * 100, "%\n")
cat("Imposter sample rate:", IMPOSTER_SAMPLE_RATE * 100, "%\n")
cat("\n")

# Load and parse corpus using helper (run from papers/2024-otao/ or set CORPUS_DIR accordingly)
freq_table_trigrams   <- load_ngram_freq_table("c", 3, "character trigram")
freq_table_unigrams   <- load_ngram_freq_table("w", 1, "word unigram")
freq_table_bigrams    <- load_ngram_freq_table("w", 2, "word bigram")
freq_table_word_trigrams <- load_ngram_freq_table("w", 3, "word trigram")

# Get list of all disputed texts (files that start with "Disputed_")
all_texts <- rownames(freq_table_trigrams)
disputed_texts <- grep(DISPUTED_PATTERN, all_texts, value = TRUE)
sankara_texts <- grep("^Sankara_", all_texts, value = TRUE)
imposter_texts <- all_texts[!grepl("^Sankara_", all_texts) & !grepl(DISPUTED_PATTERN, all_texts)]

cat("\n========================================\n")
cat("CORPUS BREAKDOWN:\n")
cat("========================================\n")
cat("Disputed texts (to be tested):", length(disputed_texts), "\n")
cat("Sankara candidates:", length(sankara_texts), "\n")
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
    list(name = "Trigrams + MinMax", ngram = "trigrams", dist_func = dist.minmax),
    list(name = "Trigrams + Cosine", ngram = "trigrams", dist_func = dist.cosine),
    list(name = "Trigrams + Wurzburg", ngram = "trigrams", dist_func = dist.wurzburg),
    # Word trigrams
    list(name = "Word Trigrams + MinMax", ngram = "word_trigrams", dist_func = dist.minmax),
    list(name = "Word Trigrams + Cosine", ngram = "word_trigrams", dist_func = dist.cosine),
    list(name = "Word Trigrams + Wurzburg", ngram = "word_trigrams", dist_func = dist.wurzburg),
    list(name = "Word Bigrams + MinMax", ngram = "bigrams", dist_func = dist.minmax),
    list(name = "Word Bigrams + Cosine", ngram = "bigrams", dist_func = dist.cosine),
    list(name = "Word Bigrams + Wurzburg", ngram = "bigrams", dist_func = dist.wurzburg),
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
        } else if(config$ngram == "word_trigrams") {
            freq_table_word_trigrams
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
        
        cat("  Authenticated (>=0.66):", authenticated_count, "/ 12 tests\n")
        cat("  Not authenticated (<=0.34):", not_authenticated_count, "/ 12 tests\n")
        cat("  Uncertain (0.34-0.66):", uncertain_count, "/ 12 tests\n")
        
        avg_score <- mean(sapply(target_results, function(x) x$score), na.rm = TRUE)
        cat("  Average score:", sprintf("%.3f", avg_score), "\n")
        
        if(authenticated_count >= 9) {
            cat("  VERDICT: Strong evidence for Sankara authorship\n")
        } else if(authenticated_count >= 6) {
            cat("  VERDICT: Moderate evidence for Sankara authorship\n")
        } else if(not_authenticated_count >= 9) {
            cat("  VERDICT: Strong evidence AGAINST Sankara authorship\n")
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

output_file <- file.path(OUTPUT_DIR, paste0("gi_results_all_disputed_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".csv"))
write.csv(results_csv, output_file, row.names = FALSE)
cat("\nResults saved to:", output_file, "\n")

# Stop logging
sink()
cat("\nLog saved to:", log_file, "\n")