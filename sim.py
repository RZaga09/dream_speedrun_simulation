import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import time
from random import randint

MULTIPLIER = 1000 #Data will be adjusted to this number of attempts for the sake of clarity in the graph
SIMULATION_LENGTH = 50000

def adjustTuple(x):
	adjustmentValue = MULTIPLIER/x[1]
	return(x[0]*adjustmentValue, MULTIPLIER)

def adjustSimData(x, y):
	adjustmentValue = MULTIPLIER/y
	return x*adjustmentValue

#data from Dream's 6 investigated streams
initPearls = adjustTuple((42,262))
initRods = adjustTuple((211,305))
initCombined = adjustTuple((8862,79910))

#data from Dream's additional 5 streams
addPearls = adjustTuple((12,356))
addRods = adjustTuple((73,134))
addCombined = adjustTuple((876,47704))

#data from all 11 of Dream's streams
totalPearls = adjustTuple((54,618))
totalRods = adjustTuple((284,439))
totalCombined = adjustTuple((15336, 271302)) #product of total pearl and rod rates, not product of init and add rates

#expected data (based on the probabilities programmed into Minecraft)
expectPearls = adjustTuple((20,423))
expectRods = adjustTuple((1,2))
expectCombined = adjustTuple((20,846))

pearlTrials = 618
rodTrials = 439

pearlsList = [] #list of successful barters per 618 trades
rodsList = [] #list of successful rod drops per 439 kills
totalList = [] #list of pearlsList x rodsList per simulation

maxPearl = 0
minPearl = 0
avePearl = 0
maxRod = 0
minRod = 0
aveRod = 0
bestCombined = 0
worstCombined = 0
bestCombinedTup = (0,0)
worstCombinedTup = (0,0)
aveCombined = 0

def ender_pearl():
	num = randint(1, expectPearls[1])
	if num <= expectPearls[0]:
		return 1
	else:
		return 0

def blaze_rod():
	num = randint(1, expectRods[1])
	if num <= expectRods[0]:
		return 1
	else:
		return 0

def process():

	enderPearls = 0
	blazeRods = 0

	for i in range(pearlTrials): 
		enderPearls += ender_pearl()
	for i in range(rodTrials): 
		blazeRods += blaze_rod()

	pearlsList.append(enderPearls)
	rodsList.append(blazeRods)
	totalList.append(enderPearls * blazeRods)

def getNotablePoints():
	global maxPearl
	global minPearl
	global avePearl
	global maxRod
	global minRod
	global aveRod
	global bestCombined
	global worstCombined
	global aveCombined
	global bestCombinedTup
	global worstCombinedTup

	maxPearl = max(pearlsList)
	minPearl = min(pearlsList)
	avePearl = sum(pearlsList)/len(pearlsList)

	maxRod = max(rodsList)
	minRod = min(rodsList)
	aveRod = sum(rodsList)/len(rodsList)

	bestCombined = max(totalList)
	worstCombined = min(totalList)
	aveCombined = (bestCombined + worstCombined)/2
	bestCombinedIndex = totalList.index(bestCombined)
	worstCombinedIndex = totalList.index(worstCombined)
	bestCombinedTup = (pearlsList[bestCombinedIndex], rodsList[bestCombinedIndex])
	worstCombinedTup = (pearlsList[worstCombinedIndex], rodsList[worstCombinedIndex])

def printNotablePoints():
	print('')
	print('-----REFERENCE DATA-----')
	print('-----EXPECTED PROBABILITY-----')
	print('Ender Pearls: 20 out of 423')
	print('Blaze Rods: 1 out of 2')
	print('Combined: 20 out of 846')
	print('-----DREAM\'S RUNS (6 INVESTIGATED STREAMS)-----')
	print('Ender Pearls: 42 out of 262')
	print('Blaze Rods: 211 out of 305')
	print('Combined: 8862 out of 79910')
	print('-----DREAM\'S RUNS (5 ADDITIONAL STREAMS)-----')
	print('Ender Pearls: 12 out of 356')
	print('Blaze Rods: 73 out of 134')
	print('Combined: 876 out of 47704')
	print('-----DREAM\'S RUNS (ALL 11 STREAMS)-----')
	print('Ender Pearls: 54 out of 618')
	print('Blaze Rods: 284 out of 439')
	print('Combined: 15336 out of 271302')
	print('')
	print('-----SIMULATION RESULTS-----')
	print('-----ENDER PEARLS-----')
	print(f'Best Pearl Run: {maxPearl} out of {pearlTrials}')
	print(f'Worst Pearl Run: {minPearl} out of {pearlTrials}')
	print(f'Average Pearl Run: {avePearl} out of {pearlTrials}')
	print('-----BLAZE RODS-----')
	print(f'Best Rod Run: {maxRod} out of {rodTrials}')
	print(f'Worst Rod Run: {minRod} out of {rodTrials}')
	print(f'Average Rod Run: {aveRod} out of {rodTrials}')
	print('-----COMBINED-----')
	print(f'Best Run: {bestCombined} out of {pearlTrials * rodTrials}: ({bestCombinedTup[0]} Ender Pearls, {bestCombinedTup[1]} Blaze Rods)')
	print(f'Worst Run: {worstCombined} out of {pearlTrials * rodTrials}: ({worstCombinedTup[0]} Ender Pearls, {worstCombinedTup[1]} Blaze Rods)')
	print(f'Average Run: {aveCombined} out of {pearlTrials * rodTrials}')

