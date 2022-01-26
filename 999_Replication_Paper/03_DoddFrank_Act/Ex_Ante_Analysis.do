cd "Ex_ante_dictionary\"

import delimited ex-ante_dictionary_1.csv, clear 

gen found = 0
replace found = 1 if v2 > 0
gen not_found = 1-found

collapse(sum) found not_found, by(v3)

gen title = 1

save ExAnte.dta, replace


forval i = 2/16{
import delimited ex-ante_dictionary_`i'.csv, clear 

gen found = 0
replace found = 1 if v2 > 0
gen not_found = 1-found

collapse(sum) found not_found, by(v3)

gen title = `i'

append using ExAnte.dta
save ExAnte.dta, replace
}

sort title

gen operands_found = 0
replace operands_found = found if (v3 =="EconomicOperands" || v3 =="Attributes")

gen logical_found = 0
replace logical_found = found if (v3 =="LogicalConnectors")

gen regulatory_found = 0
replace regulatory_found = found if (v3 =="RegulatoryOperators")

gen mathematical_found = 0
replace mathematical_found = found if (v3 =="MathematicalOperators")

gen all_found = 0
replace all_found = found

gen other_found = 0
replace other_found = found if (v3 == "Other" || v3 =="LegalReferences" || v3 == "FunctionWords")

gen operands_not_found = 0
replace operands_not_found = not_found if (v3 =="EconomicOperands" || v3 =="Attributes")

gen logical_not_found = 0
replace logical_not_found = not_found if (v3 =="LogicalConnectors")

gen regulatory_not_found = 0
replace regulatory_not_found = not_found if (v3 =="RegulatoryOperators")

gen mathematical_not_found = 0
replace mathematical_not_found = not_found if (v3 =="MathematicalOperators")

gen all_not_found = 0
replace all_not_found = not_found

gen other_not_found = 0
replace other_not_found = not_found if (v3 == "Other" || v3 =="LegalReferences" || v3 == "FunctionWords")

collapse (sum) all_found operands_found logical_found regulatory_found mathematical_found other_found all_not_found operands_not_found logical_not_found regulatory_not_found mathematical_not_found other_not_found, by(title)

gen pct_all = all_found /(all_found+all_not_found)
gen pct_operands = operands_found / (operands_found+operands_not_found)
gen pct_logical = logical_found /(logical_found+logical_not_found)
gen pct_regulatory = regulatory_found /(regulatory_found+regulatory_not_found)
gen pct_mathematical = mathematical_found /(mathematical_found+mathematical_not_found)
gen pct_other = other_found /(other_found+other_not_found)

quietly estpost tabstat pct_all pct_operands pct_logical pct_regulatory pct_mathematical pct_other, by(title)
esttab, cells("pct_all(fmt(%12.2fc)) pct_operands(fmt(%12.2fc)) pct_logical(fmt(%12.2fc)) pct_regulatory(fmt(%12.2fc)) pct_mathematical(fmt(%12.2fc)) pct_other(fmt(%12.2fc))") ///
noobs nomtitle nonumber varlabels(`e(labels)') varwidth(20)  tex


