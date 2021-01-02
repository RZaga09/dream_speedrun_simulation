#Context: Minecraft speedrunner Dream has been accused of cheating in his speedruns due to his unusually high success rate
#in gathering "Ender Pearl" items through bartering with NPCs and in gathering "Blaze Rod" items through killing enemies

#Dream has a success rate of 42/262 ender pearls per barter
#Probability of a successful ender pearl barter is 20/423

#Dream has a success rate of 211/305 blaze rods per kill
#Probability of a successful blaze rod drop is 1/2

#This only takes into account the probabilities programmed for the game events to happen
#External factors are not considered in this simulation

#Expected probability of being successful in both events is 20/846 (approx. 2.364%)
#Dream's success rate is 8862/79910 (approx. 11.090%)
#this does not take into account that both events may not have necessarily been attempted in a single speedrun

#Learned how to code a line graph from https://www.w3resource.com/graphics/matplotlib/basic/matplotlib-basic-exercise-5.php
#Data from https://mcspeedrun.com/dream.pdf

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import time
from random import randint

TRADES_ATTEMPTED = 262
DREAM_PEARL_RATE = 42
ADJUST_PEARL = 262/423
EXPECTED_PEARL_RATE = (20, 423) #(successful trades, attempted trades)
EXPECTED_PEARL_ADJUSTED = (20 * ADJUST_PEARL, 423 * ADJUST_PEARL)

KILLS_ATTEMPTED = 305
DREAM_ROD_RATE = 211
ADJUST_ROD = 305/2
EXPECTED_ROD_RATE = (1, 2) #(successful kills, attempted kills)
EXPECTED_ROD_ADJUSTED = (1 * ADJUST_ROD, 2 * ADJUST_ROD)

DREAM_TOTAL_RATE = (8862, 79910)
ADJUST_TOTAL = 79910/846 #to be multiplier to EXPECTED TOTAL_RATE to adjust to the 79910 denominator from Dream's rate
EXPECTED_TOTAL_RATE = (20 * ADJUST_TOTAL, 846 * ADJUST_TOTAL)

SIMULATION_LENGTH = 50000

pearlsList = [] #list of successful barters per 262 trades
rodsList = [] #list of successful rod drops per 305 kills
totalSuccess = [] #list of pearlsList x rodsList per simulation
start = 0 #var for startTime
end = 0 #var for endTime

def process():

	enderPearls = 0
	blazeRods = 0

	for i in range(TRADES_ATTEMPTED):
		enderPearls += ender_pearl()
	for i in range(KILLS_ATTEMPTED):
		blazeRods += blaze_rod()

	pearlsList.append(enderPearls)
	rodsList.append(blazeRods)
	totalSuccess.append(enderPearls * blazeRods)


def ender_pearl():
	num = randint(1, EXPECTED_PEARL_RATE[1])
	if num <= EXPECTED_PEARL_RATE[0]:
		return 1
	else:
		return 0

def blaze_rod():
	num = randint(1, EXPECTED_ROD_RATE[1])
	if num <= EXPECTED_ROD_RATE[0]:
		return 1
	else:
		return 0


def plot_graph():

	colorsList = ['c', 'y']
	colorShuffler = 0

	#ENDER PEARLS GRAPH

	plt.figure(1)

	for i in range(SIMULATION_LENGTH):
		print('Graph 1: Plotting line ' + str(i))
		plt.plot([0, TRADES_ATTEMPTED], [0, pearlsList[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dashed')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, TRADES_ATTEMPTED], [0, DREAM_PEARL_RATE], label = "Dream's Runs", linewidth = 3, c = 'g')
	plt.plot([0, EXPECTED_PEARL_ADJUSTED[1]], [0, EXPECTED_PEARL_ADJUSTED[0]], label = "Expected Rate", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'b', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('PIGLIN TRADES')
	plt.ylabel('SUCCESSFUL ENDER PEARL TRADES')
	plt.title('ENDER PEARLS')
	plt.legend()

	#BLAZE RODS GRAPH

	plt.figure(2)

	for i in range(SIMULATION_LENGTH):
		print('Graph 2: Plotting line ' + str(i))
		plt.plot([0, KILLS_ATTEMPTED], [0, rodsList[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dotted')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, KILLS_ATTEMPTED], [0, DREAM_ROD_RATE], label = "Dream's Runs", linewidth = 3, c = 'g')
	plt.plot([0, EXPECTED_ROD_ADJUSTED[1]], [0, EXPECTED_ROD_ADJUSTED[0]], label = "Expected Rate", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'b', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('BLAZE KILLS')
	plt.ylabel('SUCCESSFUL BLAZE ROD DROPS')
	plt.title('BLAZE RODS')
	plt.legend()

	#TOTAL GRAPH

	plt.figure(3)

	for i in range(SIMULATION_LENGTH):
		print('Graph 3: Plotting line ' + str(i))
		plt.plot([0, DREAM_TOTAL_RATE[1]], [0, totalSuccess[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dashed')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, DREAM_TOTAL_RATE[1]], [0, DREAM_TOTAL_RATE[0]], label = "Dream's Runs", linewidth = 3, c = 'g')
	plt.plot([0, EXPECTED_TOTAL_RATE[1]], [0, EXPECTED_TOTAL_RATE[0]], label = "Expected Rate", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'b', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('ATTEMPTS')
	plt.ylabel('SUCCESSFUL ATTEMPTS')
	plt.title('COMBINED')
	plt.legend()

def main():
	start = time.time()
	for i in range(SIMULATION_LENGTH):
		print('Simulation ' + str(i))
		process()
	plot_graph()
	end = time.time()
	print('Process Time: ' + str(end - start) + ' seconds')
	plt.show()

main()