def adjustLists(adjustList, adjustmentValue):
	for i in range(len(adjustList)):
		adjustList[i] = adjustSimData(adjustList[i], adjustmentValue)

def plotGraph():
	colorsList = ['c', 'y']
	colorShuffler = 0

	#ENDER PEARL GRAPH
	plt.figure(1)
	
	for i in range(SIMULATION_LENGTH):
		print('Graph 1: Plotting line ' + str(i+1))
		plt.plot([0, totalPearls[1]], [0, pearlsList[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dashed')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, initPearls[1]], [0, initPearls[0]], label = "Dream's 6 Investigated Streams", linewidth = 3, c = 'b')
	plt.plot([0, addPearls[1]], [0, addPearls[0]], label = "Dream's Additional 5 Streams", linewidth = 3, c = 'm')
	plt.plot([0, totalPearls[1]], [0, totalPearls[0]], label = "All 11 of Dream's Streams", linewidth = 3, c = 'g')
	plt.plot([0, expectPearls[1]], [0, expectPearls[0]], label = "Expected Data", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'c', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('PIGLIN TRADES')
	plt.ylabel('SUCCESSFUL ENDER PEARL TRADES')
	plt.title('ENDER PEARLS')
	plt.legend()

	#BLAZE RODS GRAPH
	plt.figure(2)
	
	for i in range(SIMULATION_LENGTH):
		print('Graph 2: Plotting line ' + str(i+1))
		plt.plot([0, totalRods[1]], [0, rodsList[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dashed')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, initRods[1]], [0, initRods[0]], label = "Dream's 6 Investigated Streams", linewidth = 3, c = 'b')
	plt.plot([0, addRods[1]], [0, addRods[0]], label = "Dream's Additional 5 Streams", linewidth = 3, c = 'm')
	plt.plot([0, totalRods[1]], [0, totalRods[0]], label = "All 11 of Dream's Streams", linewidth = 3, c = 'g')
	plt.plot([0, expectRods[1]], [0, expectRods[0]], label = "Expected Data", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'c', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('BLAZE KILLS')
	plt.ylabel('SUCCESSFUL BLAZE ROD DROPS')
	plt.title('BLAZE RODS')
	plt.legend()

	#COMBINED GRAPH
	plt.figure(3)
	
	for i in range(SIMULATION_LENGTH):
		print('Graph 3: Plotting line ' + str(i+1))
		plt.plot([0, totalCombined[1]], [0, totalList[i]], linewidth = 1, c = colorsList[colorShuffler], linestyle = 'dashed')
		colorShuffler += 1
		if colorShuffler == 2:
			colorShuffler = 0

	plt.plot([0, initCombined[1]], [0, initCombined[0]], label = "Dream's 6 Investigated Streams", linewidth = 3, c = 'b')
	plt.plot([0, addCombined[1]], [0, addCombined[0]], label = "Dream's Additional 5 Streams", linewidth = 3, c = 'm')
	plt.plot([0, totalCombined[1]], [0, totalCombined[0]], label = "All 11 of Dream's Streams", linewidth = 3, c = 'g')
	plt.plot([0, expectCombined[1]], [0, expectCombined[0]], label = "Expected Data", linewidth = 3, c = 'r')
	plt.plot(0, 0, label = "Simulation Data", c = 'c', linestyle = 'dashed') #Here solely to add "Simulation Data" to legend

	plt.xlabel('ATTEMPTS')
	plt.ylabel('SUCCESSFUL ATTEMPTS')
	plt.title('COMBINED')
	plt.legend()

def main():
	start = time.time()
	for i in range(SIMULATION_LENGTH):
		print('Simulation ' + str(i+1))
		process()
	getNotablePoints()
	adjustLists(pearlsList, pearlTrials)
	adjustLists(rodsList, rodTrials)
	adjustLists(totalList, pearlTrials * rodTrials)
	plotGraph()
	end = time.time()
	print('Process Time: ' + str(end - start) + ' seconds')
	printNotablePoints()
	plt.show()

main()