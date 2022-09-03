'''
Looks at how factors may correlate with eachother
'''
from reader import df, pd
from labels import factors

def organize_data(df):
  """
  Organizes data to get rid of unused columns
  and rows with invalid data (na, 0, 6).

  df: pandas DataFrame

  returns:
  data: Organized and normalized dataset (numpy array)
  """
  from sklearn.preprocessing import MinMaxScaler
  # Collects just questionaire data
  ranges = list(factors.values())
  data = df.iloc[:,ranges[0][0]:ranges[-1][-1]]

  # Deletes people with NaN, 0, or a 6 in their answer
  # 0 or 6 means a skipped question
  data = data.dropna()
  data = data[data.ne(0).all(1)]
  data = data[data.ne(6).all(1)]

  # Scale data between 0 and 1
  # Note: I dont know how useful this is considering that
  # All the data is at the same scale 1-5 anyways but I 
  # See people do this all the time and it can't hurt.
  scaler = MinMaxScaler(feature_range=(0,1))
  data = scaler.fit_transform(data)

  data = pd.DataFrame(data, columns=df.columns[ranges[0][0]:ranges[-1][-1]])
  return data

def group_features(data, method = 'spearman'):
  """Find how columns correlate.
  
  data: Dataset (2d array)
  method: Method used to find correlations ('pearson', 'kendall', 'spearman') (str)
  
  returns:
  out: A list showing how columns correlate
  """
  corrs = data.corr(method = method)
  # Create test, a dictionary of each col paired to correlated features
  test = {}
  for row in corrs:
    test[row] = []
    for col in corrs:
      cell = corrs.loc[row,col]
      if abs(cell) >= 0.5:
        test[row].append(col)

  test = list(test.values())

  # Group together groups of correlated features that share a feature
  out = []
  while len(test)>0:
      first, *rest = test
      first = set(first)

      lf = -1
      while len(first)>lf:
          lf = len(first)

          rest2 = []
          for r in rest:
              if len(first.intersection(set(r)))>0:
                  first |= set(r)
              else:
                  rest2.append(r)     
          rest = rest2

      out.append(first)
      test = rest
  return out



if __name__ == "__main__":
  data = organize_data(df)
  corrs = group_features(data)
  for group in corrs:
    if len(group) > 1:
      group = list(group)
      group.sort()
      print(group)
  #with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
  #    print(corrs.loc['M1':'M10', :])

