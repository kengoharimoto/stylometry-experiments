library(stylo)

CORPUS_DIR <- "corpus/gi"
timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

# ================================================
# TEST CONFIGURATIONS
# ================================================
# Each config produces 31 stylo() calls:
#   PCV (1) + 10 distance metrics x 3 methods (30)

configs <- list(
  list(features = "w", ngram = 1, mfw_min = 50,   mfw_max = 100,   mfw_incr = 10,   label = "W1_50-100"),
  list(features = "w", ngram = 1, mfw_min = 100,  mfw_max = 100,   mfw_incr = 0,    label = "W1_100"),
  list(features = "w", ngram = 1, mfw_min = 100,  mfw_max = 500,   mfw_incr = 100,  label = "W1_100-500"),
  list(features = "c", ngram = 3, mfw_min = 500,  mfw_max = 1500,  mfw_incr = 100,  label = "C3_500-1500"),
  list(features = "c", ngram = 3, mfw_min = 1000, mfw_max = 2000,  mfw_incr = 100,  label = "C3_1000-2000"),
  list(features = "c", ngram = 3, mfw_min = 5000, mfw_max = 10000, mfw_incr = 1000, label = "C3_5000-10000")
)

# ================================================
# SHARED PARAMETERS
# ================================================

PRESERVE_CASE <- FALSE
ENCODING <- "UTF-8"
CULLING_MIN <- 0
CULLING_MAX <- 0
CULLING_INCR <- 0
MFW_LIST_CUTOFF <- 20000
CONSENSUS_STRENGTH <- 0.5
SAMPLING <- "no.sampling"
SAMPLE_SIZE <- 10000
NUMBER_OF_SAMPLES <- 1
SAMPLING_WITH_REPLACEMENT <- FALSE

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

SAVE_DISTANCE_TABLES <- TRUE

distance_measures <- c("delta", "argamon", "eder", "simple", "canberra",
                       "manhattan", "euclidean", "cosine", "wurzburg", "minmax")

# ================================================
# CORPUS LOADING HELPER
# ================================================

original_dir <- getwd()
corpus_abs <- file.path(original_dir, CORPUS_DIR)

load_corpus <- function(features, ngram, mfw_max, outdir) {
  cat("Loading corpus:", corpus_abs, "features =", features, "ngram =", ngram, "\n")
  setwd(outdir)
  res <- stylo(
    gui = FALSE,
    corpus.dir = corpus_abs,
    analyzed.features = features,
    ngram.size = ngram,
    preserve.case = PRESERVE_CASE,
    encoding = ENCODING,
    mfw.min = mfw_max,
    mfw.max = mfw_max,
    mfw.incr = 0,
    culling.min = CULLING_MIN,
    culling.max = CULLING_MAX,
    culling.incr = CULLING_INCR,
    mfw.list.cutoff = MFW_LIST_CUTOFF,
    analysis.type = "CA",
    distance.measure = "delta",
    display.on.screen = FALSE,
    write.pdf.file = FALSE,
    save.analyzed.features = TRUE,
    save.analyzed.freqs = TRUE
  )
  setwd(original_dir)
  freq_table <- res$table.with.all.freqs
  cat("  Texts:", nrow(freq_table), " Features:", ncol(freq_table), "\n")
  freq_table
}

# ================================================
# RUN ALL CONFIGURATIONS
# ================================================

cat("========================================\n")
cat("EXTENSIVE CLUSTER ANALYSIS\n")
cat("========================================\n")
cat("Corpus:", CORPUS_DIR, "\n")
cat("Configs:", length(configs), "\n")
cat("Timestamp:", timestamp, "\n")
cat("========================================\n\n")

# Pre-load corpora: one for word features, one for char-3grams
# Use the largest mfw_max from each feature type

w_max <- max(sapply(Filter(function(c) c$features == "w", configs), function(c) c$mfw_max))
c_max <- max(sapply(Filter(function(c) c$features == "c", configs), function(c) c$mfw_max))

# Create a temporary directory for corpus loading
tmp_load_dir <- file.path(original_dir, "results", "gi", ".tmp_load")
dir.create(tmp_load_dir, recursive = TRUE, showWarnings = FALSE)

cat("Pre-loading word corpus (mfw_max =", w_max, ")...\n")
freq_table_w <- load_corpus("w", 1, w_max, tmp_load_dir)

cat("Pre-loading char-3gram corpus (mfw_max =", c_max, ")...\n")
freq_table_c <- load_corpus("c", 3, c_max, tmp_load_dir)

