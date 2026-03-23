library(stylo)
CORPUS_DIR <- "corpus/main"
# Adjust this to the filename pattern used for your primary candidate group.
CANDIDATE_PATTERN <- "^Candidate_"

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

cat("========================================\n")
cat("SANSKRIT INDECLINABLES ANALYSIS\n")
cat("========================================\n\n")

# ================================================
# SANSKRIT INDECLINABLES (AVYAYA) LIST
# ================================================

# High-frequency particles and conjunctions
high_freq <- c("ca", "tu", "hi", "eva", "api", "vā", "na", "iti", 
               "atha", "tathā", "yathā", "yadi", "kim", "u")

# Medium-frequency emphatic particles
emphatic <- c("vai", "khalu", "kila", "ha", "nūnam")

# Locative adverbs
locative <- c("tatra", "atra", "yatra", "kva", "kutra", "sarvatra", 
              "anyatra", "ūrdhvam", "adhas")

# Temporal adverbs
temporal <- c("tadā", "yadā", "adya", "śvas", "hyas", "sadā", "kadā", 
              "idānīm", "purā", "prāk", "paścāt", "ciram")

# Iterative/frequency
iterative <- c("punaḥ", "sakṛt", "muhur")

# Conditional/alternative
conditional <- c("ced", "athavā", "uta", "vātha")

# Negative
negative <- c("na", "mā", "no", "nahi")

# Manner adverbs
manner <- c("evam", "ittham", "katham")

# Other common particles
other <- c("cet", "tu", "sma", "vai", "iva", "nanu", "alam", "svid")

# Combine all into comprehensive list
indeclinables_all <- unique(c(high_freq, emphatic, locative, temporal, 
                               iterative, conditional, negative, manner, other))

cat("Total indeclinables in list:", length(indeclinables_all), "\n")
cat("\nIndeclinables:\n")
print(indeclinables_all)

# ================================================
# ANALYSIS CONFIGURATION
# ================================================

# You can choose which subset to use:
# OPTION 1: All indeclinables (most comprehensive)
FEATURES_TO_USE <- indeclinables_all

# OPTION 2: Only high-frequency (most reliable)
# FEATURES_TO_USE <- high_freq

# OPTION 3: Only particles (most style-indicative)
# FEATURES_TO_USE <- c(high_freq, emphatic)

cat("\n\nUsing", length(FEATURES_TO_USE), "features for analysis\n\n")

# Analysis types
analysis_types <- c("CA", "BCT", "PCV", "MDS")

# Distance measures - test all options
distance_measures <- c("delta", "argamon", "eder", "simple", "canberra", 
                       "manhattan", "euclidean", "cosine", "wurzburg", "minmax")

# Other settings
PRESERVE_CASE <- FALSE
ENCODING <- "UTF-8"
CONSENSUS_STRENGTH <- 0.5
DISPLAY_ON_SCREEN <- FALSE
WRITE_PDF_FILE <- TRUE
PLOT_CUSTOM_HEIGHT <- 20
PLOT_CUSTOM_WIDTH <- 20
PLOT_FONT_SIZE <- 10
TEXT_ID_ON_GRAPHS <- "both"
COLORS_ON_GRAPHS <- "colors"

# MFW settings (adjusted for small feature set of ~55 indeclinables)
MFW_MIN <- 10
MFW_MAX <- 55
MFW_INCR <- 5

# Culling settings
CULLING_MIN <- 0
CULLING_MAX <- 0
CULLING_INCR <- 0

# Sampling settings
SAMPLING <- "no.sampling"
SAMPLE_SIZE <- 10000
NUMBER_OF_SAMPLES <- 1
SAMPLING_WITH_REPLACEMENT <- FALSE

# Save options
SAVE_DISTANCE_TABLES <- TRUE
SAVE_ANALYZED_FEATURES <- TRUE
SAVE_ANALYZED_FREQS <- TRUE

# ================================================
# OUTPUT DIRECTORY SETUP
# ================================================

OUTPUT_DIR <- paste0("clusters_indeclinables_", timestamp)
dir.create(OUTPUT_DIR, showWarnings = FALSE)

cat("========================================\n")
cat("OUTPUT DIRECTORY CREATED\n")
cat("========================================\n")
cat("All results will be saved to:", OUTPUT_DIR, "\n")
cat("========================================\n\n")

