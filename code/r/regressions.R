library(modelsummary)
library(reticulate)
library(data.table)
library(fixest)

root <- '~/Dropbox/social_connectedness_education'
data <- paste0(root, '/data')
tab <- paste0(root, '/tab')
regs <- paste0(root, '/code/r')

pd <- import('pandas')

var_labels <- c(
	'log_sci' = 'Log(SCI)',
	'log_distance_miles' = 'Log(distance in miles)'
)
	
source(paste0(regs, '/reg_sci_state_educ_public.R'))