unlink(tmp_load_dir, recursive = TRUE)

cat("\nCorpora loaded. Starting analyses...\n\n")

total_configs <- length(configs)

for (ci in seq_along(configs)) {
  cfg <- configs[[ci]]
  features <- cfg$features
  ngram <- cfg$ngram
  mfw_min <- cfg$mfw_min
  mfw_max <- cfg$mfw_max
  mfw_incr <- cfg$mfw_incr
  label <- cfg$label

  feature_type <- if (features == "c") paste0("C", ngram) else paste0("W", ngram)

  cat("\n########################################\n")
  cat("### CONFIG", ci, "/", total_configs, ":", label, "\n")
  cat("########################################\n")

  # Select pre-loaded frequency table
  freq_table <- if (features == "w") freq_table_w else freq_table_c

  # Create output directory
  out_dir <- file.path(original_dir, "results", "gi", label, timestamp)
  dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
  setwd(out_dir)

  # --- PCV ---
  cat("\n  PCV analysis...\n")
  filename <- paste0("clusters_", feature_type, "_", mfw_min, "-", mfw_max, "_PCV_", timestamp)

  results <- stylo(gui = FALSE,
                   frequencies = freq_table,
                   analyzed.features = features,
                   ngram.size = ngram,
                   preserve.case = PRESERVE_CASE,
                   distance.measure = "delta",
                   analysis.type = "PCV",
                   encoding = ENCODING,
                   mfw.min = mfw_max,
                   mfw.max = mfw_max,
                   mfw.incr = 0,
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
                   custom.graph.title = paste(label, "- PCV"),
                   custom.graph.filename = filename,
                   text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                   colors.on.graphs = COLORS_ON_GRAPHS,
                   titles.on.graphs = TITLES_ON_GRAPHS,
                   label.offset = LABEL_OFFSET,
                   save.distance.tables = FALSE,
                   save.analyzed.features = FALSE,
                   save.analyzed.freqs = FALSE)
  cat("  PCV done\n")

  # --- CA, BCT, MDS for each distance measure ---
  for (dist_measure in distance_measures) {
    cat("\n  Distance:", dist_measure, "\n")

    for (analysis_type in c("CA", "BCT", "MDS")) {
      cat("    ", analysis_type, "...")

      filename <- paste0("clusters_", feature_type, "_", mfw_min, "-", mfw_max,
                         "_", dist_measure, "_", analysis_type, "_", timestamp)

      use_mfw_min <- if (analysis_type == "BCT") mfw_min else mfw_max
      use_mfw_incr <- if (analysis_type == "BCT") mfw_incr else 0

      results <- stylo(gui = FALSE,
                       frequencies = freq_table,
                       analyzed.features = features,
                       ngram.size = ngram,
                       preserve.case = PRESERVE_CASE,
                       distance.measure = dist_measure,
                       analysis.type = analysis_type,
                       encoding = ENCODING,
                       mfw.min = use_mfw_min,
                       mfw.max = mfw_max,
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
                       custom.graph.title = paste(label, "-", analysis_type, "-", dist_measure),
                       custom.graph.filename = filename,
                       text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                       colors.on.graphs = COLORS_ON_GRAPHS,
                       titles.on.graphs = TITLES_ON_GRAPHS,
                       label.offset = LABEL_OFFSET,
                       save.distance.tables = SAVE_DISTANCE_TABLES,
                       save.analyzed.features = FALSE,
                       save.analyzed.freqs = FALSE)
      cat(" done\n")
    }
  }

  setwd(original_dir)

  # Summary for this config
  out_files <- list.files(out_dir)
  pdf_count <- sum(grepl("\\.pdf$", out_files))
  csv_count <- sum(grepl("\\.csv$|EDGES", out_files))
  cat("\n  ", label, "complete:", pdf_count, "PDFs,", csv_count, "CSV/EDGES files\n")
}

# ================================================
# FINAL SUMMARY
# ================================================

cat("\n========================================\n")
cat("ALL ANALYSES COMPLETE\n")
cat("========================================\n")
cat("Configs run:", total_configs, "\n")
cat("Total stylo() calls:", total_configs * 31 + 2, "(incl. 2 corpus loads)\n\n")

for (ci in seq_along(configs)) {
  cfg <- configs[[ci]]
  out_dir <- file.path("results", "gi", cfg$label, timestamp)
  n <- length(list.files(out_dir))
  cat("  ", cfg$label, ":", n, "files in", out_dir, "\n")
}

cat("\n========================================\n")
