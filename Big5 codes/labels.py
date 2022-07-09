# Each factor has 10 questions
factors = {
  "EXT" : [0,9],
  "EST" : [10,19],
  "AGR" : [20,29],
  "CSN" : [30, 39],
  "OPN" : [40,49]
}

titles = {
  "EXT" : "Extraversion",
  "EST" : "Neuroticism",
  "AGR" : "Agreeableness",
  "CSN" : "Conscientousness",
  "OPN" : "Openness"
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