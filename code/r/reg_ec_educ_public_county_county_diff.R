connectedness_county <- pd$read_pickle(paste0(data, '/connectedness_county.pickle'))

reg1 <- feols(diff_ec ~ log_distance_miles +
			  diff_income +
			  same_state |
			  user_county,
		  data = connectedness_county)

reg2 <- feols(diff_ec ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college |
			  user_county,
		  data = connectedness_county)

reg3 <- feols(diff_ec ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_enrolled_public_college |
			  user_county,
		  data = connectedness_county)

reg4 <- feols(diff_ec ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college +
			  same_state * diff_frac_enrolled_public_college |
			  user_county,
		  data = connectedness_county)

regs = list(reg1, reg2, reg3, reg4)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_ec_educ_public_county_county_diff.tex'))
