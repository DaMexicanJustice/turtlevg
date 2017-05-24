import matplotlib.pyplot as plt
	
def plot_results_bar(src, title):
	plt.bar(range(len(src)), src.values(), align='center')
	plt.xticks(range(len(src)), list(src.keys()))
	
	lowestval = min(src, key=src.get)
	
	plt.title("TurtleVG guesses " + title + " is a game on: " +lowestval)
	plt.xlabel('Console')
	plt.ylabel('Deviation from best fit')
	plt.show()
	plt.savefig("TestBarChart.png")
	
def prepare_for_plotting(results):
	res = {}
	
	for key, value in results.items():
		if value == 99999: 
			value = 20000
		res[key] = value
	
	return res