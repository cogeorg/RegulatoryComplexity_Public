#!/usr/bin/env bash
# OPTIMIZED FOR OS X

#
# STEP 0 -- PREPARE INPUT DATA
#

# cp ~/git/RegulatoryComplexity/030_ClassificationWebsite/apps/words/templates/PreClass/* html/
# cp ~/git/RegulatoryComplexity/030_ClassificationWebsite/apps/words/templates/Original/* html_noclass/
# cp ~/git/RegulatoryComplexity/010_cleaned_data/DODDFRANK.txt .


#
# STEP 0 -- CONDUCT PRELIMINARY ANALYSIS OF WORD COUNTS (outdated)
#
# ./10_do_analysis.py html/ results/word_count.csv


#
# STEP 1 -- PREPARE DICTIONARY
#

# ./11_create_word_dictionary.py html/ results/all_words_dictionary.csv
# /usr/local/stata17/stata-se -b do 11_clean_dictionary.do


#
# STEP 2
#

# ./12_count_html.py ./test/ ./results/test/

# ./12_count_txt.py ./txt/ ./results/all_words_dictionary_clean.csv ./results/txt/
# OR
# cp ../020_auxiliary_data/Master_clean.csv ./results/
# ./12_count_txt.py ./txt/ ./results/Master_clean.csv ./results/txt/

# ./12_count_html.py ./html/ ./results/html/
# cd results/html/
# rm *_all_titles.* 2>/dev/null
# cat results_title_*.csv >> results_all_titles.csv
# cat residual_title_*.txt >> residual_all_titles.txt
# cd ../../

# /usr/local/stata17/stata-se -b do 12_complete_dictionaries.do


#
# STEP 3
#

# ./13_standardize_master.py ./results/Master_extended.csv ./results/Master_standardized.csv
# /usr/local/stata17/stata-se -b do 13_standardize_master.do


#
# STEP 4
#

# ./14_count_html_noclass.py ./html_noclass/ ./results/Master_consolidated.csv ./results/html_noclass/
# ./14_count_html_noclass.py ./html_noclass/ ./results/Master_v1.0.csv ./results/html_noclass/
# /usr/local/stata17/stata-se -b do 14_count_html_noclass.do


#
# STEP 5
#
# for i in {0..16} ; do ./15_ex-ante_dictionary_quality.py \
#   ./results/html_noclass/category_cons_all_titles_most_frequent_keys.csv \
#   ./results/html_noclass/cons-count_title_$i.csv \
#   ./results/html_noclass/ex-ante_dictionary_$i.csv ; \
# done


#
# STEP 6 -- EBA REGULATIONS
#
./17_analyze_EBA.py ../310_EBA/ ./results/Master_v1.0.csv ./results/EBA/
cd results/EBA/ ; rm all_cons-count.csv 2>/dev/null ; cat cons-count_* >> all_cons-count.csv ; cd -


#
# OUTDATED -- ANALYZE AGENCY FEEDBACK LETTERS
#
# ./15_analyze_agencyletters.py ../300_AgencyFeedbackLetters/ ./results/Master_v1.0.csv ./results/agency_feedback_letters/
# cd results/agency_feedback_letters/ ; rm all_cons-count.csv 2>/dev/null ; cat cons-count_* >> all_cons-count.csv ; cd -