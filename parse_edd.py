# this code looks at the fas file and tries to find the number of difference in each column from the most common base.
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import LinearAxis, SingleIntervalTicker
import math

def get_fas_dict():
	'''
		This  function reads the fas file and returns a dictionary where the keys is the name of the pseudomonas and the values is a string containing the base values
	'''
	temp_pseudomonas = ''
	fas_dict 		 = {}
	filename = input("Enter FAS file name: ")
	with open(filename) as fas_file:
		for line in fas_file:
			if (line[0] == '>'):
				temp_pseudomonas = line[1:-1]
			else:
				fas_dict[temp_pseudomonas] = line[:-1]

	return fas_dict

def most_common(lst):
	'''
		gets the most common item in a list
	'''
	return max(set(lst), key=lst.count)

def make_plot(x, y, plot_width, bar_width, ticker_override = None, xstart = None, xend = None, ystart = None, name = "plot.html", xaxis_label = '', yaxis_label = '', title = ''):
	'''
		make a pretty bar plot
	'''
	output_file(name)

	if isinstance(x[0], str):
		p = figure(x_range = x, plot_width = plot_width, title = title)
	else:
		p = figure(plot_width = plot_width, title = title)

	p.vbar(x = x, width = bar_width, top = y)

	if ticker_override is not None:
		p.xaxis.ticker  = ticker_override

	if ystart is not None:
		p.y_range.start = ystart

	if xstart is not None:
		p.x_range.start = xstart

	if xend is not None:
		p.x_range.end   = xend

	p.xaxis.major_label_orientation = math.pi/2

	p.xaxis.axis_label  = xaxis_label

	p.yaxis.axis_label  = yaxis_label

	show(p)

def main():
	# fas_dict contains all the info from the fas file.
	# it is stored by pseudomonas : base string pairs
	fas_dict         = get_fas_dict()

	# this is a list of base strings
	base_list        = list(fas_dict.values())

	# transpose to column form
	column_base_list = list(map(list, zip(*base_list)))

	# get the name of the reference pseudonoma
	reference_pseudomonas_name = input("References Pseudomonas: ")

	# searched reference in dictionary, deleted this from dictionary
	reference = fas_dict[reference_pseudomonas_name]
	del fas_dict[reference_pseudomonas_name]

	# count the number of bases in each column that are the same as the reference
	simi_count       = []
	diff_count       = []

	# getting a column index so we can index into the reference
	col_index        = 0

	# iterating through all the columns
	for col in column_base_list:
		# counter for the number equal to the reference
		simi_counter_temp = 0
		diff_counter_temp = 0
		# iterating through all the bases in each column
		for base in col:
			if base != reference[col_index]:
				# if we are different, increment counter
				diff_counter_temp = diff_counter_temp + 1
			else:
				simi_counter_temp = simi_counter_temp + 1

		# append the counter into a list
		simi_count.append(simi_counter_temp)
		diff_count.append(diff_counter_temp)
		col_index = col_index + 1

	base_pair_posn = list(range(1, len(diff_count) + 1))

	# specify a section of the x axis to show
	xstart = int(input("Enter the Starting Base Position: "))
	xend = xstart + int(input("Enter the Number of Positions to Plot: "))

	# declare a new variable called x which is a list slice starting from variable xstart to variable xend
	x = base_pair_posn[xstart:xend]

	# declare a new variable called y which is a list slice starting from variable xstart to variable xend
	# this time the variable being sliced is  called simi_count
	y_simi = simi_count[xstart:xend]
	y_diff = diff_count[xstart:xend]

	# make a pretty bar chart
	make_plot	(
					x,                      # x
					y_simi,                 # y
					5000, 			        # plot_width
					0.5, 			        # bar_width
					ticker_override = SingleIntervalTicker(interval = 1, num_minor_ticks = 0),
					xstart      	= xstart + 0.5,
					xend        	= xend + 0.5,
					ystart      	= 0,
					name        	= "no_similarites_plot.html",
					xaxis_label 	= "Base Index",
					yaxis_label 	= "Number of Occurences",
					title			= "Number of Bases Equal to the Reference"
				)

	# make a pretty bar chart
	make_plot	(
					x,                      # x
					y_diff,                 # y
					5000, 			        # plot_width
					0.5, 			        # bar_width
					ticker_override = SingleIntervalTicker(interval = 1, num_minor_ticks = 0),
					xstart      	= xstart + 0.5,
					xend        	= xend + 0.5,
					ystart      	= 0,
					name        	= "no_differences_plot.html",
					xaxis_label 	= "Base Index",
					yaxis_label 	= "Number of Occurences",
					title			= "Number of Bases Different to the Reference"
				)

if __name__ == '__main__':
	main()
