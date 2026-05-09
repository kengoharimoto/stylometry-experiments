#!/usr/bin/env Rscript
# Delta Nearest-Neighbor Authorship Attribution
#
# For a given target text, ranks all other texts in the corpus by stylistic
# distance across multiple feature types and distance measures.  Reports the
# rank of each candidate and the top-N closest texts per configuration, with
# an aggregated summary across all configurations.
#
# Unlike GI (probabilistic, imposter-pool-dependent), this is deterministic
# nearest-neighbor attribution: the question is simply "who in the corpus is
# closest to the target?"  It scales cleanly to large corpora.
#
# Example:
#   Rscript scripts/delta_nn_test.R \
#     --target=sankara_gitabhasya \
#     --candidate-regex='^sankara_' \
#     --feature-count=2000 \
#     --top-n=10
#
# Candidate flags:
#   --candidates=name1,name2,name3
#   --candidate=name1 --candidate=name2
#   --candidate-regex='^sankara_'
#
# Feature flags:
#   --feature-count=N             sets both trigrams and unigrams
#   --feature-count-trigrams=N
#   --feature-count-unigrams=N
#   --feature-set=/path/to/features.txt   uses a fixed word unigram list
#                                          (disables trigram tests)
#
# Other flags:
#   --corpus-dir=corpus/gi        default: corpus/gi
#   --top-n=N                     texts shown per config (default 10)
#   --exclude=name1,name2         exclude texts from ranking
#   --exclude-regex='pattern'     exclude by regex
#   --note='short note'
#   --log-note='short note'

library(stylo)

set.seed(123)

# ================================================
# CONFIGURATION
# ================================================

CORPUS_DIR              <- "corpus/gi"
OUTPUT_DIR              <- "results"
TARGET_NAME             <- ""
CANDIDATE_NAMES         <- character(0)
FEATURE_COUNT_TRIGRAMS  <- 2000
FEATURE_COUNT_UNIGRAMS  <- 200
FEATURE_SET_FILE        <- NULL
TOP_N                   <- 10
LOG_NOTE                <- ""

normalize_name <- function(x) sub("\\.[^.]+$", "", x)

# ================================================
# CLI PARSING
# ================================================

args <- commandArgs(trailingOnly = TRUE)
cli_candidate_names   <- character(0)
cli_candidate_regexes <- character(0)
cli_exclude_names     <- character(0)
cli_exclude_regexes   <- character(0)

for (a in args) {
    if (grepl("^--target=",                  a)) TARGET_NAME  <- sub("^--target=",  "", a)
    if (grepl("^--candidate=$",              a)) {}
    if (grepl("^--candidate=.",              a)) {
        val <- sub("^--candidate=", "", a)
        if (nzchar(val)) cli_candidate_names <- c(cli_candidate_names, val)
    }
    if (grepl("^--candidates=",              a)) {
        vals <- trimws(unlist(strsplit(sub("^--candidates=", "", a), ",", fixed = TRUE)))
        cli_candidate_names <- c(cli_candidate_names, vals[nzchar(vals)])
    }
    if (grepl("^--candidate-regex=",         a)) {
        val <- sub("^--candidate-regex=", "", a)
        if (nzchar(val)) cli_candidate_regexes <- c(cli_candidate_regexes, val)
    }
    if (grepl("^--exclude=",                 a)) {
        vals <- trimws(unlist(strsplit(sub("^--exclude=", "", a), ",", fixed = TRUE)))
        cli_exclude_names <- c(cli_exclude_names, vals[nzchar(vals)])
    }
    if (grepl("^--exclude-regex=",           a)) {
        val <- sub("^--exclude-regex=", "", a)
        if (nzchar(val)) cli_exclude_regexes <- c(cli_exclude_regexes, val)
    }
    if (grepl("^--feature-count=",           a)) {
        val <- as.integer(sub("^--feature-count=", "", a))
        FEATURE_COUNT_TRIGRAMS <- val
        FEATURE_COUNT_UNIGRAMS <- val
    }
    if (grepl("^--feature-count-trigrams=",  a)) FEATURE_COUNT_TRIGRAMS <- as.integer(sub("^--feature-count-trigrams=",  "", a))
    if (grepl("^--feature-count-unigrams=",  a)) FEATURE_COUNT_UNIGRAMS <- as.integer(sub("^--feature-count-unigrams=", "", a))
    if (grepl("^--feature-set=",             a)) FEATURE_SET_FILE <- sub("^--feature-set=", "", a)
    if (grepl("^--feature_set=",             a)) FEATURE_SET_FILE <- sub("^--feature_set=", "", a)
    if (grepl("^--top-n=",                   a)) TOP_N <- as.integer(sub("^--top-n=", "", a))
    if (grepl("^--corpus-dir=",              a)) CORPUS_DIR <- sub("^--corpus-dir=", "", a)
    if (grepl("^--note=",                    a)) LOG_NOTE <- sub("^--note=", "", a)
    if (grepl("^--log-note=",                a)) LOG_NOTE <- sub("^--log-note=", "", a)
}

