// =============================================================================
//
// PREPARE EBA DATA
//
// =============================================================================
cd ~/Git/RegulatoryComplexity_Public/200_analysis/results/EBA/

insheet using all_cons-count.csv, delimiter(";") nonames clear
	drop if v1 == ".DS_Store"
	split v1, p(".txt")
	drop v1
	rename v11 name_entity
	rename v3 category
	rename v4 occurrence
	rename v2 key 
	
	gen one = 1
	bysort name_entity category: egen unique_count = total(one)
	
	order name_entity category occurrence
	destring occurrence, replace

	drop key
	bysort name_entity category: egen foo = sum(occurrence)
	rename foo tot_occurence
	keep name_entity category tot_occurence unique_count
	duplicates drop
	
	// complexity measures
	egen id_name = group(name_entity)
	egen id_cat = group(category)
save tmp.dta, replace

use tmp.dta, clear
	rename unique_count o_unique_count
	rename tot_occurence o_tot_occurrence

merge 1:1 name_entity category id_name id_cat using foo2.dta // all_cons-count-old.dta 
	drop _merge 
	
	gen d_unique_count = o_unique_count - unique_count
	gen d_tot_occurrence = o_tot_occurrence - tot_occurence

// interlude: create mappings
use tmp.dta, clear
	keep id_name name_entity
	duplicates drop
save id_name_entity.dta, replace
use tmp.dta, clear
	keep category id_cat 
	duplicates drop
save id_cat_category.dta, replace

// dependent variables
insheet using ~/Dropbox/Papers/30_Submitted/MeasuringRegulatoryComplexity/650_Resubmission/EBA/Annex5/Annex5_mapping.csv, names delimiter(";") clear
	foreach var of varlist share_large share_medium share_snci {
		replace `var' = subinstr(`var', ",", ".", .)
		destring `var', replace
	}
	merge 1:1 name_entity using id_name_entity.dta
	keep if _merge == 3
	drop _merge 
save Annex5_mapping.dta, replace


// continue with main dataset
use tmp.dta, clear
	// compute complexity measures
	drop category name_entity
	order id_name id_cat
	xtset id_name id_cat

	reshape wide tot_occurence unique_count, i(id_name) j(id_cat)
	
	rename tot_occurence1 Attributes_tot
	rename unique_count1 Attributes_uniq
	rename tot_occurence2 EconOp_tot
	rename unique_count2 EconOp_uniq
	rename tot_occurence3 FctWords_tot
	rename unique_count3 FctWords_uniq
	rename tot_occurence4 LegalRef_tot
	rename unique_count4 LegalRef_uniq
	rename tot_occurence5 LogicalConn_tot
	rename unique_count5 LogicalConn_uniq
	rename tot_occurence6 MathOp_tot
	rename unique_count6 MathOp_uniq
	rename tot_occurence7 Other_tot
	rename unique_count7 Other_uniq
	rename tot_occurence8 RegOp_tot
	rename unique_count8 RegOp_uniq

	foreach var of varlist EconOp_tot-RegOp_tot {
		replace `var' = 0 if `var' == .
	}
	
	gen length = Attributes_tot + EconOp_tot + FctWords_tot + LegalRef_tot + LogicalConn_tot + MathOp_tot + RegOp_tot + Other_tot
	gen cyclomatic = LogicalConn_tot
	gen quantity = RegOp_tot
	gen potential = 2 + EconOp_uniq
	gen level = potential / length 
	gen diversity = 2 + LogicalConn_tot + MathOp_tot + RegOp_tot

	// merge entity names
merge 1:1 id_name using id_name_entity.dta
	keep if _merge == 3
	drop _merge
	
merge 1:1 id_name using Annex5_mapping.dta 
	drop if _merge != 3
	drop _merge
// 	foreach var of varlist share_large share_medium share_snci {
// 		replace `var' = 0.0 if `var' == .
// 	}
save EBA_Master.dta, replace


// =============================================================================
//
// ANALYZE EBA DATA
//
// =============================================================================
use EBA_Master.dta, clear
	
