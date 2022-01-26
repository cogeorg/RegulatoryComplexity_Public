REGULATORY COMPLEXITY - REPLICATION INSTRUCTIONS
2022-01-19

Jean-Edouard Colliard (colliard@hec.fr)
Co-Pierre Georg (co-pierre.georg@uct.ac.za)


* 01_Basel_I/

  Run Compute_Measures.m . This returns:

- Measures_Table_Algo.tex (Table 2)

- Correlation_Table_Algo.tex (Table 3 Panel A in the text) and Correlation_Table_Algo_Spearman.tex (Table 3 Panel B in the text)

- Table 4 in the text is directly obtained from Basel_I_Text_Data.xlsx

- Measures_Table_Text (Table 5 in the text)

- Correlation_Table_Text.tex (Table 6 Panel A in the text)

- Correlation_Table_Text_Spearman.tex (Table 6 Panel B in the text)

- Measures_Corr.tex (Table 7)


* 02_Experiments/

0. Preliminaries

- The repository for the experiments website (https://regulatorycomplexity.org), which is hosted on Heroku, can be found at https://github.com/cogeorg/regulatory-complexity . The balance sheet used in the experiments is always the same and included on the website as an image (https://github.com/cogeorg/regulatory-complexity/blob/main/app/static/balance_sheet.png).

- The regulations shown to participants on the website were generated randomly using 10_generate_regulations.sh . We then selected regulations to be included in the experiments after a manual inspection to ensure that they "make sense", i.e. are free of contradictions and look roughly similar to the actual Basel I regulations. In /10_regulations/exercises_website/ we include all regulations that were shown to the participants. Note that the balancesheet_0.html etc. are only place holders and that participants see the balance sheet image above.

1. Run Compute_Measures.m . This returns:

- Correlation_Table_Text.tex (Table 9 Panel A in the text) and Correlation_Table_Text_Spearman.tex (Table 9 Panel B in the text)

- Measures.csv

2. Run 01_data_preparation.do : matches the student answers with the complexity measures on each regulation, returns master.dta

3. Run 02_regressions.do . This returns:

- Table 8 

- Table 10

- Table 11

- Table 12

- Table 13

4. Table 14 is manually constructed by checking whether the criteria (i)-(ii') are satisfied in Tables 10-13.

5. Run 03_panel_regressions.do . This returns:

- Table 18

- Table 19


* 03_DoddFrank_Act/

1. Table 15 can be obtained directly from category_cons_all_titles_most_frequent_keys.csv . This file is generated in STEP 4 of the analysis outlined here: https://github.com/cogeorg/RegulatoryComplexity_Public/blob/main/README.md

2. Run Summary_Stats_DFA.do . This returns Table 16

3. Run Ex_Ante_Analysis.do . This returns Table 17
