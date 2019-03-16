#!/usr/local/bin/python3

import random
import numpy as np
import subprocess
import sys
from operator import attrgetter

def main():
    n_ind = 10 # The number of individuals in a population
    CXPB = 0.4 # The probability of crossover.
    MUTPB = 0.2 # The probability of individual mutation.
    NGEN = 10  # Then number of generation loop.

    random.seed(64)
    # --- Step1 : Create initial generation
    pop = create_pop(n_ind)
    set_fitness(evaluate, pop)
    best_ind = max(pop, key=attrgetter("fitness"))

    # --- Generation loop.
    print("Generation loop start.")
    print("Generation: 0. Best ind:" + best_ind.show())
    for g in range(NGEN):

        # --- Step2 : Selection
        offspring = selTournament(pop, n_ind, tournsize=3)

        # --- Step3 : Crossover
        crossover = []
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                child1, child2 = cxTwoPointCopy(child1, child2)
                child1.fitness = None
                child2.fitness = None
            crossover.append(child1)
            crossover.append(child2)
        offspring = crossover[:]

        # --- Step4 : Mutation.
        mutant = []
        for mut in offspring:
            if random.random() < MUTPB:
                mut.mutate()
                mut.fitness = None
            mutant.append(mut)

        # --- Update next population.
        pop = offspring[:]
        set_fitness(evaluate, pop)

        # --- Print best fitness in the population.
        best_ind = max(pop, key=attrgetter("fitness"))
        print("Generation: " + str(g+1) + ". Best ind:" + best_ind.show())

    print("Generation loop ended. best population")
    half_num = int(n_ind // 2)
    for people in sorted(pop, key=attrgetter("fitness"), reverse=True)[:half_num]:
        print("fitness: {0:3d}, ind:  {1}".format(people.fitness, people.show()))

class individual:
    fitness = None
    hp = 0
    attack = 0
    speed = 0
    def __init__(self, hp, attack, speed):
        self.hp = hp
        self.attack = attack
        self.speed = speed
    def mutate(self):
        """Mutation function"""
        use_param_num = 3      # 使用しているパラメータ数
        max_all_param = 100 # 今回使用するパラメータの全合計値
        val = max_all_param 
        self.hp = random.randint(1, val- use_param_num)
        self.attack = random.randint(1, val - (self.hp + 1))
        self.speed = val - (self.hp + self.attack)
    def show(self):
        return "hp:{0:3d}, attack:{1:3d}, speed:{2:3d}".format(self.hp, self.attack, self.speed)

def create_ind():
    """Create a individual"""
    use_param_num = 3      # 使用しているパラメータ数
    max_all_param = 100 # 今回使用するパラメータの全合計値
    val = max_all_param 
    hp = random.randint(1, val- use_param_num)
    attack = random.randint(1, val - (hp + 1))
    speed = val - (hp + attack)
    return individual(hp, attack, speed)

def create_pop(n_ind):
    """Create a population"""
    pop = []
    for i in range(n_ind):
        ind = create_ind()
        pop.append(ind)
    return pop

def set_fitness(eval_func, pop):
    """Set fitnesses of each individual in a population"""
    for ind in pop:
        ind.fitness = eval_func(ind, pop)

def evaluate(ind, pop):
    """Evaluate function"""
    win_num = 0
    program_name = './battle_prg/battle_game'
    challenger = '"{\\"name\\":\\"No01\\", \\"hp\\":' + str(ind.hp) + ', \\"attack\\":' + str(ind.attack) + ', \\"agility\\":' + str(ind.speed) + '}"'
    for tar in pop:
        target = '"{\\"name\\":\\"No02\\", \\"hp\\":' + str(tar.hp) + ', \\"attack\\":' + str(tar.attack) + ', \\"agility\\":' + str(tar.speed) + '}"'
        exec_battle = program_name + ' ' + challenger + ' ' + target
        result = subprocess.run(exec_battle, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        winner_name = result.stdout[2:4].decode()
        if (winner_name == "01"):
            win_num += 1
        # 攻守交代
        exec_battle = program_name + ' ' + target + ' ' + challenger
        result = subprocess.run(exec_battle, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        winner_name = result.stdout[2:4].decode()
        if (winner_name == "01"):
            win_num += 1
    print("win num: {}".format(win_num))
    return win_num

def selTournament(pop, n_ind, tournsize):
    """Selection function."""
    chosen = []
    for i in range(n_ind):
        aspirants = [random.choice(pop) for j in range(tournsize)]
        # 現世代からtournsize分のindをランダムに取得し、その中で最も強いものを次世代へ
        champ = max(aspirants, key=attrgetter("fitness"))
        chosen.append(champ)
    return chosen

def cxTwoPointCopy(ind1, ind2):
    """Crossover function.
    2点交叉とするため、順列での変換とする"""
    # 交叉する点を決める
    use_param_num = 3 # 使用しているパラメータ数
    change_param_num = random.randint(1, use_param_num - 1) # 変更するパラメータ数
    ind1.hp, ind2.hp = ind2.hp, ind1.hp
    if change_param_num >= 2:
        ind1.attack, ind2.attack = ind2.attack, ind1.attack
    return ind1, ind2

if __name__ == "__main__":
    main()
