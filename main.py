from kanpstack_solution_with_ga import Knapsack

# properties for this particular problem
weights = [12,  7, 11, 8, 9, 3]
price = [24, 13, 23, 15, 16, 1]

C = 17 				#limit knapstack
population = 15		#population size
wanted = 25			#enough price
limit = 100 		#iteration limit
p_mut = 0.5

k = Knapsack()
k.properties(weights, price, C, population, wanted, limit, p_mut)
k.run()