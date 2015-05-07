#!/usr/bin/env python

""" Traveling salesman problem solved using Simulated Annealing.
"""

def NPTSPviable(path, c):
    repeat = 0
    last = None
    for i in path:
        this = c[i]
        if this is last:
            repeat += repeat
            if repeat > 3:
                return False
        else:
            last = this
            repeat = 1
    return True

def NPTSPviablePath(c):
    visited = [0]
    notvisited = range(1, len(c))
    color = c[1:]
    this = c[0]
    for _ in range(len(c)):
        if this is 'R':
            i = color.find('B')
            this = 'B'
        else:
            i = color.find('R')
            this = 'B'           
        visited.append(notvisited[i])
        notvisited = notvisited[0:i] + notvisited[i+1:]
        color = color[0:i] + color[i+1:]
    return visited


def Distance(i1, i2, d):
    return d[i1][i2]

def TotalDistance(city, d):
    dist=0
    for i in range(len(city)-1):
        dist += Distance(i,i+1,d)
    dist += Distance(len(city)-1,0,d)
    return dist
    
def reverse(city, n):
    nct = len(city)
    nn = (1+ ((n[1]-n[0]) % nct))/2 # half the length of the segment to be reversed
    # the segment is reversed in the following way n[0]<->n[1], n[0]+1<->n[1]-1, n[0]+2<->n[1]-2,...
    # Start at the ends of the segment and swap pairs of cities, moving towards the center.
    for j in range(nn):
        k = (n[0]+j) % nct
        l = (n[1]-j) % nct
        (city[k],city[l]) = (city[l],city[k])  # swap
    
def transpt(city, n):
    nct = len(city)
    
    newcity=[]
    # Segment in the range n[0]...n[1]
    for j in range( (n[1]-n[0])%nct + 1):
        newcity.append(city[ (j+n[0])%nct ])
    # is followed by segment n[5]...n[2]
    for j in range( (n[2]-n[5])%nct + 1):
        newcity.append(city[ (j+n[5])%nct ])
    # is followed by segment n[3]...n[4]
    for j in range( (n[4]-n[3])%nct + 1):
        newcity.append(city[ (j+n[3])%nct ])
    return newcity
    

TT = 495 # number of test cases
fout = open ("answer.out", "w")
for t in xrange(1, TT+1):
    fin = open("instances/"+str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    # find an answer, and put into assign

    ################################################################################################################################################################
    ncity = N       # Number of cities to visit
    maxTsteps = 100    # Temperature is lowered not more than maxTsteps
    Tstart = 0.2       # Starting temperature - has to be high enough
    fCool = 0.9        # Factor to multiply temperature at each cooling step
    maxSteps = 100*ncity     # Number of steps at constant temperature
    maxAccepted = 10*ncity   # Number of accepted steps at constant temperature

    Preverse = 0.5      # How often to choose reverse/transpose trial move

    # The index table -- the order the cities are visited. ##### has to call the function which returns a valid order first (without violating color restriction)
    city = NPTSPviablePath(c)

    # Distance of the travel at the beginning
    dist = TotalDistance(city, d)

    # Stores points of a move
    n = zeros(6, dtype=int)
    nct = ncity # number of cities
    
    T = Tstart # temperature

    # Plot(city, R, dist)
    
    for t in range(maxTsteps):  # Over temperature

        accepted = 0
        for i in range(maxSteps): # At each temperature, many Monte Carlo steps
            
            while True: # Will find two random cities sufficiently close by
                # Two cities n[0] and n[1] are choosen at random
                n[0] = int((nct)*rand())     # select one city
                n[1] = int((nct-1)*rand())   # select another city, but not the same
                if (n[1] >= n[0]): n[1] += 1   #
                if (n[1] < n[0]): (n[0],n[1]) = (n[1],n[0]) # swap, because it must be: n[0]<n[1]
                nn = (n[0]+nct -n[1]-1) % nct  # number of cities not on the segment n[0]..n[1]
                if nn>=3: break
        
            # We want to have one index before and one after the two cities
            # The order hence is [n2,n0,n1,n3]
            n[2] = (n[0]-1) % nct  # index before n0  -- see figure in the lecture notes
            n[3] = (n[1]+1) % nct  # index after n2   -- see figure in the lecture notes
            
            if Preverse > rand(): 
                # Here we reverse a segment
                # What would be the cost to reverse the path between city[n[0]]-city[n[1]]?
                de = Distance(n[2],n[1], d) + Distance(n[3],n[0],d) - Distance(n[2],n[0],d) - Distance(n[3],n[1],d)
                
                if de<0 or exp(-de/T)>rand(): # Metropolis
                    accepted += 1
                    dist += de
                    reverse(city, n)
            else:
                # Here we transpose a segment
                nc = (n[1]+1+ int(rand()*(nn-1)))%nct  # Another point outside n[0],n[1] segment. See picture in lecture nodes!
                n[4] = nc
                n[5] = (nc+1) % nct
        
                # Cost to transpose a segment
                de = -Distance(n[1],n[3],d) - Distance(n[0],n[2],d) - Distance(n[4],n[5],d)
                de += Distance(n[0],n[4],d) + Distance(n[1],n[5],d) + Distance(n[2],n[3],d)
                
                if de<0 or exp(-de/T)>rand(): # Metropolis
                    accepted += 1
                    dist += de
                    city = transpt(city, n)
                    
            if accepted > maxAccepted: break

        print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted)
        T *= fCool             # The system is cooled down
        if accepted == 0: break  # If the path does not want to change any more, we can stop
        
    ################################################################################################################################################################




    assign = [0] * N
    for i in xrange(N):
        assign[i] = i+1

    fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()
