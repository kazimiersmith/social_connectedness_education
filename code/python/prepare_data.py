from pathlib import Path
import pandas as pd
import numpy as np

root = Path('~/Dropbox/social_connectedness_education').expanduser()
data = root / 'data'
raw = data / 'raw'

rename = {'S1501_C01_001E': 'pop_18_24',
        'S1501_C01_004E': 'pop_18_24_some_college',
        'S1501_C01_005E': 'pop_18_24_bachelors',
        'S1501_C01_006E': 'pop_25_plus',
        'S1501_C01_010E': 'pop_25_plus_some_college',
        'S1501_C01_011E': 'pop_25_plus_associates',
        'S1501_C01_012E': 'pop_25_plus_bachelors',
        'S1501_C01_013E': 'pop_25_plus_graduate',
        'S1901_C01_012E': 'median_income',
        'S1401_C04_008E': 'perc_enrolled_public_college'}

cols = list(rename.keys())

county_educ = pd.read_csv(raw / 'acs_5year_2021_county_education.csv')
county_educ = county_educ.drop(0)

county_income = pd.read_csv(raw / 'acs_5year_2021_county_income.csv')
county_income = county_income.drop(0)

county_school_enrollment = pd.read_csv(raw / 'acs_5year_2021_county_school_enrollment.csv')
county_school_enrollment = county_school_enrollment.drop(0)

county_demo = pd.merge(left = county_educ,
        right = county_income,
        on = 'GEO_ID',
        how = 'inner')

county_demo = pd.merge(left = county_demo,
        right = county_school_enrollment,
        on = 'GEO_ID',
        how = 'inner')

county_demo = county_demo[['GEO_ID'] + cols]
county_demo = county_demo.rename(columns = rename)

county_demo['state_county_fips'] = county_demo['GEO_ID'].apply(lambda g: g.split('US')[1])
county_demo['county'] = county_demo['state_county_fips'].apply(lambda g: int(g))
county_demo['state'] = county_demo['state_county_fips'].apply(lambda g: int(g[:2]))
county_demo = county_demo.drop(columns = ['GEO_ID', 'state_county_fips'])

# Lose 1 county here
county_demo = county_demo[county_demo['median_income'] != '-']

# Lose 11 counties here
county_demo = county_demo[county_demo['perc_enrolled_public_college'] != '-']

# Convert all values in county_demo to numeric
for col in county_demo.columns:
    county_demo[col] = pd.to_numeric(county_demo[col])

county_demo['total_pop'] = county_demo['pop_18_24'] + county_demo['pop_25_plus']

county_demo['pop_18_24_any_college'] = county_demo['pop_18_24_some_college'] + county_demo['pop_18_24_bachelors']

county_demo['pop_25_plus_any_college'] = county_demo['pop_25_plus_some_college']
county_demo['pop_25_plus_any_college'] += county_demo['pop_25_plus_associates']
county_demo['pop_25_plus_any_college'] += county_demo['pop_25_plus_bachelors']
county_demo['pop_25_plus_any_college'] += county_demo['pop_25_plus_graduate']

county_demo['total_pop_any_college'] = county_demo['pop_18_24_any_college'] + county_demo['pop_25_plus_any_college']
county_demo['frac_any_college'] = county_demo['total_pop_any_college'] / county_demo['total_pop']

county_demo['frac_enrolled_public_college'] = county_demo['perc_enrolled_public_college'] / 100

county_demo = county_demo[['county',
    'frac_any_college',
    'median_income',
    'frac_enrolled_public_college']]

sc_county = pd.read_csv(raw / 'social_connectedness_county_county_october_2021.tsv', sep = '\t')
sc_county['user_state_county_fips'] = sc_county['user_loc'].apply(lambda g: str(g).zfill(5))
sc_county['user_county'] = sc_county['user_state_county_fips'].apply(lambda g: int(g))
sc_county['user_state'] = sc_county['user_state_county_fips'].apply(lambda g: int(g[:2]))
sc_county['fr_state_county_fips'] = sc_county['fr_loc'].apply(lambda g: str(g).zfill(5))
sc_county['fr_county'] = sc_county['fr_state_county_fips'].apply(lambda g: int(g))
sc_county['fr_state'] = sc_county['fr_state_county_fips'].apply(lambda g: int(g[:2]))
sc_county = sc_county[['user_state', 'user_county', 'fr_state', 'fr_county', 'scaled_sci']]

# Merge user county demographics
sci_county = pd.merge(left = sc_county,
        right = county_demo,
        left_on = 'user_county',
        right_on = 'county',
        how = 'inner')

# Merge friend county demographics
sci_county = pd.merge(left = sci_county,
        right = county_demo,
        left_on = 'fr_county',
        right_on = 'county',
        how = 'inner',
        suffixes = ('_user', '_fr'))

# Merge in county distances
county_distances = pd.read_csv(raw / 'county_county_distance_miles_2010_nber.csv')
sci_county = pd.merge(left = sci_county,
        right = county_distances,
        left_on = ['user_county', 'fr_county'],
        right_on = ['county1', 'county2'],
        how = 'inner')

sci_county = sci_county.drop(columns = ['county1', 'county2'])
sci_county = sci_county.rename(columns = {'mi_to_county': 'distance_miles'})

sci_county['same_state'] = sci_county.apply(lambda r: 1 if r['user_state'] == r['fr_state'] else 0, axis = 1)
sci_county['log_sci'] = np.log10(sci_county['scaled_sci'])
sci_county['log_distance_miles'] = np.log10(sci_county['distance_miles'])
sci_county['diff_frac_any_college'] = sci_county['frac_any_college_user'] - sci_county['frac_any_college_fr']
sci_county['diff_income'] = sci_county['median_income_user'] - sci_county['median_income_fr']
sci_county['diff_frac_enrolled_public_college'] = sci_county['frac_enrolled_public_college_user'] - sci_county['frac_enrolled_public_college_fr']

ec_county = pd.read_csv(raw / 'social_capital_county.csv')[['county', 'ec_county']]

# Left merge here since I don't need economic connectedness for all analysis
connectedness_county = pd.merge(left = sci_county,
        right = ec_county,
        left_on = 'user_county',
        right_on = 'county',
        how = 'left')

connectedness_county.to_pickle(data / 'connectedness_county.pickle')
