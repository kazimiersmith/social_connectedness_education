library(modelsummary)
library(reticulate)
library(data.table)
library(fixest)

root <- '~/Dropbox/social_connectedness_education'
data <- paste0(root, '/data')
tab <- paste0(root, '/tab')

pd <- import('pandas')

var_labels <- c(
	'log_sci' = 'Log(SCI)',
	'log_distance_miles' = 'Log(distance in miles)'
)
	
sci_educ <- pd$read_pickle(paste0(data, '/social_connectedness_county_demographics.pickle'))

cat('Distance only\n')
reg1 <- feols(log_sci ~ log_distance_miles |
			  user_state,
		  data = sci_educ)

cat('Distance + same state\n')
reg2 <- feols(log_sci ~ log_distance_miles +
		   same_state |
		   user_state,
	   data = sci_educ)

cat('Distance + education\n')
reg3 <- feols(log_sci ~ log_distance_miles +
		   frac_bachelors_user |
		   user_state,
	   data = sci_educ)

cat('Distance + same state + education\n')
reg4 <- feols(log_sci ~ log_distance_miles +
		   same_state +
		   frac_bachelors_user |
		   user_state,
	   data = sci_educ)

cat('Distance + same state + education + interaction\n')
reg5 <- feols(log_sci ~ log_distance_miles +
		   same_state * frac_bachelors_user |
		   user_state,
	   data = sci_educ)

cat('Distance + diff income + same state + education + interaction\n')
reg6 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * frac_bachelors_user |
		   user_state,
	   data = sci_educ)

regs <- list(reg1, reg2, reg3, reg4, reg5, reg6)

options(modelsummary_format_numeric_latex = 'plain')
out<- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ.tex'))

cat('Distance only\n')
reg1 <- feols(log_sci ~ log_distance_miles |
			  user_state,
		  data = sci_educ)

cat('Distance + same state\n')
reg2 <- feols(log_sci ~ log_distance_miles +
		   same_state |
		   user_state,
	   data = sci_educ)

cat('Distance + education\n')
reg3 <- feols(log_sci ~ log_distance_miles +
		   frac_bachelors_fr |
		   user_state,
	   data = sci_educ)

cat('Distance + same state + education\n')
reg4 <- feols(log_sci ~ log_distance_miles +
		   same_state +
		   frac_bachelors_fr |
		   user_state,
	   data = sci_educ)

cat('Distance + same state + education + interaction\n')
reg5 <- feols(log_sci ~ log_distance_miles +
		   same_state * frac_bachelors_fr |
		   user_state,
	   data = sci_educ)

reg6 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * frac_bachelors_fr |
		   user_state,
	   data = sci_educ)

regs <- list(reg1, reg2, reg3, reg4, reg5, reg6)

options(modelsummary_format_numeric_latex = 'plain')
out<- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ_fr.tex'))

cat('Distance only\n')
reg1 <- feols(log_sci ~ log_distance_miles |
			  user_county,
		  data = sci_educ)

cat('Distance + same state\n')
reg2 <- feols(log_sci ~ log_distance_miles +
		   same_state |
		   user_county,
	   data = sci_educ)

cat('Distance + education\n')
reg3 <- feols(log_sci ~ log_distance_miles +
		   diff_frac_bachelors |
		   user_county,
	   data = sci_educ)

cat('Distance + same state + education\n')
reg4 <- feols(log_sci ~ log_distance_miles +
		   same_state +
		   diff_frac_bachelors |
		   user_county,
	   data = sci_educ)

cat('Distance + same state + education + interaction\n')
reg5 <- feols(log_sci ~ log_distance_miles +
		   same_state * diff_frac_bachelors |
		   user_county,
	   data = sci_educ)

reg6 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_bachelors |
		   user_county,
	   data = sci_educ)

regs <- list(reg1, reg2, reg3, reg4, reg5, reg6)

options(modelsummary_format_numeric_latex = 'plain')
out<- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ_diff.tex'))

reg1 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * frac_any_college_user +
		   same_state * frac_enrolled_public_college_user |
		   user_state,
	   data = sci_educ)

reg2 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * frac_any_college_user +
		   same_state * frac_any_college_public_est_user |
		   user_state,
	   data = sci_educ)

reg3 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * frac_bachelors_user +
		   same_state * frac_bachelors_public_est_user |
		   user_state,
	   data = sci_educ)

reg4 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * frac_any_college_user +
		   same_state * frac_coll_coll_public_est_user |
		   user_state,
	   data = sci_educ)

reg5 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * frac_bachelors_user +
		   same_state * frac_bach_bach_public_est_user |
		   user_state,
	   data = sci_educ)

regs <- list(reg1, reg2, reg3, reg4, reg5)

options(modelsummary_format_numeric_latex = 'plain')
out<- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ_public'))

reg1 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_enrolled_public_college |
		   user_county,
	   data = sci_educ)

reg2 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_any_college_public_est |
		   user_county,
	   data = sci_educ)

reg3 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_bachelors_public_est |
		   user_county,
	   data = sci_educ)

reg4 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_coll_coll_public_est |
		   user_county,
	   data = sci_educ)

reg5 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
		   same_state * diff_frac_bach_bach_public_est |
		   user_county,
	   data = sci_educ)

regs <- list(reg1, reg2, reg3, reg4, reg5)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ_public_diff'))

reg1 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college +
		   same_state * diff_frac_enrolled_public_college |
		   user_county,
	   data = sci_educ)

reg2 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college +
		   same_state * diff_frac_coll_coll_public_est |
		   user_county,
	   data = sci_educ)

reg3 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_bachelors +
		   same_state * diff_frac_bach_bach_public_est |
		   user_county,
	   data = sci_educ)

regs = list(reg1, reg2, reg3)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   output = 'latex_tabular')

cat(out, file = paste0(tab, '/reg_sci_state_educ_public_diff_control_college'))