foreach var of varlist share_large share_medium share_snci {
	qui reg share_snci length
	eststo `var'1
	qui reg share_snci potential
	eststo `var'2
	qui reg share_snci length potential
	eststo `var'3 
}

foreach var of varlist share_large share_medium share_snci {
esttab `var'1 `var'2 `var'3, ///
    replace ///
    label ///
    se ///
    b(%9.4f) ///
    star(* 0.10 ** 0.05 *** 0.01) ///
    varwidth(25) ///
	stats(N r2, fmt(%9.0fc %9.3f)) ///
    alignment(D{.}{.}{-1})		
}
eststo clear 

// gen is_large = 0
// replace is_large = 1 if share_large > 0.0
// gen is_medium = 0
// replace is_medium = 1 if share_medium > 0.0
// gen is_snci = 0
// replace is_snci = 1 if share_snci > 0.0
//
// probit is_large quantity length

use EBA_Master.dta, clear
	keep id_name length potential level quantity cyclomatic diversity name_entity share_*
	rename share_large share1 
	rename share_medium share2
	rename share_snci share3
	
	reshape long share, i(id_name length potential level quantity cyclomatic diversity name_entity) j(share_type)
	
	foreach var of varlist potential level quantity cyclomatic diversity {
		su `var', d
	}

	foreach var of varlist potential level quantity cyclomatic diversity {
		reg share length `var' i.share_type##c.`var'
	}
	
	
	
// =============================================================================
//
// PREPARE BLOOMBERG DATA
//
// =============================================================================
cd ~/Git/RegulatoryComplexity_Public/200_analysis/results/agency_feedback_letters/

use name_entity_manual2.dta, clear // there are multiple letter company names per single bloomberg company name, needs to be corrected for consolidation
	keep company_id_bloomberg company_name
	duplicates drop
save name_entity_manual3.dta, replace  // use this for bloomberg consolidation

use ~/Downloads/StockPrices_Data/StockMarketData.dta, clear
	rename conm company_id_bloomberg 	
merge m:1 company_id_bloomberg using name_entity_manual3.dta
	keep if _merge == 3
	drop _merge
	
	drop company_id_bloomberg 

	rename datadate date	
	order company_name date
	sort company_name date
	
	keep company_name prccd prcod date
	
	// merge letter dates
save agency_letters_bloomberg.dta, replace

// create unique entity ids
use agency_letters_bloomberg.dta, clear
	egen id_company = group(company_name)
	keep company_name id_company 
	duplicates drop
save id_company_name.dta, replace

// ...AND CONTINUE WITH BLOOMBERG DATA
use agency_letters_bloomberg.dta, clear
merge m:1 company_name using id_company_name.dta
	keep if _merge == 3
	drop _merge 

	xtset id_company date 
	tsfill, full
	
merge m:1 id_company using id_company_name.dta, update  // merge again for newly generated dates
	keep if _merge == 3 | _merge == 4
	drop _merge 
	
	drop if date < mdy(01,01,2014) | date > mdy(06,30,2023)  // only keep dates right around letter dates
	
	// impute prices by setting them to the last known value
	bysort company_name: replace prccd = prccd[_n-1] if prccd == .
	bysort company_name: replace prcod = prcod[_n-1] if prcod == .
	
	drop if prccd == .  // first three dates for every company 
	
merge m:n company_name date using letter_dates.dta

	gen is_pub_date = 0
	replace is_pub_date = 1 if _merge == 3
	drop _merge

// 	gen post_10d = 0
// 	forval i = 1/10 {
// 		replace post_10d = 1 if is_pub_date[_n-`i'] == 1
// 	}
//
// 	gen post_21d = 0
// 	forval i = 1/21 {
// 		replace post_21d = 1 if is_pub_date[_n-`i'] == 1
// 	}
	
	// generate daily returns
	bysort company_name: gen ret = 100*(prccd - prccd[_n-1])/prccd[_n-1]
	// generate aggregate daily returns
	bysort date: egen market_return = mean(ret)
	
	sort company_name date
