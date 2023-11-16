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
    'state',
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
sci_county = sci_county.drop(columns = ['county_user', 'county_fr', 'state_user', 'state_fr'])

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

ec_county = pd.read_csv(raw / 'social_capital_county.csv',
        usecols = ['county', 'ec_county'])
ec_county['log_ec'] = np.log10(ec_county['ec_county'])

# Left merge since I don't need economic connectedness for all analysis
connectedness_county = pd.merge(left = sci_county,
        right = ec_county,
        left_on = 'user_county',
        right_on = 'county',
        how = 'left')

connectedness_county = pd.merge(left = connectedness_county,
        right = ec_county,
        left_on = 'fr_county',
        right_on = 'county',
        how = 'left',
        suffixes = ('_user', '_fr'))
connectedness_county = connectedness_county.drop(columns = ['county_user', 'county_fr'])

connectedness_county['diff_ec'] = connectedness_county['ec_county_user'] - connectedness_county['ec_county_fr']

connectedness_county.to_pickle(data / 'connectedness_county.pickle')

# County level data
ec_county = pd.merge(left = ec_county,
        right = county_demo,
        on = 'county',
        how = 'inner')

ec_county.to_pickle(data / 'ec_education_county.pickle')

# ----- College level data -----
# Economic connectedness of colleges
ec_college = pd.read_csv(raw / 'social_capital_college.csv',
        usecols = ['college',
            'college_name',
            'ec_own_ses_college',
            'exposure_own_ses_college',
            'bias_own_ses_college',
            'clustering_college',
            'support_ratio_college',
            'volunteering_rate_college'])
ec_college = ec_college.rename(columns = {'ec_own_ses_college': 'ec_college',
    'college': 'college_opeid',
    'exposure_own_ses_college': 'exposure',
    'bias_own_ses_college': 'friending_bias',
    'clustering_college': 'clustering',
    'support_ratio_college': 'support_ratio',
    'volunteering_rate_college': 'volunteering_rate'})

ec_college['log_ec'] = np.log10(ec_college['ec_college'])
ec_college['log_exposure'] = np.log10(ec_college['exposure'])
ec_college['log_friending_bias'] = np.log10(1 - ec_college['friending_bias'])

# College enrollment data to calculate fraction of instate freshmen
enrollment_rename = {'UNITID': 'college_unitid',
        'EFCSTATE': 'freshmen_residence_state',
        'EFRES01': 'num_freshmen'}

college_enrollment = pd.read_csv(raw / 'college_enrollment_state_residence_2018.csv',
        usecols = enrollment_rename.keys())
college_enrollment = college_enrollment.rename(columns = enrollment_rename)

chars_rename = {'UNITID': 'college_unitid',
        'OPEID': 'college_opeid',
        'FIPS': 'college_state'}

college_chars = pd.read_csv(raw / 'college_characteristics_2018.csv',
        encoding = 'latin_1',
        usecols = chars_rename.keys())
college_chars = college_chars.rename(columns = chars_rename)

college_enrollment = pd.merge(left = college_enrollment,
        right = college_chars,
        on = 'college_unitid',
        how = 'inner')

# State code 99 is total freshmen
total_freshmen = college_enrollment[college_enrollment['freshmen_residence_state'] == 99][['college_unitid', 'num_freshmen']]
total_freshmen = total_freshmen.rename(columns = {'num_freshmen': 'total_freshmen'})
college_enrollment = pd.merge(left = college_enrollment,
        right = total_freshmen,
        on = 'college_unitid',
        how = 'inner')

college_enrollment = college_enrollment[college_enrollment['freshmen_residence_state'] == college_enrollment['college_state']]
college_enrollment['frac_freshmen_instate'] = college_enrollment['num_freshmen'] / college_enrollment['total_freshmen']

college_instate_ec = pd.merge(left = college_enrollment,
        right = ec_college,
        on = 'college_opeid',
        how = 'inner')

# College mobility rate from Chetty et al.
superopeid_opeid_crosswalk = pd.read_csv(raw / 'superopeid_opeid_crosswalk.csv',
        usecols = ['super_opeid', 'opeid'])
superopeid_opeid_crosswalk['opeid'] = superopeid_opeid_crosswalk['opeid'] * 100

colleges = pd.merge(left = college_instate_ec,
        right = superopeid_opeid_crosswalk,
        left_on = 'college_opeid',
        right_on = 'opeid',
        how = 'inner')

college_mobility = pd.read_csv(raw / 'college_mobility_rates.csv',
        usecols = ['super_opeid', 'mr_kq5_pq1'])
college_mobility = college_mobility.rename(columns = {'mr_kq5_pq1': 'mobility_rate'})

colleges = pd.merge(left = colleges,
        right = college_mobility,
        on = 'super_opeid',
        how = 'inner')
colleges = colleges.drop(columns = ['freshmen_residence_state',
    'college_opeid',
    'college_name',
    'super_opeid',
    'opeid'])

colleges.to_pickle(data / 'colleges.pickle')
