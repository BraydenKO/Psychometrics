# Each factor has 10 questions
factors = {
  "E" : [7,16],
  "N" : [17,26],
  "A" : [27,36],
  "C" : [37, 46],
  "O" : [47,56]
}

titles = {
  "E" : "Extraversion",
  "N" : "Neuroticism",
  "A" : "Agreeableness",
  "C" : "Conscientousness",
  "O" : "Openness"
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
