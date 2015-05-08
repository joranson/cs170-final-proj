#!/usr/bin/env python

""" Traveling salesman problem solved using Simulated Annealing.
"""
from random import random as rand
from math import exp

def NPTSPviable(path, c):
    color = c[path[0]]
    count = 1
    for i in range(1, len(c)):
        # print i, path[i], c[path[i]]
        if c[path[i]]==color:
            count += 1
            if count > 3:
                return False
        else:
            color = c[path[i]]
            count = 1
    return True

def NPTSPviablePath(c):
    visited = [0]
    color = c[1:]
    this = c[0]
    r_index = 0
    b_index = 0
    for _ in range(1,len(c)):
        if this is 'R':
            while b_index < len(c):
                b_index += 1
                if b_index==len(c):
                    break
                if c[b_index]=="B":
                    visited.append(b_index)
                    break
            this = 'B'
        else:
            while r_index < len(c):
                r_index += 1
                if r_index==len(c):
                    break
                if c[r_index]=="R":
                    visited.append(r_index)
                    break
            this = 'R'   
    return visited

def Distance(i1, i2, d):
    return d[i1][i2]

def TotalDistance(path, d):
    dist=0
    for i in range(len(path)-1):
        dist += Distance(path[i],path[i+1],d)
    # dist += Distance(path[len(path)-1],path[0],d)
    return dist
    
def reverse(path, n):
    newpath = []
    for i in path:
        newpath.append(i)
    nct = len(path)
    nn = (1+ ((n[1]-n[0]) % nct))/2 # half the length of the segment to be reversed
    # the segment is reversed in the following way n[0]<->n[1], n[0]+1<->n[1]-1, n[0]+2<->n[1]-2,...
    # Start at the ends of the segment and swap pairs of cities, moving towards the center.
    for j in range(nn):
        k = (n[0]+j) % nct
        l = (n[1]-j) % nct
        (newpath[k],newpath[l]) = (newpath[l],newpath[k])  # swap
    return newpath
    
def transpt(path, n):
    nct = len(path)
    
    newpath=[]
    # Segment in the range n[0]...n[1]
    for j in range( (n[1]-n[0])%nct + 1):
        newpath.append(path[ (j+n[0])%nct ])
    # is followed by segment n[5]...n[2]
    for j in range( (n[2]-n[5])%nct + 1):
        newpath.append(path[ (j+n[5])%nct ])
    # is followed by segment n[3]...n[4]
    for j in range( (n[4]-n[3])%nct + 1):
        newpath.append(path[ (j+n[3])%nct ])
    return newpath
    
def longestEdge(path, d):
    maxDist = float("-inf")
    nn1 = -1
    nn2 = -1
    for i in range(len(path)):
        n1 = i%len(path)
        n2 = (i+1)%len(path)
        if d[path[n1]][path[n2]] > maxDist:
            maxDist = d[path[n1]][path[n2]]
            nn1 = n1
            nn2 = n2
    if nn2 == 0:
        return path
    else:
        return path[nn2:]+path[:nn2]


TT = 495 # number of test cases
fout = open ("answer6.out", "w")
for t in xrange(401, TT+1):
    fin = open("instances/"+str(t) + ".in", "r")            ## modified
    # fin = open("instances/"+"103" + ".in", "r")  
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()[:N]

    # find an answer, and put into assign

    ################################################################################################################################################################
    ncity = N       # Number of cities to visit
    maxTsteps = 1000   # Temperature is lowered not more than maxTsteps
    Tstart = 0.5       # Starting temperature - has to be high enough
    fCool = 0.995       # Factor to multiply temperature at each cooling step
    maxSteps = 200*ncity     # Number of steps at constant temperature
    maxAccepted = 10*ncity   # Number of accepted steps at constant temperature

    Preverse = 0.5      # How often to choose reverse/transpose trial move

    # The index table -- the order the cities are visited. ##### has to call the function which returns a valid order first (without violating color restriction)
    minDist = float("inf")
    minPath = []

    for kk in range(5):
        # print kk, "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        path = longestEdge(NPTSPviablePath(c),d)

        # Distance of the travel at the beginning
        dist = TotalDistance(path, d)
        # print dist

        # Stores points of a move
        n = [0,0,0,0,0,0]
        nct = ncity # number of cities

        T = Tstart # temperature

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
                    # try reversing it
                    n[4]=0
                    n[5]=0
                    trial_path=reverse(path,n)
                    alpha=TotalDistance(trial_path,d)
                    beta=TotalDistance(path,d)
                    de=alpha-beta

                    n[4]=0
                    n[5]=0
                    if de<0:
                        if NPTSPviable(trial_path, c):
                            accepted += 1
                            dist = alpha #was dist += de before
                            path = trial_path
                            # print "de < 0: dist = ", dist
                    elif exp(-0.5/T)>rand(): # Metropolis
                        if NPTSPviable(trial_path, c):
                            accepted += 1
                            dist = alpha #was dist += de before
                            path = trial_path
                            # print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted), "reverse and de = ", de, "prob = ", exp(-(abs(de+0.0)/minDist)/T)
                    # else:
                    #     print "!!!!!!!!!!!!!!!!!!!!!!!!"

                else:
                    # Here we transpose a segment
                    nc = (n[1]+1+ int(rand()*(nn-1)))%nct  # Another point outside n[0],n[1] segment. See picture in lecture nodes!
                    n[4] = nc
                    n[5] = (nc+1) % nct
            
                    # Cost to transpose a segment
                    trial_path=transpt(path,n)
                    alpha=TotalDistance(trial_path,d)
                    beta=TotalDistance(path,d)
                    de=alpha-beta

                    if de<0:
                        if NPTSPviable(trial_path, c):
                            accepted += 1
                            dist = alpha #was += de
                            path = trial_path
                            # print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted), "transpt and de < 0"
                            # print "de < 0: dist = ", dist
                    elif exp(-0.5/T)>rand(): # Metropolis
                        if NPTSPviable(trial_path, c):
                            accepted += 1
                            dist = alpha #was += de
                            path = trial_path
                            # print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted), "transpt and de = ", de, "prob = ", exp(-(abs(de+0.0)/minDist)/T)
                    # else:
                    #     print "!!!!!!!!!!!!!!!!!!!!!!!!"
                        
                if dist<minDist:
                    minPath = path
                    # print "well, dist = ", dist, " is smaller than minDist = ", minDist, "and minPath =", minPath
                    minDist=dist
                if accepted > maxAccepted: break

            # print "T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted)
            T *= fCool             # The system is cooled down
            if accepted == 0: break  # If the path does not want to change any more, we can stop
        #minDist = dist
        
    ################################################################################################################################################################

    assign = [i+1 for i in minPath]
    print minDist, assign

    fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()
