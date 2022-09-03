from reader import df
'''
Some questions are have flipped answers:
For some questions, a 5 means high in that factor
for others, a 5 means low in that factor
{labels.flips} records which questions a 5 means low
and should be flipped.
'''

print(df)
def flip_answer(answer, middle):
  """Flips an answer (int) across some middle value (int)."""
  return (middle-answer) + middle 

def fix_flips(df, save = True):
  """
  If labels.py says a column should be flipped,
  flip all values in that column using flip_anser(answer, middle).

  df: pandas DataFrame
  save: whether you want to test the function or actually save to r"data/16PF_fix.csv"
  """
  from labels import flips

  # an item in flips looks like (A, [8,10])
  for key, value in flips.items():
      # go through the flipped columns (inclusive)
      for q in range(value[0],value[1]+1):
          # flip all values of that column
          df[f"{key}{q}"] = flip_answer(df[f"{key}{q}"], 3)
          print(f"Flipped {key}{q}")

  # Save the fixed file
  # usually you want this to run, hence by default it does.
  if save:
      df.to_csv(r"data/16PF_fix.csv", sep = "\t", index = False)


fix_flips(df)