import matplotlib.pyplot as plt
import numpy as np
import csv

filename='data/head_movement_speed_no_outliers.csv'

sp_speed=[]
nsp_speed=[]

def plot_histogram(data,title,outfile):

	fig = plt.figure(figsize=(16,12))


	n, bins, patches = plt.hist(data, bins=np.arange(0.0, 0.11, 0.01))

	plt.grid(color='white', lw = 0.5, axis='x')
	plt.title(title, loc = 'left', fontsize = 36)

	plt.yticks(np.arange(0,5,1), fontsize=20)
	plt.xticks(np.arange(0,0.11,0.01), fontsize=20)

	plt.xlabel('\nHead movement speed (m/s)', fontsize=28)
	plt.ylabel('Frequency', fontsize=28)

	plt.savefig(outfile)

with open(filename, newline='') as csvfile:
	reader = csv.reader(csvfile)
	next(reader)
	for row in reader:
		sp_speed.append(float(row[0]))
		nsp_speed.append(float(row[1]))

plot_histogram(sp_speed,'Histogram of Head Movement Speed: SPATIAL', 'images/hist_head_movement_spatial.png')
plot_histogram(nsp_speed,'Histogram of Head Movement Speed: NO_SPATIAL', 'images/hist_head_movement_nospatial.png')
