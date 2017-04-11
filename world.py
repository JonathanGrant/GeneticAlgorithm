#!/usr/bin/env python
from cosc343world import Creature, World
import numpy as np
import time
import random

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
        self.createRandomChromosome()

    def createRandomChromosome(self):
        self.chanceDoNothing = random.uniform(0, 0)
        self.chanceRandomMove = random.uniform(0, 0)
        self.chanceMoveAwayFromEnemy = random.uniform(1, 1)
        self.chanceMoveTowardsEnemy = random.uniform(0, 0)
        self.chanceEatGreenFood = random.uniform(0, 1)
        self.chanceEatRedFood = random.uniform(1, 1)
        self.chanceMoveTowardsGreenFood = random.uniform(0, 1)
        self.chanceMoveTowardsRedFood = random.uniform(1, 1)
        self.chanceMoveAwayFromFood = random.uniform(0, 0)
        self.chanceMoveAwayFromCreatures = random.uniform(0, 1)
        self.chanceMoveTowardsCreatures = random.uniform(0, 1)
        self.enemyScore = random.uniform(0, 3)
        self.creatureScore = random.uniform(0, 5)
        self.greenFoodScore = random.uniform(0, 5)
        self.redFoodScore = random.uniform(0, 40)
        self.eatingScore = random.uniform(0, 500)
        self.randomScore = random.uniform(0, 3)

    def printAll(self):
        #0.43613676307385285 0.09480247721914803 0.14494199420715725 0.9982520221847306 0.39173034657120165 9.223957249293935 0.34990401566364016 3.5577070638866806 0.0 0.33787175223470245 0.19659380842477236 0.7474487719141872 0.8973677806472418 0.08032722056099706 2.9058905688895247 3.3349320949598105 0.019542668723833256
        print(self.chanceDoNothing, self.chanceRandomMove, self.chanceMoveAwayFromEnemy, self.chanceMoveTowardsEnemy, self.chanceEatGreenFood, self.chanceEatRedFood, self.chanceMoveTowardsGreenFood, self.chanceMoveTowardsRedFood, self.chanceMoveAwayFromFood, self.chanceMoveAwayFromCreatures, self.chanceMoveTowardsCreatures, self.enemyScore, self.creatureScore, self.greenFoodScore, self.redFoodScore, self.eatingScore, self.randomScore)

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
        if random.uniform(0, 1) <= self.chromosome.chanceDoNothing:
            return actions
        actions[len(actions) - 1] = self.chromosome.randomScore
        if random.uniform(0, 1) <= self.chromosome.chanceRandomMove:
            return actions

        # Roll the dice on what to do.
        for i in range(0, 9):
            if percepts[i] == 0:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveAwayFromEnemy:
                    actions[i] += self.chromosome.enemyScore
            else:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveTowardsEnemy:
                    actions[i] += self.chromosome.enemyScore
        for i in range(9, 18):
            if percepts[i] == 0:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveAwayFromCreatures:
                    actions[i % 9] += self.chromosome.creatureScore
            else:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveTowardsCreatures:
                    actions[i % 9] += self.chromosome.creatureScore
        for i in range(18, 27):
            if percepts[i] == 0:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveAwayFromFood:
                    actions[i % 9] += self.chromosome.greenFoodScore + self.chromosome.redFoodScore
            elif percepts[i] == 1:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveTowardsGreenFood:
                    actions[i % 9] += self.chromosome.greenFoodScore
                if i == 22:
                    if random.uniform(0, 1) <= self.chromosome.chanceEatGreenFood:
                        actions[9] += self.chromosome.eatingScore
            else:
                if random.uniform(0, 1) <= self.chromosome.chanceMoveTowardsRedFood:
                    actions[i % 9] += self.chromosome.redFoodScore
                if i == 22:
                    if random.uniform(0, 1) <= self.chromosome.chanceEatRedFood:
                        actions[9] += self.chromosome.eatingScore
            
        
        return actions

def mateTwoParents(a, b):
    # ToDo - mutations
    c = MyCreature(a.numP, a.numA)
    c.chromosome = a.chromosome
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceDoNothing = b.chromosome.chanceDoNothing
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceRandomMove = b.chromosome.chanceRandomMove
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveAwayFromEnemy = b.chromosome.chanceMoveAwayFromEnemy
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveTowardsEnemy = b.chromosome.chanceMoveTowardsEnemy
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceEatGreenFood = b.chromosome.chanceEatGreenFood
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceEatRedFood = b.chromosome.chanceEatRedFood
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveTowardsGreenFood = b.chromosome.chanceMoveTowardsGreenFood
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveTowardsRedFood = b.chromosome.chanceMoveTowardsRedFood
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveAwayFromFood = b.chromosome.chanceMoveAwayFromFood
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveAwayFromCreatures = b.chromosome.chanceMoveAwayFromCreatures
    if random.uniform(0,1) <= 0.5:
        c.chromosome.chanceMoveTowardsCreatures = b.chromosome.chanceMoveTowardsCreatures
    if random.uniform(0,1) <= 0.5:
        c.chromosome.enemyScore = b.chromosome.enemyScore
    if random.uniform(0,1) <= 0.5:
        c.chromosome.creatureScore = b.chromosome.creatureScore
    if random.uniform(0,1) <= 0.5:
        c.chromosome.greenFoodScore = b.chromosome.greenFoodScore
    if random.uniform(0,1) <= 0.5:
        c.chromosome.redFoodScore = b.chromosome.redFoodScore
    if random.uniform(0,1) <= 0.5:
        c.chromosome.eatingScore = b.chromosome.eatingScore
    if random.uniform(0,1) <= 0.5:
        c.chromosome.randomScore = b.chromosome.randomScore
    return c

def createNewPopulationFromOld(oldPopulation):
    newPopulation = []
    oldPopulation.sort(key=lambda x: x.fitness, reverse=True)
    i = 0
    # Keep the survivors from last time
    while(oldPopulation[i].fitness >= 200):
        c = MyCreature(oldPopulation[i].numP, oldPopulation[i].numA)
        c.chromosome = oldPopulation[i].chromosome
        newPopulation.append(c)
        i+=1
    for i in range(len(newPopulation), len(oldPopulation)):
        # Randomly choose 50% of the old population
        randomPopulation = random.sample(oldPopulation, 2 * int(len(oldPopulation) / 4))
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
    global numTurns

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
        fitnessScore = 200
        # You can read the creature's energy at the end of the simulation.  It will be 0 if creature is dead
        energy = individual.getEnergy()

        # This method tells you if the creature died during the simulation
        dead = individual.isDead()

        # If the creature is dead, you can get its time of death (in turns)
        if dead:
            timeOfDeath = individual.timeOfDeath()
            fitnessScore = energy / 3 + timeOfDeath
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

    # The information gathered above should allow you to build a fitness function that evaluates fitness of
    # every creature.  You should show the average fitness, but also use the fitness for selecting parents and
    # creating new creatures.

    return createNewPopulationFromOld(old_population)

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
w.show_simulation(titleStr='Initial population', speed='fast')

for i in range(numGenerations):
    print("\nGeneration %d:" % (i+1))

    # Create a new population from the old one
    population = newPopulation(population)

    # Pass the new population to the world simulator
    w.setNextGeneration(population)

    # Run the simulation again to evalute the next population
    w.evaluate(numTurns)

    # Show visualisation of final generation
    if i==numGenerations-1:
        w.show_simulation(titleStr='Final population', speed='fast')


