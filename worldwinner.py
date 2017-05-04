#!/usr/bin/env python
from cosc343world import Creature, World
import numpy as np
import time
import random
import matplotlib.pyplot as plt
import math

# To keep track for the plot
avgFitnessOverTime = []
avgTurnsOverTime = []
numWinnersOverTime = []
lastPopulation = []
oldAvgFitness = 0
numGenerationsSinceSwitch = 0

# You can change this number to specify how many generations creatures are going to evolve over...
numGenerations = 500

# You can change this number to specify how many turns in simulation of the world for given generation
numTurns = 100

# You can change this number to change the percept format.  You have three choice - format 1, 2 and 3 (described in
# the assignment 2 pdf document)
perceptFormat=1

# You can change this number to chnage the world size
gridSize=24

# You can set this mode to True to have same initial conditions for each simulation in each generation.  Good
# for development, when you want to have some determinism in how the world runs from generatin to generation.
repeatableMode=False

class Chromosome:
    def __init__(self):
        self.enemyScore = random.randint(-100, 100)
        self.eatEnemyScore = random.randint(-100, 100)
        self.friendScore = random.randint(-50, 50)
        self.eatFriendScore = random.randint(-100, 100)
        self.goToFoodScore = random.randint(-100, 100)
        self.awayFromFoodScore = random.randint(-100, 100)
        self.eatFoodScore = random.randint(-100, 100)
        self.randomScore = random.randint(-100, 100)

    def printAll(self):
        print("     Enemy Score    : %d" % self.enemyScore)
        print("    Friend Score    : %d" % self.friendScore)
        print("   Go To Food Score : %d" % self.goToFoodScore)
        print("Away From Food Score: %d" % self.awayFromFoodScore)
        print("     Eat Score      : %d" % self.eatFoodScore)
        print("     Random Score   : %d" % self.randomScore)

# This is a class implementing you creature a.k.a MyCreature.  It extends the basic Creature, which provides the
# basic functionality of the creature for the world simulation.  Your job is to implement the AgentFunction
# that controls creature's behavoiur by producing actions in respons to percepts.
class MyCreature(Creature):

    # Initialisation function.  This is where you creature
    # should be initialised with a chromosome in random state.  You need to decide the format of your
    # chromosome and the model that it's going to give rise to
    #
    # Input: numPercepts - the size of percepts list that creature will receive in each turn
    #        numActions - the size of actions list that creature must create on each turn
    def __init__(self, numPercepts, numActions):
        self.numP = numPercepts
        self.numA = numActions

        # Place your initialisation code here.  Ideally this should set up the creature's chromosome
        # and set it to some random state.
        self.chromosome = Chromosome()
        #self.chromosome.printAll()
        # Do not remove this line at the end.  It calls constructors
        # of the parent classes.
        Creature.__init__(self)


    # This is the implementation of the agent function that is called on every turn, giving your
    # creature a chance to perform an action.  You need to implement a model here, that takes its parameters
    # from the chromosome and it produces a set of actions from provided percepts
    #
    # Input: percepts - a list of percepts
    #        numAction - the size of the actions list that needs to be returned
    def AgentFunction(self, percepts, numActions):
        actions = [0] * numActions
        actions[10] = self.chromosome.randomScore

        # The farther I am from an enemy, the better
        for i in range(0, 9):
            if percepts[i] != 0:
                if i == 4:
                    actions[9] += self.chromosome.eatEnemyScore * (100 - self.getEnergy())
                for j in range(0, 9):
                    actions[j] += Distance(j % 3, j / 3, i % 3, i / 3) * self.chromosome.enemyScore

        # The farther I am from a friend, the better, because then we won't fight over food.
        for i in range(9, 18):
            if percepts[i] != 0:
                for j in range(0, 9):
                    actions[j] += Distance(j % 3, j / 3, i % 3, (i - 9) / 3) * self.chromosome.friendScore

        # The closer I am to food, the better, because then I can eat.
        for i in range(18, 27):
            if percepts[i] != 0:
                if i == 22:
                    actions[9] += self.chromosome.eatFoodScore * (100 - self.getEnergy()) * percepts[i]
                for j in range(0, 9):
                    actions[j] -= Distance(j % 3, j / 3, i % 3, (i - 18) / 3) * self.chromosome.awayFromFoodScore * percepts[i]
                    if Distance(j % 3, j / 3, i % 3, (i - 18) / 3) == 0:
                        actions[j] += self.chromosome.goToFoodScore * (100 - self.getEnergy()) * percepts[i]

        
        return actions

