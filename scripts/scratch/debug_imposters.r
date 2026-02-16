#!/usr/bin/env Rscript
# Minimal test of imposters() function

library(stylo)
set.seed(123)

cat("Loading corpus...\n")
raw_data <- load.corpus.and.parse(corpus.dir = "corpus", ngram.type = "c", ngram.size = 3)
top_features <- make.frequency.list(raw_data, head = 20000)
freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)

TARGET_NAME <- "005_Sankara_Adhyatmapatala_segmented_complete"
sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
sankara_rows <- sankara_rows[sankara_rows != TARGET_NAME]

cat("\nPreparing data...\n")
reference_set <- freq_table[rownames(freq_table) != TARGET_NAME, , drop = FALSE]
test_vector <- as.numeric(freq_table[TARGET_NAME, ])
names(test_vector) <- colnames(freq_table)

cat("Reference set:", nrow(reference_set), "x", ncol(reference_set), "\n")
cat("Test vector length:", length(test_vector), "\n")
cat("Candidates:", length(sankara_rows), "\n")
cat("Candidate names:", paste(sankara_rows, collapse=", "), "\n\n")

# Try the simplest possible call
cat("Attempting imposters() call...\n")

# Method 1: Try with just the basic parameters
tryCatch({
    result <- imposters(
        reference.set = reference_set,
        test = test_vector,
        candidate.set = sankara_rows
    )
    cat("SUCCESS! Score:", result, "\n")
}, error = function(e) {
    cat("Method 1 FAILED:", e$message, "\n\n")
    
    # Method 2: Try passing test as single-row matrix
    cat("Trying with test as matrix...\n")
    tryCatch({
        test_matrix <- matrix(test_vector, nrow=1)
        colnames(test_matrix) <- names(test_vector)
        rownames(test_matrix) <- TARGET_NAME
        
        result <- imposters(
            reference.set = reference_set,
            test = test_matrix,
            candidate.set = sankara_rows
        )
        cat("SUCCESS! Score:", result, "\n")
    }, error = function(e2) {
        cat("Method 2 FAILED:", e2$message, "\n\n")
        
        # Method 3: Check if candidate.set names match reference.set rownames
        cat("Checking candidate names...\n")
        cat("Are all candidates in reference set?\n")
        print(all(sankara_rows %in% rownames(reference_set)))
        cat("\nCandidates present:\n")
        print(sankara_rows %in% rownames(reference_set))
        
        # Method 4: Try using oppose() function instead (older stylo versions)
        cat("\nTrying oppose() function (alternative to imposters)...\n")
        tryCatch({
            result <- oppose(
                gui = FALSE,
                path = "corpus",
                corpus.format = "plain",
                mfw.min = 2000,
                mfw.max = 2000,
                corpus.lang = "Other"
            )
            cat("oppose() worked!\n")
            print(result)
        }, error = function(e3) {
            cat("oppose() also failed:", e3$message, "\n")
        })
    })
})