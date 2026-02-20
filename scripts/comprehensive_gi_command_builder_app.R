#!/usr/bin/env Rscript

library(shiny)

build_flag <- function(name, value) {
  if (is.null(value) || !nzchar(trimws(value))) return(NULL)
  paste0("--", name, "=", shQuote(value))
}

list_corpus_text_names <- function(corpus_dir) {
  if (!nzchar(trimws(corpus_dir))) return(character(0))
  if (!dir.exists(corpus_dir)) return(character(0))
  files <- list.files(corpus_dir, pattern = "\\.txt$", full.names = FALSE)
  if (length(files) == 0) return(character(0))
  sort(unique(sub("\\.[^.]+$", "", files)))
}

resolve_corpus_dir <- function(corpus_dir) {
  raw_path <- trimws(corpus_dir)
  if (!nzchar(raw_path)) return("")
  if (dir.exists(raw_path)) return(raw_path)

  # Common case: app launched from scripts/, but corpus path is project-relative.
  fallback <- file.path("..", raw_path)
  if (dir.exists(fallback)) return(fallback)

  raw_path
}

app_ui <- fluidPage(
  titlePanel("Comprehensive GI Test Command Builder"),
  sidebarLayout(
    sidebarPanel(
      textInput("script_path", "Script path", "scripts/comprehensive_gi_test.R"),
      textInput("corpus_dir", "Corpus directory", "corpus/gi"),
      verbatimTextOutput("corpus_status", placeholder = TRUE),
      selectizeInput("target", "Target", choices = character(0), multiple = FALSE),
      selectizeInput("candidates", "Candidates", choices = character(0), multiple = TRUE),
      textInput("candidate_regex", "Candidate regex (optional)", ""),
      selectizeInput("exclude_imposters", "Exclude imposters by name", choices = character(0), multiple = TRUE),
      textInput("exclude_imposters_regex", "Exclude imposters by regex (optional)", ""),
      textInput("feature_set", "Feature-set file path (optional)", ""),
      textInput("run_note", "Run note (optional)", ""),
      numericInput("feature_sample_rate", "Feature sample rate", 0.5, min = 0.01, max = 1, step = 0.01),
      numericInput("imposter_sample_rate", "Imposter sample rate", 0.5, min = 0.01, max = 1, step = 0.01),
      numericInput("feature_count_trigrams", "Feature count trigrams", 2000, min = 1, step = 1),
      numericInput("feature_count_unigrams", "Feature count unigrams", 2000, min = 1, step = 1),
      numericInput("iterations", "Iterations", 100, min = 1, step = 1),
      checkboxInput("diagnostic_mode", "Diagnostic mode", FALSE),
      numericInput("diagnostic_top_n", "Diagnostic top N", 10, min = 1, step = 1)
    ),
    mainPanel(
      h4("Generated command"),
      tags$p("Copy this command and run it in terminal."),
      verbatimTextOutput("command_preview", placeholder = TRUE)
    )
  )
)

app_server <- function(input, output, session) {
  resolved_corpus_dir <- reactive({
    resolve_corpus_dir(input$corpus_dir)
  })

  corpus_names <- reactive({
    list_corpus_text_names(resolved_corpus_dir())
  })

  output$corpus_status <- renderText({
    names <- corpus_names()
    if (!dir.exists(resolved_corpus_dir())) {
      return(paste("Corpus directory not found:", input$corpus_dir))
    }
    if (normalizePath(resolved_corpus_dir(), winslash = "/", mustWork = FALSE) !=
        normalizePath(trimws(input$corpus_dir), winslash = "/", mustWork = FALSE)) {
      paste("Loaded", length(names), "text names from", resolved_corpus_dir(), "(resolved from", input$corpus_dir, ")")
    } else {
      paste("Loaded", length(names), "text names from", resolved_corpus_dir())
    }
  })

  observe({
    names <- corpus_names()
    selected_target <- if (!is.null(input$target) && input$target %in% names) input$target else ""
    updateSelectizeInput(session, "target", choices = names, selected = selected_target, server = TRUE)

    candidate_choices <- setdiff(names, selected_target)
    selected_candidates <- intersect(input$candidates, candidate_choices)
    updateSelectizeInput(session, "candidates", choices = candidate_choices, selected = selected_candidates, server = TRUE)

    imposter_exclude_choices <- setdiff(names, c(selected_target, selected_candidates))
    selected_excluded <- intersect(input$exclude_imposters, imposter_exclude_choices)
    updateSelectizeInput(session, "exclude_imposters", choices = imposter_exclude_choices, selected = selected_excluded, server = TRUE)
  })

  command_text <- reactive({
    candidates_value <- if (length(input$candidates) > 0) paste(input$candidates, collapse = ",") else ""
    exclude_imposters_value <- if (length(input$exclude_imposters) > 0) paste(input$exclude_imposters, collapse = ",") else ""
    flags <- c(
      build_flag("target", input$target),
      build_flag("candidates", candidates_value),
      build_flag("candidate-regex", input$candidate_regex),
      build_flag("exclude-imposters", exclude_imposters_value),
      build_flag("exclude-imposters-regex", input$exclude_imposters_regex),
      build_flag("feature-set", input$feature_set),
      build_flag("note", input$run_note),
      build_flag("feature-sample-rate", as.character(input$feature_sample_rate)),
      build_flag("imposter-sample-rate", as.character(input$imposter_sample_rate)),
      build_flag("feature-count-trigrams", as.character(as.integer(input$feature_count_trigrams))),
      build_flag("feature-count-unigrams", as.character(as.integer(input$feature_count_unigrams))),
      build_flag("iterations", as.character(as.integer(input$iterations))),
      if (isTRUE(input$diagnostic_mode)) "--diagnostic-mode" else NULL,
      if (isTRUE(input$diagnostic_mode)) build_flag("diagnostic-top-n", as.character(as.integer(input$diagnostic_top_n))) else NULL
    )

    flags <- Filter(Negate(is.null), flags)
    paste(c("Rscript", shQuote(input$script_path), flags), collapse = " ")
  })

  output$command_preview <- renderText({
    command_text()
  })
}

shinyApp(ui = app_ui, server = app_server)
