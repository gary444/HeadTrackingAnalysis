import numpy as np
import csv
from scipy.stats import ttest_ind


def test_significance_of_values_in_csv(filename):
	v1=[]
	v2=[]

	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		for row in reader:
			v1.append(float(row[0]))
			v2.append(float(row[1]))

		res = ttest_ind(v1, v2)
		print("From file: " + filename)
		print(res)


# test_significance_of_values_in_csv('data/head_movement_speed.csv')
# test_significance_of_values_in_csv('data/head_rotation_speed.csv')


test_significance_of_values_in_csv('data/head_movement_speed_no_outliers.csv')
test_significance_of_values_in_csv('data/head_rotation_speed_no_outliers.csv')
