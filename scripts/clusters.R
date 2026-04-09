library(stylo)
CORPUS_DIR <- "corpus/main"

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S") # used for file names

# ================================================
# SHARED STYLO PARAMETERS - DEFINED ONCE
# ================================================
# These parameters are used for ALL stylo() calls
# to ensure consistency across all analysis types

ANALYZED_FEATURES <- "w"      # "w" for words, "c" for characters
NGRAM_SIZE <- 1               # 1 for unigrams, 2 for bigrams, 3 for trigrams
PRESERVE_CASE <- FALSE
ENCODING <- "UTF-8"

# # MFW settings (use bigger values when doing character n-grams)
# MFW_MIN <- 2000
# MFW_MAX <- 5000
# MFW_INCR <- 1000

# MFW settings (use smaller values when doing word n-grams)
MFW_MIN <- 50
MFW_MAX <- 80
MFW_INCR <- 10

# Culling settings (no need to cull when doing character n-grams; keep the ratio big when doing words)
CULLING_MIN <- 0
CULLING_MAX <- 0
CULLING_INCR <- 0

# Other settings
MFW_LIST_CUTOFF <- 20000
CONSENSUS_STRENGTH <- 0.5
SAMPLING <- "no.sampling"
SAMPLE_SIZE <- 10000
NUMBER_OF_SAMPLES <- 1
SAMPLING_WITH_REPLACEMENT <- FALSE

# Display and output settings
DISPLAY_ON_SCREEN <- FALSE
WRITE_PDF_FILE <- TRUE
WRITE_JPG_FILE <- FALSE
WRITE_SVG_FILE <- FALSE
WRITE_PNG_FILE <- FALSE
PLOT_CUSTOM_HEIGHT <- 20
PLOT_CUSTOM_WIDTH <- 20
PLOT_FONT_SIZE <- 10
PLOT_LINE_THICKNESS <- 1
PLOT_OPTIONS_RESET <- FALSE
TEXT_ID_ON_GRAPHS <- "both"
COLORS_ON_GRAPHS <- "colors"
TITLES_ON_GRAPHS <- TRUE
LABEL_OFFSET <- 0
GROUPS_COL <- NULL  # named character vector, e.g. c(group1 = "red", group2 = "#1a9850")

# Save options
SAVE_DISTANCE_TABLES <- TRUE
SAVE_ANALYZED_FEATURES <- TRUE
SAVE_ANALYZED_FREQS <- TRUE

# ================================================
# PARSE COMMAND-LINE ARGS
# ================================================

args <- commandArgs(trailingOnly = TRUE)
for (a in args) {
    if (grepl("^--corpus-dir=", a)) {
        CORPUS_DIR <- sub("^--corpus-dir=", "", a)
    }
    if (grepl("^--features=", a)) {
        ANALYZED_FEATURES <- sub("^--features=", "", a)
    }
    if (grepl("^--ngram-size=", a)) {
        NGRAM_SIZE <- as.integer(sub("^--ngram-size=", "", a))
    }
    if (grepl("^--mfw-min=", a)) {
        MFW_MIN <- as.integer(sub("^--mfw-min=", "", a))
    }
    if (grepl("^--mfw-max=", a)) {
        MFW_MAX <- as.integer(sub("^--mfw-max=", "", a))
    }
    if (grepl("^--mfw-incr=", a)) {
        MFW_INCR <- as.integer(sub("^--mfw-incr=", "", a))
    }
    if (grepl("^--culling-min=", a)) {
        CULLING_MIN <- as.integer(sub("^--culling-min=", "", a))
    }
    if (grepl("^--culling-max=", a)) {
        CULLING_MAX <- as.integer(sub("^--culling-max=", "", a))
    }
    if (grepl("^--culling-incr=", a)) {
        CULLING_INCR <- as.integer(sub("^--culling-incr=", "", a))
    }
    if (grepl("^--consensus-strength=", a)) {
        CONSENSUS_STRENGTH <- as.numeric(sub("^--consensus-strength=", "", a))
    }
    if (a == "--preserve-case") {
        PRESERVE_CASE <- TRUE
    }
    if (grepl("^--plot-height=", a)) {
        PLOT_CUSTOM_HEIGHT <- as.numeric(sub("^--plot-height=", "", a))
    }
    if (grepl("^--plot-width=", a)) {
        PLOT_CUSTOM_WIDTH <- as.numeric(sub("^--plot-width=", "", a))
    }
    if (grepl("^--plot-font-size=", a)) {
        PLOT_FONT_SIZE <- as.numeric(sub("^--plot-font-size=", "", a))
    }
    if (grepl("^--highlight=", a)) {
        val <- sub("^--highlight=", "", a)
        pairs <- strsplit(val, ",")[[1]]
        pairs <- pairs[nchar(trimws(pairs)) > 0]
        groups <- sub(":.*", "", pairs)
        colors <- sub("[^:]*:", "", pairs)
        GROUPS_COL <- setNames(trimws(colors), trimws(groups))
    }
}

