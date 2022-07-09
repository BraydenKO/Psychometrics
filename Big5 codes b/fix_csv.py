from reader import df
'''
Some questions are have flipped answers:
For some questions, a 5 means high in that factor
for others, a 5 means low in that factor
{labels.flips} records which questions a 5 means low
and should be flipped.
'''

def flip_answer(answer, middle):
    return (middle-answer) + middle 

def fix_flips(df, save = True):
    from labels import flips

    # an item in flips looks like ("E", [1,1,0,0...])
    for key, value in flips.items():
        for idx, i in enumerate(value):
          if i == 0:
            df[f"{key}{idx+1}"] = flip_answer(df[f"{key}{idx+1}"], 3)
            print(f"Flipped {key}{idx+1}")

    # Save the fixed file
    # usually you want this to run, hence by default it does.
    if save:
        df.to_csv(r"data/Big5_b_fix.csv", sep = "\t", index = False)

fix_flips(df)