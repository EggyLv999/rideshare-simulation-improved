import pickle, numpy, itertools, math
from copy import copy

MAXSIZE = 4

SIZ = 9
A_LOT = 999999

# want to max
def minsavings(alloc, sourced):
	return min([sourced[i] - alloc[i] for i in xrange(len(alloc))])

def maxsavings(alloc, sourced):
	return max([sourced[i] - alloc[i] for i in xrange(len(alloc))])

# want to min
def varsavings(alloc, sourced):
	return numpy.std([sourced[i] - alloc[i] for i in xrange(len(alloc))])

def CEG(sourced, vn):
	vn = float(vn)
	sourced = list(sourced)
	alloc = numpy.zeros(SIZ)
	chosen = min(sourced)
	while chosen < vn / len([x for x in sourced if x != A_LOT]):
		cindex = list(sourced).index(chosen)
		alloc[cindex] = chosen
		vn -= chosen
		sourced[cindex] = A_LOT
		chosen = min(sourced)
	mean = vn / len([x for x in sourced if x != A_LOT])
	for i in xrange(len(alloc)):
		if alloc[i] == 0:
			alloc[i] = mean
	return alloc

def CEL(sourced, vn):
	vn = float(vn)
	sourced = list(sourced)
	alloc = numpy.full(SIZ, -1)
	chosen = min(sourced)
	savings = sum(sourced) - vn
	while chosen < savings / len([x for x in sourced if x != A_LOT]):
		cindex = list(sourced).index(chosen)
		alloc[cindex] = 0
		sourced[cindex] = A_LOT
		savings -= chosen
		chosen = min(sourced)
	mean = savings / len([x for x in sourced if x != A_LOT])
	for i in xrange(len(sourced)):
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

def st2list(st):
	group = []
	for i in xrange(SIZ):
		if (1<<i) & st:
			group.append(i)
	return group

def groupify(allocator):
	def GROUPED(sourced, vn, finalgroups, groups):
		groups[0] = 0
		alloc = numpy.zeros(len(sourced))
		for groupnum in finalgroups[(1<<len(sourced))-1]:
			group = []
			for i in xrange(len(sourced)):
				if (1<<i) & groupnum:
					group.append(i)
			groupalloc = allocator(numpy.array([sourced[i] for i in group]), groups[groupnum])
			gaind = 0
			for i in group:
				alloc[i] = groupalloc[gaind]
				gaind += 1
		return alloc
	return GROUPED

def SHAPLEY(sourced, vn, finalgroups, groups):
	groups[0] = 0
	alloc = numpy.zeros(len(sourced))
	for groupnum in finalgroups[(1<<len(sourced))-1]:
		group = st2list(groupnum)
		for member in group:
			perms = itertools.permutations(group)
			marginal = 0.0
			for perm in perms:
				# if len(group) == 2:
				# 	print perm[0:1+perm.index(member)]
				# 	print groups[list2st(perm[0:1+perm.index(member)])]
				# 	print perm[0:perm.index(member)]
				# 	print groups[list2st(perm[0:perm.index(member)])]
				# if 1+perm.index(member) == len(group):
				# 	marginal += groups[groupnum] -\
				# 		groups[list2st(perm[0:perm.index(member)])]
				# else:
				marginal += groups[list2st(perm[0:1+perm.index(member)])] -\
						groups[list2st(perm[0:perm.index(member)])]
			alloc[member] = marginal / math.factorial(len(group))
	return alloc


def popcount(x):
	return bin(x).count('1')

def printarr(a):
	s = ''
	for i in xrange(len(a)):
		for j in xrange(len(a[0])):
			s += str(a[i][j]) + '\t'
		s += '\n'
	print s

def main():
	allocations = [[], [], [], [], []]
	statistics = [[], [], [], [], []]
	fullallocations = []
	fullstatistics = []
	suc = 0
	fail = 0
	# for run in xrange(210, 211):
	for run in xrange(423):
		# print run
		omat = numpy.array(pickle.load(open('data2/mat{}'.format(run), 'r')))
		# print omat
		osourced = omat[0,1:]
		dim = len(osourced)
		s2d = [(osourced[i], i) for i in xrange(dim)]
		s2d.sort(key=lambda a: a[0])
		mat = numpy.zeros((dim, dim))
		sourced = numpy.array([-1 for k in xrange(dim)])
		for i in xrange(SIZ):
			sourced[i] = s2d[i][0]
		for i in xrange(SIZ):
			for j in xrange(SIZ):
				mat[i][j] = omat[s2d[i][1]+1][s2d[j][1]+1]
		# print s2d
		# print sourced
		# print mat
		groups = {}
		finals = {}
		finalgroups = {}
		validst = []
		for st in xrange(1 << dim):
			if popcount(st) <= MAXSIZE and st != 0:
				validst.append(st)
		for st in validst:
			mi = A_LOT
			pl = st2list(st)
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
		GCEG = groupify(CEG)
		GCEL = groupify(CEL)
		GPROP = groupify(PROP)
		ceg = GCEG(sourced, vn, finalgroups, groups)
		cel = GCEL(sourced, vn, finalgroups, groups)
		prop = GPROP(sourced, vn, finalgroups, groups)
		shapley = SHAPLEY(sourced, vn, finalgroups, groups)
		for groupnum in finalgroups[(1<<len(sourced))-1]:
			group = st2list(groupnum)
			normalizer = 100.0 / groups[groupnum]
			galloc = [numpy.array([alloc[i] for i in group]) * normalizer for alloc in [sourced, ceg, cel, prop, shapley]]
			if len(galloc[1])==4:
				if galloc[1][0] == galloc[1][1] and galloc[1][1] == galloc[1][2] and galloc[1][2] == galloc[1][3]:
					suc += 1
				fail += 1
			if len(galloc[1])==3:
				if galloc[1][0] == galloc[1][1] and galloc[1][1] == galloc[1][2]:
					suc += 1
				fail += 1
			if len(galloc[1])==2:
				# print len(galloc[1])
				# print(galloc[1][len(galloc[1])-2]-galloc[1][len(galloc[1])-1])
				# print galloc[1]
				if galloc[1][0] == galloc[1][1]:
					suc += 1
				fail += 1
			# if len(galloc[4])==2:
			# 	print groups[groupnum]
			# 	print galloc[4]
			allocations[len(group)].append(galloc)
			gsourced = galloc[0]
			statistics[len(group)].append([[fun(alloc, gsourced) for fun in [minsavings, maxsavings, varsavings]] for alloc in galloc])
		Fnormalizer = 100.0 / vn
		Falloc = [alloc * Fnormalizer for alloc in [sourced, ceg, cel, prop, shapley]]
		fullallocations.append(Falloc)
		fullstatistics.append([[fun(alloc, sourced * Fnormalizer) for fun in [minsavings, maxsavings, varsavings]] for alloc in Falloc])
	print float(suc) / fail
	print fail
	print 'Number of groups is {}'.format(fail + len(allocations[1]))

	allocations = [numpy.array(a) for a in allocations]
	statistics = [numpy.array(a) for a in statistics]
	print allocations[1].shape
	print allocations[2].shape
	print allocations[3].shape
	print allocations[4].shape
	printarr(numpy.average(allocations[2], 0))
	printarr(numpy.average(allocations[3], 0))
	printarr(numpy.average(allocations[4], 0))
	# printarr(numpy.average(statistics[2], 0))
	# printarr(numpy.average(statistics[3], 0))
	# printarr(numpy.average(statistics[4], 0))
	printarr(numpy.average(fullallocations, 0))
	printarr(numpy.average(fullstatistics, 0))

if __name__ == '__main__':
	main()