def checkAndSwapGenerations(newGen, avgFitness, oldPopulation, oldAvgFitness, numGenerationsSinceSwitch):
    if oldPopulation and oldAvgFitness > avgFitness and (numGenerationsSinceSwitch <= 5 or avgFitness * 4 / 3 < oldAvgFitness):
        return oldPopulation, oldAvgFitness, numGenerationsSinceSwitch + 1
    return newGen, avgFitness, 0

def Distance(a1, a2, b1, b2):
    return math.sqrt((a1 - b1) * (a1 - b1) + (a2 - b2) * (a2 - b2))

def mateTwoParents(a, b):
    c = MyCreature(a.numP, a.numA)
    mutationChance = 0.001
    c.chromosome = a.chromosome
    if random.uniform(0,1) <= 0.5:
        c.chromosome.enemyScore = b.chromosome.enemyScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.enemyScore = random.randint(0, 100)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.eatEnemyScore = b.chromosome.eatEnemyScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.eatEnemyScore = random.randint(0, 100)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.friendScore = b.chromosome.friendScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.friendScore += random.randint(-5, 5)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.eatFriendScore = b.chromosome.eatFriendScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.eatFriendScore += random.randint(-5, 5)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.goToFoodScore = b.chromosome.goToFoodScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.goToFoodScore = random.randint(0, 100)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.awayFromFoodScore = b.chromosome.awayFromFoodScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.awayFromFoodScore = random.randint(0, 100)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.eatFoodScore = b.chromosome.eatFoodScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.eatFoodScore = random.randint(0, 100)
    if random.uniform(0,1) <= 0.5:
        c.chromosome.randomScore = b.chromosome.randomScore
    if random.uniform(0,1) <= mutationChance:
        c.chromosome.randomScore = random.randint(0, 100)
    return c

def rouletteWheelSelection(oldPopulation):
    newPopulation = []
    totalFitness = 0
    # Keep the survivors from last time
    oldPopulation.sort(key=lambda x: x.fitness, reverse=True)
    for i in range(0, len(oldPopulation)):
        if oldPopulation[i].fitness >= 1000:
            c = MyCreature(oldPopulation[i].numP, oldPopulation[i].numA)
            c.chromosome = oldPopulation[i].chromosome
            newPopulation.append(c)
        totalFitness += oldPopulation[i].fitness
    for i in range(len(newPopulation), len(oldPopulation)):
        randA = random.randint(0, int(totalFitness))
        randB = random.randint(0, int(totalFitness))
        A = None
        B = None
        currTotal = 0
        for i in range(0, len(oldPopulation)):
            currTotal += oldPopulation[i].fitness
            if currTotal >= randA:
                A = oldPopulation[i]
            if currTotal >= randB:
                B = oldPopulation[i]
            if A and B:
                newPopulation.append(mateTwoParents(A, B))
                break
    return newPopulation

def tournamentSelection(oldPopulation):
    newPopulation = []
    # Keep the survivors from last time
    oldPopulation.sort(key=lambda x: x.fitness, reverse=True)
    i = 0
    while(oldPopulation[i].fitness >= 1000):
        c = MyCreature(oldPopulation[i].numP, oldPopulation[i].numA)
        c.chromosome = oldPopulation[i].chromosome
        newPopulation.append(c)
        i+=1
    for i in range(len(newPopulation), len(oldPopulation)):
        # Randomly choose 75% of the old population
        randomPopulation = random.sample(oldPopulation, int(len(oldPopulation) / 2))
        randomPopulation.sort(key=lambda x: x.fitness, reverse=True)
        newPopulation.append(mateTwoParents(randomPopulation[0], randomPopulation[1]))
    return newPopulation

