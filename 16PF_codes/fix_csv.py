from reader import df, pd

def flip_answer(answer, middle):
    return (middle-answer) + middle 



def fix_flips(df, save = True):
    from labels import flips

    for key, value in flips.items():
        for q in range(value[0],value[1]+1):
            df[f"{key}{q}"] = flip_answer(df[f"{key}{q}"], 3)

    if save:
        df.to_csv(r"Docs\16PF/data_fix.csv", sep = "\t", index = False)


fix_flips(df)