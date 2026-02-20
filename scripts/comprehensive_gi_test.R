#!/usr/bin/env Rscript
# GI Authorship Verification - SDh configurable target/candidates
#
# Example:
#   Rscript scripts/test_sdh_gi_custom_candidates.R \
#     --target=SDh_sdhuv_unsandhied \
#     --candidate-regex='^SDh_' \
#     --exclude-imposters-regex='^SomeKnownOutlier$' \
#     --feature-count=3000 --feature-sample-rate=0.6 --imposter-sample-rate=0.4
#
# Candidate flags supported:
#   --candidates=name1,name2,name3
#   --candidate=name1 --candidate=name2
#   --candidate-regex='^SDh_'
#
# Imposter exclusion flags supported:
#   --exclude-imposters=name1,name2,name3
#   --exclude-imposter=name1
#   --exclude-imposters-regex='pattern'
#   --exclude-imposter-regex='pattern'
#
# Diagnostic flags supported:
#   --diagnostic-mode
#   --diagnostic-top-n=10
#   --iterations=1
#
# Feature-set flag supported:
#   --feature-set=/path/to/features.txt
#   --feature_set=/path/to/features.txt
#
# Log-note flags supported:
#   --note='short note for this run'
#   --log-note='short note for this run'

library(stylo)

set.seed(123)

# ================================================
# CONFIGURATION
# ================================================

CORPUS_DIR <- "corpus/gi"
OUTPUT_DIR <- "results"
TARGET_NAME <- "SDh_sdhuv_unsandhied"
CANDIDATE_NAMES <- c("SDh_sdhsviv_unsandhied")

ITERATIONS <- 100
FEATURE_COUNT_TRIGRAMS <- 2000
FEATURE_COUNT_UNIGRAMS <- 2000
FEATURE_SAMPLE_RATE <- 0.50
IMPOSTER_SAMPLE_RATE <- 0.50
DIAGNOSTIC_MODE <- FALSE
DIAGNOSTIC_TOP_N <- 10
FEATURE_SET_FILE <- NULL
LOG_NOTE <- ""

normalize_name <- function(x) {
    sub("\\.[^.]+$", "", x)
}

# Parse command-line args
args <- commandArgs(trailingOnly = TRUE)
cli_candidate_names <- character(0)
cli_candidate_regexes <- character(0)
cli_imposter_exclude_names <- character(0)
cli_imposter_exclude_regexes <- character(0)
iterations_set_by_cli <- FALSE

for (a in args) {
    if (grepl("^--target=", a)) {
        TARGET_NAME <- sub("^--target=", "", a)
    }
    if (grepl("^--candidate=", a)) {
        val <- sub("^--candidate=", "", a)
        if (nzchar(val)) cli_candidate_names <- c(cli_candidate_names, val)
    }
    if (grepl("^--candidates=", a)) {
        raw_vals <- sub("^--candidates=", "", a)
        vals <- trimws(unlist(strsplit(raw_vals, ",", fixed = TRUE)))
        vals <- vals[nzchar(vals)]
        cli_candidate_names <- c(cli_candidate_names, vals)
    }
    if (grepl("^--candidate-regex=", a)) {
        val <- sub("^--candidate-regex=", "", a)
        if (nzchar(val)) cli_candidate_regexes <- c(cli_candidate_regexes, val)
    }
    if (grepl("^--exclude-imposters-regex=", a)) {
        val <- sub("^--exclude-imposters-regex=", "", a)
        if (nzchar(val)) cli_imposter_exclude_regexes <- c(cli_imposter_exclude_regexes, val)
    }
    if (grepl("^--exclude-imposter-regex=", a)) {
        val <- sub("^--exclude-imposter-regex=", "", a)
        if (nzchar(val)) cli_imposter_exclude_regexes <- c(cli_imposter_exclude_regexes, val)
    }
    if (grepl("^--exclude-imposters=", a)) {
        raw_vals <- sub("^--exclude-imposters=", "", a)
        vals <- trimws(unlist(strsplit(raw_vals, ",", fixed = TRUE)))
        vals <- vals[nzchar(vals)]
        cli_imposter_exclude_names <- c(cli_imposter_exclude_names, vals)
    }
    if (grepl("^--exclude-imposter=", a)) {
        val <- sub("^--exclude-imposter=", "", a)
        if (nzchar(val)) cli_imposter_exclude_names <- c(cli_imposter_exclude_names, val)
    }
    if (grepl("^--feature-count=", a)) {
        val <- as.integer(sub("^--feature-count=", "", a))
        FEATURE_COUNT_TRIGRAMS <- val
        FEATURE_COUNT_UNIGRAMS <- val
    }
    if (grepl("^--feature-count-trigrams=", a)) {
        FEATURE_COUNT_TRIGRAMS <- as.integer(sub("^--feature-count-trigrams=", "", a))
    }
    if (grepl("^--feature-count-unigrams=", a)) {
        FEATURE_COUNT_UNIGRAMS <- as.integer(sub("^--feature-count-unigrams=", "", a))
    }
    if (grepl("^--feature-set=", a)) {
        FEATURE_SET_FILE <- sub("^--feature-set=", "", a)
    }
    if (grepl("^--feature_set=", a)) {
        FEATURE_SET_FILE <- sub("^--feature_set=", "", a)
    }
    if (grepl("^--feature-sample-rate=", a)) {
        FEATURE_SAMPLE_RATE <- as.numeric(sub("^--feature-sample-rate=", "", a))
    }
    if (grepl("^--imposter-sample-rate=", a)) {
        IMPOSTER_SAMPLE_RATE <- as.numeric(sub("^--imposter-sample-rate=", "", a))
    }
    if (a == "--diagnostic-mode") {
        DIAGNOSTIC_MODE <- TRUE
    }
    if (grepl("^--diagnostic-top-n=", a)) {
        DIAGNOSTIC_TOP_N <- as.integer(sub("^--diagnostic-top-n=", "", a))
    }
    if (grepl("^--iterations=", a)) {
        ITERATIONS <- as.integer(sub("^--iterations=", "", a))
        iterations_set_by_cli <- TRUE
    }
    if (grepl("^--note=", a)) {
        LOG_NOTE <- sub("^--note=", "", a)
    }
    if (grepl("^--log-note=", a)) {
        LOG_NOTE <- sub("^--log-note=", "", a)
    }
}

