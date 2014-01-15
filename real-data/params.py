dens = {'density':1000}
from numpy import loadtxt
seeds = [(p, dens) for p in loadtxt('seeds.txt')]
thresh = 0.00005
mu = 10**(-1)
power = 1
shape = (20, 100, 130)
output = 'result.pickle'
