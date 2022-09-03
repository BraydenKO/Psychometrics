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
  "E" : "Extraversion",
  "N" : "Neuroticism",
  "A" : "Agreeableness",
  "C" : "Conscientousness",
  "O" : "Openness"
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
  "E" : [1,0,1,0,1,0,1,0,1,0],
  "N" : [1,0,1,0,1,1,1,1,1,1],
  "A" : [0,1,0,1,0,1,0,1,1,1],
  "C" : [1,0,1,0,1,0,1,0,1,1],
  "O" : [1,0,1,0,1,0,1,1,1,1]
}

# Used in race.py
race_label = {
  1  : "Mixed",
  2  : "Arctic",
  3  : "Caucasian (European)",
  4  : "Caucasian (Indian)",
  5  : "Caucasian (Middle East)",
  6  : "Caucasian (North African, Other)",
  7  : "Indigenous Australian",
  8  : "Native American",
  9  : "North East Asian",
  10 : "Pacific",
  11 : "South East Asian",
  12 : "West African",
  13 : "Other"
}