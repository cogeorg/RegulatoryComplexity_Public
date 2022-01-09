import delimited "C:\Users\colliard\Desktop\Measuring Regulatory Complexity\Material\DFA\category_cons_count_all_titles.csv"
save counts_titles.dta, replace

clear

import delimited "C:\Users\colliard\Desktop\Measuring Regulatory Complexity\Material\DFA\Master_v1.0_category_unique_count.csv"
append using counts_titles.dta

replace category_unique_count = unique_count if title ==.
replace title = 100 if title ==.

egen sum_attributes = total(category_count) if category =="Attributes"
egen sum_operands = total(category_count) if category =="EconomicOperands"
egen sum_logical = total(category_count) if category =="LogicalConnectors"
egen sum_regulatory = total(category_count) if category =="RegulatoryOperators"
egen sum_mathematical = total(category_count) if category =="MathematicalOperators"
egen sum_function = total(category_count) if category =="FunctionWords"
egen sum_legal = total(category_count) if category =="LegalReferences"
egen sum_other = total(category_count) if category =="Other"

replace category_count = sum_attributes if (category =="Attributes" && category_count==.)
replace category_count = sum_operands if (category =="EconomicOperands" && category_count==.)
replace category_count = sum_logical if (category =="LogicalConnectors" && category_count==.)
replace category_count = sum_regulatory if (category =="RegulatoryOperators" && category_count==.)
replace category_count = sum_mathematical if (category =="MathematicalOperators" && category_count==.)
replace category_count = sum_function if (category =="FunctionWords" && category_count==.)
replace category_count = sum_legal if (category =="LegalReferences" && category_count==.)
replace category_count = sum_other if (category =="Other" && category_count==.)

drop unique_count sum_attributes sum_operands sum_logical sum_regulatory sum_mathematical sum_function sum_legal sum_other

gen operands = 0
replace operands = category_count if (category =="EconomicOperands" || category =="Attributes")

gen u_operands = 0
replace u_operands = category_unique_count if (category =="EconomicOperands" || category =="Attributes")

gen logical = 0
replace logical = category_count if (category =="LogicalConnectors")

gen u_logical = 0
replace u_logical = category_unique_count if (category =="LogicalConnectors")

gen regulatory = 0
replace regulatory = category_count if (category =="RegulatoryOperators")

gen u_regulatory = 0
replace u_regulatory = category_unique_count if (category =="RegulatoryOperators")

gen mathematical = 0
replace mathematical = category_count if (category =="MathematicalOperators")

gen u_mathematical = 0
replace u_mathematical = category_unique_count if (category =="MathematicalOperators")

collapse (sum) operands u_operands logical u_logical regulatory u_regulatory mathematical u_mathematical, by(title)

gen length = operands + logical + regulatory + mathematical
gen cyclomatic = logical
gen quantity = regulatory
gen potential = 2 + u_operands
gen diversity = u_logical + u_regulatory + u_mathematical
gen level = potential / length

quietly estpost tabstat length cyclomatic quantity potential diversity level, by(title)
esttab, cells("length(label(`:var lab length')) cyclomatic(label(`:var lab cyclomatic')) quantity(label(`:var lab quantity')) potential(label(`:var lab potential')) diversity(label(`:var lab diversity')) level(fmt(%12.2fc))") ///
noobs nomtitle nonumber varlabels(`e(labels)') varwidth(20)  tex