if (length(cli_candidate_names) > 0) CANDIDATE_NAMES <- cli_candidate_names

TARGET_NAME       <- normalize_name(trimws(TARGET_NAME))
CANDIDATE_NAMES   <- unique(normalize_name(trimws(CANDIDATE_NAMES)))
CANDIDATE_NAMES   <- CANDIDATE_NAMES[nzchar(CANDIDATE_NAMES)]
cli_candidate_regexes <- unique(trimws(cli_candidate_regexes[nzchar(cli_candidate_regexes)]))
cli_exclude_names     <- unique(normalize_name(trimws(cli_exclude_names[nzchar(cli_exclude_names)])))
cli_exclude_regexes   <- unique(trimws(cli_exclude_regexes[nzchar(cli_exclude_regexes)]))

RUN_TRIGRAM_TESTS <- is.null(FEATURE_SET_FILE)

# ================================================
# VALIDATION
# ================================================

if (!nzchar(TARGET_NAME))                                            stop("--target is required")
if (!is.finite(FEATURE_COUNT_TRIGRAMS) || FEATURE_COUNT_TRIGRAMS <= 0) stop("--feature-count-trigrams must be a positive integer")
if (!is.finite(FEATURE_COUNT_UNIGRAMS) || FEATURE_COUNT_UNIGRAMS <= 0) stop("--feature-count-unigrams must be a positive integer")
if (!is.finite(TOP_N) || TOP_N < 1)                                  stop("--top-n must be a positive integer")
if (!is.null(FEATURE_SET_FILE) && !nzchar(trimws(FEATURE_SET_FILE))) stop("--feature-set cannot be empty")

# ================================================
# LOGGING
# ================================================

dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
log_file <- file.path(OUTPUT_DIR, paste0("delta_nn_", format(Sys.time(), "%Y%m%d_%H%M%S"), ".txt"))
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

load_corpus_cached <- function(corpus_dir, ngram_type, ngram_size) {
    cache_path <- file.path(corpus_dir, sprintf(".cache_%s%d.rds", ngram_type, ngram_size))
    corpus_files <- list.files(corpus_dir, pattern = "\\.txt$", full.names = TRUE)
    current_names <- sort(sub("\\.txt$", "", basename(corpus_files)))
    newest_input <- if (length(corpus_files) > 0) max(file.mtime(corpus_files)) else -Inf
    if (file.exists(cache_path) && file.mtime(cache_path) > newest_input) {
        cached <- readRDS(cache_path)
        if (identical(current_names, sort(names(cached)))) {
            cat("  (cache hit:", basename(cache_path), ")\n")
            return(cached)
        }
        cat("  (cache stale: corpus membership changed, rebuilding)\n")
    }
    parsed <- load.corpus.and.parse(corpus.dir = corpus_dir, ngram.type = ngram_type, ngram.size = ngram_size)
    saveRDS(parsed, cache_path)
    cat("  (cache written:", basename(cache_path), ")\n")
    parsed
}

load_freq_table <- function(ngram_type, ngram_size, label, exclude_from_features, feature_count) {
    cat("\nLoading", label, "corpus...\n")
    raw_full <- load_corpus_cached(CORPUS_DIR, ngram_type, ngram_size)
    non_query <- raw_full[!(names(raw_full) %in% exclude_from_features)]
    cat("Making", label, "frequency list (based on", length(non_query), "texts)...\n")
    top_features <- make.frequency.list(non_query, head = feature_count)
    cat("Creating", label, "frequency table...\n")
    make.table.of.frequencies(corpus = raw_full, features = top_features)
}