if (length(cli_candidate_names) > 0) {
    CANDIDATE_NAMES <- cli_candidate_names
}

TARGET_NAME <- normalize_name(trimws(TARGET_NAME))
CANDIDATE_NAMES <- unique(normalize_name(trimws(CANDIDATE_NAMES)))
CANDIDATE_NAMES <- CANDIDATE_NAMES[nzchar(CANDIDATE_NAMES)]
cli_candidate_regexes <- unique(trimws(cli_candidate_regexes))
cli_candidate_regexes <- cli_candidate_regexes[nzchar(cli_candidate_regexes)]
cli_imposter_exclude_names <- unique(normalize_name(trimws(cli_imposter_exclude_names)))
cli_imposter_exclude_names <- cli_imposter_exclude_names[nzchar(cli_imposter_exclude_names)]
cli_imposter_exclude_regexes <- unique(trimws(cli_imposter_exclude_regexes))
cli_imposter_exclude_regexes <- cli_imposter_exclude_regexes[nzchar(cli_imposter_exclude_regexes)]

if (TARGET_NAME %in% CANDIDATE_NAMES) {
    stop("Target cannot also be in candidates: ", TARGET_NAME)
}
if (!is.finite(FEATURE_COUNT_TRIGRAMS) || FEATURE_COUNT_TRIGRAMS <= 0) {
    stop("--feature-count-trigrams must be a positive integer (or use --feature-count for both)")
}
if (!is.finite(FEATURE_COUNT_UNIGRAMS) || FEATURE_COUNT_UNIGRAMS <= 0) {
    stop("--feature-count-unigrams must be a positive integer (or use --feature-count for both)")
}
if (!is.finite(FEATURE_SAMPLE_RATE) || FEATURE_SAMPLE_RATE <= 0 || FEATURE_SAMPLE_RATE > 1) {
    stop("--feature-sample-rate must be in (0, 1]")
}
if (!is.finite(IMPOSTER_SAMPLE_RATE) || IMPOSTER_SAMPLE_RATE <= 0 || IMPOSTER_SAMPLE_RATE > 1) {
    stop("--imposter-sample-rate must be in (0, 1]")
}
if (!is.finite(ITERATIONS) || ITERATIONS <= 0) {
    stop("--iterations must be a positive integer")
}
if (!is.finite(DIAGNOSTIC_TOP_N) || DIAGNOSTIC_TOP_N <= 0) {
    stop("--diagnostic-top-n must be a positive integer")
}
if (!is.null(FEATURE_SET_FILE) && !nzchar(trimws(FEATURE_SET_FILE))) {
    stop("--feature-set cannot be empty")
}

