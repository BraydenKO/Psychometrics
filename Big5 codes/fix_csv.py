from reader import df
'''
Some questions are have flipped answers:
For some questions, a 5 means high in that factor
for others, a 5 means low in that factor
{labels.flips} records which questions a 5 means low
and should be flipped.
'''

def fix_flips(df, save = True, doprint = True):
  """Some columns should be flipped, this fixes that.
  
  df: pandas DataFrame
  save: Whether to save to a new csv r"data/Big5_fix.csv (default True) (bool)
  doprint: Whether to print which columns were flipped (defulat True) (bool)
  """
  from labels import flips
  def flip_answer(answer, middle):
    """Flips an answer (int) across some middle value (int)."""
    return (middle-answer) + middle 
    
  # an item in flips looks like ("EXT", [1,1,0,0...])
  for key, value in flips.items():
      for idx, i in enumerate(value):
        if i == 0:
          df[f"{key}{idx+1}"] = flip_answer(df[f"{key}{idx+1}"], 3)
          if doprint: print(f"Flipped {key}{idx+1}")

  # Save the fixed file
  # usually you want this to run, hence by default it does.
  if save:
      df.to_csv(r"data/Big5_fix.csv", sep = "\t", index = False)
  else:
    return df
    
if __name__ == "__main__":
  fix_flips(df, save=True, doprint=True)