load_freq_table_from_feature_set <- function(exclude_from_features, feature_set_tokens) {
    cat("\nLoading word unigram corpus (feature-set mode)...\n")
    raw_full <- load_corpus_cached(CORPUS_DIR, "w", 1)
    available <- unique(unlist(raw_full[!(names(raw_full) %in% exclude_from_features)], use.names = FALSE))
    features_in_corpus <- intersect(feature_set_tokens, available)
    cat("Feature-set size:", length(feature_set_tokens), "| In corpus:", length(features_in_corpus),
        "| Missing:", length(feature_set_tokens) - length(features_in_corpus), "\n")
    if (length(features_in_corpus) == 0) stop("None of the --feature-set features were found in the corpus.")
    make.table.of.frequencies(corpus = raw_full, features = features_in_corpus)
}

read_feature_set <- function(path) {
    if (!file.exists(path)) stop("Feature-set file not found: ", path)
    lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
    feats <- unique(trimws(unlist(strsplit(paste(lines, collapse = " "), "\\s+"))))
    feats <- feats[nzchar(feats)]
    if (length(feats) == 0) stop("Feature-set file is empty: ", path)
    feats
}

match_texts_by_regex <- function(texts, patterns, label) {
    if (length(patterns) == 0) return(character(0))
    out <- character(0)
    for (p in patterns) {
        m <- tryCatch(texts[grepl(p, texts, perl = TRUE)],
                      error = function(e) stop("Invalid regex for ", label, ": '", p, "'"))
        out <- c(out, m)
    }
    unique(out)
}

get_distance_functions <- function(example_table) {
    distance_names <- sort(ls("package:stylo")[startsWith(ls("package:stylo"), "dist.")])
    configs <- list()
    probe <- example_table[seq_len(min(4, nrow(example_table))), seq_len(min(20, ncol(example_table))), drop = FALSE]
    for (dn in distance_names) {
        fn <- get(dn, envir = asNamespace("stylo"))
        ok <- TRUE
        tryCatch({
            dm <- as.matrix(fn(probe))
            if (nrow(dm) != nrow(probe)) ok <- FALSE
        }, error = function(e) { ok <<- FALSE })
        if (ok) configs[[length(configs) + 1]] <- list(
            id    = dn,
            label = tools::toTitleCase(gsub("\\.", " ", sub("^dist\\.", "", dn))),
            fn    = fn
        )
    }
    if (length(configs) == 0) stop("No compatible distance functions found in stylo.")
    configs
}

run_delta_nn <- function(freq_table, target_name, candidate_rows, config_name) {
    cat("\n================================================\n")
    cat("CONFIG:", config_name, "\n")
    cat("================================================\n")

    if (!(target_name %in% rownames(freq_table))) {
        warning("Target '", target_name, "' not found in freq table — skipping.")
        return(NULL)
    }

    # Compute distances from target to all other texts
    all_rows <- rownames(freq_table)
    comparison_rows <- all_rows[all_rows != target_name]

    dist_matrix <- tryCatch({
        rows_to_use <- c(target_name, comparison_rows)
        as.matrix(dist_func(freq_table[rows_to_use, , drop = FALSE]))
    }, error = function(e) {
        cat("ERROR computing distances:", conditionMessage(e), "\n")
        return(NULL)
    })
    if (is.null(dist_matrix)) return(NULL)

    dists <- dist_matrix[target_name, comparison_rows]
    ranked <- sort(dists)

    # Report top-N
    top_n_actual <- min(TOP_N, length(ranked))
    cat("\nTop", top_n_actual, "closest texts:\n")
    for (k in seq_len(top_n_actual)) {
        nm   <- names(ranked)[k]
        is_c <- nm %in% candidate_rows
        tag  <- if (is_c) " [CANDIDATE]" else ""
        cat(sprintf("  %3d. %-60s %.6f%s\n", k, nm, ranked[k], tag))
    }

    # Report candidate ranks
    if (length(candidate_rows) > 0) {
        cat("\nCandidate ranks:\n")
        for (cand in candidate_rows) {
            if (cand %in% names(dists)) {
                r <- which(names(ranked) == cand)
                cat(sprintf("  %-60s rank %d / %d  (dist %.6f)\n",
                            cand, r, length(ranked), dists[cand]))
            } else {
                cat(sprintf("  %-60s not found in freq table\n", cand))
            }
        }
    }

    # Build per-candidate results
    cand_results <- lapply(candidate_rows, function(cand) {
        if (!(cand %in% names(dists))) return(NULL)
        r <- which(names(ranked) == cand)
        list(name = cand, rank = r, dist = dists[cand], n_texts = length(ranked))
    })
    cand_results <- Filter(Negate(is.null), cand_results)

    list(
        config      = config_name,
        ranked      = ranked,
        candidates  = cand_results,
        n_texts     = length(ranked)
    )
}

