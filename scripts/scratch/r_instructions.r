library(stylo)

# --- STEP 1: PREPARE DATA ---
# Load and process the corpus (Character Trigrams, as per paper)
raw_data <- load.corpus.and.parse(corpus.dir = "corpus", ngram.type = "c", ngram.size = 3)
top_features <- make.frequency.list(raw_data, head = 20000)
freq_table <- make.table.of.frequencies(corpus = raw_data, features = top_features)

# --- STEP 2: DEFINE SETS ---
target_name <- "Test_vivarana_unsandhied"
# target_name <- "Kumarila_Tantravartika2.2.1-4_segmented"

# Identify rows
sankara_rows <- grep("^Sankara_", rownames(freq_table), value = TRUE)
imposter_rows <- rownames(freq_table)[!grepl("^Sankara_", rownames(freq_table)) & rownames(freq_table) != target_name]

# Safety Check
if(length(sankara_rows) == 0) stop("No Sankara files found.")
if(length(imposter_rows) == 0) stop("No Imposter files found.")

# --- STEP 3: RUN MANUAL GI LOOP ---
# We replicate the paper's logic: 100 iterations, comparing distances.

gi_score <- 0
iterations <- 100

print("Running manual verification loop...")

for(i in 1:iterations) {
  
  # A. Randomly sample 10% of the features (Paper logic )
  # (2000 features * 0.10 = 200 features per round)
  current_features <- sample(colnames(freq_table), size = length(colnames(freq_table)) * 1.0)
  
  # B. Randomly sample 50% of the Imposters (Paper logic )
  # We compare against ALL Sankara texts, but only HALF the imposters each time.
  current_imposters <- sample(imposter_rows, size = length(imposter_rows) * 0.5)
  
  # C. Build the specific matrix for this round
  # Rows = Test Text + All Sankara + Selected Imposters
  # Cols = The random 10% of features
  comparison_names <- c(target_name, sankara_rows, current_imposters)
  current_matrix <- freq_table[comparison_names, current_features]
  
  # D. Calculate Distances
  # We use 'dist.wurzburg' (Cosine Delta) as preferred by the paper[cite: 128, 149].
  # Note: This function automatically handles Z-scoring.
  dist_matrix <- as.matrix(dist.wurzburg(current_matrix))
  
  # E. Find the closest match
  # Get distances from our Test Text to everyone else
  dists_from_test <- dist_matrix[target_name, ]
  
  # Find the closest distance to ANY Sankara text
  min_sankara_dist <- min(dists_from_test[sankara_rows])
  
  # Find the closest distance to ANY of the selected Imposters
  min_imposter_dist <- min(dists_from_test[current_imposters])
  
  # F. Scoring
  # If the test text is closer to Sankara than to the best Imposter, Sankara wins.
  if(min_sankara_dist < min_imposter_dist) {
    gi_score <- gi_score + 1
  }
}

# --- STEP 4: RESULT ---
final_probability <- gi_score / iterations

print(paste("Final Probability:", final_probability))

# Visualization
barplot(final_probability, ylim=c(0,1), main="Probability of Sankara Authorship", 
        ylab="Probability", col="lightblue")
abline(h=0.66, col="green", lty=2) # Authentic Threshold
abline(h=0.34, col="red", lty=2)   # Inauthentic Threshold