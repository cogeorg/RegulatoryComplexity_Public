//Stats on students
use "master.dta", replace

collapse (mean) time is_correct, by(user)

//Generates table with summary stats and correlations for the different measures.

use "master.dta", replace

collapse length cyclomatic quantity potentialvolume operatordiversity level, by(id_regulation)

sum length cyclomatic quantity potentialvolume operatordiversity level

quietly: tabstat length cyclomatic quantity potentialvolume operatordiversity level, c(s) stat(mean) save
matrix output = r(StatTotal)'
quietly: tabstat length cyclomatic quantity potentialvolume operatordiversity level, c(s) stat(sd) save
matrix output = output,r(StatTotal)'
quietly: tabstat length cyclomatic quantity potentialvolume operatordiversity level, c(s) stat(min) save
matrix output = output,r(StatTotal)'
quietly: tabstat length cyclomatic quantity potentialvolume operatordiversity level, c(s) stat(max) save
matrix output = output,r(StatTotal)'

outtable using stats.tex, mat(output) center replace ///
caption("Summary Statistics") nobox f(%12.2fc) label ///
clabel(Table:SumStatReg)

use "master.dta", replace
//We have 7 students who took the test more than once and mess up the panel, also it means they got extra training, don't know what to do with them. I just drop them. 

drop if (user=="71448" || user=="71502" || user=="71519" || user=="71533" || user=="S60331" || user=="S62720" || user=="riwa.kanaan@hec.edu")

//Convert time into number of seconds
rename time time2
generate time = 60*mm(time2)+ss(time2)
drop time2

//Encode user
rename user user1
encode user1, gen(user)
drop user1

//Some housekeeping
drop score sex ed_level answer correctanswer id_student ed_yr_obtained ed_area ed_institution ex_area ex_yr

//Create a dataset with 38 regulations and average time taken and frequency of correct answers

replace time = . if is_correct==0
replace time = . if time <= 7
replace time = . if time >= 579


collapse(mean) is_correct time length cyclomatic quantity potentialvolume operatordiversity level, by(id_regulation)

//1. Explaining "is_correct". 

quietly reg is_correct length
estimates store regr1a1
quietly reg is_correct cyclomatic
estimates store regr1a2
quietly reg is_correct quantity
estimates store regr1a3
quietly reg is_correct potentialvolume
estimates store regr1a4
quietly reg is_correct operatordiversity
estimates store regr1a5
quietly reg is_correct level
estimates store regr1a6

estout regr1a1 regr1a2 regr1a3 regr1a4 regr1a5 regr1a6, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

quietly reg is_correct length cyclomatic
estimates store regr1b2
quietly reg is_correct length quantity
estimates store regr1b3
quietly reg is_correct length potentialvolume
estimates store regr1b4
quietly reg is_correct length operatordiversity
estimates store regr1b5
quietly reg is_correct length level
estimates store regr1b6
quietly reg is_correct length cyclomatic quantity potentialvolume operatordiversity
estimates store regr1b7

estout regr1b2 regr1b3 regr1b4 regr1b5 regr1b6 regr1b7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

//2. Explaining time. 

quietly reg time length
estimates store regr2a1
quietly reg time cyclomatic
estimates store regr2a2
quietly reg time quantity
estimates store regr2a3
quietly reg time potentialvolume
estimates store regr2a4
quietly reg time operatordiversity
estimates store regr2a5
quietly reg time level
estimates store regr2a6

estout regr2a1 regr2a2 regr2a3 regr2a4 regr2a5 regr2a6, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

quietly reg time length cyclomatic
estimates store regr2b2
quietly reg time length quantity
estimates store regr2b3
quietly reg time length potentialvolume
estimates store regr2b4
quietly reg time length operatordiversity
estimates store regr2b5
quietly reg time length level
estimates store regr2b6
quietly reg time length cyclomatic quantity potentialvolume operatordiversity
estimates store regr2b7

estout regr2b2 regr2b3 regr2b4 regr2b5 regr2b6 regr2b7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type
