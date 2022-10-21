import sys
sys.path.insert(0, '../exp_py/graphene')

import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
print(graphene.get('RMC', 'now'))

