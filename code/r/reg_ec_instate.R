ec_college <- pd$read_pickle(paste0(data, '/college_instate_ec.pickle'))

reg1 <- feols(log_ec ~ frac_freshmen_instate |
			  college_state,
		  data = ec_college)

reg2 <- feols(log_ec ~ frac_freshmen_instate +
			  total_freshmen |
			  college_state,
		  data = ec_college)

regs = list(reg1, reg2)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_ec_instate.tex'))
