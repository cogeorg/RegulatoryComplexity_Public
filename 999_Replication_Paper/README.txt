REGULATORY COMPLEXITY - REPLICATION INSTRUCTIONS
2022-01-07

Jean-Edouard Colliard (colliard@hec.fr)
Co-Pierre Georg (co-pierre.georg@uct.ac.za)


* 01_Basel_I/

1. Open Basel_I_Algo.xls : gives a count of occurrences of each word in each Basel I item (algo version) as well as the word category. Replace each word with a word identifier, e.g., "=" => 1, "==" => 2, etc., save as Basel_I_Algo_Data.xls.

2. Open Basel_I_Text.xls : gives a count of occurrences of each word in each Basel I item (text version) as well as the word category. Replace each word with a word identifier, e.g., "0%" => 1, "10%" => 2, etc., save as Basel_I_Text_Data.xls.

3. Run Compute_Measures.m . This returns:

- Measures_Table_Algo.tex (Table 2)

- Correlation_Table_Algo.tex (Table 3 Panel A in the text) and Correlation_Table_Algo_Spearman.tex (Table 3 Panel B in the text)

- Table 4 in the text is directly obtained from Basel_I_Text.xlsx

- Measures_Table_Text (Table 5 in the text)

- Correlation_Table_Text.tex (Table 6 Panel A in the text)

- Correlation_Table_Text_Spearman.tex (Table 6 Panel B in the text)

- Measures_Corr.tex (Table 7)


* 02_Experiments/

0. Preliminaries

- All regulations shown to participants can be found in 10_regulations/exercises_website/ .

- The repository for the experiments website (https://regulatorycomplexity.org), which is hosted on Heroku, can be found at https://github.com/cogeorg/regulatory-complexity . The balance sheet used in the experiments is always the same and included on the website as an image (https://github.com/cogeorg/regulatory-complexity/blob/main/app/static/balance_sheet.png).

- The regulations shown to participants on the website were generated randomly using 10_generate_regulations.sh . In ./250_random_regulations/10_regulations/exercises_website/ we include all regulations that were shown to participants. Note that the balancesheet_0.html etc. are only place holders and that participants see the balance sheet image above.

- We select regulations to be included in the experiments after a manual inspection to ensure that they "make sense", i.e. are free of contradictions and look roughly similar to the actual Basel I regulations. We could have also manually generated these regulations, but using the random regulation generator enabled us to eliminate biases we might introduce in a purely manual process.

1. Open random_regulations_results.xls : gives a count of occurrences of each word in each random regulation, as well as the word category. Replace each word with a word identifier, e.g., 0.00% => 1, 10.00% => 2, etc., save as random_regulations_data.xls

2. Run Compute_Measures.m . This returns:

- Measures_Table_Text.tex (Table 8)

- Correlation_Table_Text.tex (Table 9 Panel A in the text) and Correlation_Table_Text_Spearman.tex (Table 9 Panel B in the text)

- Measures.csv

3. Next, start with Master-1.dta, with anonymization etc.

4. Run 01_data_analysis.do : matches the student answers with the complexity measures on each regulation, returns Master.dta

5. Then, delete the first part in Master.dta, until line 130

6. Run 02_regressions.do . This returns:

- Table 10

- Table 11

- Table 12

- Table 13

7. Table 14 is manually constructed by checking whether the criteria (i)-(ii') are satisfied in Tables 10-13.

8. Run 03_panel_regressions.do . This returns:

- Table 18

- Table 19


* 03_DoddFrank_Act/

1. Table 15 can be obtained directly from category_cons_all_titles_most_frequent_keys.csv . This file is generated in STEP 4 of the analysis outlined here: https://github.com/cogeorg/RegulatoryComplexity_Public/blob/main/README.md

2. Run Summary_Stats_DFA.do . This returns Table 16

3. Run Ex_Ante_Analysis.do . This returns Table 17