original_dir <- getwd()
setwd(OUTPUT_DIR)

# ================================================
# LOAD CORPUS ONCE
# ================================================

cat("========================================\n")
cat("LOADING CORPUS (ONE TIME ONLY)\n")
cat("========================================\n")
cat("Loading corpus from:", file.path(original_dir, CORPUS_DIR), "\n")

initial_results <- stylo(
  gui = FALSE,
  corpus.dir = file.path(original_dir, CORPUS_DIR),
  features = FEATURES_TO_USE,
  analysis.type = "CA",
  distance.measure = "delta",
  encoding = ENCODING,
  preserve.case = PRESERVE_CASE,
  culling.min = CULLING_MIN,
  culling.max = CULLING_MAX,
  culling.incr = CULLING_INCR,
  display.on.screen = FALSE,
  write.pdf.file = FALSE,
  save.analyzed.features = SAVE_ANALYZED_FEATURES,
  save.analyzed.freqs = SAVE_ANALYZED_FREQS
)

freq_table <- initial_results$table.with.all.freqs

cat("Corpus loaded! Texts:", nrow(freq_table), "\n")
cat("Frequency table created! Features:", ncol(freq_table), "\n")
cat("========================================\n\n")

# ================================================
# STEP 1: RUN PCV (NO DISTANCE MEASURE)
# ================================================

cat("\n########################################\n")
cat("### STEP 1: PCV ANALYSIS\n")
cat("########################################\n")

filename <- paste0("indeclinables_PCV_", timestamp)

results <- stylo(gui = FALSE,
                 frequencies = freq_table,
                 analysis.type = "PCV",
                 distance.measure = "delta",
                 encoding = ENCODING,
                 preserve.case = PRESERVE_CASE,
                 mfw.min = MFW_MAX,
                 mfw.max = MFW_MAX,
                 mfw.incr = 0,
                 culling.min = CULLING_MIN,
                 culling.max = CULLING_MAX,
                 culling.incr = CULLING_INCR,
                 consensus.strength = CONSENSUS_STRENGTH,
                 sampling = SAMPLING,
                 sample.size = SAMPLE_SIZE,
                 number.of.samples = NUMBER_OF_SAMPLES,
                 sampling.with.replacement = SAMPLING_WITH_REPLACEMENT,
                 display.on.screen = DISPLAY_ON_SCREEN,
                 write.pdf.file = WRITE_PDF_FILE,
                 write.jpg.file = FALSE,
                 write.svg.file = FALSE,
                 write.png.file = FALSE,
                 plot.custom.height = PLOT_CUSTOM_HEIGHT,
                 plot.custom.width = PLOT_CUSTOM_WIDTH,
                 plot.font.size = PLOT_FONT_SIZE,
                 custom.graph.title = "PCV - Sanskrit Indeclinables",
                 custom.graph.filename = filename,
                 text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                 colors.on.graphs = COLORS_ON_GRAPHS,
                 save.distance.tables = FALSE,
                 save.analyzed.features = FALSE,
                 save.analyzed.freqs = FALSE)

cat("Completed: PCV\n")

# ================================================
# STEP 2: RUN CA, BCT, MDS FOR EACH DISTANCE MEASURE
# ================================================

cat("\n########################################\n")
cat("### STEP 2: CA, BCT, MDS ANALYSES\n")
cat("########################################\n\n")

