colleges <- pd$read_pickle(paste0(data, '/colleges.pickle'))

reg1 <- feols(log_ec ~ frac_freshmen_instate |
			  college_state,
		  data = colleges)

reg2 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate |
			  college_state,
		  data = colleges)

reg3 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate +
			  total_freshmen |
			  college_state,
		  data = colleges)

reg4 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate +
			  total_freshmen +
			  log_exposure |
			  college_state,
		  data = colleges)

reg5 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate +
			  total_freshmen +
			  log_friending_bias |
			  college_state,
		  data = colleges)

reg6 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate +
			  total_freshmen +
			  log_exposure +
			  clustering +
			  volunteering_rate |
			  college_state,
		  data = colleges)

reg7 <- feols(log_ec ~ frac_freshmen_instate +
			  mobility_rate +
			  total_freshmen +
			  log_friending_bias +
			  clustering +
			  volunteering_rate |
			  college_state,
		  data = colleges)

regs = list(reg3, reg4, reg5, reg6, reg7)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_ec_instate.tex'))