# This function is called after every simulation, passing a list of the old population of creatures, whose fitness
# you need to evaluate and whose chromosomes you can use to create new creatures.
#
# Input: old_population - list of objects of MyCreature type that participated in the last simulation.  You
#                         can query the state of the creatures by using some built-in methods as well as any methods
#                         you decide to add to MyCreature class.  The length of the list is the size of
#                         the population.  You need to generate a new population of the same size.  Creatures from
#                         old population can be used in the new population - simulation will reset them to starting
#                         state.
#
# Returns: a list of MyCreature objects of the same length as the old_population.
def newPopulation(old_population):
    global numTurns, oldAvgFitness, lastPopulation, numGenerationsSinceSwitch

    nSurvivors = 0
    avgLifeTime = 0
    fitnessScoreList = []

    # For each individual you can extract the following information left over
    # from evaluation to let you figure out how well individual did in the
    # simulation of the world: whether the creature is dead or not, how much
    # energy did the creature have a the end of simualation (0 if dead), tick number
    # of creature's death (if dead).  You should use this information to build
    # a fitness function, score for how the individual did
    for individual in old_population:
        fitnessScore = 1000
        # You can read the creature's energy at the end of the simulation.  It will be 0 if creature is dead
        energy = individual.getEnergy()

        # This method tells you if the creature died during the simulation
        dead = individual.isDead()

        # If the creature is dead, you can get its time of death (in turns)
        if dead:
            timeOfDeath = individual.timeOfDeath()
            fitnessScore = energy / 4 + timeOfDeath / 2
            avgLifeTime += timeOfDeath
        else:
            nSurvivors += 1
            avgLifeTime += numTurns
            fitnessScore += energy
            #individual.chromosome.printAll()
        fitnessScoreList.append(fitnessScore)
        individual.fitness = fitnessScore

    # Here are some statistics, which you may or may not find useful
    avgLifeTime = float(avgLifeTime)/float(len(population))
    avgFitness = float(sum(fitnessScoreList)) / float(len(population))
    print("Simulation stats:")
    print("  Survivors    : %d out of %d" % (nSurvivors, len(population)))
    print("  Avg life time: %.1f turns" % avgLifeTime)
    print("  Avg fitness  : %.1f points" % avgFitness)
    print("oldAvg fitness : %.1f points" % oldAvgFitness)

    avgFitnessOverTime.append(avgFitness)
    avgTurnsOverTime.append(avgLifeTime)
    numWinnersOverTime.append(nSurvivors)

    # The information gathered above should allow you to build a fitness function that evaluates fitness of
    # every creature.  You should show the average fitness, but also use the fitness for selecting parents and
    # creating new creatures.

    # Here we decide if we want to make babies of the newer gen, or the older and (maybe) better gen
    lastPopulation, oldAvgFitness, numGenerationsSinceSwitch = checkAndSwapGenerations(old_population, avgFitness, lastPopulation, oldAvgFitness, numGenerationsSinceSwitch)

    return tournamentSelection(lastPopulation)
    # return rouletteWheelSelection(lastPopulation)

# Create the world.  Representaiton type choses the type of percept representation (there are three types to chose from);
# gridSize specifies the size of the world, repeatable parameter allows you to run the simulation in exactly same way.
w = World(representationType=perceptFormat, gridSize=gridSize, repeatable=repeatableMode)

#Get the number of creatures in the world
numCreatures = w.maxNumCreatures()

#Get the number of creature percepts
numCreaturePercepts = w.numCreaturePercepts()

#Get the number of creature actions
numCreatureActions = w.numCreatureActions()

# Create a list of initial creatures - instantiations of the MyCreature class that you implemented
population = list()
for i in range(numCreatures):
   c = MyCreature(numCreaturePercepts, numCreatureActions)
   population.append(c)

# Pass the first population to the world simulator
w.setNextGeneration(population)

# Runs the simulation to evalute the first population
w.evaluate(numTurns)

# Show visualisation of initial creature behaviour
# w.show_simulation(titleStr='Initial population', speed='fast')

for i in range(numGenerations):
    print("\nGeneration %d:" % (i+1))

    # Create a new population from the old one
    population = newPopulation(population)

    # Pass the new population to the world simulator
    w.setNextGeneration(population)

    # Run the simulation again to evalute the next population
    w.evaluate(numTurns)

    # Show visualisation of final generation
    # if i==numGenerations-1:
    #     w.show_simulation(titleStr='Final population', speed='fast')


plt.plot(avgFitnessOverTime)
plt.show()


