#!/usr/bin/env Rscript
# GI Authorship Verification using stylo's imposters() function
# This uses the official implementation instead of a manual loop

library(stylo)

# Set seed for reproducibility
set.seed(123)

# Configuration
CORPUS_DIR <- "corpus"
TARGET_NAME <- "005_Sankara_Adhyatmapatala_segmented_complete"

cat("\n")
cat("========================================\n")
cat("GI TEST USING STYLO imposters() FUNCTION\n")
cat("========================================\n\n")

# Function to run imposters() with a given setup
test_with_imposters <- function(ngram_type, ngram_size, distance_metric, setup_name) {
    cat("\n================================================\n")
    cat("TESTING:", setup_name, "\n")
    cat("================================================\n")
    
    # Load and process corpus
    cat("Loading corpus...\n")
    raw_data <- load.corpus.and.parse(corpus.dir = CORPUS_DIR, 
                                      ngram.type = ngram_type, 
                                      ngram.size = ngram_size)
    
    cat("Making frequency list...\n")
    top_features <- make.frequency.list(raw_data, head = 20000)
    
    cat("Creating frequency table...\n")
    freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)
    
    # Identify Sankara texts (candidates)
    sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
    
    # Remove target from Sankara candidates if it's there
    sankara_rows <- sankara_rows[sankara_rows != TARGET_NAME]
    
    cat("\nCorpus info:\n")
    cat("  Total texts:", nrow(freq_table), "\n")
    cat("  Target text:", TARGET_NAME, "\n")
    cat("  Sankara candidates:", length(sankara_rows), "\n")
    cat("  Total features:", ncol(freq_table), "\n\n")
    
    # Safety check
    if(length(sankara_rows) == 0) stop("No Sankara candidate files found.")
    if(!(TARGET_NAME %in% rownames(freq_table))) stop("Target text not found in corpus!")
    
    cat("Running imposters() function...\n")
    cat("  This may take a minute...\n\n")
    
    # The imposters() function expects:
    # - reference.set: all texts INCLUDING candidates and imposters, but NOT the test
    # - test: VECTOR of frequencies for the test text (not a matrix)
    # - candidate.set: vector of candidate author text names
    
    # Split the frequency table
    reference_set <- freq_table[rownames(freq_table) != TARGET_NAME, , drop = FALSE]
    test_vector <- as.numeric(freq_table[TARGET_NAME, ])
    names(test_vector) <- colnames(freq_table)
    
    cat("  Reference set dimensions:", nrow(reference_set), "x", ncol(reference_set), "\n")
    cat("  Test vector length:", length(test_vector), "\n")
    cat("  Candidate set size:", length(sankara_rows), "\n\n")
    
    tryCatch({
        result <- imposters(
            reference.set = reference_set,
            test = test_vector,
            candidate.set = sankara_rows,
            features = 0.1,  # 10% of features
            iterations = 100,
            distance = distance_metric
        )
        
        cat("--- RESULTS ---\n")
        cat("Setup:", setup_name, "\n")
        cat("Score:", result, "\n")
        cat("\nInterpretation:\n")
        cat("  >= 0.66 = Authentic (likely by Sankara)\n")
        cat("  <= 0.34 = Not authentic\n")
        cat("  0.34-0.66 = Uncertain (grey zone)\n\n")
        
        return(list(
            setup = setup_name,
            score = result,
            error = FALSE
        ))
        
    }, error = function(e) {
        cat("ERROR:", e$message, "\n\n")
        return(list(
            setup = setup_name,
            score = NA,
            error = TRUE,
            error_msg = e$message
        ))
    })
}

# ================================================
# RUN ALL TESTS
# ================================================

all_results <- list()

cat("Starting tests with imposters() function...\n")

# Test 1: Trigrams + MinMax
all_results[[1]] <- test_with_imposters("c", 3, "minmax", "Trigrams + MinMax")

# Test 2: Trigrams + Cosine
all_results[[2]] <- test_with_imposters("c", 3, "cosine", "Trigrams + Cosine")

# Test 3: Trigrams + Wurzburg
all_results[[3]] <- test_with_imposters("c", 3, "wurzburg", "Trigrams + Wurzburg")

# Test 4: Unigrams + MinMax
all_results[[4]] <- test_with_imposters("w", 1, "minmax", "Unigrams + MinMax")

# Test 5: Unigrams + Cosine
all_results[[5]] <- test_with_imposters("w", 1, "cosine", "Unigrams + Cosine")

# Test 6: Unigrams + Wurzburg
all_results[[6]] <- test_with_imposters("w", 1, "wurzburg", "Unigrams + Wurzburg")

# ================================================
# SUMMARY
# ================================================

cat("\n")
cat("========================================\n")
cat("SUMMARY OF RESULTS\n")
cat("========================================\n\n")

# Create summary
for(i in 1:length(all_results)) {
    r <- all_results[[i]]
    if(r$error) {
        cat(sprintf("%-35s: ERROR - %s\n", r$setup, r$error_msg))
    } else {
        cat(sprintf("%-35s: %.3f\n", r$setup, r$score))
    }
}

cat("\n")
cat("Paper's reported scores:\n")
cat("  Trigrams + Cosine Delta: 0.88\n")
cat("  Unigrams + Cosine Delta: 0.84\n")
cat("\n")

cat("Your manual loop scores:\n")
cat("  Trigrams + Cosine:   0.775\n")
cat("  Trigrams + MinMax:   0.660\n")
cat("  Unigrams + Cosine:   0.700\n")
cat("  Unigrams + MinMax:   0.840\n")
cat("  Trigrams + Wurzburg: 0.000\n")
cat("  Unigrams + Wurzburg: 0.340\n")
cat("\n")

# Count successful authentications
successful_tests <- sum(sapply(all_results, function(x) !x$error && !is.na(x$score) && x$score >= 0.66))
cat("Tests authenticating the text:", successful_tests, "/ 6\n")

cat("\n========================================\n")
cat("Test completed!\n")
cat("========================================\n")