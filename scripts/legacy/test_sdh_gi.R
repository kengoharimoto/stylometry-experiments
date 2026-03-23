#!/usr/bin/env Rscript
# GI Authorship Verification - SDh vs SDh_sdhsviv
# Tests whether SDh_sdhuv_unsandhied.txt has the same authorship as SDh_sdhsviv_unsandhied.txt
# Uses corpus/sdhv_gi with:
#   - Target: SDh_sdhuv_unsandhied.txt (query text)
#   - Candidate: SDh_sdhsviv_unsandhied.txt (hypothesized same author)
#   - Imposters: All other texts in the corpus
#
# Tests: 6 configurations (character trigrams + word unigrams × 3 distance metrics)
#
# Optional command-line overrides:
#   Rscript test_sdh_gi.R --feature-count=3000 --feature-sample-rate=0.6 --imposter-sample-rate=0.4

library(stylo)

# Set seed for reproducibility
set.seed(123)

# ================================================
# CONFIGURATION
# ================================================

CORPUS_DIR <- "corpus/sdhv_gi"
OUTPUT_DIR <- "results"
TARGET_NAME <- "SDh_sdhuv_unsandhied"
CANDIDATE_NAME <- "SDh_sdhsviv_unsandhied"

ITERATIONS <- 100
FEATURE_COUNT <- 2000
FEATURE_SAMPLE_RATE <- 0.50
IMPOSTER_SAMPLE_RATE <- 0.50

# Parse command-line overrides: --feature-count=2000 --feature-sample-rate=0.5 --imposter-sample-rate=0.5
args <- commandArgs(trailingOnly = TRUE)
for (a in args) {
  if (grepl("^--feature-count=", a)) FEATURE_COUNT <- as.integer(sub("^--feature-count=", "", a))
  if (grepl("^--feature-sample-rate=", a)) FEATURE_SAMPLE_RATE <- as.numeric(sub("^--feature-sample-rate=", "", a))
  if (grepl("^--imposter-sample-rate=", a)) IMPOSTER_SAMPLE_RATE <- as.numeric(sub("^--imposter-sample-rate=", "", a))
}

