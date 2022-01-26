use "master.dta", replace

//Convert time into number of seconds
rename time time2
generate time = 60*mm(time2)+ss(time2)
drop time2

//1. Explaining "is_correct". Fixed effects.

//Table 18

quietly probit is_correct length i.id_question i.user if total_score<9
estimates store regr2a1
quietly probit is_correct cyclomatic i.id_question i.user if total_score<9
estimates store regr2a2
quietly probit is_correct quantity i.id_question i.user if total_score<9
estimates store regr2a3
quietly probit is_correct potentialvolume i.id_question i.user if total_score<9
estimates store regr2a4
quietly probit is_correct operatordiversity i.id_question i.user if total_score<9
estimates store regr2a5
quietly probit is_correct level i.id_question i.user if total_score<9
estimates store regr2a6
quietly probit is_correct length cyclomatic quantity potentialvolume operatordiversity i.id_question i.user if total_score<9
estimates store regr2a7

estout regr2a1 regr2a2 regr2a3 regr2a4 regr2a5 regr2a6 regr2a7, cells(b(star fmt(3)) t(par fmt(2))) stats(ll r2_p, fmt(2 3) labels(Log-Likelihood Pseudo-R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

//2. Explaining time. Fixed effects.

//Table 19

quietly reg time length i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a1
quietly reg time cyclomatic i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a2
quietly reg time quantity i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a3
quietly reg time potentialvolume i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a4
quietly reg time operatordiversity i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a5
quietly reg time level i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a6
quietly reg time length cyclomatic quantity potentialvolume operatordiversity i.id_question i.user if is_correct==1 & time > 7 & time < 579
estimates store regr4a7

estout regr4a1 regr4a2 regr4a3 regr4a4 regr4a5 regr4a6 regr4a7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(2 3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type