save agency_letters_bloomberg1.dta, replace

	keep date market_return 
	duplicates drop
	drop if market_return == 0
	gen id_trading_day = _n
	drop market_return
save trading_days.dta, replace


// =============================================================================
//
// ANALYZE BLOOMBERG DATA
//
// =============================================================================
use agency_letters_bloomberg1.dta, clear
	merge m:1 date using trading_days.dta
	drop if id_trading_day == .
// 	replace id_trading_day = -1 if id_trading_day == .
	drop _merge
	
	// CREATE EVENTS BASED ON COMPANY-YEAR 
	gen year = year(date)
	gen company_year = company + string(year)
	egen company_id = group(company_year)  // we have at most one letter per company and year

	// CREATE EVENT AND ESTIMATION WINDOWS
	sort company_id date
	order company_id date
	by company_id: gen datenum=_n
	by company_id: gen target=datenum if is_pub_date == 1
	egen td=min(target), by(company_id)
	drop target
	gen dif=datenum-td

	by company_id: gen event_window=1 if dif>=0 & dif<=4
	egen count_event_obs=count(event_window), by(company_id)
	by company_id: gen estimation_window=1 if dif<0 & dif>=-20
	
	egen count_est_obs=count(estimation_window), by(company_id)
	
	replace event_window=0 if event_window==.
	replace estimation_window=0 if estimation_window==.
	
	// drop stuff outside the windows
	drop if count_event_obs == 0 | count_est_obs == 0
	drop count_event_obs count_est_obs

	// ESTIMATE NORMAL PERFORMANCE
	gen predicted_return=.
	egen id=group(company_id)
	forvalues i=1(1)54{ // NOTE: replace 52 with max of id
		 l id company_id if id==`i' & dif==0
		   reg ret market_return if id==`i' & estimation_window==1
		   predict p if id==`i'
		   replace predicted_return = p if id==`i' & event_window==1
		   drop p
	   }

	// we only want dates in the event window to remain from here on
	keep if event_window == 1
	
	// COMPUTE ABNORMAL RETURN
	sort id date
	gen abnormal_return=ret-predicted_return
	by id: egen cumulative_abnormal_return = sum(abnormal_return)

	// TEST IF ABNORMAL RETURN IS DIFFERENT FROM ZERO
	sort id date
	by id: egen ar_sd = sd(abnormal_return)
	
	gen test =(1/sqrt(324))*(cumulative_abnormal_return /ar_sd) // sqrt over number of observations
	list company_id cumulative_abnormal_return test if dif==0
	
	outsheet company_id is_pub_date cumulative_abnormal_return test using stats.csv if dif==0, comma names replace
	
	reg cumulative_abnormal_return if dif==0, robust
save agency_letters_bloomberg2.dta, replace

use agency_letters_bloomberg2.dta, clear
	// KEEP ONLY RELEVANT OBSERVATIONS, I.E. CAR 
	keep company_name date is_pub_date company_id cumulative_abnormal_return ar_sd
	keep if is_pub_date == 1
	drop is_pub_date 
	
	// MERGE COMPLEXITY MEASURES
	order company_name date
	sort company_name date
	
	
merge 1:1 company_name date using agency_letters_master1.dta
	keep if _merge == 3  // we lose 5 observations because 2016 had two years where letters are published and the td computation above is messed up in this case; FIXME
	drop _merge
	
	sort company_name date
	egen id_company = group(company_name)
	egen id_year = group(year)
	
	reg cumulative_abnormal_return length
	
	reg cumulative_abnormal_return quantity
	reg cumulative_abnormal_return length quantity
	reg cumulative_abnormal_return i.id_year length quantity
	
	reg cumulative_abnormal_return potential 
	reg cumulative_abnormal_return length potential
	reg cumulative_abnormal_return i.id_year length potential
	
	reg cumulative_abnormal_return cyclomatic
	reg cumulative_abnormal_return level
	reg cumulative_abnormal_return diversity
	