# Start logging to file (on.exit ensures sink is closed even on error)
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
log_file <- file.path(OUTPUT_DIR, paste0("gi_results_sdh_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".txt"))
sink(log_file, split = TRUE)
on.exit(sink(), add = TRUE)

# ================================================
# FUNCTIONS
# ================================================

# Load n-gram corpus, build frequency list (excluding target from feature selection), return frequency table
load_ngram_freq_table <- function(ngram_type, ngram_size, label, exclude_from_features) {
    cat("\nLoading", label, "corpus...\n")
    raw_full <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, ngram.type = ngram_type, ngram.size = ngram_size)
    # Exclude target from feature list construction
    for_exclude <- names(raw_full) %in% exclude_from_features
    non_query <- raw_full[!for_exclude]
    cat("Excluding target from frequency list construction...\n")
    cat("Making", label, "frequency list (based on", length(non_query), "texts)...\n")
    top_features <- make.frequency.list(non_query, head = FEATURE_COUNT)
    cat("Creating", label, "frequency table (including all texts)...\n")
    make.table.of.frequencies(corpus = raw_full, features = top_features)
}

# Function to run a single GI test
run_gi_test <- function(freq_table, target_name, candidate_rows, imposter_rows, distance_func, setup_name) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("Target:", target_name, "\n")
    cat("Candidate (same-author hypothesis):", paste(candidate_rows, collapse = ", "), "\n")
    cat("================================================\n")

    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", target_name, "\n")
    cat("  Candidate(s):", length(candidate_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")

    # Safety checks
    if(length(candidate_rows) == 0) {
        warning("No candidate files found.")
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

    gi_score <- 0
    skipped <- 0
    iteration_log_list <- vector("list", ITERATIONS)
    log_idx <- 0L

    cat("Running", ITERATIONS, "iterations...\n")

    for(i in 1:ITERATIONS) {
        if(i %% 20 == 0) {
            cat("  Progress:", i, "/", ITERATIONS, "\n")
        }

        current_features <- sample(colnames(freq_table),
                                   size = floor(ncol(freq_table) * FEATURE_SAMPLE_RATE))
        current_imposters <- sample(imposter_rows,
                                    size = floor(length(imposter_rows) * IMPOSTER_SAMPLE_RATE))

        comparison_names <- c(target_name, candidate_rows, current_imposters)
        current_matrix <- freq_table[comparison_names, current_features]

        tryCatch({
            dist_matrix <- as.matrix(distance_func(current_matrix))

            if(any(is.na(dist_matrix)) || any(is.infinite(dist_matrix))) {
                skipped <- skipped + 1
                next
            }

            dists_from_test <- dist_matrix[target_name, ]
            candidate_dists <- dists_from_test[candidate_rows]
            imposter_dists <- dists_from_test[current_imposters]

            min_candidate_dist <- min(candidate_dists, na.rm = TRUE)
            min_imposter_dist <- min(imposter_dists, na.rm = TRUE)

            closest_candidate <- names(which.min(candidate_dists))
            closest_imposter <- names(which.min(imposter_dists))

            if(!is.na(min_candidate_dist) && !is.na(min_imposter_dist)) {
                winner <- if(min_candidate_dist < min_imposter_dist) "CANDIDATE" else "IMPOSTER"

                log_idx <- log_idx + 1L
                iteration_log_list[[log_idx]] <- data.frame(
                    iteration = i,
                    winner = winner,
                    candidate_dist = min_candidate_dist,
                    imposter_dist = min_imposter_dist,
                    closest_candidate = closest_candidate,
                    closest_imposter = closest_imposter,
                    stringsAsFactors = FALSE
                )

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

    iteration_log <- if(log_idx > 0) {
        do.call(rbind, iteration_log_list[seq_len(log_idx)])
    } else {
        data.frame(
            iteration = integer(), winner = character(),
            candidate_dist = numeric(), imposter_dist = numeric(),
            closest_candidate = character(), closest_imposter = character(),
            stringsAsFactors = FALSE
        )
    }

    successful_iterations <- ITERATIONS - skipped
    final_probability <- if(successful_iterations > 0) {
        gi_score / successful_iterations
    } else {
        NA
    }

    cat("\n--- RESULTS ---\n")
    cat("Successful iterations:", successful_iterations, "\n")
    cat("Skipped iterations:", skipped, "\n")
    cat("GI Score (CANDIDATE wins):", gi_score, "\n")
    cat("Final Probability:", sprintf("%.3f", final_probability), "\n")
    cat("  >= 0.66 = Same authorship (SDh_sdhuv matches SDh_sdhsviv)\n")
    cat("  <= 0.34 = Different authorship\n")
    cat("  0.34-0.66 = Uncertain\n")

    if(nrow(iteration_log) > 0) {
        cat("\n--- ITERATION ANALYSIS ---\n")
        cand_wins <- sum(iteration_log$winner == "CANDIDATE")
        imp_wins <- sum(iteration_log$winner == "IMPOSTER")
        cat("Candidate (SDh_sdhsviv) wins:", cand_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * cand_wins / nrow(iteration_log)))
        cat("Imposter wins:", imp_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * imp_wins / nrow(iteration_log)))

        cat("\nAverage distances:\n")
        cat("  Candidate:", sprintf("%.4f", mean(iteration_log$candidate_dist, na.rm = TRUE)), "\n")
        cat("  Imposter:", sprintf("%.4f", mean(iteration_log$imposter_dist, na.rm = TRUE)), "\n")

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
cat("GI AUTHORSHIP VERIFICATION\n")
cat("SDh_sdhuv vs SDh_sdhsviv (same author?)\n")
cat("========================================\n")
cat("Corpus directory:", CORPUS_DIR, "\n")
cat("Output directory:", OUTPUT_DIR, "\n")
cat("Target:", TARGET_NAME, "\n")
cat("Candidate:", CANDIDATE_NAME, "\n")
cat("Iterations per test:", ITERATIONS, "\n")
cat("FEATURE_COUNT:", FEATURE_COUNT, "\n")
cat("FEATURE_SAMPLE_RATE:", FEATURE_SAMPLE_RATE, sprintf("(%.0f%%)\n", FEATURE_SAMPLE_RATE * 100))
cat("IMPOSTER_SAMPLE_RATE:", IMPOSTER_SAMPLE_RATE, sprintf("(%.0f%%)\n", IMPOSTER_SAMPLE_RATE * 100))
cat("\n")

# Load corpus (exclude target from feature selection)
freq_table_trigrams <- load_ngram_freq_table("c", 3, "character trigram", TARGET_NAME)
freq_table_unigrams <- load_ngram_freq_table("w", 1, "word unigram", TARGET_NAME)

all_texts <- rownames(freq_table_trigrams)

# Verify target and candidate exist
if(!(TARGET_NAME %in% all_texts)) {
    stop("Target '", TARGET_NAME, "' not found in corpus. Available: ", paste(head(all_texts, 5), collapse = ", "), "...")
}
if(!(CANDIDATE_NAME %in% all_texts)) {
    stop("Candidate '", CANDIDATE_NAME, "' not found in corpus.")
}

candidate_rows <- CANDIDATE_NAME
imposter_rows <- all_texts[all_texts != TARGET_NAME & all_texts != CANDIDATE_NAME]

cat("\n========================================\n")
cat("CORPUS BREAKDOWN:\n")
cat("========================================\n")
cat("Target:", TARGET_NAME, "\n")
cat("Candidate:", CANDIDATE_NAME, "\n")
cat("Imposter texts:", length(imposter_rows), "\n")
cat("Total texts:", length(all_texts), "\n\n")

test_configs <- list(
    list(name = "Trigrams + MinMax", ngram = "trigrams", dist_func = dist.minmax),
    list(name = "Trigrams + Cosine", ngram = "trigrams", dist_func = dist.cosine),
    list(name = "Trigrams + Wurzburg", ngram = "trigrams", dist_func = dist.wurzburg),
    list(name = "Unigrams + MinMax", ngram = "unigrams", dist_func = dist.minmax),
    list(name = "Unigrams + Cosine", ngram = "unigrams", dist_func = dist.cosine),
    list(name = "Unigrams + Wurzburg", ngram = "unigrams", dist_func = dist.wurzburg)
)

all_results <- list()
for(config in test_configs) {
    freq_table <- if(config$ngram == "trigrams") freq_table_trigrams else freq_table_unigrams

    result <- run_gi_test(
        freq_table = freq_table,
        target_name = TARGET_NAME,
        candidate_rows = candidate_rows,
        imposter_rows = imposter_rows,
        distance_func = config$dist_func,
        setup_name = config$name
    )

    if(!is.null(result)) {
        all_results[[length(all_results) + 1]] <- result
    }
}

# ================================================
# FINAL SUMMARY
# ================================================

cat("\n\n")
cat("========================================\n")
cat("FINAL SUMMARY - SDh_sdhuv vs SDh_sdhsviv\n")
cat("========================================\n\n")

summary_df <- data.frame(
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) sprintf("%.3f", x$score)),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    stringsAsFactors = FALSE
)
print(summary_df, row.names = FALSE)

authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score >= 0.66))
not_auth_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score <= 0.34))
uncertain_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score > 0.34 && x$score < 0.66))

