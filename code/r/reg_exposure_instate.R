colleges <- pd$read_pickle(paste0(data, '/colleges.pickle'))

reg1 <- feols(log_exposure ~ frac_freshmen_instate |
			  college_state,
		  data = colleges)

reg2 <- feols(log_exposure ~ frac_freshmen_instate +
			  mobility_rate |
			  college_state,
		  data = colleges)

reg3 <- feols(log_exposure ~ frac_freshmen_instate +
			  mobility_rate +
			  clustering |
			  college_state,
		  data = colleges)

reg4 <- feols(log_exposure ~ frac_freshmen_instate +
			  mobility_rate +
			  clustering +
			  volunteering_rate |
			  college_state,
		  data = colleges)

regs = list(reg1, reg2, reg3, reg4)

options(modelsummary_format_numeric_latex = 'plain')
out <- modelsummary(regs,
				   stars = TRUE,
				   gof_omit = 'Adj|Within|AIC|BIC|RMSE',
				   output = paste0(tab, '/reg_exposure_instate.tex'))
