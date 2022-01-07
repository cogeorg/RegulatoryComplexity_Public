cd /Users/co/Dropbox/Papers/10_WorkInProgress/MeasuringRegulatoryComplexity/110_BaselI_Pseudocode
insheet using 30_results/results_all.csv, delimiter(";") clear

rename v1 identifier
rename v2 num_operands
rename v3 num_unique_operands
rename v4 num_operators
rename v5 num_unique_operators
rename v6 total_volume
rename v7 potential_volume
rename v8 level

label var level "Level"
label var total_volume "Volume"

scatter level  total_volume 
graph export 40_results/volume_level_random.png, replace
