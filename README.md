# RegulatoryComplexity_Public
Public repository for Colliard and Georg (2021) "Measuring Regulatory Complexity"

*Note 1:* The replication folder for our paper is 999_Replication_Paper/. The README file contains detailed instructions for how to replicate all results in our paper.

*Note 2:* The most recent Master Dictionary we create is MasterDictionary_v1.0.csv in this folder.


**PART A - Classification Website**

URL: https://regulatorycomplexity.pythonanywhere.com


**PART B - Experiments Website**

URL: https://regulatorycomplexity.org

SOURCE: https://github.com/cogeorg/regulatory-complexity/


**PART C - Section 4 - Dodd-Frank Act**

*STEP 1:*

The titles of the Dodd-Frank Act converted into html before any words are classified:

030_ClassificationWebsite/apps/words/templates/Original/title_*.html


The DFA titles after words are pre-classified:

030_ClassificationWebsite/apps/words/templates/PreClass/


Then go to:

./RegulatoryComplexity/200_analysis/

And execute (e.g. on Linux, by uncommenting the appropriate steps):

./01_do_analysis.sh

Which includes:

./11_create_word_dictionary.py html/
	results/all_words_dictionary.csv
(creates the raw words dictionary which then is extended using stata and all duplicates are removed)

/usr/local/stata17/stata-se -b do 11_clean_dictionary.do
(cleans the dictionary)

*STEP 2:*

The next couple of commands do various counts of n-grams, in: (i) the raw Dodd-Frank Act text; (ii) the html version without classified words marked up; and (iii) the html version with classified words marked up:


cp ../020_auxiliary_data/Master_clean.csv ./results/
./12_count_txt.py ./txt/ ./results/Master_clean.csv ./results/txt/
(count occurrences of n-grams in each file in ./txt/ using the words file.)
Note: the cleaned dictionary has been manually changed to be in the format:

Token;Type

Where Token is an n-gram, and Type is its classification.

Next, analyze the raw text and unclassified html files using either of the two dictionary files above. The pre-classified html files already have a classification and don’t need an additional dictionary file.

./12_count_txt.py ./txt/ ./results/all_words_dictionary_clean.csv
./results/txt/
OR:
./12_count_txt.py ./txt/ ./results/Master_clean.csv
./results/txt/


OPTIONAL (not included, just added here for completeness):
./12_count_html_noclass.py ./html_noclass/
./results/all_words_dictionary_clean.csv
./results/html_noclass/
./12_count_html_noclass.py ./html_noclass/
./results/Master_clean.csv ./results/html_noclass/

./12_count_html.py ./html/ ./results/Master_clean.csv
./results/html/

The two dictionaries used as input are: ./results/all_words_dictionary_clean.csv
./results/Master_clean.csv
(where Master_clean.csv is copied from ../020_auxiliary_files/ once)

To produce the final classification, we use the marked-up html version:


./12_count_html.py ./html/ ./results/html/

and then the following few lines to create results_all_titles.csv and
residual_all_titles.txt.

Next, use Stata and:

12_complete_dictionaries.do

To create:
./results/html/master_dict.csv ./results/html/category_count.csv
./results/html/category_count_title_`i'.csv (i=1/16)
(this is where the actual count is generated)
../020_auxiliary_data/Master_clean.dta
./results/html/residual_all_titles.dta
./results/html/residuals_matched.csv

Then, manually complete the ./results/html/residuals_matched.csv file and convert it into a stata .dta.

*STEP 3:*

Then, to do a comparison with the count we get from using the preClass html, standardize the txt and use the manually consolidated master file to identify the largest possible number of n-grams.

The last part in 12_complete_dictionaries.do creates the new master dictionary which is then read by 13_standardize_master.py to create ./results/Master_standardized.csv

Using 13_stadardize_master.do, the consolidated Master file, ./results/Master_consolidated.csv is created.


*STEP 4:*

Run:

./14_count_html_noclass.py ./html_noclass/
../020_auxiliary_data/Sections/Protected_list/Master_consolidated.csv
./results/html_noclass/

To create ./results/html_noclass/cons-count_title_`i’.csv (i=1/16)

This file is read by 14_count_html_noclass.do, which produces the output reportes in Tables 15-17 in the paper. Results are included in the following files:

./results/html_noclass/category_cons_count_all_titles-total.csv
(number of total and unique occurrences per category)


In ./results/Master_consolidated.csv, there are a few minor errors that come from the use of ; in the keys. This is manually corrected for ./results/Master_consolidated+cleaned.csv
