//
// CONSOLIDATE NAMES MANUALLY
//
cd ~/Git/RegulatoryComplexity_Public/200_analysis/results/agency_feedback_letters/
import excel names_matching.xlsx, clear
	rename A company_id_dates 
	drop B 
	drop if C == "ticker_bloomberg"
	rename C ticker_bloomberg 
	rename D company_id_bloomberg
	rename E company_name
save name_entity_manual2.dta, replace


//
// FEEDBACK LETTERS
//
cd ~/Git/RegulatoryComplexity_Public/200_analysis/results/agency_feedback_letters/

// PREPARE PUBLICATION DATES
// insheet using entity_year_date.csv, delimiter(",") clear
// 	rename date str_date
// 	gen date = date(str_date, "mdy")
// 	gen date = date(str_date, "MDY")
// 	format date %td
// save entity_year_date.dta, replace

use entity_year_date.dta, clear
	sort name_entity year
	rename name_entity company_id_dates
merge m:1 company_id_dates using name_entity_manual2.dta 
	keep if _merge == 3
	drop _merge
	drop company_id_dates
	order company_name year date 
	sort company_name year date 
	duplicates drop
// 	drop year  // the naming convention for the files is a bit complicated; this is the correct date
// 	gen year2 = yofd(date)
// 	order year year2
save entity_year_date2.dta, replace


//
// PREPARE MAIN FILE
//
insheet using all_cons-count.csv, delimiter(";") nonames clear
	drop if v1 == ".DS_Store"
	split v1, p(".txt")
	drop v1
	rename v11 name_entity
	rename v3 category
	rename v4 occurrence
	
	gen one = 1
	bysort name_entity category: egen unique_count = total(one)
	
	order name_entity category occurrence
	destring occurrence, replace

	drop v2
	bysort name_entity category: egen foo = sum(occurrence)
	rename foo tot_occurence
	keep name_entity category tot_occurence unique_count
	duplicates drop
	
	split name_entity, p("-")
	drop name_entity
	gen name_entity = name_entity2 + name_entity3 
	drop name_entity2 name_entity3
	rename name_entity1 year
	destring year, replace
	order name_entity year category tot_occurence
	
	rename name_entity company_id_dates
	replace company_id_dates = "AMERICAN EXPRESS COMPANY" if company_id_dates == " AMERICAN EXPRESS COMPANY"

merge m:1 company_id_dates using name_entity_manual2.dta 
	keep if _merge == 3
	drop _merge
	
save all_cons-count.dta, replace

use all_cons-count.dta, clear	
	order company_name year company_id_dates company_id_bloomberg ticker_bloomberg
	sort  company_name year

	// correct dates first
merge m:1 company_name year using entity_year_date2.dta
	keep if _merge == 3
	drop _merge 
	
	egen i_cat = group(category)  // operators, operands, etc.
	
	gen company_name_year = company_name + str_date
	egen i_name = group(company_name_year)

	order i_name i_cat 
	xtset i_name i_cat

	drop category company_name_year
	reshape wide tot_occurence unique_count, i(i_name) j(i_cat)
	
	rename year letter_year
	order i_name company_name letter_year date
	sort i_name date
	drop i_name

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
	
	foreach var of varlist EconOp_tot-RegOp_uniq {
		replace `var' = 0 if `var' == .
	}
	
	gen length = Attributes_tot + EconOp_tot + FctWords_tot + LegalRef_tot + LogicalConn_tot + MathOp_tot + RegOp_tot + Other_tot
	gen cyclomatic = LogicalConn_tot
	gen quantity = RegOp_tot
	gen potential = 2 + EconOp_uniq
	gen level = potential / length 
	gen diversity = 2 + LogicalConn_tot + MathOp_tot + RegOp_tot
	
	gen year = yofd(date)
save agency_letters_master1.dta, replace
	sort company_name date
save letter_dates.dta, replace


// ----------------------------------------------------------------------------
//
// PREPARE BLOOMBERG DATA
//
// ----------------------------------------------------------------------------
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
// BLOOMBERG DATA
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
	