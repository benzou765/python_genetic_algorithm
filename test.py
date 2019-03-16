#!/usr/local/bin/python3

import subprocess

program_name = './battle_prg/battle_game'
i = 0
j = 1
argument1 = '"{\\"name\\":\\"No' + str(i) + '\\", \\"hp\\": 50, \\"attack\\": 10, \\"agility\\": 9}"'
argument2 = '"{\\"name\\":\\"No' + str(j) + '\\", \\"hp\\": 50, \\"attack\\": 9, \\"agility\\": 10}"'

exec_battle = program_name + ' ' + argument1 + ' ' + argument2

#print(exec_battle)

result = subprocess.call(exec_battle, shell=True)
