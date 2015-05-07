import sys

def main(argv):
  if len(argv) != 1:
    print "Usage: python validator.py [path_to_input_file]"
    return
  print processFile(argv[0])

def processFile(s):
  fin = open(s, "r")
  line = fin.readline().split()
  if len(line) != 1 or not line[0].isdigit():
    return "Line 1 must contain a single integer."
  N = int(line[0])
  if N < 4 or N > 50 or N % 2 != 0:
    return "N must be an even integer between 4 and 50, inclusive."

  d = [[0 for j in range(N)] for i in range(N)]
  for i in xrange(N):
    line = fin.readline().split()
    if len(line) != N:
      return "Line " + `i+2` + " must contain N integers."
    for j in xrange(N):
      if not line[j].isdigit():
        return "Line " + `i+2` + " must contain N integers."
      d[i][j] = int(line[j])
      a = int(line[j])
      if d[i][j] < 0 or d[i][j] > 100:
        return "All edge weights must be between 0 and 100, inclusive."
  for i in xrange(N):
    if d[i][i] != 0:
      return "The distance from a node to itself must be 0."
    for j in xrange(N):
      if d[i][j] != d[j][i]:
        return "The distance matrix must be symmetric."

  line = fin.readline()
  if len(line) != N:
    return "Line " + `N+2` + " must be a string of length N."
  r = 0
  b = 0
  for j in xrange(N):
    c = line[j]
    if c != 'R' and c != 'B':
      return "Each character of the string must be either R or B."
    if c == 'R': r += 1
    if c == 'B': b += 1

  if r != b:
    return "The number of red and blue cities must be equal."
  return "ok"

if __name__ == '__main__':
    main(sys.argv[1:])