# ================================================
# HEADER
# ================================================

cat("\n")
cat("========================================\n")
cat("DELTA NEAREST-NEIGHBOR ATTRIBUTION\n")
cat("========================================\n")
cat("Corpus directory:        ", CORPUS_DIR, "\n")
cat("Output directory:        ", OUTPUT_DIR, "\n")
cat("Target:                  ", TARGET_NAME, "\n")
if (length(CANDIDATE_NAMES) > 0 || length(cli_candidate_regexes) > 0) {
    if (length(CANDIDATE_NAMES) > 0)
        cat("Candidates (exact):      ", paste(CANDIDATE_NAMES, collapse = ", "), "\n")
    if (length(cli_candidate_regexes) > 0)
        cat("Candidate regex:         ", paste(cli_candidate_regexes, collapse = " | "), "\n")
}
cat("FEATURE_COUNT_TRIGRAMS:  ", FEATURE_COUNT_TRIGRAMS, "\n")
cat("FEATURE_COUNT_UNIGRAMS:  ", FEATURE_COUNT_UNIGRAMS, "\n")
cat("TOP_N:                   ", TOP_N, "\n")
if (!is.null(FEATURE_SET_FILE)) cat("FEATURE_SET_FILE:        ", FEATURE_SET_FILE, "\n")
if (nzchar(trimws(LOG_NOTE)))   cat("LOG_NOTE:                ", trimws(LOG_NOTE), "\n")
cat("\n")

# ================================================
# LOAD CORPUS
# ================================================

FEATURE_SET_TOKENS <- if (!is.null(FEATURE_SET_FILE)) read_feature_set(FEATURE_SET_FILE) else character(0)

freq_table_trigrams <- NULL
freq_table_unigrams <- NULL

if (RUN_TRIGRAM_TESTS) {
    freq_table_trigrams <- load_freq_table("c", 3, "character trigram", TARGET_NAME, FEATURE_COUNT_TRIGRAMS)
}
if (!is.null(FEATURE_SET_FILE)) {
    freq_table_unigrams <- load_freq_table_from_feature_set(TARGET_NAME, FEATURE_SET_TOKENS)
} else {
    freq_table_unigrams <- load_freq_table("w", 1, "word unigram", TARGET_NAME, FEATURE_COUNT_UNIGRAMS)
}

all_texts <- rownames(if (RUN_TRIGRAM_TESTS) freq_table_trigrams else freq_table_unigrams)

if (!(TARGET_NAME %in% all_texts)) stop("Target '", TARGET_NAME, "' not found in corpus.")

# ================================================
# RESOLVE CANDIDATES AND EXCLUSIONS
# ================================================

candidate_rows <- unique(c(CANDIDATE_NAMES, match_texts_by_regex(all_texts, cli_candidate_regexes, "--candidate-regex")))
candidate_rows <- candidate_rows[candidate_rows %in% all_texts & candidate_rows != TARGET_NAME]

excluded_exact <- intersect(all_texts, cli_exclude_names)
excluded_regex <- match_texts_by_regex(all_texts, cli_exclude_regexes, "--exclude-regex")
excluded       <- unique(c(excluded_exact, excluded_regex, TARGET_NAME))

missing_cands <- setdiff(CANDIDATE_NAMES, all_texts)
if (length(missing_cands) > 0) stop("Candidates not found in corpus: ", paste(missing_cands, collapse = ", "))

cat("========================================\n")
cat("CORPUS BREAKDOWN\n")
cat("========================================\n")
cat("Total texts in corpus:", length(all_texts), "\n")
cat("Target:               ", TARGET_NAME, "\n")
cat("Candidates (", length(candidate_rows), "):\n", sep = "")
for (nm in candidate_rows) cat("  -", nm, "\n")
if (length(excluded) > 1) {  # >1 because TARGET_NAME is always excluded
    others <- setdiff(excluded, TARGET_NAME)
    cat("Excluded from ranking (", length(others), "):\n", sep = "")
    for (nm in others) cat("  -", nm, "\n")
}
cat("Texts ranked against:", length(all_texts) - length(excluded), "\n\n")