read_feature_set <- function(path) {
    if (!file.exists(path)) {
        stop("Feature-set file not found: ", path)
    }
    lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
    raw <- trimws(unlist(strsplit(paste(lines, collapse = " "), "\\s+")))
    raw <- raw[nzchar(raw)]
    feats <- unique(raw)
    if (length(feats) == 0) {
        stop("Feature-set file is empty (no features found): ", path)
    }
    feats
}

FEATURE_SET_TOKENS <- if (!is.null(FEATURE_SET_FILE)) read_feature_set(FEATURE_SET_FILE) else character(0)
RUN_TRIGRAM_TESTS <- is.null(FEATURE_SET_FILE)

if (DIAGNOSTIC_MODE) {
    FEATURE_SAMPLE_RATE <- 1.0
    IMPOSTER_SAMPLE_RATE <- 1.0
    if (!iterations_set_by_cli) {
        ITERATIONS <- 1
    }
}

match_texts_by_regex <- function(texts, patterns, label) {
    if (length(patterns) == 0) return(character(0))
    out <- character(0)
    for (p in patterns) {
        matches <- tryCatch({
            texts[grepl(p, texts, perl = TRUE)]
        }, error = function(e) {
            stop("Invalid regex for ", label, ": '", p, "' (", conditionMessage(e), ")")
        })
        out <- c(out, matches)
    }
    unique(out)
}

# Start logging

dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
log_file <- file.path(OUTPUT_DIR, paste0("gi_results_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".txt"))
sink(log_file, split = TRUE)
on.exit(sink(), add = TRUE)

if (nzchar(trimws(LOG_NOTE))) {
    cat("========================================\n")
    cat("RUN NOTE:\n")
    cat(trimws(LOG_NOTE), "\n")
    cat("========================================\n\n")
}

# ================================================
# FUNCTIONS
# ================================================

load_ngram_freq_table <- function(ngram_type, ngram_size, label, exclude_from_features, feature_count) {
    cat("\nLoading", label, "corpus...\n")
    raw_full <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, ngram.type = ngram_type, ngram.size = ngram_size)
    for_exclude <- names(raw_full) %in% exclude_from_features
    non_query <- raw_full[!for_exclude]
    cat("Excluding target from frequency list construction...\n")
    cat("Making", label, "frequency list (based on", length(non_query), "texts)...\n")
    top_features <- make.frequency.list(non_query, head = feature_count)
    cat("Creating", label, "frequency table (including all texts)...\n")
    make.table.of.frequencies(corpus = raw_full, features = top_features)
}

load_unigram_freq_table_from_feature_set <- function(exclude_from_features, feature_set_tokens) {
    cat("\nLoading word unigram corpus...\n")
    raw_full <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, ngram.type = "w", ngram.size = 1)
    for_exclude <- names(raw_full) %in% exclude_from_features
    non_query <- raw_full[!for_exclude]
    available_features <- unique(unlist(non_query, use.names = FALSE))
    features_in_corpus <- intersect(feature_set_tokens, available_features)
    missing_features <- setdiff(feature_set_tokens, available_features)

    cat("Using feature-set file for word unigram frequency table...\n")
    cat("Feature-set size:", length(feature_set_tokens), "\n")
    cat("Features present in corpus:", length(features_in_corpus), "\n")
    cat("Features missing from corpus:", length(missing_features), "\n")

    if (length(features_in_corpus) == 0) {
        stop("None of the features from --feature-set were found in the corpus.")
    }

    freq_table <- make.table.of.frequencies(corpus = raw_full, features = features_in_corpus)
    list(
        freq_table = freq_table,
        features_in_corpus = features_in_corpus,
        missing_features = missing_features
    )
}

