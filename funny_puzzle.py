import heapq

goal_state = [1,2,3,
              4,5,6,
              7,8,0]

#Computes distance between indices a,b
def manhattan(a, b):
    x_distance = abs((a%3)-(b%3))
    y_distance = abs(int((a/3))-int((b/3)))
    return x_distance + y_distance

#Heuristic: Sums manhattan distance accross al tiles
def h(state):
    global goal_state
    h = 0
    for i,n in enumerate(goal_state):
        if (n != state[i]) & (n != 0):
            h += manhattan(i, state.index(n))
    return h

#Preforms one move with direction/magnitude n
def move(i, state, n):
    suc = state.copy()
    suc[i] = state[i+n]
    suc[i+n] = state[i]
    return suc

#Returns sorted list of all successor states
def get_sucessors(state):
    i = state.index(0)
    sucessors = []
    if i == 4: #Center
        sucessors.append(move(i,state,1))
        sucessors.append(move(i,state,-1))
        sucessors.append(move(i,state,3))
        sucessors.append(move(i,state,-3))
    elif i%2 == 0: #Corner  
        #left/right
        if i%3 == 0:
            sucessors.append(move(i,state,1))
        else:
            sucessors.append(move(i,state,-1))
        #bottom/top
        if i<3:
            sucessors.append(move(i,state,3))
        else:
            sucessors.append(move(i,state,-3))          
    else: #Edge
        #horizontal/vertical
        if i%6 == 1:
            sucessors.append(move(i,state,1))
            sucessors.append(move(i,state,-1))
            if i < 3:
                sucessors.append(move(i,state,3))
            else:
                sucessors.append(move(i,state,-3))
        else:
            sucessors.append(move(i,state,3))
            sucessors.append(move(i,state,-3))
            if i%3 == 0:
                sucessors.append(move(i,state,1))
            else:
                sucessors.append(move(i,state,-1)) 
    return sorted(sucessors)

#If a state in listy matches state, return its g value. Otherwise return -1
def return_match(listy,state):
    for item in listy:
        if item[1] == state:
            return item[2][0]
    return -1

#Prints all successor states
def print_succ(state):    
    sucessors = get_sucessors(state)
    for suc in sucessors:
        print(suc, "h=" + str(h(suc)))

#Preforms A*
def solve(state):
    global goal_state
    pq = [] #OPEN
    visited = [] #CLOSED
    heapq.heappush(pq,(0, state, (0, h(state), -1)))
    
    lenny = 0
    
    while(len(pq) != 0):
        #Pop & append to visited, calculate parent length
        n = heapq.heappop(pq)
        parent_idx = len(visited)
        visited.append(n)
        
        #Finished: Trace back parent indexes through visited[]
        if n[1] == goal_state:
            path = []
            while n[2][2] != -1:
                path.insert(0,n)
                n = visited[n[2][2]]   
            path.insert(0,n)
            for p in path:
                print(p[1],"h="+str(p[2][1]),"moves:",p[2][0])
            pq = []
        #Not Finished: Expand node, add all sucessors to pq
        else:
            sucessors = get_sucessors(n[1])            
            for suc in sucessors:
                #Sucessor not visited, push state
                if (return_match(visited,suc) == -1) & (return_match(pq,suc) == -1):
                    hval = h(suc)
                    g = n[2][0]+1
                    heapq.heappush(pq,(hval+g, suc, (g, hval, parent_idx)))
                #Sucessor visited, push if new g is less than the nodes current g
                else:
                    hval = h(suc)
                    g = n[2][0]+1
                    if g < return_match(visited,suc):
                        for i,n in enumerate(visited):
                            if suc == n[1]:
                                del visited[i]
                        heapq.heappush(pq,(hval+g, suc, (g, hval, parent_idx))) 
                    elif g < return_match(pq,suc):
                        for i,n in enumerate(pq):
                            if suc == n[1]:
                                del pq[i]
                        heapq.heappush(pq,(hval+g, suc, (g, hval, parent_idx)))
