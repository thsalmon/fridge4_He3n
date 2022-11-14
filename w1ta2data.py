import sys

from matplotlib import pyplot as plt
sys.path.insert(0, '../exp_py/graphene')

import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
graphene.set_cache('.graphene')
def time_set(t1, t2):
    temp=graphene.get_range('w1ta2:f1', t1-5*60, t2+9*60)
    volt=graphene.get_range('volt_h1', t1-5*60, t2+9*60)
    plt.figure(1)
    plt.clf()
    plt.plot(temp[0], temp[1])
    plt.savefig('1plot%d.png' %(t1))
    plt.figure(2)
    plt.clf()
    plt.plot(volt[0], volt[1], '*-')
    plt.savefig('2plot%d.png' %(t1))

time_set(1666345881, 1666345903)


'''
#convert unix time 
from datetime import datetime
ts = int('1666358760')
#gives time in UTC timezone 
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
'''