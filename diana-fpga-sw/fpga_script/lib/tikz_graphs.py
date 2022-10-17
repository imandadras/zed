#!/usr/bin/env python

def put_line_in_graph(x,y,filehandle,legend=None):
	filehandle.write("\\addplot table[row sep=crcr]{\n")
	n = 0
	for n_x in x:
		n_y = y[n]
		n = n+1
		filehandle.write(str(n_x) + " " + str(n_y) + "\\\\ \n")
	filehandle.write("};\n")
	if not legend is None:
		filehandle.write("\addlegendentry{" + legend + "}\n")
	return

def create_graph(x, y, filename, legend):
	file = open(filename, "w")

	# Create the header
	file.write("\\begin{tikzpicture}[scale=1]\n")
	file.write("\\begin{axis} [\n")
	file.write("    xmin=" + str() + ",\n")
	file.write("    xmax=" + str() + ",\n")
	file.write("    xlabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    xmajorgrids,\n")
	file.write("    ymin=" + str() + ",\n")
	file.write("    ymax=" + str() + ",\n")
	file.write("    ylabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    ymajorgrids,\n")
	file.write("    legend style={\n")
	file.write("        at={(0.03,0.97)},\n")
	file.write("        anchor=north west,\n")
	file.write("        draw=black,\n")
	file.write("        fill=white,\n")
	file.write("        legend cell align=left}]\n")

	# Create the graph itself
	if len(legend) <= 1:
		# There is only one line in the graph
		put_line_in_graph(x,y,file)
	else:
		n = 0
		for legend_entry in legend:
			put_line_in_graph(x[n],y[n],file,legend_entry)
			n = n + 1

	# Create the footer
	file.write("\\end{axis}\n")
	file.write("\\end{tikzpicture}\n")

	file.close()

	return

def create_double_graph(x, y1, y2, filename):
	file = open(filename, "w")

	# Create the general header and the header for graph 1
	file.write("\\begin{tikzpicture}[scale=1]\n")
	file.write("\\begin{axis} [\n")
	file.write("    separate axis lines,\n")
	file.write("    xmin=" + str() + ",\n")
	file.write("    xmax=" + str() + ",\n")
	file.write("    xlabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    xmajorgrids,\n")
	file.write("    ymin=" + str() + ",\n")
	file.write("    ymax=" + str() + ",\n")
	file.write("    ylabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    ymajorgrids]\n")

	# Create the graph itself
	put_line_in_graph(x,y2,file)

	# Create the footer for graph1 and the header for graph 2
	file.write("\\end{axis}\n")
	file.write("\\begin{axis} [\n")
	file.write("    xmin=" + str() + ",\n")
	file.write("    xmax=" + str() + ",\n")
	file.write("    xlabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    xmajorgrids,\n")
	file.write("    ymin=" + str() + ",\n")
	file.write("    ymax=" + str() + ",\n")
	file.write("    ylabel={PUT_YOUR_LABEL_HERE},\n")
	file.write("    ymajorgrids,\n")
	file.write("    axis y line*=right,\n")
	file.write("    ylabel near ticks]\n")

	# Create the graph itself
	put_line_in_graph(x,y1,file)

	# Create the footer
	file.write("\\end{axis}\n")
	file.write("\\end{tikzpicture}\n")

	file.close()

	return


def create_heatmap(x,y,value,filename):
	file = open(filename, "w")

	# Create the header
	file.write("\\pgfplotstabletypeset[\n")
	file.write("       color cells={min=0, max=1},\n")
	file.write("       col sep=comma]\n")
	file.write("{\n")

	# Create the heatmap
	## First we create a 2D matrix
	all_x = sorted(set(x))
	all_y = sorted(set(y))
	grid = [0]*len(all_x)*len(all_y)
	for index in range(0,len(value)):
		coordinate_x = 0
		coordinate_y = 0
		for index_x in range(0,len(all_x)):
			if all_x[index_x] == x[index]:
				coordinate_x = index_x
		for index_y in range(0,len(all_y)):
			if all_y[index_y] == y[index]:
				coordinate_y = index_y
		#print("coordinate_x = " + str(coordinate_x))
		#print("coordinate_y = " + str(coordinate_y))
		#print("value = " + str(value[index]))

		grid[coordinate_y+coordinate_x*len(all_y)] = value[index]

	## Then we export the matrix
	# Start with a line of indices
	file.write("0,")
	for index_x in range(0,len(all_x)):
		file.write(str(all_x[index_x]) + ",")
	file.write("\n")
	for index_y in range(0,len(all_y)):
		# Start every line with an index
		file.write(str(all_y[len(all_y)-1-index_y]) + ",")
		for index_x in range(0,len(all_x)):
			file.write(str(grid[len(all_y)-1-index_y+index_x*len(all_y)]))
			if index_x == len(all_x) - 1:
				file.write("\n")
			else:
				file.write(",")

	# Create the footer
	file.write("}\n")
	file.close()
	return


