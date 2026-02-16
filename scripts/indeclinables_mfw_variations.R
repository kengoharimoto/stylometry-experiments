library(stylo)
CORPUS_DIR <- "corpus/main"

timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

cat("========================================\n")
cat("INDECLINABLES MFW VARIATIONS\n")
cat("========================================\n\n")

# ================================================
# SANSKRIT INDECLINABLES (AVYAYA) LIST
# ================================================

high_freq <- c("ca", "tu", "hi", "eva", "api", "vā", "na", "iti",
               "atha", "tathā", "yathā", "yadi", "kim", "u")
emphatic <- c("vai", "khalu", "kila", "ha", "nūnam")
locative <- c("tatra", "atra", "yatra", "kva", "kutra", "sarvatra",
              "anyatra", "ūrdhvam", "adhas")
temporal <- c("tadā", "yadā", "adya", "śvas", "hyas", "sadā", "kadā",
              "idānīm", "purā", "prāk", "paścāt", "ciram")
iterative <- c("punaḥ", "sakṛt", "muhur")
conditional <- c("ced", "athavā", "uta", "vātha")
negative <- c("na", "mā", "no", "nahi")
manner <- c("evam", "ittham", "katham")
other <- c("cet", "tu", "sma", "vai", "iva", "nanu", "alam", "svid")

FEATURES_TO_USE <- unique(c(high_freq, emphatic, locative, temporal,
                             iterative, conditional, negative, manner, other))

cat("Total indeclinables in list:", length(FEATURES_TO_USE), "\n\n")

# ================================================
# 10 MFW VARIATIONS
# ================================================
# With 55 usable features, we test different windows:

mfw_variations <- list(
  list(min = 5,  max = 15,  incr = 1,  label = "top5-15"),
  list(min = 5,  max = 25,  incr = 2,  label = "top5-25"),
  list(min = 5,  max = 35,  incr = 3,  label = "top5-35"),
  list(min = 5,  max = 55,  incr = 5,  label = "top5-55"),
  list(min = 10, max = 30,  incr = 2,  label = "top10-30"),
  list(min = 10, max = 55,  incr = 5,  label = "top10-55"),
  list(min = 15, max = 40,  incr = 5,  label = "top15-40"),
  list(min = 20, max = 55,  incr = 5,  label = "top20-55"),
  list(min = 30, max = 55,  incr = 5,  label = "top30-55"),
  list(min = 40, max = 55,  incr = 5,  label = "top40-55")
)

# ================================================
# COMMON SETTINGS
# ================================================

distance_measures <- c("delta", "argamon", "eder", "simple", "canberra",
                       "manhattan", "euclidean", "cosine", "wurzburg", "minmax")

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
CULLING_MIN <- 0
CULLING_MAX <- 0
CULLING_INCR <- 0
SAMPLING <- "no.sampling"
SAMPLE_SIZE <- 10000
NUMBER_OF_SAMPLES <- 1
SAMPLING_WITH_REPLACEMENT <- FALSE
SAVE_DISTANCE_TABLES <- TRUE

# ================================================
# OUTPUT DIRECTORY
# ================================================

OUTPUT_DIR <- paste0("results_indeclinables_mfw_variations_", timestamp)
dir.create(OUTPUT_DIR, showWarnings = FALSE)

cat("Output directory:", OUTPUT_DIR, "\n\n")

original_dir <- getwd()
setwd(OUTPUT_DIR)

# ================================================
# LOAD CORPUS ONCE
# ================================================

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
  save.analyzed.features = TRUE,
  save.analyzed.freqs = TRUE
)

freq_table <- initial_results$table.with.all.freqs

cat("Corpus loaded! Texts:", nrow(freq_table), "\n")
cat("Features available:", ncol(freq_table), "\n\n")

# ================================================
# RUN ALL VARIATIONS
# ================================================

for (v_idx in seq_along(mfw_variations)) {
  v <- mfw_variations[[v_idx]]

  cat("\n########################################################\n")
  cat("### VARIATION", v_idx, "of", length(mfw_variations), ":", v$label,
      "(MFW", v$min, "-", v$max, "by", v$incr, ")\n")
  cat("########################################################\n")

  for (dist_measure in distance_measures) {
    for (analysis_type in c("CA", "BCT", "MDS")) {

      # BCT iterates over MFW range; CA/MDS use single point at max
      use_mfw_min  <- if (analysis_type == "BCT") v$min else v$max
      use_mfw_incr <- if (analysis_type == "BCT") v$incr else 0

      filename <- paste0("indecl_", v$label, "_", analysis_type, "_",
                        dist_measure, "_", timestamp)

      cat("  ", analysis_type, dist_measure, "(", v$label, ")\n")

      results <- stylo(gui = FALSE,
                       frequencies = freq_table,
                       analysis.type = analysis_type,
                       distance.measure = dist_measure,
                       encoding = ENCODING,
                       preserve.case = PRESERVE_CASE,
                       mfw.min = use_mfw_min,
                       mfw.max = v$max,
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
                       custom.graph.title = paste(analysis_type, "-", dist_measure,
                                                  "- MFW", v$min, "-", v$max),
                       custom.graph.filename = filename,
                       text.id.on.graphs = TEXT_ID_ON_GRAPHS,
                       colors.on.graphs = COLORS_ON_GRAPHS,
                       save.distance.tables = SAVE_DISTANCE_TABLES,
                       save.analyzed.features = FALSE,
                       save.analyzed.freqs = FALSE)
    }
  }

  cat("\nCompleted variation:", v$label, "\n")
}

setwd(original_dir)

cat("\n========================================\n")
cat("ALL", length(mfw_variations), "VARIATIONS COMPLETE!\n")
cat("Total tests:", length(mfw_variations) * length(distance_measures) * 3, "\n")
cat("Output directory:", OUTPUT_DIR, "\n")
cat("========================================\n")
