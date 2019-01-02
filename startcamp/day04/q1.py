scores = {
    'a':{
        '수학':80,
        '국어':90,
        '음악':70
    },
    'b': {
        '수학':80,
        '국어':90,
        '음악':100
    }
}

#print(score.keys())
#print(score['a'].values())

#total = []
#number = []
#for key in score.keys():
#    total.append(sum(score[key].values()))
#    number.append(len(score[key].values()))
#print(number)

#average = []
#for i in range(0, len(total)):
#    average.append(total[i]/number[i])
#print(average)

#print(sum(average)/len(average))


total = 0
number = 0
for key in scores.keys():
    total += (sum(scores[key].values()))
    number += (len(scores[key].values()))

print(total/number)


total_score = 0
count = 0
for person_score in scores.values():
    for subject_score in person_score.values():
        total_score += subject_score
        count += 1
print(total_score / count)