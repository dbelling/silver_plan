import pandas as pd

results = pd.read_csv('slcsp.csv', header=0, dtype={'zipcode':'str'})
plans = pd.read_csv('plans.csv', header=0)
zips = pd.read_csv('zips.csv', header=0, dtype={'zipcode':'str'})
silver_plans = pd.merge(plans, zips, on=['rate_area', 'state'])
silver_plans = silver_plans.loc[silver_plans['metal_level'] == 'Silver'].sort_values(by='rate', kind='mergesort')

if __name__ == "__main__":
    # iterate over results CSV
    for index, row in results.iterrows():
      # find zip codes currently without a slcsp rate
      if pd.isnull(row['rate']):
          regional_plans = silver_plans.loc[silver_plans['zipcode'] == row['zipcode']]
          if len(regional_plans.index) < 1:
              print("No silver plans available for " + row['zipcode'])
          else:

        #   try:
        #       silver_plans.loc[silver_plans['zipcode'] == zipcode]
        #   except:
        #       print("No silver plan available for %(zipcode)")
