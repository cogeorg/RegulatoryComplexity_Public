use master_public.dta, replace
sort id_regulation

save master_public.dta, replace

import delimited "Measures.csv", clear
rename regulation id_regulation
sort id_regulation
save measures.dta, replace

use master_public.dta, replace

merge m:1 id_regulation using measures.dta
drop if id_regulation > 38
drop if id_regulation ==0
drop _merge
save master.dta, replace