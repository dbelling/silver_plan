import pandas as pd

results = pd.read_csv('slcsp.csv', header=0, dtype={'zipcode': 'string'})
plans = pd.read_csv('plans.csv', header=0)
zips = pd.read_csv('zips.csv', header=0, dtype={'zipcode': 'string', 'state': 'string'})
silver_plans = plans.loc[plans['metal_level'] == 'Silver'].sort_values(by='rate', kind='mergesort')

class RateAreaTuple:
    def __init__(self, state, rate_area):
        self.state = state
        self.rate_area = rate_area

def rate_area_from_zip(zipcode):
    state = zips.loc[zips['zipcode'] == zipcode]
    if len(state.index) == 1:
      return RateAreaTuple(state.iloc[0]['state'], state.iloc[0]['rate_area'])
    else:
      rate_areas = []
      for area, zip_code in state.iterrows():
          rate_areas.append(RateAreaTuple(zip_code['state'], zip_code['rate_area']))
      return rate_areas

def slcp_from_silver_plans(rate_area):
    if isinstance(rate_area, list):
        print(rate_area[0].state)
    else:
        relevant_plans = silver_plans.loc[(silver_plans['state'] == rate_area.state) & (silver_plans['rate_area'] == rate_area.rate_area)]
        # return relevant_plans.iloc[1]['rate']

if __name__ == "__main__":
    # Iterate over results CSV
    for index, row in results.iterrows():
      # find zip codes without a rate
      if pd.isnull(row['rate']):
        rate_area = rate_area_from_zip(row['zipcode'])
        slcsp = slcp_from_silver_plans(rate_area)
        if rate_area:
            print(slcp_from_silver_plans(rate_area))
        # Unique zip code - county
        if len(state.index) == 1:
          rate_area = state.iloc[0]['rate_area']
          state = state.iloc[0]['state']
          relevant_plans = silver_plans.loc[(silver_plans['state'] == state) & (silver_plans['rate_area'] == rate_area)]
        # Ambiguous zip code- county assignment.
        else:
            rate_area = state.iloc[0]['rate_area']
            state = state.iloc[0]['state']
            relevant_plans = silver_plans.loc[(silver_plans['state'] == state) & (silver_plans['rate_area'] == rate_area)]
            print(relevant_plans)
