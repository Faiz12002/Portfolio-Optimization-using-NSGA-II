# imports 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Domination Relation 

def dominates(a,b,obj):
  if obj == 'max':
    if ( (a[0] >= b[0] and a[1] >= b[1]) and (a[0] > b[0] or a[1] > b[1]) ):
      return True
  elif obj == 'min':
    if ( (a[0] <= b[0] and a[1] <= b[1]) and (a[0] < b[0] or a[1] < b[1]) ):
      return True
def isnondominated(a,b):
  if ((a[0] > b[0] and a[1] < b[1]) or (a[0] < b[0] and a[1] > b[1])):
    return True
  elif a[0] == b[0] and a[1] == b[1]:
    return True
  else:
    return False

def DominationRelation(a,b,obj):
  if dominates(a,b,obj):
    return True
  elif isnondominated(a,b):
    return 'ND'


# Check Dominance

def check_dominance(arr):
    for element in arr:
        if element != True and element != "ND":
            return False
    return True


# Non dominated sorting

def non_dominated_sorting(f1, f2):
  # zip them into tuples
  points = list(zip(f1,f2))
  domCounter = []
  nonDomContainer = []
  ranks = []
  while (len(points) > 0):
    for i in range(len(points)):
      for j in range(len(points)):
        domCounter.append(DominationRelation(points[i], points[j], 'min'))
      if (check_dominance(domCounter)):
        nonDomContainer.append(points[i])
      domCounter = []
    ranks.append(nonDomContainer)
    points = [tup for tup in points if tup not in nonDomContainer]
    nonDomContainer = []
  return ranks
  # returns a list type (list of tuples)
  # inputs two elements of list type


# crowding distance

def crowding_distance(F1, F2, front_index):
  ranks = non_dominated_sorting(F1, F2)
  # We want to calculate crowding distance for the desired front
  desired_front = np.array(ranks[front_index])

  f1_Omax = max(F1)
  f1_Omin = min(F1)

  f2_Omax = max(F2)
  f2_Omin = min(F2)

  f1_range = f1_Omax - f1_Omin
  f2_range = f2_Omax - f2_Omin

  f1_non_sorted = {index: value for index, value in enumerate(desired_front[:,0])}
  f2_non_sorted = {index: value for index, value in enumerate(desired_front[:,1])}

  f1_sorted = dict(sorted(f1_non_sorted.items(), key=lambda item: item[1]))
  f2_sorted = dict(sorted(f2_non_sorted.items(), key=lambda item: item[1]))

  f1_sorted_indices = [i for i in f1_sorted.keys()]
  f1_sorted_values = np.array([i for i in f1_sorted.values()])
  f2_sorted_indices = [i for i in f2_sorted.keys()]
  f2_sorted_values = np.array([i for i in f2_sorted.values()])

  D1 = []
  D2 = []

  for i in range(len(f1_sorted_values)):
      if i == 0:
          D1.append(float('inf'))
      elif i == len(f1_sorted_values)-1:
          D1.append(float('inf'))
      else:
          D1.append((f1_sorted_values[i+1] - f1_sorted_values[i-1]) / (f1_range))

  for i in range(len(f2_sorted_values)):
      if i == 0:
          D2.append(float('inf'))
      elif i == len(f2_sorted_values)-1:
          D2.append(float('inf'))
      else:
          D2.append((f2_sorted_values[i+1] - f2_sorted_values[i-1]) / (f2_range))

  D1 = {f1_sorted_indices[i]: D1[i] for i in range(len(f1_sorted_indices))}
  D2 = {f2_sorted_indices[i]: D2[i] for i in range(len(f2_sorted_indices))}
  CD = {}
  for key in D1:
      if key in D2:
          CD[key] = D1[key] + D2[key]

  CD_sorted = dict(sorted(CD.items(), key=lambda item: item[1], reverse = True))
  return CD_sorted
  # returns a dict type (a dict of crowding distance values, which their indices are indices of fitness nondominated sorting)
  # inputs two elements of list type and one element of int type


# generate inital random population

def generate_random_population(size, n):
  # size est la longueur de w (nbr de variable) (taille de la solution)
    solutions = []

    for _ in range(n):
        random_poids = np.random.rand(size)  # Génère un vecteur de valeurs aléatoires entre 0 et 1
        random_poids /= np.sum(random_poids)  # Divise toutes les valeurs par la somme pour que la somme des poids soit égale à 1
        if (list(np.round(random_poids, 4)) not in solutions): # unicite de l'individu
          solutions.append(list(np.round(random_poids, 4))) # 4 nombres après ,

    return solutions
    # retuns a list type (a list with list type lists)
    # inputs two elements of int type




