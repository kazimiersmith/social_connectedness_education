sci_educ <- pd$read_pickle(paste0(data, '/sci_education_county_county.pickle'))

reg1 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state |
			  user_county,
		  data = sci_educ)

reg2 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college |
			  user_county,
		  data = sci_educ)

reg3 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_enrolled_public_college |
			  user_county,
		  data = sci_educ)

reg4 <- feols(log_sci ~ log_distance_miles +
			  diff_income +
			  same_state * diff_frac_any_college +
			  same_state * diff_frac_enrolled_public_college |
			  user_county,
		  data = sci_educ)

regs = list(reg1, reg2, reg3, reg4)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_sci_state_educ_public.tex'))