# ================================================
# OUTPUT DIRECTORY SETUP
# ================================================

# Create output directory name based on analysis parameters
feature_type <- if(ANALYZED_FEATURES == "c") {
  paste0("C", NGRAM_SIZE)
} else {
  paste0("W", NGRAM_SIZE)
}

OUTPUT_DIR <- paste0("results_", feature_type, "_", 
                     MFW_MIN, "-", MFW_MAX, "_", timestamp)

# Create the output directory
dir.create(OUTPUT_DIR, showWarnings = FALSE)

cat("========================================\n")
cat("OUTPUT DIRECTORY CREATED\n")
cat("========================================\n")
cat("All results will be saved to:", OUTPUT_DIR, "\n")
cat("========================================\n\n")

# Store original working directory
original_dir <- getwd()
CORPUS_PATH <- if (startsWith(CORPUS_DIR, "/")) CORPUS_DIR else CORPUS_PATH

# Filter corpus: copy only regular .txt files to a temp directory so that
# non-file entries like __pycache__ don't confuse stylo's loader.
corpus_tmp <- file.path(tempdir(), paste0("stylo_corpus_", format(Sys.time(), "%Y%m%d_%H%M%S")))
dir.create(corpus_tmp, recursive = TRUE)
txt_files <- list.files(CORPUS_PATH, pattern = "\\.txt$", full.names = TRUE, recursive = FALSE)
txt_files <- txt_files[file.info(txt_files)$isdir == FALSE]
if (length(txt_files) == 0) stop("No .txt files found in corpus directory: ", CORPUS_PATH)
invisible(file.copy(txt_files, corpus_tmp))
CORPUS_PATH <- corpus_tmp
cat("Filtered corpus: using", length(txt_files), ".txt files from", CORPUS_DIR, "\n")

# Change to output directory for all stylo operations
setwd(OUTPUT_DIR)

# ================================================
# LOAD CORPUS AND CREATE FREQUENCY TABLE ONCE
# ================================================

cat("========================================\n")
cat("LOADING CORPUS (ONE TIME ONLY)\n")
cat("========================================\n")

# Use stylo.default.settings to prepare everything
cat("Loading corpus from:", CORPUS_PATH, "\n")

# Create frequency table using stylo's internal method
# This is more reliable than manual parsing
initial_results <- stylo(
  gui = FALSE,
  corpus.dir = CORPUS_PATH,
  analyzed.features = ANALYZED_FEATURES,
  ngram.size = NGRAM_SIZE,
  preserve.case = PRESERVE_CASE,
  encoding = ENCODING,
  mfw.min = MFW_MIN,
  mfw.max = MFW_MAX,
  mfw.incr = MFW_INCR,
  culling.min = CULLING_MIN,
  culling.max = CULLING_MAX,
  culling.incr = CULLING_INCR,
  mfw.list.cutoff = MFW_LIST_CUTOFF,
  analysis.type = "CA",  # Dummy analysis just to get frequency table
  distance.measure = "delta",
  display.on.screen = FALSE,
  write.pdf.file = FALSE,  # Don't save this dummy analysis
  save.analyzed.features = SAVE_ANALYZED_FEATURES,
  save.analyzed.freqs = SAVE_ANALYZED_FREQS,
  groups.col = GROUPS_COL
)

# Extract the frequency table from results
freq_table <- initial_results$table.with.all.freqs

cat("Corpus loaded! Texts:", nrow(freq_table), "\n")
cat("Frequency table created! Features:", ncol(freq_table), "\n")
cat("========================================\n\n")

# ================================================
# ANALYSIS CONFIGURATION
# ================================================

# List of all analysis types to test
analysis_types <- c("CA", "BCT", "PCV", "MDS")

# List of all distance measures to test
distance_measures <- c("delta", "argamon", "eder", "simple", "canberra", 
                       "manhattan", "euclidean", "cosine", "wurzburg", "minmax")

