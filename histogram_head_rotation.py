import matplotlib.pyplot as plt
import numpy as np
import csv

filename='data/head_rotation_speed_no_outliers.csv'

sp_speed=[]
nsp_speed=[]

def plot_histogram(data,title,outfile):

	fig = plt.figure(figsize=(16,12))

	# n, bins, patches = plt.hist(data)
	n, bins, patches = plt.hist(data, bins=np.arange(0.0, 0.4, 0.05))

	print(bins)

	plt.grid(color='white', lw = 0.5, axis='x')
	plt.title(title, loc = 'left', fontsize = 36)

	plt.yticks(np.arange(0,6,1), fontsize=20)
	plt.xticks(np.arange(0.0, 0.4, 0.05), fontsize=20)

	plt.xlabel('\nHead rotation speed (rad/s)', fontsize=28)
	plt.ylabel('Frequency', fontsize=28)

	plt.savefig(outfile)

with open(filename, newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader)
	for row in reader:
		sp_speed.append(float(row[0]))
		nsp_speed.append(float(row[1]))

plot_histogram(sp_speed,'Histogram of Head Rotation Speed: SPATIAL', 'images/hist_head_rotation_spatial.png')
plot_histogram(nsp_speed,'Histogram of Head Rotation Speed: NO_SPATIAL', 'images/hist_head_rotation_nospatial.png')
