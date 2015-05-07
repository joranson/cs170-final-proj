T = 1 # number of test cases
fout = open ("answer.out", "w")
for t in xrange(1, T+1):
    fin = open(str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    # find an answer, and put into assign
    assign = [0] * N
    for i in xrange(N):
        assign[i] = i+1

    fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()