# ================================================
# OPTIMIZED ANALYSIS STRATEGY
# ================================================
# 1. Run PCV once (doesn't use distance measures)
# 2. For each distance measure:
#    - Run CA, BCT, MDS in sequence
#    - EDGES files created by first analysis are reused
# This avoids duplicate EDGES files

# ================================================
# STEP 1: RUN PCV (NO DISTANCE MEASURE)
# ================================================

cat("\n########################################\n")
cat("### STEP 1: PCV ANALYSIS\n")
cat("########################################\n")

filename <- paste0("clusters_", feature_type, "_", MFW_MIN, "-", MFW_MAX, 
                  "_PCV_", timestamp)

results <- stylo(gui = FALSE,
                 frequencies = freq_table,
                 analyzed.features = ANALYZED_FEATURES,
                 ngram.size = NGRAM_SIZE,
                 preserve.case = PRESERVE_CASE,
                 distance.measure = "delta",  # Placeholder
                 analysis.type = "PCV",
                 encoding = ENCODING,
                 mfw.min = MFW_MAX,  # Single iteration at maximum
                 mfw.max = MFW_MAX,
                 mfw.incr = 0,       # No iterations
                 culling.min = CULLING_MIN,
                 culling.max = CULLING_MAX,
                 culling.incr = CULLING_INCR,
                 mfw.list.cutoff = MFW_LIST_CUTOFF,
                 consensus.strength = CONSENSUS_STRENGTH,
                 sampling = SAMPLING,
                 sample.size = SAMPLE_SIZE,
                 number.of.samples = NUMBER_OF_SAMPLES,
                 sampling.with.replacement = SAMPLING_WITH_REPLACEMENT,
                 display.on.screen = DISPLAY_ON_SCREEN,
                 write.pdf.file = WRITE_PDF_FILE,
                 write.jpg.file = WRITE_JPG_FILE,
                 write.svg.file = WRITE_SVG_FILE,
                 write.png.file = WRITE_PNG_FILE,
                 plot.custom.height = PLOT_CUSTOM_HEIGHT,
                 plot.custom.width = PLOT_CUSTOM_WIDTH,
                 plot.font.size = PLOT_FONT_SIZE,
                 plot.line.thickness = PLOT_LINE_THICKNESS,
                 plot.options.reset = PLOT_OPTIONS_RESET,
                 custom.graph.title = "PCV (Principal Components)",
                 custom.graph.filename = filename,
                 text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                 colors.on.graphs = COLORS_ON_GRAPHS,
                 titles.on.graphs = TITLES_ON_GRAPHS,
                 label.offset = LABEL_OFFSET,
                 save.distance.tables = FALSE,
                 save.analyzed.features = FALSE,
                 save.analyzed.freqs = FALSE,
                 groups.col = GROUPS_COL)

cat("Completed: PCV\n")

# ================================================
# STEP 2: RUN CA, BCT, MDS FOR EACH DISTANCE MEASURE
# ================================================

cat("\n########################################\n")
cat("### STEP 2: CA, BCT, MDS ANALYSES\n")
cat("########################################\n\n")