# ================================================
# DISTANCE FUNCTIONS & TEST CONFIGS
# ================================================

distance_configs <- get_distance_functions(if (RUN_TRIGRAM_TESTS) freq_table_trigrams else freq_table_unigrams)
cat("Distance functions (", length(distance_configs), "): ",
    paste(sapply(distance_configs, `[[`, "id"), collapse = ", "), "\n\n", sep = "")

test_configs <- list()
for (dc in distance_configs) {
    if (RUN_TRIGRAM_TESTS)
        test_configs[[length(test_configs) + 1]] <- list(ngram = "trigrams", dist = dc, name = paste("Trigrams +", dc$label))
    test_configs[[length(test_configs) + 1]]     <- list(ngram = "unigrams", dist = dc, name = paste("Unigrams +", dc$label))
}

# ================================================
# RUN TESTS
# ================================================

all_results <- list()

for (cfg in test_configs) {
    freq_table <- if (cfg$ngram == "trigrams") freq_table_trigrams else freq_table_unigrams

    # Build comparison set: all texts except target and explicitly excluded ones
    comparison_rows <- rownames(freq_table)
    comparison_rows <- comparison_rows[!(comparison_rows %in% excluded)]

    dist_func <- cfg$dist$fn  # used inside run_delta_nn via lexical scoping

    cat("\n================================================\n")
    cat("CONFIG:", cfg$name, "\n")
    cat("================================================\n")

    if (!(TARGET_NAME %in% rownames(freq_table))) {
        warning("Target not found in freq table — skipping.")
        next
    }

    rows_to_use  <- c(TARGET_NAME, comparison_rows)
    dist_matrix  <- tryCatch(
        as.matrix(dist_func(freq_table[rows_to_use, , drop = FALSE])),
        error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL }
    )
    if (is.null(dist_matrix)) next
    if (any(is.na(dist_matrix)) || any(is.infinite(dist_matrix))) {
        cat("WARNING: NA/Inf distances — skipping this config.\n")
        next
    }

    dists  <- dist_matrix[TARGET_NAME, comparison_rows]
    ranked <- sort(dists)

    top_n_actual <- min(TOP_N, length(ranked))
    cat("\nTop", top_n_actual, "closest texts:\n")
    for (k in seq_len(top_n_actual)) {
        nm  <- names(ranked)[k]
        tag <- if (nm %in% candidate_rows) " [CANDIDATE]" else ""
        cat(sprintf("  %3d. %-60s %.6f%s\n", k, nm, ranked[k], tag))
    }

    cand_results <- list()
    if (length(candidate_rows) > 0) {
        cat("\nCandidate ranks:\n")
        for (cand in candidate_rows) {
            if (cand %in% names(dists)) {
                r <- which(names(ranked) == cand)
                cat(sprintf("  %-60s rank %3d / %d  (dist %.6f)\n", cand, r, length(ranked), dists[cand]))
                cand_results[[length(cand_results) + 1]] <- list(
                    name = cand, rank = r, dist = dists[cand], n_texts = length(ranked)
                )
            }
        }
    }

    all_results[[length(all_results) + 1]] <- list(
        config     = cfg$name,
        ngram      = cfg$ngram,
        dist_id    = cfg$dist$id,
        ranked     = ranked,
        candidates = cand_results,
        n_texts    = length(ranked)
    )
}

# ================================================
# SUMMARY
# ================================================

cat("\n\n")
cat("========================================\n")
cat("FINAL SUMMARY\n")
cat("========================================\n\n")

n_configs <- length(all_results)
cat("Configurations run:", n_configs, "\n\n")