cat("\n")
cat("Authenticated (same author, >=0.66):", authenticated_count, "/ 6 tests\n")
cat("Not authenticated (different author, <=0.34):", not_auth_count, "/ 6 tests\n")
cat("Uncertain (0.34-0.66):", uncertain_count, "/ 6 tests\n")

avg_score <- mean(sapply(all_results, function(x) x$score), na.rm = TRUE)
cat("Average score:", sprintf("%.3f", avg_score), "\n\n")

if(authenticated_count >= 5) {
    cat("VERDICT: Strong evidence for SAME authorship (SDh_sdhuv ≈ SDh_sdhsviv)\n")
} else if(authenticated_count >= 4) {
    cat("VERDICT: Moderate evidence for same authorship\n")
} else if(not_auth_count >= 5) {
    cat("VERDICT: Strong evidence for DIFFERENT authorship\n")
} else {
    cat("VERDICT: Inconclusive\n")
}

cat("\n========================================\n")
cat("All tests completed!\n")
cat("========================================\n")

results_csv <- data.frame(
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) x$score),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    Total = sapply(all_results, function(x) x$total),
    stringsAsFactors = FALSE
)
output_file <- file.path(OUTPUT_DIR, paste0("gi_results_sdh_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".csv"))
write.csv(results_csv, output_file, row.names = FALSE)
cat("\nResults saved to:", output_file, "\n")
cat("Log saved to:", log_file, "\n")
