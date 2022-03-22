import matplotlib.pyplot as plt
import numpy as np
import csv


sp_speed=[]
nsp_speed=[]

def plot_histogram(data,title,outfile):

	fig = plt.figure(figsize=(16,12))


	# n, bins, patches = plt.hist(data, bins=100)
	n, bins, patches = plt.hist(data, bins=np.arange(0.0, 0.5, 0.01))

	print(bins)

	# plt.grid(color='white', lw = 0.5, axis='x')
	plt.title(title, loc = 'left', fontsize = 36)

	plt.yticks(np.arange(0,55000,10000), fontsize=20)
	# plt.xticks(np.arange(0,0.11,0.01), fontsize=20)

	plt.xlabel('\nHead movement speed per frame (m/s)', fontsize=28)
	plt.ylabel('Frequency', fontsize=28)

	plt.savefig(outfile)
	# plt.show()

filename='data/all_head_movement_speed_spatial.csv'

with open(filename, newline='') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		sp_speed.append(float(row[0]))

filename='data/all_head_movement_speed_nonspatial.csv'

with open(filename, newline='') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		nsp_speed.append(float(row[0]))



# shorten longest list to even out length
if len(sp_speed) > len(nsp_speed):
	sp_speed = sp_speed[0 : len(nsp_speed)]
else:
	nsp_speed = nsp_speed[0 : len(sp_speed)]

print("Length sp_speed: " + str(len(sp_speed)))
print("Length nsp_speed: " + str(len(nsp_speed)))

plot_histogram(sp_speed,'Histogram of Head Movement Speed: SPATIAL', 'images/hist_all_head_movement_spatial.png')
plot_histogram(nsp_speed,'Histogram of Head Movement Speed: NO_SPATIAL', 'images/hist_all_head_movement_nospatial.png')
