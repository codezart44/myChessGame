import random
from time import time


random.seed(2)

import json




with open('./constants/bishop_occupancy_attacks.json', 'r') as f:
    bishop_occupancy_attacks = json.load(f)

for i in range(len(bishop_occupancy_attacks)):
    map = bishop_occupancy_attacks[i]
    bishop_occupancy_attacks[i] = {int(k): v for k,v in map.items()}

with open('./constants/rook_occupancy_attacks.json', 'r') as f:
    rook_occupancy_attacks = json.load(f)
    
for i in range(len(rook_occupancy_attacks)):
    map = rook_occupancy_attacks[i]
    rook_occupancy_attacks[i] = {int(k): v for k,v in map.items()}


with open('./constants/attack_maps.py', 'w') as f:
    f.writelines('BISHOP_OCCUPANCY_ATTACK_MAP = [\n')
    for map in bishop_occupancy_attacks:
        f.writelines('\t' + '{\n')
        for k, v in map.items():
            f.writelines('\t\t' +f'{k}: {v}' + ',\n')
        f.writelines('\t' + '},\n')
    f.writelines(']\n')

    f.writelines('\n\nROOK_OCCUPANCY_ATTACK_MAP = [\n')
    for map in rook_occupancy_attacks:
        f.writelines('\t' + '{\n')
        for k, v in map.items():
            f.writelines('\t\t' +f'{k}: {v}' + ',\n')
        f.writelines('\t' + '},\n')
    f.writelines(']\n')

    