# massFitness calculation

def massFitness(w, E, V):
   #E:vecteur des espérances
   #V:matrice de variance covariance
   #w:vecteur des poids
    # vect = [[...],
    #         [...],
    #         [...],
    #         ]
    f1 = []
    f2 = []
#calcul de f1=E(r_p)
    for i in range(len(w)):
      assert w[i].shape[0] == E.shape[0]  #les taille compatible
      f1.append(round(np.dot(w[i],E),4))

# Calcul f2 = Var(r_p)
    for i in range(len(w)):
      assert w[i].shape[0] == V.shape[0] == V.shape[1] #les tailles compatible
      f2.append(round(np.dot(w[i],np.dot(V, w[i])),4))

    return (f1,f2)
    # returns a tuple type, a 2d tuple that contains two list type
    # inputs 3 elements of numpy.ndarray type of same shape




# crossover function

def croisement(parent1, parent2, c):
        #c borne sup
        #parent1 solution
        #parent2 solution
    #Les parents doivent avoir la même longueur
  assert len(parent1) == len(parent2)

    # Initialiser une liste pour stocker les descendants
  descendants = []
  counter = 0
  while counter != 100:
    # Choisir un point de croisement aléatoire
    point_de_croisement = random.randint(1, len(parent1) - 1)

    # Créer un descendant en combinant des parties des deux parents
    if (random.uniform(0,1) < 0.5):
      offspring = parent1[:point_de_croisement] + parent2[point_de_croisement:]
    else:
      offspring = parent1[point_de_croisement:] + parent2[:point_de_croisement]

    # Vérifier si le descendant est déjà dans la liste
    if offspring not in descendants:
      # Verifier si la somme est egale ou inferieur a 1
      if sum(offspring) <= 1:
        descendants.append(offspring)
    counter +=1

  return descendants[0:c]
  # returns a list type containing elements of list type
  # inputs two elements of list type and one element of int type


# mutation1 

def mutation1(offspring):
    random_ind = random.randint(0, len(offspring)-1)
    offspring[random_ind] = offspring[random_ind] * 0.9
    return offspring
    # returns a list type
    # inputs one element of list type




# mutation_L1

def mutation_L1(sequence, m):
    # Vérifier si le taux de mutation est dans la plage valide
    assert 0 <= m <= 1, "Le taux de mutation doit être compris entre 0 et 1"

    has_negative = False
    for row in sequence:
      for element in row:
        if element < 0:
          has_negative = True
          break
        if has_negative:
          raise ValueError("The sequence contains at least one negative value.")


    sequence_mutée = []

    # Copier la séquence originale pour maintenir les individus non mutés
    sequence_mutée = sequence.copy()

    # Individu à muter (sélection aléatoire)
    individu_index = random.randint(0, len(sequence)-1)
    individu = sequence[individu_index].copy()  # Make a copy of the selected individual

    # Sélectionner deux indices distincts de manière aléatoire
    indices = random.sample(range(len(individu)), 2)

    # Générer un nombre aléatoire entre 0 et 1
    rand = random.random()

    # Si le nombre aléatoire est inférieur ou égal au taux de mutation, effectuer la mutation
    if rand <= m:
        # Calculer la mutation
        mutation_value = rand * (min(individu) if rand < 0.5 else (1 - max(individu)))

        # Ajouter ou soustraire la mutation aux éléments sélectionnés
        individu[indices[0]] += mutation_value
        individu[indices[1]] -= mutation_value
    else:
        individu[indices[0]], individu[indices[1]] = individu[indices[1]], individu[indices[0]]

        # S'assurer que les w restent dans [0, 1] et la somme est 1
    for i in range(len(individu)):
      individu[i] = max(0, min(1, individu[i]))
    if sum(individu) < 1:
      individu[indices[0]] += 1 - sum(individu)
    elif sum(individu) > 1:
      individu[indices[0]] -= 1 - sum(individu)
    # Remplacer l'individu muté dans la séquence mutée
    sequence_mutée[individu_index] = individu

    return sequence_mutée









# get_chromosome

