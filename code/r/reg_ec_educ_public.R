ec_county <- pd$read_pickle(paste0(data, '/ec_education_county.pickle'))

reg1 <- feols(log_ec ~ frac_any_college |
			  state,
		  data = ec_county)

reg2 <- feols(log_ec ~ frac_any_college +
			  median_income |
			  state,
		  data = ec_county)

reg3 <- feols(log_ec ~ frac_any_college +
			  median_income +
			  frac_enrolled_public_college |
			  state,
		  data = ec_county)

regs = list(reg1, reg2, reg3)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_ec_educ_public.tex'))
