import csv

accuracy = list()
precision = list()
x_axis = list()
for i in range(-20, 25, 5):

    with open("../../Results_2/Quad/Robustness/White_Noise/"+str(i)+".csv", 'r') as csvFile:
        reader = list(csv.reader(csvFile, delimiter=','))
        result = [i[3] for i in reader]
        true_positive = result.count("True Positive")
        # true_negative = result.count("True Negative")
        false_positive = result.count("False Positive")
        false_negative = result.count("False Negative")
        if true_positive + false_positive == 0:
            p = 0
        else:
            p = round(true_positive / (true_positive + false_positive), 3)
        a = round(true_positive / (true_positive + false_negative + false_positive), 3)
        accuracy.append(a)
        precision.append(p)
        x_axis.append(i)
row = ["White_Noise", "Accuracy", "Precision"]
result_path = "../../Results_2/quad_white_noise.csv"
with open(result_path, 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()
count = 0
for i in x_axis:
    row1 = [x_axis[count], accuracy[count], precision[count]]
    with open(result_path, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row1)
    csvFile.close()
    count += 1
