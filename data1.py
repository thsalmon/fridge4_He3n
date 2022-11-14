import sys
sys.path.insert(0, '../exp_py/graphene')

import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
graphene.set_cache('.graphene')
print(graphene.get('RMC', 'now'))
range=graphene.get_range('RMC', '1666357870', '1666358470')
print(range)

import numpy as np
np.savetxt("/Users/tinekesalmon/Documents/Pythonfiles/range1.txt", range)

#convert unix time 
from datetime import datetime
ts = int('1666358760')
#gives time in UTC timezone 
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

