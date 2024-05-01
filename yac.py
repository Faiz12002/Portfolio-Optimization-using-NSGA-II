# EN: All the necessary imports 
# FR: tout les packages necessaires
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# EN: Domination Relation 
# FR: Releation de Domination

  # EN: dominates(a: tuple, b: tuple, obj: str) : returns Boolean
  # FR: dominates(a: tuple, b: tuple, obj: str) : retourne un Boulean  
def dominates(a,b,obj):
  """
  a: tuple
  b: tuple
  obj: str

  return: bool
  """
  if obj == 'max':
    if ( (a[0] >= b[0] and a[1] >= b[1]) and (a[0] > b[0] or a[1] > b[1]) ):
      return True
  elif obj == 'min':
    if ( (a[0] <= b[0] and a[1] <= b[1]) and (a[0] < b[0] or a[1] < b[1]) ):
      return True
  # EN: isnondominated(a: tuple, b: tuple) : returns  Boolean
  # FR: isnondominated(a: tuple, b: tuple) : retourne un Boulean
def isnondominated(a,b):
  """
  a: tuple
  b: tuple

  return: bool
  """
  if ((a[0] > b[0] and a[1] < b[1]) or (a[0] < b[0] and a[1] > b[1])):
    return True
  elif a[0] == b[0] and a[1] == b[1]:
    return True
  else:
    return False
  # EN: DominationRelation(a: tuple, b: tuple, obj: str) : returns True or 'ND'
  # FR: DominationRelation(a: tuple, b: tuple, obj: str) : retourne True ou 'ND'
def DominationRelation(a,b,obj):
  """
  a: tuple
  b: tuple
  obj: str

  return: True (bool), "ND" (str)
  """
  if dominates(a,b,obj):
    return True
  elif isnondominated(a,b):
    return 'ND'
  # EN: check_dominance(arr: list) : retuns Boolean
  # FR: check_dominance(arr: list) : retourne un boulean
def check_dominance(arr):
    """
    arr: list

    return: bool
    """
    for element in arr:
        if element != True and element != "ND":
            return False
    return True

# EN: Non dominated sorting 
# FR: Le tri non dominé

  #EN: non_dominated_sorting(f1: list, f2: list): returns a list of tuples
  #FR: non_dominated_sorting(f1: list, f2: list): retourne une liste des tuples
def non_dominated_sorting(f1, f2):
  """
  f1: list
  f2: list

  return: list 
  """
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

#EN: Crowding distance
#FR: Distance de repartition

  #EN: crowding_distance(F1: list, F2: list, front_index: int): returns a dict of distances
  #FR: crowding_distance(F1: list, F2: list, front_index: int): retourne un dictionaire des distances
def crowding_distance(F1, F2, front_index):
  """
  F1: list
  F2: list
  front_index: int

  return: dict
  """
  ranks = non_dominated_sorting(F1, F2)
    #EN: We want to calculate crowding distance for the desired front
    #FR: Nous voulons calculer la distance de repatition pour le front desire
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

#EN: Generate inital random population
#FR: Generer aleatoirement une population initiale 

  #EN: generate_random_population(size: int, n: int) : returns a list of lists
  #FR: generate_random_population(size: int, n: int) : retourne une liste des listes
def generate_random_population(size, n):
    """
    size: int
    n: int

    return: list
    """
    #EN: size is the length of w (length of the solution), n is the number of solutions
    #FR: size est la longueur de w (taille de la solution), n est le nombre des solutions
    solutions = []

    for _ in range(n):
      #EN: Generate a vector of random values between 0 and 1
      #FR: Genere un vecteur de valeurs aleatoires entre 0 et 1
        random_poids = np.random.rand(size)  
      #EN: Divide all the values by the sum so that the sum of the weights equals 1
      #FR: Divise toutes les valeurs par la somme pour que la somme des poids soit egale a 1
        random_poids /= np.sum(random_poids)
        #EN: uniqueness of the individual
        #FR: unicite de l'individu  
        if (list(np.round(random_poids, 4)) not in solutions): 
          #EN: 4 numbers after ,
          #FR: 4 nombres apres ,
          solutions.append(list(np.round(random_poids, 4))) 

    return solutions
    
#EN: Fitness calculation
#FR: Calculation de fitness

  #EN: massFitness(w: numpy.ndarray, E: numpy.ndarray, V: numpy.ndarray) : Return a tuple containing 2 lists
  #FR: massFitness(w: numpy.ndarray, E: numpy.ndarray, V: numpy.ndarray) : retourne tuple contenant 2 listes 