for (dist_measure in distance_measures) {

  cat("\n========================================\n")
  cat("DISTANCE MEASURE:", dist_measure, "\n")
  cat("========================================\n")

  for (analysis_type in c("CA", "BCT", "MDS")) {

    cat("\nProcessing:", analysis_type, "with", dist_measure, "\n")

    filename <- paste0("indeclinables_", analysis_type, "_",
                      dist_measure, "_", timestamp)

    # BCT needs MFW iteration range; CA and MDS use single point
    use_mfw_min <- if(analysis_type == "BCT") MFW_MIN else MFW_MAX
    use_mfw_incr <- if(analysis_type == "BCT") MFW_INCR else 0

    results <- stylo(gui = FALSE,
                     frequencies = freq_table,
                     analysis.type = analysis_type,
                     distance.measure = dist_measure,
                     encoding = ENCODING,
                     preserve.case = PRESERVE_CASE,
                     mfw.min = use_mfw_min,
                     mfw.max = MFW_MAX,
                     mfw.incr = use_mfw_incr,
                     culling.min = CULLING_MIN,
                     culling.max = CULLING_MAX,
                     culling.incr = CULLING_INCR,
                     consensus.strength = CONSENSUS_STRENGTH,
                     sampling = SAMPLING,
                     sample.size = SAMPLE_SIZE,
                     number.of.samples = NUMBER_OF_SAMPLES,
                     sampling.with.replacement = SAMPLING_WITH_REPLACEMENT,
                     display.on.screen = DISPLAY_ON_SCREEN,
                     write.pdf.file = WRITE_PDF_FILE,
                     write.jpg.file = FALSE,
                     write.svg.file = FALSE,
                     write.png.file = FALSE,
                     plot.custom.height = PLOT_CUSTOM_HEIGHT,
                     plot.custom.width = PLOT_CUSTOM_WIDTH,
                     plot.font.size = PLOT_FONT_SIZE,
                     custom.graph.title = paste(analysis_type, "- Indeclinables -", dist_measure),
                     custom.graph.filename = filename,
                     text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                     colors.on.graphs = COLORS_ON_GRAPHS,
                     save.distance.tables = SAVE_DISTANCE_TABLES,
                     save.analyzed.features = FALSE,
                     save.analyzed.freqs = FALSE)

    cat("Completed:", analysis_type, "with", dist_measure, "\n")
  }

  cat("\n========================================\n")
  cat("Completed all analysis types for", dist_measure, "\n")
  cat("========================================\n")
}

cat("\n========================================\n")
cat("ANALYSIS COMPLETE!\n")
cat("========================================\n")
cat("Total PDFs created: 31\n")
cat("  - PCV: 1\n")
cat("  - CA/BCT/MDS: 30 (3 analysis types x 10 distance measures)\n")
cat("Analysis focused on", length(FEATURES_TO_USE), "Sanskrit indeclinables\n")
cat("========================================\n\n")

# ================================================
# POST-ANALYSIS: SUMMARY OF INDECLINABLE USAGE
# ================================================

cat("Generating usage statistics...\n\n")

# Use the freq_table we already have from the initial load
if (exists("freq_table") && !is.null(freq_table)) {

  cat("========================================\n")
  cat("INDECLINABLE USAGE STATISTICS\n")
  cat("========================================\n\n")

  # Total usage per text
  cat("--- Total indeclinable count per text ---\n")
  total_per_text <- rowSums(freq_table)
  print(head(sort(total_per_text, decreasing = TRUE), 10))

  # Most frequent indeclinables overall
  cat("\n--- Most frequent indeclinables (corpus-wide) ---\n")
  total_per_feature <- colSums(freq_table)
  print(head(sort(total_per_feature, decreasing = TRUE), 20))

  # Calculate proportions for the primary candidate texts
  candidate_texts <- grep(CANDIDATE_PATTERN, rownames(freq_table), value = TRUE)
  if (length(candidate_texts) > 0) {
    cat("\n--- Average usage in primary candidate texts ---\n")
    candidate_avg <- colMeans(freq_table[candidate_texts, , drop = FALSE])
    print(head(sort(candidate_avg, decreasing = TRUE), 20))
  }

  # Disputed texts
  disputed_texts <- grep("^Disputed_", rownames(freq_table), value = TRUE)
  if (length(disputed_texts) > 0) {
    cat("\n--- Average usage in Disputed texts ---\n")
    disputed_avg <- colMeans(freq_table[disputed_texts, , drop = FALSE])
    print(head(sort(disputed_avg, decreasing = TRUE), 20))
  }

  # Export detailed statistics
  stats_file <- paste0("indeclinable_statistics_", timestamp, ".csv")

  stats_df <- data.frame(
    Text = rownames(freq_table),
    Total_Indeclinables = rowSums(freq_table),
    Most_Common = apply(freq_table, 1, function(x) names(which.max(x))),
    Most_Common_Count = apply(freq_table, 1, max),
    stringsAsFactors = FALSE
  )

  write.csv(stats_df, stats_file, row.names = FALSE)
  cat("\n\nDetailed statistics saved to:", stats_file, "\n")
}

# Return to original directory
setwd(original_dir)

cat("\n========================================\n")
cat("All analyses and statistics complete!\n")
cat("========================================\n")
cat("Output directory:", OUTPUT_DIR, "\n")
cat("========================================\n")
