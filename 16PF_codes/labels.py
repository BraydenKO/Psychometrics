from reader import df
def get_columns(factor):
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
    'A': 'Warmth',
    'B': 'Reasoning',
    'C': 'Emotional Stability',
    'D': 'Dominance',
    'E': 'Liveliness',
    'F': 'Dutifulness',
    'G': 'Social Assertiveness',
    'H': 'Sensitivity',
    'I': 'Vigilance',
    'J': 'Abstractedness',
    'K': 'Privateness',
    'L': 'Apprehension',
    'M': 'Openmindedness',
    'N': 'Independance',
    'O': 'Perfectionism',
    'P': 'Tension'
}

factors ={
    "Warmth":get_columns("Warmth"),
    "Reasoning":get_columns("Reasoning"),
    "Emotional Stability":get_columns("Emotional Stability"),
    "Dominance":get_columns("Dominance"),
    "Liveliness":get_columns("Liveliness"),
    "Dutifulness":get_columns("Dutifulness"),
    "Social Assertiveness":get_columns("Social Assertiveness"),
    "Sensitivity":get_columns("Sensitivity"),
    "Vigilance":get_columns("Vigilance"),
    "Abstractedness":get_columns("Abstractedness"),
    "Privateness":get_columns("Privateness"),
    "Apprehension":get_columns("Apprehension"),
    "Openmindedness":get_columns("Openmindedness"),
    "Independance":get_columns("Independance"),
    "Perfectionism":get_columns("Perfectionism"),
    "Tension":get_columns("Tension")
}
# When fixing the csv, this is used to flip
# responses to flipped questions
flips = {
    "A" : [8,10],
    "B" : [9,13],
    "C" : [6,10],
    "D" : [7,10],
    "E" : [7,10],
    "F" : [6,10],
    "G" : [6,10],
    "H" : [7,10],
    "I" : [7,10],
    "J" : [8,10],
    "K" : [6,10],
    "L" : [8,10],
    "M" : [6,10],
    "N" : [8,10],
    "O" : [6,10],
    "P" : [8,9]
}