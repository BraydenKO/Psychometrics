16 Personality Factors (Cattell)

reader.py:
    
    Simply reads reads the csv from data.csv into a pandas dataframe
  
labels.py:
    
    Holds information on labels in from the data set
  
fix_csv.py:
    
    The dataset when originally downloaded has all of the labels and data in one column.
    This script splits up each answer and question into their own cell (as they should be!).
        Note: As of now, this script will take a while to run.
     
gender.py:
    
    Analyzes and compares men's and women's average response to each labelled question.
    One might find that women, on average, score 0.18 higher in sensitivity than man.

country.py:

    Graphs traits based on countries with the top most responses. Then in the terminal is printed
    the greatest difference between graphs.