run_gi_test <- function(freq_table, target_name, candidate_rows, imposter_rows, distance_func, setup_name,
                        diagnostic_mode = FALSE, diagnostic_top_n = 10) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("Target:", target_name, "\n")
    cat("Candidate(s):", paste(candidate_rows, collapse = ", "), "\n")
    cat("================================================\n")

    cat("Corpus statistics:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", target_name, "\n")
    cat("  Candidate(s):", length(candidate_rows), "\n")
    cat("  Imposter texts:", length(imposter_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")

    if (length(candidate_rows) == 0) {
        warning("No candidate files found.")
        return(NULL)
    }
    if (length(imposter_rows) == 0) {
        warning("No imposter files found.")
        return(NULL)
    }
    if (!(target_name %in% rownames(freq_table))) {
        warning("Target text not found in corpus!")
        return(NULL)
    }

    diagnostic <- NULL
    if (diagnostic_mode) {
        cat("\n--- DIAGNOSTIC SNAPSHOT (FULL SET, NO SUBSAMPLING) ---\n")
        diagnostic <- tryCatch({
            full_names <- c(target_name, candidate_rows, imposter_rows)
            full_matrix <- freq_table[full_names, , drop = FALSE]
            dist_matrix_full <- as.matrix(distance_func(full_matrix))
            dists_full <- dist_matrix_full[target_name, ]

            candidate_dists_full <- sort(dists_full[candidate_rows], decreasing = FALSE)
            imposter_dists_full <- sort(dists_full[imposter_rows], decreasing = FALSE)
            top_n_c <- min(length(candidate_dists_full), diagnostic_top_n)
            top_n_i <- min(length(imposter_dists_full), diagnostic_top_n)

            min_candidate_full <- if (length(candidate_dists_full) > 0) unname(candidate_dists_full[1]) else NA
            min_imposter_full <- if (length(imposter_dists_full) > 0) unname(imposter_dists_full[1]) else NA
            margin_full <- min_imposter_full - min_candidate_full

            cat("Closest candidate distance:", sprintf("%.6f", min_candidate_full), "\n")
            cat("Closest imposter distance:", sprintf("%.6f", min_imposter_full), "\n")
            cat("Margin (imposter - candidate):", sprintf("%.6f", margin_full), "\n")

            cat("Top", top_n_c, "closest candidates:\n")
            if (top_n_c > 0) {
                for (k in seq_len(top_n_c)) {
                    cat(sprintf("  %d. %s (%.6f)\n", k, names(candidate_dists_full)[k], candidate_dists_full[k]))
                }
            } else {
                cat("  (none)\n")
            }

            cat("Top", top_n_i, "closest imposters:\n")
            if (top_n_i > 0) {
                for (k in seq_len(top_n_i)) {
                    cat(sprintf("  %d. %s (%.6f)\n", k, names(imposter_dists_full)[k], imposter_dists_full[k]))
                }
            } else {
                cat("  (none)\n")
            }

            list(
                min_candidate = min_candidate_full,
                min_imposter = min_imposter_full,
                margin = margin_full
            )
        }, error = function(e) {
            cat("Diagnostic snapshot failed:", conditionMessage(e), "\n")
            NULL
        })
    }

    gi_score <- 0
    skipped <- 0
    iteration_log_list <- vector("list", ITERATIONS)
    log_idx <- 0L

    cat("Running", ITERATIONS, "iterations...\n")

    for (i in 1:ITERATIONS) {
        if (i %% 20 == 0) {
            cat("  Progress:", i, "/", ITERATIONS, "\n")
        }

        current_features <- if (diagnostic_mode) {
            colnames(freq_table)
        } else {
            sample(colnames(freq_table),
                   size = floor(ncol(freq_table) * FEATURE_SAMPLE_RATE))
        }
        current_imposters <- if (diagnostic_mode) {
            imposter_rows
        } else {
            sample(imposter_rows,
                   size = floor(length(imposter_rows) * IMPOSTER_SAMPLE_RATE))
        }

        comparison_names <- c(target_name, candidate_rows, current_imposters)
        current_matrix <- freq_table[comparison_names, current_features]

        tryCatch({
            dist_matrix <- as.matrix(distance_func(current_matrix))

            if (any(is.na(dist_matrix)) || any(is.infinite(dist_matrix))) {
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

            if (!is.na(min_candidate_dist) && !is.na(min_imposter_dist)) {
                winner <- if (min_candidate_dist < min_imposter_dist) "CANDIDATE" else "IMPOSTER"

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

                if (winner == "CANDIDATE") {
                    gi_score <- gi_score + 1
                }
            } else {
                skipped <- skipped + 1
            }

        }, error = function(e) {
            skipped <<- skipped + 1
        })
    }

    iteration_log <- if (log_idx > 0) {
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
    final_probability <- if (successful_iterations > 0) {
        gi_score / successful_iterations
    } else {
        NA
    }

    cat("\n--- RESULTS ---\n")
    cat("Successful iterations:", successful_iterations, "\n")
    cat("Skipped iterations:", skipped, "\n")
    cat("GI Score (CANDIDATE wins):", gi_score, "\n")
    cat("Final Probability:", sprintf("%.3f", final_probability), "\n")
    cat("  >= 0.66 = Same authorship\n")
    cat("  <= 0.34 = Different authorship\n")
    cat("  0.34-0.66 = Uncertain\n")

    if (nrow(iteration_log) > 0) {
        cat("\n--- ITERATION ANALYSIS ---\n")
        cand_wins <- sum(iteration_log$winner == "CANDIDATE")
        imp_wins <- sum(iteration_log$winner == "IMPOSTER")
        cat("Candidate wins:", cand_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * cand_wins / nrow(iteration_log)))
        cat("Imposter wins:", imp_wins, "/", nrow(iteration_log),
            sprintf("(%.1f%%)\n", 100 * imp_wins / nrow(iteration_log)))

        cat("\nAverage distances:\n")
        cat("  Candidate:", sprintf("%.4f", mean(iteration_log$candidate_dist, na.rm = TRUE)), "\n")
        cat("  Imposter:", sprintf("%.4f", mean(iteration_log$imposter_dist, na.rm = TRUE)), "\n")

        cat("\nMost frequently closest Candidate:\n")
        candidate_freq <- table(iteration_log$closest_candidate)
        candidate_top <- head(sort(candidate_freq, decreasing = TRUE), 5)
        for (j in seq_along(candidate_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n",
                       j, names(candidate_top)[j], candidate_top[j],
                       100 * candidate_top[j] / nrow(iteration_log)))
        }

        cat("\nMost frequently closest Imposter:\n")
        imposter_freq <- table(iteration_log$closest_imposter)
        imposter_top <- head(sort(imposter_freq, decreasing = TRUE), 5)
        for (j in seq_along(imposter_top)) {
            cat(sprintf("  %d. %s (%d times, %.1f%%)\n",
                       j, names(imposter_top)[j], imposter_top[j],
                       100 * imposter_top[j] / nrow(iteration_log)))
        }

        cat("\nWhen IMPOSTER wins, who wins most often:\n")
        imposter_winner_log <- iteration_log[iteration_log$winner == "IMPOSTER", ]
        if (nrow(imposter_winner_log) > 0) {
            imposter_winner_freq <- table(imposter_winner_log$closest_imposter)
            imposter_winner_top <- head(sort(imposter_winner_freq, decreasing = TRUE), 5)
            for (j in seq_along(imposter_winner_top)) {
                cat(sprintf("  %d. %s (%d times, %.1f%% of imposter wins)\n",
                           j, names(imposter_winner_top)[j], imposter_winner_top[j],
                           100 * imposter_winner_top[j] / nrow(imposter_winner_log)))
            }
        } else {
            cat("  (Imposter never won)\n")
        }
    }

    return(list(
        target = target_name,
        setup = setup_name,
        score = final_probability,
        successful = successful_iterations,
        skipped = skipped,
        total = ITERATIONS,
        iteration_log = iteration_log,
        diagnostic = diagnostic
    ))
}

get_distance_functions <- function(example_table) {
    distance_names <- sort(ls("package:stylo")[startsWith(ls("package:stylo"), "dist.")])
    distance_configs <- list()

    test_rows <- min(4, nrow(example_table))
    test_cols <- min(20, ncol(example_table))
    if (test_rows < 2 || test_cols < 1) {
        stop("Corpus table is too small to validate distance functions.")
    }
    probe_matrix <- example_table[seq_len(test_rows), seq_len(test_cols), drop = FALSE]

    for (dist_name in distance_names) {
        dist_func <- get(dist_name, envir = asNamespace("stylo"))
        is_ok <- TRUE
        err_msg <- NULL

        tryCatch({
            dist_matrix <- as.matrix(dist_func(probe_matrix))
            if (nrow(dist_matrix) != test_rows || ncol(dist_matrix) != test_rows) {
                is_ok <- FALSE
                err_msg <- "returned unexpected matrix shape"
            }
        }, error = function(e) {
            is_ok <<- FALSE
            err_msg <<- conditionMessage(e)
        })

        if (is_ok) {
            distance_configs[[length(distance_configs) + 1]] <- list(
                id = dist_name,
                label = tools::toTitleCase(gsub("\\.", " ", sub("^dist\\.", "", dist_name))),
                fn = dist_func
            )
        } else {
            cat("Skipping distance function", dist_name, "-", err_msg, "\n")
        }
    }

    if (length(distance_configs) == 0) {
        stop("No compatible distance functions were found in stylo.")
    }

    return(distance_configs)
}

# ================================================
# MAIN EXECUTION
# ================================================

cat("\n")
cat("========================================\n")
cat("GI AUTHORSHIP VERIFICATION (CUSTOM)\n")
cat("========================================\n")
cat("Corpus directory:", CORPUS_DIR, "\n")
cat("Output directory:", OUTPUT_DIR, "\n")
cat("Target:", TARGET_NAME, "\n")
cat("Candidates:", paste(CANDIDATE_NAMES, collapse = ", "), "\n")
if (length(cli_candidate_regexes) > 0) {
    cat("Candidate regex:", paste(cli_candidate_regexes, collapse = " | "), "\n")
}
if (length(cli_imposter_exclude_regexes) > 0) {
    cat("Imposter exclusion regex:", paste(cli_imposter_exclude_regexes, collapse = " | "), "\n")
}
if (length(cli_imposter_exclude_names) > 0) {
    cat("Imposter exclusion names:", paste(cli_imposter_exclude_names, collapse = ", "), "\n")
}
cat("Iterations per test:", ITERATIONS, "\n")
cat("FEATURE_COUNT_TRIGRAMS:", FEATURE_COUNT_TRIGRAMS, "\n")
cat("FEATURE_COUNT_UNIGRAMS:", FEATURE_COUNT_UNIGRAMS, "\n")
cat("FEATURE_SAMPLE_RATE:", FEATURE_SAMPLE_RATE, sprintf("(%.0f%%)\n", FEATURE_SAMPLE_RATE * 100))
cat("IMPOSTER_SAMPLE_RATE:", IMPOSTER_SAMPLE_RATE, sprintf("(%.0f%%)\n", IMPOSTER_SAMPLE_RATE * 100))
cat("DIAGNOSTIC_MODE:", DIAGNOSTIC_MODE, "\n")
if (DIAGNOSTIC_MODE) {
    cat("DIAGNOSTIC_TOP_N:", DIAGNOSTIC_TOP_N, "\n")
}
if (nzchar(trimws(LOG_NOTE))) {
    cat("LOG_NOTE:", trimws(LOG_NOTE), "\n")
}
if (!is.null(FEATURE_SET_FILE)) {
    cat("FEATURE_SET_FILE:", FEATURE_SET_FILE, "\n")
    cat("FEATURE_SET_SIZE:", length(FEATURE_SET_TOKENS), "\n")
    cat("TRIGRAM_TESTS_ENABLED: FALSE\n")
}
cat("\n")

freq_table_trigrams <- NULL
freq_table_unigrams <- NULL
feature_set_missing <- character(0)
feature_set_used <- character(0)

if (RUN_TRIGRAM_TESTS) {
    freq_table_trigrams <- load_ngram_freq_table("c", 3, "character trigram", TARGET_NAME, FEATURE_COUNT_TRIGRAMS)
}

if (!is.null(FEATURE_SET_FILE)) {
    unigram_feature_set <- load_unigram_freq_table_from_feature_set(TARGET_NAME, FEATURE_SET_TOKENS)
    freq_table_unigrams <- unigram_feature_set$freq_table
    feature_set_used <- unigram_feature_set$features_in_corpus
    feature_set_missing <- unigram_feature_set$missing_features
} else {
    freq_table_unigrams <- load_ngram_freq_table("w", 1, "word unigram", TARGET_NAME, FEATURE_COUNT_UNIGRAMS)
}

all_texts <- if (RUN_TRIGRAM_TESTS) rownames(freq_table_trigrams) else rownames(freq_table_unigrams)

if (!(TARGET_NAME %in% all_texts)) {
    stop("Target '", TARGET_NAME, "' not found in corpus.")
}

has_cli_candidate_names <- length(cli_candidate_names) > 0
has_cli_candidate_regexes <- length(cli_candidate_regexes) > 0
custom_candidate_selection <- has_cli_candidate_names || has_cli_candidate_regexes

candidate_names_exact <- if (custom_candidate_selection) {
    unique(normalize_name(trimws(cli_candidate_names)))
} else {
    CANDIDATE_NAMES
}
candidate_names_exact <- candidate_names_exact[nzchar(candidate_names_exact)]

missing_candidates <- candidate_names_exact[!(candidate_names_exact %in% all_texts)]
if (length(missing_candidates) > 0) {
    stop("Candidate(s) not found in corpus (exact-name selection): ", paste(missing_candidates, collapse = ", "))
}

candidate_names_regex <- match_texts_by_regex(all_texts, cli_candidate_regexes, "--candidate-regex")
candidate_rows <- unique(c(candidate_names_exact, candidate_names_regex))
candidate_rows <- candidate_rows[candidate_rows != TARGET_NAME]

if (length(candidate_rows) == 0) {
    stop("No candidates selected. Use exact names (--candidate/--candidates) and/or --candidate-regex.")
}

imposter_rows_base <- all_texts[!(all_texts %in% c(TARGET_NAME, candidate_rows))]
missing_excluded_exact <- setdiff(cli_imposter_exclude_names, imposter_rows_base)
if (length(missing_excluded_exact) > 0) {
    stop("Imposter exclusion names not found among imposters: ", paste(missing_excluded_exact, collapse = ", "))
}
excluded_imposters_exact <- intersect(imposter_rows_base, cli_imposter_exclude_names)
excluded_imposters_regex <- match_texts_by_regex(imposter_rows_base, cli_imposter_exclude_regexes, "--exclude-imposters-regex")
excluded_imposters <- unique(c(excluded_imposters_exact, excluded_imposters_regex))
imposter_rows <- setdiff(imposter_rows_base, excluded_imposters)

cat("\n========================================\n")
cat("CORPUS BREAKDOWN:\n")
cat("========================================\n")
cat("Target:", TARGET_NAME, "\n")
cat("Candidate(s):", paste(candidate_rows, collapse = ", "), "\n")
cat("Candidate exact-name selection count:", length(candidate_names_exact), "\n")
cat("Candidate regex-matched count:", length(candidate_names_regex), "\n")
cat("Imposter texts:", length(imposter_rows), "\n")
cat("Excluded imposters:", length(excluded_imposters), "\n")
cat("Total texts:", length(all_texts), "\n\n")

cat("========================================\n")
cat("FULL COMPARISON SETS (LOG RECORD)\n")
cat("========================================\n")
if (length(cli_candidate_regexes) > 0) {
    cat("Candidate regex patterns:\n")
    for (p in cli_candidate_regexes) {
        cat("  -", p, "\n")
    }
}
if (length(cli_imposter_exclude_regexes) > 0) {
    cat("Imposter exclusion regex patterns:\n")
    for (p in cli_imposter_exclude_regexes) {
        cat("  -", p, "\n")
    }
}
if (length(cli_imposter_exclude_names) > 0) {
    cat("Imposter exclusion names:\n")
    for (nm in cli_imposter_exclude_names) {
        cat("  -", nm, "\n")
    }
}
if (!is.null(FEATURE_SET_FILE)) {
    cat("Feature-set file:", FEATURE_SET_FILE, "\n")
    cat("Feature-set total tokens:", length(FEATURE_SET_TOKENS), "\n")
    cat("Feature-set tokens found in corpus:", length(feature_set_used), "\n")
    cat("Feature-set tokens missing from corpus:", length(feature_set_missing), "\n")
}
cat("Target (1):\n")
cat("  -", TARGET_NAME, "\n")
cat("Candidates (", length(candidate_rows), "):\n", sep = "")
for (nm in candidate_rows) {
    cat("  -", nm, "\n")
}
cat("Regex-matched candidates (", length(candidate_names_regex), "):\n", sep = "")
if (length(candidate_names_regex) > 0) {
    for (nm in candidate_names_regex) {
        cat("  -", nm, "\n")
    }
} else {
    cat("  (none)\n")
}
cat("Excluded imposters (", length(excluded_imposters), "):\n", sep = "")
if (length(excluded_imposters) > 0) {
    for (nm in excluded_imposters) {
        cat("  -", nm, "\n")
    }
} else {
    cat("  (none)\n")
}
cat("Imposters (", length(imposter_rows), "):\n", sep = "")
for (nm in imposter_rows) {
    cat("  -", nm, "\n")
}
cat("\n")

distance_probe_table <- if (RUN_TRIGRAM_TESTS) freq_table_trigrams else freq_table_unigrams
distance_configs <- get_distance_functions(distance_probe_table)
test_configs <- list()
for (dist_cfg in distance_configs) {
    if (RUN_TRIGRAM_TESTS) {
        test_configs[[length(test_configs) + 1]] <- list(
            name = paste("Trigrams +", dist_cfg$label),
            ngram = "trigrams",
            dist_id = dist_cfg$id,
            dist_func = dist_cfg$fn
        )
    }
    test_configs[[length(test_configs) + 1]] <- list(
        name = paste("Unigrams +", dist_cfg$label),
        ngram = "unigrams",
        dist_id = dist_cfg$id,
        dist_func = dist_cfg$fn
    )
}

cat("Distance functions used (", length(distance_configs), "): ",
    paste(sapply(distance_configs, function(x) x$id), collapse = ", "),
    "\n", sep = "")
cat("Total test setups:", length(test_configs), "\n\n")

all_results <- list()
for (config in test_configs) {
    freq_table <- if (config$ngram == "trigrams") freq_table_trigrams else freq_table_unigrams

    result <- run_gi_test(
        freq_table = freq_table,
        target_name = TARGET_NAME,
        candidate_rows = candidate_rows,
        imposter_rows = imposter_rows,
        distance_func = config$dist_func,
        setup_name = config$name,
        diagnostic_mode = DIAGNOSTIC_MODE,
        diagnostic_top_n = DIAGNOSTIC_TOP_N
    )

    if (!is.null(result)) {
        all_results[[length(all_results) + 1]] <- result
    }
}

cat("\n\n")
cat("========================================\n")
cat("FINAL SUMMARY\n")
cat("========================================\n\n")

summary_df <- data.frame(
    Setup = sapply(all_results, function(x) x$setup),
    Score = sapply(all_results, function(x) sprintf("%.3f", x$score)),
    Successful = sapply(all_results, function(x) x$successful),
    Skipped = sapply(all_results, function(x) x$skipped),
    stringsAsFactors = FALSE
)
print(summary_df, row.names = FALSE)

if (DIAGNOSTIC_MODE) {
    cat("\nDIAGNOSTIC MARGINS (FULL SET DISTANCES):\n")
    diagnostic_df <- data.frame(
        Setup = sapply(all_results, function(x) x$setup),
        ClosestCandidate = sapply(all_results, function(x) {
            if (is.null(x$diagnostic)) return(NA_real_)
            x$diagnostic$min_candidate
        }),
        ClosestImposter = sapply(all_results, function(x) {
            if (is.null(x$diagnostic)) return(NA_real_)
            x$diagnostic$min_imposter
        }),
        MarginImposterMinusCandidate = sapply(all_results, function(x) {
            if (is.null(x$diagnostic)) return(NA_real_)
            x$diagnostic$margin
        }),
        stringsAsFactors = FALSE
    )
    print(diagnostic_df, row.names = FALSE)
}

authenticated_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score >= 0.66))
not_auth_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score <= 0.34))
uncertain_count <- sum(sapply(all_results, function(x) !is.na(x$score) && x$score > 0.34 && x$score < 0.66))
total_tests <- length(all_results)
strong_threshold <- max(1, ceiling(0.75 * total_tests))
tending_threshold <- max(1, ceiling(0.60 * total_tests))