def massFitness(w, E, V):
    """
    w: numpy.ndarray
    E: numpy.ndarray
    V: numpy.ndarray

    return: tuple
    """
#EN: E: vector of expectations
    #V: covariance matrix
    #w: vector of weights
#FR: E: vecteur des esperances
    #V: matrice de variance covariance
    #w: vecteur des poids

    f1 = []
    f2 = []
#EN: calculation of f1=E(r_p)
#FR: calcul de f1=E(r_p)
    for i in range(len(w)):
      #EN: Compatible sizes
      #FR: Les taille compatible
      assert w[i].shape[0] == E.shape[0]  
      f1.append(round(np.dot(w[i],E),4))
#EN: calculation of f2 = Var(r_p)
#FR: Calcul f2 = Var(r_p)
    for i in range(len(w)):
      assert w[i].shape[0] == V.shape[0] == V.shape[1] #les tailles compatible
      f2.append(round(np.dot(w[i],np.dot(V, w[i])),4))

    return (f1,f2)

#EN: Crossover function
#FR: Fonction croisement
def croisement(parent1, parent2, c):
  """
  parent1: list
  parent2: list
  c: int

  return: list
  """
  #EN:  c upper bound
        #parent1 solution
        #parent2 solution
  #FR:  c borne sup
        #parent1 solution
        #parent2 solution

    #EN: The parents should have the same length
    #FR: Les parents doivent avoir la meme longueur
  assert len(parent1) == len(parent2)
    #EN: Initialize a list to store the descendants
    #FR: Initialiser une liste pour stocker les descendants
  descendants = []
  counter = 0
  while counter != 100:
    #EN: Choose a random crossover point
    #FR: Choisir un point de croisement aleatoire
    point_de_croisement = random.randint(1, len(parent1) - 1)
    #EN: Create a descendant by combining parts of both parents
    #FR: Creer un descendant en combinant des parties des deux parents
    if (random.uniform(0,1) < 0.5):
      offspring = parent1[:point_de_croisement] + parent2[point_de_croisement:]
    else:
      offspring = parent1[point_de_croisement:] + parent2[:point_de_croisement]
    #EN: Check if the descendant is already in the list
    #FR: Verifier si le descendant est deja dans la liste
    if offspring not in descendants:
      #EN: Check if the sum is equal to or less than 1
      #FR: Verifier si la somme est egale ou inferieur a 1
      if sum(offspring) <= 1:
        descendants.append(offspring)
    counter +=1

  return descendants[0:c]
  
# mutation1 

  #EN: mutation1(offspring: list) : returns a list
  #FR: mutation1(offspring: list) : retourne une liste
def mutation1(offspring):
    """
    offspring: list

    return: list
    """
    random_ind = random.randint(0, len(offspring)-1)
    offspring[random_ind] = offspring[random_ind] * 0.9
    return offspring

# mutation_L1

  #EN: mutation_L1(sequence: list of lists, m: int): returns list of lists 
  #FR: mutation_L1(sequence: list of lists, m: int): retourne un liste des listes
