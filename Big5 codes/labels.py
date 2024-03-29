'''
Countains labels and other import data
'''
from reader import df
def get_columns(factor):
  """For a given factor find the column indeces of that factor.
  
  factor: Name of factor to find columns of (str)
  """
  indeces = []
  for key,value in titles.items():
      if value == factor:
          abbr = key
          break
  else:
      raise Exception(f"Factor {factor} not found in titles")

  for idx,col in enumerate(df.columns):
      if col == abbr+"1":
          indeces.append(idx)
          break
  else:
      raise Exception(f"Column {abbr}1 not found in df.columns")

  for idx,col in enumerate(df.columns[idx+1:]):
      if col[:len(abbr)] != abbr:
          indeces.append(idx+indeces[0])
          return indeces
  indeces.append(len(df.columns)-1)
  return indeces

titles = {
  "EXT" : "Extraversion",
  "EST" : "Neuroticism",
  "AGR" : "Agreeableness",
  "CSN" : "Conscientousness",
  "OPN" : "Openness"
}

# Each factor has 10 questions
factors = {
  "Extraversion" : get_columns("Extraversion"),
  "Neuroticism" : get_columns("Neuroticism"),
  "Agreeableness" : get_columns("Agreeableness"),
  "Conscientousness" : get_columns("Conscientousness"),
  "Openness" : get_columns("Openness")
}
# 1 means don't flip, 0 means do flips
# Each element refers to the question of that index
flips = {
  "EXT" : [1,0,1,0,1,0,1,0,1,0],
  "EST" : [1,0,1,0,1,1,1,1,1,1],
  "AGR" : [0,1,0,1,0,1,0,1,1,1],
  "CSN" : [1,0,1,0,1,0,1,0,1,1],
  "OPN" : [1,0,1,0,1,0,1,1,1,1]
}