# Loop through distance measures (outer loop)
for (dist_measure in distance_measures) {
  
  cat("\n========================================\n")
  cat("DISTANCE MEASURE:", dist_measure, "\n")
  cat("========================================\n")
  
  # Loop through CA, BCT, MDS (inner loop)
  # Note: We exclude PCV since it was already done
  for (analysis_type in c("CA", "BCT", "MDS")) {
    
    cat("\nProcessing:", analysis_type, "with", dist_measure, "\n")
    
    filename <- paste0("clusters_", feature_type, "_", MFW_MIN, "-", MFW_MAX, 
                      "_", dist_measure, "_", analysis_type, "_", timestamp)
    
    # BCT needs multiple MFW iterations for consensus
    # CA and MDS only need one iteration (at max MFW)
    use_mfw_min <- if(analysis_type == "BCT") MFW_MIN else MFW_MAX
    use_mfw_incr <- if(analysis_type == "BCT") MFW_INCR else 0
    
    results <- tryCatch(
      stylo(gui = FALSE,
                     frequencies = freq_table,
                     analyzed.features = ANALYZED_FEATURES,
                     ngram.size = NGRAM_SIZE,
                     preserve.case = PRESERVE_CASE,
                     distance.measure = dist_measure,
                     analysis.type = analysis_type,
                     encoding = ENCODING,
                     mfw.min = use_mfw_min,
                     mfw.max = MFW_MAX,
                     mfw.incr = use_mfw_incr,
                     culling.min = CULLING_MIN,
                     culling.max = CULLING_MAX,
                     culling.incr = CULLING_INCR,
                     mfw.list.cutoff = MFW_LIST_CUTOFF,
                     consensus.strength = CONSENSUS_STRENGTH,
                     sampling = SAMPLING,
                     sample.size = SAMPLE_SIZE,
                     number.of.samples = NUMBER_OF_SAMPLES,
                     sampling.with.replacement = SAMPLING_WITH_REPLACEMENT,
                     display.on.screen = DISPLAY_ON_SCREEN,
                     write.pdf.file = WRITE_PDF_FILE,
                     write.jpg.file = WRITE_JPG_FILE,
                     write.svg.file = WRITE_SVG_FILE,
                     write.png.file = WRITE_PNG_FILE,
                     plot.custom.height = PLOT_CUSTOM_HEIGHT,
                     plot.custom.width = PLOT_CUSTOM_WIDTH,
                     plot.font.size = PLOT_FONT_SIZE,
                     plot.line.thickness = PLOT_LINE_THICKNESS,
                     plot.options.reset = PLOT_OPTIONS_RESET,
                     custom.graph.title = paste(analysis_type, "- Distance:", dist_measure),
                     custom.graph.filename = filename,
                     text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                     colors.on.graphs = COLORS_ON_GRAPHS,
                     titles.on.graphs = TITLES_ON_GRAPHS,
                     label.offset = LABEL_OFFSET,
                     save.distance.tables = SAVE_DISTANCE_TABLES,
                     save.analyzed.features = FALSE,
                     save.analyzed.freqs = FALSE,
                     groups.col = GROUPS_COL),
      error = function(e) {
        cat("WARNING: skipped", analysis_type, "with", dist_measure,
            "- error:", conditionMessage(e), "\n")
        NULL
      }
    )

    if (!is.null(results)) cat("Completed:", analysis_type, "with", dist_measure, "\n")
  }
  
  cat("\n========================================\n")
  cat("Completed all analysis types for", dist_measure, "\n")
  cat("========================================\n")
}

# Return to original directory
setwd(original_dir)

cat("\n========================================\n")
cat("ALL ANALYSES COMPLETE!\n")
cat("========================================\n")
cat("Total PDFs created: 31\n")
cat("  - PCV: 1\n")
cat("  - CA/BCT/MDS: 30 (3 analysis types × 10 distance measures)\n")
cat("========================================\n")

# Print summary of settings used
cat("\n========================================\n")
cat("ANALYSIS SETTINGS SUMMARY:\n")
cat("========================================\n")
cat("Output directory:", OUTPUT_DIR, "\n")
cat("Feature type:", ANALYZED_FEATURES, "\n")
cat("N-gram size:", NGRAM_SIZE, "\n")
cat("MFW range:", MFW_MIN, "-", MFW_MAX, "by", MFW_INCR, "\n")
cat("Culling:", CULLING_MIN, "%\n")
cat("Iterations per analysis:", (MFW_MAX - MFW_MIN) / MFW_INCR + 1, "\n")
cat("Distance measures:", length(distance_measures), "\n")
cat("Analysis types:", length(analysis_types), "\n")
cat("Save distance tables:", SAVE_DISTANCE_TABLES, "\n")
cat("Optimizations applied:\n")
cat("  ✓ Corpus loaded once (not 31 times)\n")
cat("  ✓ EDGES files generated efficiently\n")
cat("  ✓ Distance tables reused across analysis types\n")
cat("========================================\n")

# List files in output directory
cat("\n========================================\n")
cat("FILES CREATED IN OUTPUT DIRECTORY:\n")
cat("========================================\n")
output_files <- list.files(OUTPUT_DIR)
cat("Total files:", length(output_files), "\n\n")

# Categorize files
pdf_files <- grep("\\.pdf$", output_files, value = TRUE)
csv_files <- grep("\\.csv$|EDGES", output_files, value = TRUE)
txt_files <- grep("\\.txt$", output_files, value = TRUE)

cat("PDF graphs:", length(pdf_files), "\n")
cat("CSV/EDGES files:", length(csv_files), "\n")
cat("TXT data files:", length(txt_files), "\n")
cat("\nAll files are in:", file.path(getwd(), OUTPUT_DIR), "\n")
cat("========================================\n")