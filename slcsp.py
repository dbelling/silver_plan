import pandas as pd
import csv

plans = pd.read_csv('plans.csv', header=0)
zips = pd.read_csv('zips.csv', header=0, dtype={'zipcode':'str'})
# Join on (rate area, state) tuple for easier mapping to plan zipcodes.
zip_plans = pd.merge(plans, zips, on=['rate_area', 'state'])
silver_plans = zip_plans.loc[zip_plans['metal_level'] == 'Silver']
missing_zipcodes = []

def analyze(zipcodes):
    missing_states = zips.loc[zips['zipcode'].isin(zipcodes)].state.unique()
    covered_states = pd.Index(plans['state'].unique())
    covered_zips = pd.Index(zips['state'].unique())
    print('Silver plan coverage data missing for these zipcodes: ' + str(zipcodes))
    print('Silver plan coverage data missing for these states: ' + str(missing_states))
    print('State plan coverage lacking zipcodes: ' + str(covered_states.difference(covered_zips)))
    print('Zipcode plan coverage lacking state data ' + str(covered_zips.difference(covered_states)))

if __name__ == "__main__":
    with open('slcsp.csv', 'r') as slcsp_file, open('results.csv', 'w') as results_file:
        reader = csv.reader(slcsp_file)
        writer = csv.writer(results_file)
        # iterate over SLCSP CSV
        for index, row in enumerate(reader):
            regional_plans = silver_plans.loc[silver_plans['zipcode'] == row[0]]
            # no plans found
            if len(regional_plans.index) <= 1:
                missing_zipcodes.append(row[0])
            # find second lowest cost silver plan - drop duplicate values
            else:
                unique_plans = regional_plans.drop_duplicates('rate')
                sorted_plans = unique_plans.sort_values(by='rate', kind='quicksort')
                row[1] = regional_plans.iloc[1].rate
            writer.writerow(row)
    print('Results written to results.csv')
    analyze(missing_zipcodes)
