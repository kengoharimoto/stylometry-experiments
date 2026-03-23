library(stylo)
CORPUS_DIR <- "corpus/main"

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

# ================================================
# SHARED STYLO PARAMETERS
# ================================================
ANALYZED_FEATURES <- "c"      
NGRAM_SIZE <- 3               
PRESERVE_CASE <- FALSE
ENCODING <- "UTF-8"

MFW_MIN <- 2000
MFW_MAX <- 5000
MFW_INCR <- 1000

# Consider raising CULLING_MIN to 20-50 if root-text noise is high
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
PLOT_CUSTOM_HEIGHT <- 20
PLOT_CUSTOM_WIDTH <- 20
PLOT_FONT_SIZE <- 10
PLOT_LINE_THICKNESS <- 1
TEXT_ID_ON_GRAPHS <- "both"
COLORS_ON_GRAPHS <- "colors"
TITLES_ON_GRAPHS <- TRUE

# ================================================
# PRE-CALCULATION STEP (Run Once)
# ================================================
cat("\n[1/3] INITIALIZING: Parsing corpus and calculating frequencies...\n")

# This call parses the text and builds the frequency matrix
# We set analysis.type to "CA" just to satisfy the function requirements
initial_data <- stylo(gui = FALSE,
                     corpus.dir = CORPUS_DIR,
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
                     sampling = SAMPLING,
                     display.on.screen = FALSE,
                     write.pdf.file = FALSE)

# Extract the calculated data
PRE_CALCULATED_FREQS <- initial_data$frequencies.0.culling
PRE_CALCULATED_FEATURES <- initial_data$features

cat("Pre-calculation complete. Features identified:", length(PRE_CALCULATED_FEATURES), "\n")

# ================================================
# OUTPUT DIRECTORY SETUP
# ================================================
feature_type <- if(ANALYZED_FEATURES == "c") paste0("C", NGRAM_SIZE) else paste0("W", NGRAM_SIZE)
OUTPUT_DIR <- paste0("results_", feature_type, "_", MFW_MIN, "-", MFW_MAX, "_", timestamp)
dir.create(OUTPUT_DIR, showWarnings = FALSE)

original_dir <- getwd()
setwd(OUTPUT_DIR)

# ================================================
# MAIN ANALYSIS LOOP (Using Pre-Calculated Data)
# ================================================
analysis_types <- c("CA", "BCT", "PCV", "MDS")
distance_measures <- c("delta", "argamon", "eder", "simple", "canberra", 
                       "manhattan", "euclidean", "cosine", "wurzburg", "minmax")

cat("\n[2/3] STARTING ANALYSIS LOOP...\n")

for (analysis_type in analysis_types) {
  
  # Determine distances to run (PCV only needs one iteration)
  current_distances <- if(analysis_type == "PCV") "delta" else distance_measures
  
  for (dist_measure in current_distances) {
    
    cat("Running:", analysis_type, "| Distance:", dist_measure, "\n")
    
    filename <- paste0("clusters_", feature_type, "_", analysis_type, "_", dist_measure)
    
    # We pass 'frequencies' and 'features' here to skip the parsing phase
    results <- stylo(gui = FALSE,
                     frequencies = PRE_CALCULATED_FREQS,
                     features = PRE_CALCULATED_FEATURES,
                     analysis.type = analysis_type,
                     distance.measure = dist_measure,
                     consensus.strength = CONSENSUS_STRENGTH,
                     display.on.screen = DISPLAY_ON_SCREEN,
                     write.pdf.file = WRITE_PDF_FILE,
                     plot.custom.height = PLOT_CUSTOM_HEIGHT,
                     plot.custom.width = PLOT_CUSTOM_WIDTH,
                     plot.font.size = PLOT_FONT_SIZE,
                     plot.line.thickness = PLOT_LINE_THICKNESS,
                     custom.graph.title = paste(analysis_type, "-", dist_measure),
                     custom.graph.filename = filename,
                     text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                     colors.on.graphs = COLORS_ON_GRAPHS,
                     titles.on.graphs = TITLES_ON_GRAPHS)
  }
}

setwd(original_dir)
cat("\n[3/3] ALL ANALYSES COMPLETE!\n")
cat("Results saved in:", OUTPUT_DIR, "\n")
