import csv
import os
from os.path import isfile, join

# script to replace commas in csv files that should be decimal places, but were written as commas due to german locale



input_data_base_path="data/AUD_APMR202201_test/tracking/"
output_data_base_path=input_data_base_path+"formatted/"


num_dyads=9
num_trials=3

def process_head_file(in_filename, out_filename):

	in_file = open(in_filename, "r")
	out_file = open(out_filename, "w")
	lines = in_file.readlines() 


	print("input file: " + in_filename)
	print("output file: " + out_filename)


	# write header to file and remove from lines list
	out_file.write(lines[0])
	lines.pop(0)

	for line in lines:
		split_line = line.split(',')
		new_line = split_line[0]

		for comma_idx in range(0,26):
		# for comma_idx in range(0,len(split_line)-1):
			
			if (comma_idx < 14 and comma_idx % 2 == 0) or (comma_idx == 25):
				new_line += '.'
			else:
				new_line += ','

			next_chunk = split_line[comma_idx+1] 

			# deal with case where last number was integer instead of fraction
			if next_chunk == '\n':
				next_chunk = '0'
			new_line += next_chunk

		new_line += '\n'

		out_file.write(new_line)


def process_hand_file(in_filename, out_filename):

	in_file = open(in_filename, "r")
	out_file = open(out_filename, "w")
	lines = in_file.readlines() 


	print("input file: " + in_filename)
	print("output file: " + out_filename)


	# write header to file and remove from lines list
	out_file.write(lines[0])
	lines.pop(0)

	for line in lines:
		split_line = line.split(',')
		new_line = split_line[0]

		for comma_idx in range(0,len(split_line)-2):
			
			if (comma_idx < 20 and comma_idx % 2 == 0) or  (comma_idx == 22) or (comma_idx == 26) or (comma_idx == 28) or (comma_idx == 31):
				new_line += '.'
			else:
				new_line += ','

			next_chunk = split_line[comma_idx+1] 

			# deal with case where last number was integer instead of fraction
			if next_chunk == '\n':
				next_chunk = '0'
			new_line += next_chunk

		new_line += '\n'

		out_file.write(new_line)

# create output directory
try: 
    os.mkdir(output_data_base_path) 
except OSError as error: 
    print("output directory " + output_data_base_path + " already exists")  


all_tracking_files = [f for f in os.listdir(input_data_base_path) if isfile(join(input_data_base_path, f))]

for file in all_tracking_files:
	
	in_filename=input_data_base_path+file
	out_filename=output_data_base_path+file

	if "Head" in in_filename:
		process_head_file(in_filename, out_filename)
	else:
		process_hand_file(in_filename, out_filename)