cat("\n")
cat("Authenticated (same author, >=0.66):", authenticated_count, "/", total_tests, "tests\n")
cat("Not authenticated (different author, <=0.34):", not_auth_count, "/", total_tests, "tests\n")
cat("Uncertain (0.34-0.66):", uncertain_count, "/", total_tests, "tests\n")

avg_score <- mean(sapply(all_results, function(x) x$score), na.rm = TRUE)
cat("Average score:", sprintf("%.3f", avg_score), "\n\n")

if (authenticated_count >= strong_threshold && authenticated_count > not_auth_count) {
    cat("VERDICT: Strong evidence for SAME authorship (",
        authenticated_count, "/", total_tests, " tests >= 0.66; strong threshold = ",
        strong_threshold, ")\n", sep = "")
} else if (authenticated_count >= tending_threshold && authenticated_count > not_auth_count) {
    cat("VERDICT: Tending toward SAME authorship (",
        authenticated_count, "/", total_tests, " tests >= 0.66; tending threshold = ",
        tending_threshold, ")\n", sep = "")
} else if (not_auth_count >= strong_threshold && not_auth_count > authenticated_count) {
    cat("VERDICT: Strong evidence for DIFFERENT authorship (",
        not_auth_count, "/", total_tests, " tests <= 0.34; strong threshold = ",
        strong_threshold, ")\n", sep = "")
} else if (not_auth_count >= tending_threshold && not_auth_count > authenticated_count) {
    cat("VERDICT: Tending toward DIFFERENT authorship (",
        not_auth_count, "/", total_tests, " tests <= 0.34; tending threshold = ",
        tending_threshold, ")\n", sep = "")
} else {
    cat("VERDICT: Inconclusive (same-author votes: ",
        authenticated_count, "/", total_tests,
        ", different-author votes: ", not_auth_count, "/", total_tests,
        ", uncertain: ", uncertain_count, "/", total_tests,
        "; thresholds: tending=", tending_threshold,
        ", strong=", strong_threshold, ")\n", sep = "")
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
output_file <- file.path(OUTPUT_DIR, paste0("gi_results_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".csv"))
write.csv(results_csv, output_file, row.names = FALSE)
cat("\nResults saved to:", output_file, "\n")
cat("Log saved to:", log_file, "\n")