def mutation_L1(sequence, m):
    """
    sequence: list
    m: float

    return: list
    """
    #EN: Check if m is between 0 and 1
    #FR: Verifier si m est entre 0 et 1
    assert 0 <= m <= 1 

    has_negative = False
    for row in sequence:
      for element in row:
        if element < 0:
          has_negative = True
          break
        if has_negative:
          raise ValueError("The sequence contains at least one negative value.")


    sequence_mutée = []
    #EN: Copy the original sequence to maintain the unchanged individuals
    #FR: Copier la séquence originale pour maintenir les individus non mutés
    sequence_mutée = sequence.copy()
    #EN: Individual to mutate (random selection)
    #FR: Individu à muter (sélection aléatoire)
    individu_index = random.randint(0, len(sequence)-1)
    individu = sequence[individu_index].copy()  # Make a copy of the selected individual
    #EN: Selects deux distinct indices randomly
    #FR: Sélectionner deux indices distincts de manière aléatoire
    indices = random.sample(range(len(individu)), 2)
    #EN: Generate a random number between 0 and 1
    #FR: Générer un nombre aléatoire entre 0 et 1
    rand = random.random()
    #EN: If the random number is less or equal to mutation rate, perform the mutation.
    #FR: Si le nombre aléatoire est inférieur ou égal au taux de mutation, effectuer la mutation.
    if rand <= m:
        #EN: Calculation of mutation value
        #FR: Calculer la mutation
        mutation_value = rand * (min(individu) if rand < 0.5 else (1 - max(individu)))
        #EN: Add or subtract the mutation value to selected elements.
        #FR: Ajouter ou soustraire la mutation aux éléments sélectionnés.
        individu[indices[0]] += mutation_value
        individu[indices[1]] -= mutation_value
    else:
        individu[indices[0]], individu[indices[1]] = individu[indices[1]], individu[indices[0]]
        #EN: Ensure that the w values remain within [0, 1] and the sum is 1
        #FR: S'assurer que les w restent dans [0, 1] et la somme est 1
    for i in range(len(individu)):
      individu[i] = max(0, min(1, individu[i]))
    if sum(individu) < 1:
      individu[indices[0]] += 1 - sum(individu)
    elif sum(individu) > 1:
      individu[indices[0]] -= 1 - sum(individu)
    #EN: Replace the mutated individual in the mutated sequence.
    #FR: Remplacer l'individu muté dans la séquence mutée
    sequence_mutée[individu_index] = individu

    return sequence_mutée

# EN: get_chromosome(P: list of lists, f1: list, target: int) : returns a list
# FR: get_chromosome(P: liste de listes, f1: liste, target: entier) : retourne une liste
def get_chromosome(P,f1,target):
  """
  P: list 
  f1: list
  target: int
  """
  for i in range(len(f1)):
    if f1[i] == target:
      return P[i]
      #EN: returns one element float type
      #FR: retourne un element de type reel 

      #EN: inputs one element of list type that contains elements of list type and one element of list type and one element of float type
      #FR: saisie un element de type liste qui contient des elements de type liste, et un element de type liste, et un nombre reel

#EN: NSGA-II function, that inputs mean vector, covariance matrix, maximum initial population, population size, diversity degree and mutation rate. Upper bound for crossover is set to max
#FR: la fonction NSGA-II, saisie le vecteur des esperances, matrice de covariance, nombre de population initiale, degré de diversité et le taux de mutation. La borne sup pour le croisement est definie max

