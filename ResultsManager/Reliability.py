import csv
with open("../../../../Audio A-Z/Results/Reliability/Panako/Reliability.csv", 'r') as csvFile:
        reader = list(csv.reader(csvFile, delimiter=','))
        result = [i[3] for i in reader]
        true_negative = result.count("True Negative")
        false_positive = result.count("False Positive")
        print(true_negative/(true_negative+false_positive))