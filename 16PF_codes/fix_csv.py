from reader import df, pd
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

    # an item in flips looks like (A, [8,10])
    for key, value in flips.items():
        # go through the flipped columns (inclusive)
        for q in range(value[0],value[1]+1):
            # flip all values of that column
            df[f"{key}{q}"] = flip_answer(df[f"{key}{q}"], 3)

    # Save the fixed file
    # usually you want this to run, hence by default it does.
    if save:
        df.to_csv(r"1_Mentorship\data\16pf_fix.csv", sep = "\t", index = False)

fix_flips(df)