def NSGA2(E, V, max_gen, max_pop, pop_size, divd, t): 
  """
  E: numpy.ndarray
  V: numpy.ndarray
  max_gen: int
  max_pop: int
  pop_size: int 
  divd: int 
  t: float

  return: tuple
  """
  #EN: Check if mutation rate is between 0 and 1 
  #FR: Verifier si le taux de mutation est entre 0 et 1
  assert 0 < t < 1, "Mutation rate must be between 0 and 1"
  #EN: Generate random population
  #FR: Générer une population aléatoire
  population = generate_random_population(pop_size, max_pop)
  np_population = np.array(population)


  #EN: Calculate the fitness of each population
  #FR: Calculer le fitness de chaque population
  population_fitness = massFitness(np_population, E, V)
  population_f1 = population_fitness[0]
  population_f2 = population_fitness[1]
  #EN: Perform non-dominated sorting
  #FR: Effectuer le tri non-dominé
  population_ranks = non_dominated_sorting(population_f1, population_f2)
  #EN: Select parents front first front
  #FR: Sélectionner les parents à partir du premier front
  for i in range(len(population_ranks)):
    if (len(population_ranks[i]) > 1):
      fitness_parent1 = population_ranks[i][0]
      fitness_parent2 = population_ranks[i][1]
      break
    if (len(population_ranks[i]) == 1):
      fitness_parent1 = population_ranks[i][0]
      fitness_parent2 = population_ranks[i+1][0]
      break
  #EN: Get the parents chromosomes according to their fitness 
  #FR: Obtenir les chromosomes des parents selon leur fitness
  member_parent1 = get_chromosome(population, population_f1, fitness_parent1[0])
  member_parent2 = get_chromosome(population, population_f1, fitness_parent2[0])


  #EN: Crossover between parents and produce max offspring
  #FR: Croisement entre les parents and produire le maximum de descendants
  population_offspring = croisement(member_parent1, member_parent2, max_pop)

  #EN: Mutation if number is positive using mutation1
  #FR: Mutation si le nombre est positif en utilisant mutation1
  for i in range(len(population_offspring)):
    if random.uniform(-(1/t), 0.1) > 0:
      population_offspring[i] = mutation1(population_offspring[i])

  #EN: Initiate mixed population
  #FR: Initier une population mixte
  population_mixte = population + population_offspring
  np_population_mixte = np.array(population_mixte)


  population_mixte_ranks = []
  population_mixte_ranks_distances = []
  population_elite = []
  population_elite_fitness = []
  pareto_population = []
  elite_offspring = []
  unique_elite_offspring = []

  #EN: The big loop 
  #FR: La grande boucle
  for i in range(max_gen+1):

    arr1 = np_population_mixte
    #EN: Calculate fitness of mixed population
    #FR: "Calculer le fitness de la population mixte.
    population_mixte_fitness = ()
    population_mixte_fitness = massFitness(np_population_mixte, E, V)
    population_mixte_f1 = population_mixte_fitness[0]
    population_mixte_f2 = population_mixte_fitness[1]

    #EN: Perform non-dominated sorting
    #FR: Effectuer un tri non dominé.
    population_mixte_ranks.clear()
    population_mixte_ranks = non_dominated_sorting(population_mixte_f1, population_mixte_f2)

    #EN: Calculate crowding distance
    #FR: "Calculer la distance de répartition
    population_mixte_ranks_distances.clear()
    for i in range(len(population_mixte_ranks)):
      population_mixte_ranks_distances.append(crowding_distance(population_mixte_f1, population_mixte_f2, i))




    population_elite.clear()
    population_elite_fitness.clear()



    #EN: Select elite points based on crowding distance from highest to lowest distance, from first front to last front, the number of points is denoted divd.
    #FR: Sélectionner les points d'élite en fonction de la distance de répartition, de la plus grande à la plus petite distance, du premier front au dernier front, le nombre de points est indiqué par divd.
    for i in range(len(population_mixte_ranks)):
      if (len(population_elite_fitness) == divd):
        break
      for j in range(0,divd):
        if (j >= len(list(population_mixte_ranks_distances[i].keys()))):
          continue
        population_elite_fitness.append(population_mixte_ranks[i][list(population_mixte_ranks_distances[i].keys())[j]])



    #EN: Get chromosomes of elite population
    #FR: Obtenir les chromosomes de la population d'élite.
    for element in population_elite_fitness:
      population_elite.append(get_chromosome(population_mixte, population_mixte_f1, element[0]))


    #EN: Mate best chromosome with divd-1 chromosomes 
    #FR: Accoupler le meilleur chromosome avec divd-1 chromosomes.
    elite_offspring.clear()
    for i in range(1,divd):
      elite_offspring.append(croisement(population_elite[0], population_elite[i], max_pop))

    #EN: Only take unique offspring in case there are twins
    #FR: Ne prendre que des descendants uniques en cas de jumeaux.
    unique_elite_offspring.clear()
    for i in range(len(elite_offspring)):
      for j in range(len(elite_offspring[i])):
        if (elite_offspring[i][j] not in unique_elite_offspring):
          unique_elite_offspring.append(elite_offspring[i][j])


    #EN: Perform mutation if we got a positive number using mutation_L1
    #FR: Effectuer une mutation si nous obtenons un nombre positif en utilisant mutation_L1
    if random.uniform(-(1/t), 0.1) > 0:
      unique_elite_offspring = mutation_L1(unique_elite_offspring, 0.5)


    population_mixte.clear()

    #EN: Make new generation of mixed population
    #FR: Créer une nouvelle génération de population mixte.
    for i in range(len(unique_elite_offspring)):
      population_mixte.append(unique_elite_offspring[i])

    for i in range(len(population_elite)):
      if population_elite[i] not in population_mixte:
        population_mixte.append(population_elite[i])

    #EN: Optional: you can add a new random individual after that
      # population_mixte.append(generate_random_population(5,1)[0]) # g potential hyper parameter
    #FR: Optionnel : vous pouvez ajouter un nouvel individu aléatoire après cela
      # population_mixte.append(generate_random_population(5,1)[0]) # g Hyperparamètre potentiel

    
    np_population_mixte = np.array([])
    np_population_mixte = np.array(population_mixte)
    arr2 = np_population_mixte
  # EN: Extract pareto population in the last generation
  # FR: Extraire la population de Pareto dans la dernière génération
  for element in population_mixte_ranks[0]:
    pareto_population.append(get_chromosome(arr1, population_mixte_f1, element[0]))


  return (population_mixte_ranks, pareto_population)