if (length(candidate_rows) > 0 && n_configs > 0) {
    cat("CANDIDATE RANK SUMMARY (lower rank = closer to target):\n\n")

    for (cand in candidate_rows) {
        ranks <- sapply(all_results, function(r) {
            m <- Filter(function(x) x$name == cand, r$candidates)
            if (length(m) == 0) return(NA_integer_)
            m[[1]]$rank
        })
        ranks <- ranks[!is.na(ranks)]
        if (length(ranks) == 0) {
            cat(cand, ": not found in any config\n\n")
            next
        }
        n_total <- all_results[[1]]$n_texts
        cat(cand, "\n")
        cat(sprintf("  Configs with data: %d / %d\n", length(ranks), n_configs))
        cat(sprintf("  Mean rank:         %.1f / %d\n", mean(ranks), n_total))
        cat(sprintf("  Median rank:       %.1f / %d\n", median(ranks), n_total))
        cat(sprintf("  Min rank:          %d    Max rank: %d\n", min(ranks), max(ranks)))
        cat(sprintf("  Rank = 1:          %d configs (%.0f%%)\n", sum(ranks == 1), 100 * mean(ranks == 1)))
        cat(sprintf("  Rank <= 3:         %d configs (%.0f%%)\n", sum(ranks <= 3), 100 * mean(ranks <= 3)))
        cat(sprintf("  Rank <= 5:         %d configs (%.0f%%)\n", sum(ranks <= 5), 100 * mean(ranks <= 5)))
        cat(sprintf("  Rank <= 10:        %d configs (%.0f%%)\n", sum(ranks <= 10), 100 * mean(ranks <= 10)))
        cat("\n")
    }

    # Per-config table
    cat("PER-CONFIG CANDIDATE RANKS:\n\n")
    header <- sprintf("  %-45s", "Config")
    for (cand in candidate_rows) header <- paste0(header, sprintf("  %-12s", substr(cand, 1, 12)))
    cat(header, "\n")
    cat(strrep("-", nchar(header) + 2), "\n")
    for (r in all_results) {
        row <- sprintf("  %-45s", substr(r$config, 1, 45))
        for (cand in candidate_rows) {
            m <- Filter(function(x) x$name == cand, r$candidates)
            val <- if (length(m) > 0) sprintf("%d", m[[1]]$rank) else "—"
            row <- paste0(row, sprintf("  %-12s", val))
        }
        cat(row, "\n")
    }
    cat("\n")
}

# Who was #1 most often (across all configs)?
cat("MOST FREQUENTLY CLOSEST TEXT (rank 1 across all configs):\n")
rank1_counts <- table(sapply(all_results, function(r) {
    if (length(r$ranked) == 0) return(NA_character_)
    names(r$ranked)[1]
}))
rank1_counts <- sort(rank1_counts, decreasing = TRUE)
for (i in seq_len(min(10, length(rank1_counts)))) {
    nm  <- names(rank1_counts)[i]
    cnt <- rank1_counts[i]
    tag <- if (nm %in% candidate_rows) " [CANDIDATE]" else ""
    cat(sprintf("  %2d configs: %s%s\n", cnt, nm, tag))
}

# ================================================
# SAVE RESULTS
# ================================================

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

# Summary CSV: one row per config × candidate
summary_rows <- lapply(all_results, function(r) {
    lapply(r$candidates, function(cr) {
        data.frame(Config = r$config, Candidate = cr$name,
                   Rank = cr$rank, N_texts = cr$n_texts,
                   Distance = cr$dist, stringsAsFactors = FALSE)
    })
})
summary_rows <- do.call(rbind, do.call(c, summary_rows))
if (!is.null(summary_rows) && nrow(summary_rows) > 0) {
    csv_file <- file.path(OUTPUT_DIR, paste0("delta_nn_", timestamp, ".csv"))
    write.csv(summary_rows, csv_file, row.names = FALSE)
    cat("\nResults saved to:", csv_file, "\n")
}

# Top-N rankings CSV: one row per config × rank position
topn_rows <- lapply(all_results, function(r) {
    n <- min(TOP_N, length(r$ranked))
    if (n == 0) return(NULL)
    data.frame(
        Config      = r$config,
        Rank        = seq_len(n),
        Text        = names(r$ranked)[seq_len(n)],
        Distance    = r$ranked[seq_len(n)],
        Is_Candidate = names(r$ranked)[seq_len(n)] %in% candidate_rows,
        stringsAsFactors = FALSE
    )
})
topn_rows <- do.call(rbind, Filter(Negate(is.null), topn_rows))
if (!is.null(topn_rows) && nrow(topn_rows) > 0) {
    topn_file <- file.path(OUTPUT_DIR, paste0("delta_nn_topn_", timestamp, ".csv"))
    write.csv(topn_rows, topn_file, row.names = FALSE)
    cat("Top-N rankings saved to:", topn_file, "\n")
}

cat("Log saved to:", log_file, "\n")
cat("\n========================================\n")
cat("All tests completed!\n")
cat("========================================\n")
