#!/usr/bin/env Rscript

packages <- c("stylo", "shiny")
missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]

if (length(missing) == 0) {
  message("All required packages are already installed.")
} else {
  install.packages(missing, repos = "https://cloud.r-project.org")
}
