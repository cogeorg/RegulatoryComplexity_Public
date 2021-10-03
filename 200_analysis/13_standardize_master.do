cd /home/co/git/RegulatoryComplexity_Public/200_analysis

insheet using ./results/Master_standardized.csv, delimiter(";") clear
	rename v1 key
	rename v2 key_cons
	rename v3 category
	
	drop key
	duplicates drop key_cons, force
	
	sort key_cons
	
	drop if key_cons == ""
outsheet using ./results/Master_consolidated.csv, delimiter(";") replace
