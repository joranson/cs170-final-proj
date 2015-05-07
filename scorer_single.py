import sys

# assumes files are well formatted
# if you have errors, make sure you double check our input and output format 
def main(argv):
  if len(argv) != 2:
    print "Usage: python scorer_single.py [path_to_instance] [path_to_answer]"
    return
  print processCase(argv[0], argv[1])

def processCase(s, t):
  finstance = open(s, "r")
  N = int(finstance.readline())
  d = [[] for i in range(N)]
  for i in xrange(N):
      d[i] = [int(x) for x in finstance.readline().split()]
  c = finstance.readline()

  fanswer = open(t, "r")
  perm = [int(x) for x in fanswer.readline().split()]
  
  # check it's valid
  v = [0] * N
  prev = 'X'
  count = 0
  for i in xrange(N):
    if v[perm[i]-1] == 1: 
      return "Your answer must be a permutation of {1,...,N}."
    v[perm[i]-1] = 1

    cur = c[perm[i]-1]
    if cur == prev:
      count += 1
    else:
      prev = cur
      count = 1

    if count > 3:
      return "Your tour cannot visit more than 3 same colored cities consecutively."

  cost = 0
  for i in xrange(N-1):
    cur = perm[i]-1
    next = perm[i+1]-1

    cost += d[cur][next]

  return "You got " + `cost` + " points for this case."

if __name__ == '__main__':
    main(sys.argv[1:])