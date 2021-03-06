import pickle, numpy, itertools, math
from copy import copy

fin = 'data/mat0'
MAXSIZE = 4

# want to max
def minsavings(alloc, sourced):
	return min([sourced[i] - alloc[i] for i in xrange(len(alloc))])

def maxsavings(alloc, sourced):
	return max([sourced[i] - alloc[i] for i in xrange(len(alloc))])

# want to min
def squaresavings(alloc, sourced):
	return numpy.var([sourced[i] - alloc[i] for i in xrange(len(alloc))])

def CEG(sourced, vn):
	sourced = list(sourced)
	alloc = [0] * 9
	chosen = min(sourced)
	while chosen < vn / len([x for x in sourced if x != 999999]):
		cindex = list(sourced).index(chosen)
		alloc[cindex] = chosen
		vn -= chosen
		sourced[cindex] = 999999
		chosen = min(sourced)
		print alloc
	mean = vn / len([x for x in sourced if x != 999999])
	for i in xrange(len(alloc)):
		if alloc[i] == 0:
			alloc[i] = mean
	return alloc

def CEL(sourced, vn):
	sourced = list(sourced)
	alloc = [-1] * 9
	chosen = min(sourced)
	savings = sum(sourced) - vn
	while chosen < savings / len([x for x in sourced if x != 999999]):
		cindex = list(sourced).index(chosen)
		alloc[cindex] = 0
		vn -= chosen
		sourced[cindex] = 999999
		chosen = min(sourced)
		print alloc
	mean = savings / len([x for x in sourced if x != 999999])
	for i in xrange(len(alloc)):
		if alloc[i] == -1:
			alloc[i] = sourced[i] - mean
	return alloc

def PROP(sourced, vn):
	return sourced * vn / float(sum(sourced))

def list2st(list):
	res = 0
	for i in list:
		res += 1<<i
	return res

def SHAPLEY(sourced, vn, finalgroups, groups):
	groups[0] = 0
	alloc = [0] * len(sourced)
	for groupnum in finalgroups[(1<<len(sourced))-1]:
		group = []
		for i in xrange(len(sourced)):
			if (1<<i) & groupnum:
				group.append(i)
		for member in group:
			perms = itertools.permutations(group)
			marginal = 0.0
			for perm in perms:
				marginal += groups[list2st(perm[0:1+perm.index(member)])] -\
					groups[list2st(perm[0:perm.index(member)])]
			alloc[member] = marginal / math.factorial(len(group))
	return alloc


def popcount(x):
	return bin(x).count('1')

def main():
	omat = numpy.array(pickle.load(open(fin, 'r')))
	sourced = omat[0,1:]
	dim = len(sourced)
	mat = omat[1:,1:]
	groups = {}
	finals = {}
	finalgroups = {}
	validst = []
	for st in xrange(1 << dim):
		if popcount(st) <= MAXSIZE and st != 0:
			validst.append(st)
	for st in validst:
		mi = 999999999
		pl = []
		for i in xrange(dim):
			if((st >> i) & 1):
				pl.append(i)
		perms = itertools.permutations(pl)
		for perm in perms:
			d = sourced[perm[0]]
			for i in xrange(1, len(perm)):
				d += mat[perm[i-1]][perm[i]]
			mi = min(mi, d)
		groups[st] = mi
	for st in xrange(1 << dim):
		if st == 0:
			finals[st] = 0
			finalgroups[st] = []
			continue
		best = 99999999999
		bestgroup = None
		for group in validst:
			if group & st == group:
				curr = finals[st-group] + groups[group]
				if best > curr:
					best = curr
					bestgroup = group
		finals[st] = best
		finalgroups[st] = finalgroups[st-bestgroup] + [bestgroup]
	vn = finals[(1<<dim) - 1]
	print finalgroups[(1<<dim) - 1]
	print vn
	print sum(sourced)
	print sourced
	ceg = CEG(sourced, vn)
	print ceg
	cel = CEL(sourced, vn)
	print cel
	prop = PROP(sourced, vn)
	print prop
	shapley = SHAPLEY(sourced, vn, finalgroups, groups)
	print shapley
	print minsavings(ceg, sourced)
	print maxsavings(ceg, sourced)
	print squaresavings(ceg, sourced)
	print minsavings(cel, sourced)
	print maxsavings(cel, sourced)
	print squaresavings(cel, sourced)
	print minsavings(prop, sourced)
	print maxsavings(prop, sourced)
	print squaresavings(prop, sourced)
	print minsavings(shapley, sourced)
	print maxsavings(shapley, sourced)
	print squaresavings(shapley, sourced)

if __name__ == '__main__':
	main()