import random
import sys
import operator



class Knapsack():	

	#initialize variables and lists
	def __init__(self):	

		self.C = 0
		self.weights = []
		self.price = []
		self.parents = []
		self.newparents = []
		self.bests = []
		self.best_p = [] 
		self.iterated = 1
		self.population = 0
		self.pre_optimum = (-1,[])
		self.wanted = 0
		self.limit = 0
		self.p_mut=0

		# increase max recursion for long stack
		iMaxStackSize = 15000
		sys.setrecursionlimit(iMaxStackSize)
	
	def print_info(self):
		print("\n\nGenetic Algoritm for Knapstack Problem\n",
			  "\nWeight limit :",self.C, \
			  "\nGen count :",len(self.weights), \
			  "\nInit Population Size :",self.population, \
			  "\nMutation Probability :",self.p_mut, \
			  "\nEnough fitness :",self.wanted, \
			  "\nIteration Limit :",self.limit, \
			  "\n--------------------------------------------")

	# create the initial population 
	def initialize(self):

		for i in range(self.population):
			parent = []
			for k in range(0, len(self.weights)):
				k = random.randint(0, 1)
				parent.append(k)
			self.parents.append(parent)

	# set the details of this problem
	def properties(self, weights, price, C, population, wanted, limit,p_mut):

		self.weights = weights
		self.price = price
		self.C = C
		self.population = population
		self.wanted = wanted
		self.limit = limit
		self.wanted = wanted
		self.p_mut = p_mut
		self.print_info()
		self.initialize()

	# calculate the fitness function of each list 
	def fitness(self, item):

		sum_w = 0
		sum_p = 0

		# get weights and price
		for index, i in enumerate(item):
			if i == 0:
				continue
			else:
				sum_w += self.weights[index]
				sum_p += self.price[index]

		# if greater than the optimum_solution return -1 or the number otherwise
		if sum_w > self.C:
			return -1
		else: 
			return sum_p
	
	# run generations of GA
	def evaluation(self):

		# loop through parents and calculate fitness
		best_pop = self.population // 2
		for i in range(len(self.parents)):
			parent = self.parents[i]
			ft = self.fitness(parent)
			self.bests.append((ft, parent))

		# sort the fitness list by fitness		
		self.bests.sort(key=operator.itemgetter(0), reverse=True)
		self.best_p = self.bests[:best_pop]

		#set best solution until now
		if self.best_p[0][0] > self.pre_optimum[0]:
			print(self.iterated,"=> Updated ",self.pre_optimum," to ",self.best_p[0])
			self.pre_optimum = self.best_p[0]
			

		self.best_p = [x[1] for x in self.best_p]

		

	# mutate children after certain condition
	def mutation(self, ch):

		for i in range(len(ch)):		
			k = random.uniform(0, 1)
			if k > self.p_mut:
				#if random float number greater that 0.5 flip 0 with 1 and vice versa
				if ch[i] == 1:
					ch[i] = 0
				else: 
					ch[i] = 1
		return ch

	# crossover two parents to produce two children by miixing them under random ration each time
	def crossover(self, ch1, ch2):

		threshold = random.randint(1, len(ch1)-1)
		tmp1 = ch1[threshold:]
		tmp2 = ch2[threshold:]
		ch1 = ch1[:threshold]
		ch2 = ch2[:threshold]
		ch1.extend(tmp2)
		ch2.extend(tmp1)

		return ch1, ch2

	# run the GA algorithm
	def run(self):
		
		if self.pre_optimum[0] >= self.wanted and self.wanted != -1:
			print("\nFound wanted Solution :", self.pre_optimum[1]," Fitness :",self.pre_optimum[0]," Wanted :", self.wanted)
			return
		
		if self.iterated == self.limit:
			print(" \n Result best Solution in ",self.limit," iterasion :",self.pre_optimum[1], "Fitness :",self.pre_optimum[0])
			return
			
		# run the evaluation once
		self.evaluation()
		newparents = []
		pop = len(self.best_p)-1

		# create a list with unique random integers
		sample = random.sample(range(pop), pop)
		for i in range(0, pop):
			# select the random index of best children to randomize the process
			if i < pop-1:
				r1 = self.best_p[i]
				r2 = self.best_p[i+1]
				nchild1, nchild2 = self.crossover(r1, r2)
				newparents.append(nchild1)
				newparents.append(nchild2)
			else:
				r1 = self.best_p[i]
				r2 = self.best_p[0]
				nchild1, nchild2 = self.crossover(r1, r2)
				newparents.append(nchild1)
				newparents.append(nchild2)

		# mutate the new children and potential parents to ensure global optimum_solutionima found
		for i in range(len(newparents)):
			newparents[i] = self.mutation(newparents[i])

		
		self.iterated += 1
		#print("recreate generations for {} time" .format(self.iterated))
		self.parents = newparents
		self.bests = []
		self.best_p = []
		self.run()	