use "master.dta", replace

//Convert time into number of seconds
rename time time2
generate time = 60*mm(time2)+ss(time2)
drop time2

//Statistics on time taken
sum time, d

//Create a dataset with 38 regulations and average time taken and frequency of correct answers, excluding outliers.

replace time = . if is_correct==0
replace time = . if time <= 7
replace time = . if time >= 579

collapse(mean) is_correct time length cyclomatic quantity potentialvolume operatordiversity level, by(id_regulation)

//Table 8
sum length cyclomatic quantity potentialvolume operatordiversity level

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

//Table 10
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

//Table 11
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

//Table 12
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

//Table 13
estout regr2b2 regr2b3 regr2b4 regr2b5 regr2b6 regr2b7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type