def get_chromosome(P,f1,target):
  """
  P: population
  f1: obj1 array
  target: fitness value to get its chromosome
  """
  for i in range(len(f1)):
    if f1[i] == target:
      return P[i]
      # returns one element float type
      # inputs one element of list type that contains elements of list type and one element of list type and one element of float type


# NSGA2 function



def NSGA2(E, V, max_gen, max_pop, pop_size, divd, t): # t: taux de mutation
  assert 0 < t < 1, "Mutation rate must be between 0 and 1"
  population = generate_random_population(pop_size, max_pop)
  np_population = np.array(population)



  population_fitness = massFitness(np_population, E, V)
  population_f1 = population_fitness[0]
  population_f2 = population_fitness[1]

  population_ranks = non_dominated_sorting(population_f1, population_f2)

  for i in range(len(population_ranks)):
    if (len(population_ranks[i]) > 1):
      fitness_parent1 = population_ranks[i][0]
      fitness_parent2 = population_ranks[i][1]
      break
    if (len(population_ranks[i]) == 1):
      fitness_parent1 = population_ranks[i][0]
      fitness_parent2 = population_ranks[i+1][0]
      break

  member_parent1 = get_chromosome(population, population_f1, fitness_parent1[0])
  member_parent2 = get_chromosome(population, population_f1, fitness_parent2[0])



  population_offspring = croisement(member_parent1, member_parent2, max_pop)


  for i in range(len(population_offspring)):
    if random.uniform(-(1/t), 0.1) > 0:
      population_offspring[i] = mutation1(population_offspring[i])


  population_mixte = population + population_offspring
  np_population_mixte = np.array(population_mixte)


  population_mixte_ranks = []
  population_mixte_ranks_distances = []
  population_elite = []
  population_elite_fitness = []
  pareto_population = []
  elite_offspring = []
  unique_elite_offspring = []


  for i in range(max_gen+1):

    arr1 = np_population_mixte

    population_mixte_fitness = ()
    population_mixte_fitness = massFitness(np_population_mixte, E, V)
    population_mixte_f1 = population_mixte_fitness[0]
    population_mixte_f2 = population_mixte_fitness[1]


    population_mixte_ranks.clear()
    population_mixte_ranks = non_dominated_sorting(population_mixte_f1, population_mixte_f2)




    population_mixte_ranks_distances.clear()
    for i in range(len(population_mixte_ranks)):
      population_mixte_ranks_distances.append(crowding_distance(population_mixte_f1, population_mixte_f2, i))




    population_elite.clear()
    population_elite_fitness.clear()




    for i in range(len(population_mixte_ranks)):
      if (len(population_elite_fitness) == divd):
        break
      for j in range(0,divd):
        if (j >= len(list(population_mixte_ranks_distances[i].keys()))):
          continue
        population_elite_fitness.append(population_mixte_ranks[i][list(population_mixte_ranks_distances[i].keys())[j]])




    for element in population_elite_fitness:
      population_elite.append(get_chromosome(population_mixte, population_mixte_f1, element[0]))



    elite_offspring.clear()
    for i in range(1, divd-1):
      elite_offspring.append(croisement(population_elite[0], population_elite[i], max_pop))
    # for i in range(1, len(population_elite)):
    #   elite_offspring.append(croisement(population_elite[0], population_elite[i], max_pop))

    unique_elite_offspring.clear()
    for i in range(len(elite_offspring)):
      for j in range(len(elite_offspring[i])):
        if (elite_offspring[i][j] not in unique_elite_offspring):
          unique_elite_offspring.append(elite_offspring[i][j])



    if random.uniform(-(1/t), 0.1) > 0:
      unique_elite_offspring = mutation_L1(unique_elite_offspring, 0.5)


    population_mixte.clear()


    for i in range(len(unique_elite_offspring)):
      population_mixte.append(unique_elite_offspring[i])

    for i in range(len(population_elite)):
      if population_elite[i] not in population_mixte:
        population_mixte.append(population_elite[i])

    # for i in range(len(population_elite)):
    #   population_mixte.append(population_elite[i]) # no need, population elite is already produced in offsprings
    # population_mixte.append(generate_random_population(5,1)[0]) # g potential hyper parameter



    np_population_mixte = np.array([])
    np_population_mixte = np.array(population_mixte)
    arr2 = np_population_mixte

  for element in population_mixte_ranks[0]:
    pareto_population.append(get_chromosome(arr1, population_mixte_f1, element[0]))


  return (population_mixte_ranks, pareto_population)











