R ?= Rscript

.PHONY: help install clusters clusters-tfidf indeclinables indeclinables-mfw gi-disputed gi-disputed-w3g gi-custom command-builder

help:
	@printf '%s\n' \
	'Available targets:' \
	'  make install            Install required R packages' \
	'  make clusters           Run baseline clustering analysis' \
	'  make clusters-tfidf     Run TF-IDF / rare-word clustering analysis' \
	'  make indeclinables      Run indeclinables clustering analysis' \
	'  make indeclinables-mfw  Run indeclinables MFW variation analysis' \
	'  make gi-disputed        Run disputed-text GI analysis' \
	'  make gi-disputed-w3g    Run disputed-text GI analysis across 12 configs' \
	'  make gi-custom          Run configurable GI analysis' \
	'  make command-builder    Launch the Shiny command-builder app'

install:
	$(R) scripts/install_packages.R

clusters:
	$(R) scripts/clusters.R

clusters-tfidf:
	$(R) scripts/clusters_tf_idf.R

indeclinables:
	$(R) scripts/cluster_w_indeclinables.R

indeclinables-mfw:
	$(R) scripts/indeclinables_mfw_variations.R

gi-disputed:
	$(R) scripts/test_all_disputed.R

gi-disputed-w3g:
	$(R) scripts/test_all_disputed_w3g.R

gi-custom:
	$(R) scripts/comprehensive_gi_test.R

command-builder:
	$(R) -e "shiny::runApp('scripts/comprehensive_gi_command_builder_app.R')"
