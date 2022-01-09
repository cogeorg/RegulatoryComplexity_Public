


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

//There is definitely a learning effect, perhaps also a tiredness effect
bysort id_question: egen mean_correct=mean(is_correct)
twoway connected mean_correct id_question
drop mean_correct

//Some dummy variables
gen business = 0
replace business = 1 if ed_area=="Business"
gen MSc = 0
replace MSc = 1 if ed_level =="Master’s Level"

//Some housekeeping
drop score sex ed_level answer correctanswer id_student ed_yr_obtained ed_area ed_institution ex_area ex_yr

//1. Explaining "is_correct". No fixed effects.

quietly probit is_correct length
estimates store regr1a1
quietly probit is_correct cyclomatic
estimates store regr1a2
quietly probit is_correct quantity
estimates store regr1a3
quietly probit is_correct potentialvolume
estimates store regr1a4
quietly probit is_correct operatordiversity
estimates store regr1a5
quietly probit is_correct level
estimates store regr1a6
quietly probit is_correct length cyclomatic quantity potentialvolume operatordiversity
estimates store regr1a7

//2. Explaining "is_correct". Fixed effects.

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

estout regr1a1 regr1a2 regr1a3 regr1a4 regr1a5 regr1a6 regr1a7, cells(b(star fmt(3)) t(par fmt(2))) stats(ll r2_p, fmt(2 3) labels(Log-Likelihood Pseudo-R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

estout regr2a1 regr2a2 regr2a3 regr2a4 regr2a5 regr2a6 regr2a7, cells(b(star fmt(3)) t(par fmt(2))) stats(ll r2_p, fmt(2 3) labels(Log-Likelihood Pseudo-R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type


//Stats on time taken.
sum time, d


//3. Explaining time. No fixed effects.

quietly reg time length if is_correct==1 & time > 7 & time < 579
estimates store regr3a1
quietly reg time cyclomatic if is_correct==1 & time > 7 & time < 579
estimates store regr3a2
quietly reg time quantity if is_correct==1 & time > 7 & time < 579
estimates store regr3a3
quietly reg time potentialvolume if is_correct==1 & time > 7 & time < 579
estimates store regr3a4
quietly reg time operatordiversity if is_correct==1 & time > 7 & time < 579
estimates store regr3a5
quietly reg time level if is_correct==1 & time > 7 & time < 579
estimates store regr3a6
quietly reg time length cyclomatic quantity potentialvolume operatordiversity if is_correct==1 & time > 7 & time < 579
estimates store regr3a7

//4. Explaining time. Fixed effects.

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

estout regr3a1 regr3a2 regr3a3 regr3a4 regr3a5 regr3a6 regr3a7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(2 3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

estout regr4a1 regr4a2 regr4a3 regr4a4 regr4a5 regr4a6 regr4a7, cells(b(star fmt(3)) t(par fmt(2))) stats(r2, fmt(2 3) labels(R2))  style(tex) keep(length cyclomatic quantity potentialvolume operatordiversity level) starlevels(* 0.10 ** 0.05 *** 0.01) ///
legend label collabels(none)  type

//5. Are effects heterogeneous across students?
gen MSc_length = MSc*length
gen MSc_cyclomatic = MSc*cyclomatic
gen MSc_quantity = MSc*quantity
gen MSc_potential = MSc*potentialvolume
gen MSc_diversity = MSc*operatordiversity

gen business_length = business*length
gen business_cyclomatic = business*cyclomatic
gen business_quantity = business*quantity
gen business_potential = business*potentialvolume
gen business_diversity = business*operatordiversity

probit is_correct length MSc_length cyclomatic MSc_cyclomatic quantity MSc_quantity potentialvolume MSc_potential operatordiversity MSc_diversity MSc if total_score<9
probit is_correct length business_length cyclomatic business_cyclomatic quantity business_quantity potentialvolume business_potential operatordiversity business_diversity business if total_score<9
probit is_correct length MSc_length cyclomatic MSc_cyclomatic quantity MSc_quantity potentialvolume MSc_potential operatordiversity MSc_diversity MSc i.id_question if total_score<9
probit is_correct length business_length cyclomatic business_cyclomatic quantity business_quantity potentialvolume business_potential operatordiversity business_diversity business i.id_question if total_score<9

reg time length MSc_length cyclomatic MSc_cyclomatic quantity MSc_quantity potentialvolume MSc_potential operatordiversity MSc_diversity MSc if is_correct==1
reg time length business_length cyclomatic business_cyclomatic quantity business_quantity potentialvolume business_potential operatordiversity business_diversity business if is_correct==1
reg time length MSc_length cyclomatic MSc_cyclomatic quantity MSc_quantity potentialvolume MSc_potential operatordiversity MSc_diversity MSc i.id_question if is_correct==1
reg time length business_length cyclomatic business_cyclomatic quantity business_quantity potentialvolume business_potential operatordiversity business_diversity business i.id_question if is_correct==1


