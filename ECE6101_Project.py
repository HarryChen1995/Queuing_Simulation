import random
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from queue import Queue
import math
from collections import Counter

# (1)(a) write a computer program enerate random numbers between [0,1]. 
#        Such a randomnumber generator simulates 
#        the values generated by a uniform random variable U[0,1].
def Uniform(start =0 , end =1):
    x = start + (end-start)*random.random()
    return x


#(1)(b) Write another program (using the program in (a)) to estimate P(U > x). 
#       Plot P(U > x)for values of x  in (0.5,1).

def plot_Prob_Uniform():
    # generate 10000 samples
    n = 10000
    numbers = [  Uniform() for  i in range(n)]


   
    
    # calculate probability of p(U>x)
    p = defaultdict(lambda:0, {})
    for i in list(np.arange(0.5,1,0.001)):
         for j in numbers:
             if i < j:
                 p[str(i)]+=1/n
    
    x= list(map(float, p.keys()))
    y = list(p.values())
    plt.plot(x,y)
    plt.xlabel('x')
    plt.ylabel('P(U>x)')
    plt.title('P(U>x) in (0.5 ,1)')
    plt.grid()
    plt.show()

#(2)(a) Write a computer program to simulate the values generated by Exponential (X) and
#        Poisson random (Y) variables using the program you developed in (1).
def Exponential(Mu):
    X = Uniform() 
    inverse_exp = lambda x : math.log(1-x)*(-Mu)
    X = inverse_exp(X)
    return X





def Poisson(Lambda):
    i = Uniform()

    y =0
    p = math.exp(-Lambda)
    t = p
    while i>t:
        y+=1
        p =p*Lambda/y
        t = t+p

    return y


#(2)(b) Provide plots for P(X > x) and P(Y > x), for E(Y) = E(X) = 2. 
#    It may be necessary to show your result on a plot where the vertical axis is logarithmic.
def plot_Pro_Exp_Poisson():
    
    ## generate 10000 samples
    n = 10000
    X = [ Exponential(0.5) for i in range(n)]
    Y = [ Poisson(2) for i in range(n)]
    ## calculate probability of exponential random variable 
    p_x = defaultdict(lambda:0, {})
    for i in list(np.arange(0,30,0.01)):
         for j in X:
             if i < j:
                 p_x[str(i)]+=1/n
    
    x_e= list(map(float, p_x.keys()))
    y_e= list(p_x.values())
     ## calculate probability of poisson random variable 
    p_y = defaultdict(lambda:0, {})
    for i in list(np.arange(0,30,0.01)):
         for j in Y:
             if i < j:
                 p_y[str(i)]+=1/n
    
    x_p= list(map(float, p_y.keys()))
    y_p= list(p_y.values())

    ## plot 
    plt.subplot(2,1,1)
    plt.plot(x_e, y_e)
    plt.xlabel('x')
    plt.ylabel('P(X>x)')
    plt.title('P(X>x) - Exponential Random Variable')
    plt.grid(True)
    plt.subplot(2,1,2)
    plt.plot(x_p, y_p)
    plt.xlabel('y')
    plt.ylabel('P(Y>y)')
    plt.title('P(Y>y) Poisson Random Variable')
    plt.grid(True)
    plt.show()


#3) (a) Write a computer program that simulates an M/M/1 queue.
#   (b) Based on this program, plot Pn against n when lambda = 5 and mu = 6.
#   (c) Again, from your program, find the expected number and expected delay in yourM/M/1queueing system when rho= 5/6.
def MM_1_Queue():
    #all  parameters
    simulation_time = 500   # simulation time in seconds
    Lambda = 5  # arrival rate  (/second)
    Mu = 6      # service rate (/second)
    rho = Lambda/Mu   # utilization 
    queue = Queue() #  Queue
    number_customer = int(Poisson(Lambda)*60*60) # total number of customers arrived within one hour
    
   
    inter_arrival_time = [] # inter arrival time of each customer 
    for i in range(number_customer):
        t = (Exponential(1/Lambda))
        if i == 0:
            inter_arrival_time.append(0)
        else:
            inter_arrival_time.append(t)
    
    
    arrival_time = [] #arrival time of each customer
    for i in range(number_customer):
        
        if i == 0:
            arrival_time.append(0.00)
        else:
            arrival_time.append(arrival_time[i-1]+inter_arrival_time[i])
    arrival_time  = list(map(lambda x: round(x,2) , arrival_time))


    service_time = []  # service time of each customer
    for i  in range (number_customer):
        t= Exponential(1/Mu)
        t=round(t,2)
        service_time.append(t)
    
    idle = True # flags that indate wether server is busy
    N = [] #number of customer in system at each time point
    W_Q = [0 for i in range(number_customer)] # waiting time of each customer in Queue
    finished_customer = 0 # counter of finished customer
    temp_service_time = list(service_time) # copy of service time and decrement temp service time when customer is in server
    t = 0.00  # start from 0 second

    # run simulation
    while t <= simulation_time:

        print("simulation at {} seconds".format(t))
        
        # check which customer arrives 
        for k in range(number_customer):
            if  arrival_time[k] == t:
                queue.put(k)
                

         #  if server is in idle and customer leave queue and enter server
        if not queue.empty() and idle :
            customer_in_server = queue.get()
            idle = False

        # if server is busy
        if not idle:
            # increase waiting time of each customer in queue
            for customer in list(queue.queue):
                W_Q[customer] = round(W_Q[customer]+0.01,2)
            
            # decrease service time of customer in server
            if temp_service_time[customer_in_server] >=0.01:
                temp_service_time[customer_in_server] = round(temp_service_time[customer_in_server]-0.01,2)  
            
            # finished customer departure server 
            if temp_service_time[customer_in_server] == 0.00:
                idle = True
                finished_customer+=1 # count finished customers
        
        # number of customer in Queue and Server at each time point

        n = len(list(queue.queue)) + (1 if not idle else 0)
        N.append(n)

        # add time point to list
        t = round(t +0.01, 2)

    print("Simulation Done")

    #plot pn vs  n 
    counter = Counter(N)
    n=[]
    p_n= []
    counter =dict(sorted(counter.items(), key = lambda x:x[0]))
    for key, val in counter.items():
        n.append(key)
        p_n.append(val/len(N))
    theretical_p_n = list(map(lambda x: (rho**x)*(1-rho), n))
    plt.plot(n,p_n, label = "Simulation")
    plt.plot(n, theretical_p_n, label="Theretical")
    theretical_p_n
    plt.xlabel("n")
    plt.ylabel("P_n")
    plt.legend()
    plt.grid()
    plt.title("P_n vs n for M/M/1 queue")
    plt.show()

    # Expected number of customer in system
    E_N = list(map(lambda x: x[0]*x[1], list(zip(n,p_n))))
    E_N= sum(E_N)


    #Expected waiting delay within queue of each customer in seconds
    E_W_Q = []
    for customer in range(finished_customer):
        E_W_Q.append(W_Q[customer])
    counter = Counter(E_W_Q)
    w_q = []
    p_w_q = []
    for key, val in counter.items():
        w_q.append(key)
        p_w_q.append(val/len(E_W_Q))
    E_WQ = list(map(lambda x:(x[0]*x[1]), list(zip(w_q,p_w_q))))
    E_WQ = sum(E_WQ)
    
    # Expected Service time of each customer in seconds
    E_S_T = []
    for customer in range(finished_customer):
        E_S_T.append(service_time[customer])
    counter = Counter(E_S_T)
    s_t = []
    p_s_t = []
    for key, val in counter.items():
        s_t.append(key)
        p_s_t.append(val/len(E_S_T))
    E_ST = list(map(lambda x:(x[0]*x[1]), list(zip(s_t,p_s_t))))
    E_ST = sum(E_ST)
    
    # Expected delay of system in seconds
    E_T = E_ST + E_WQ

    print( "Expected Delay of system is {} seconds".format(round(E_T,3)))
    print("Expected number of customer in system is {}".format(round(E_N,2)))    

#(4)(a) Write a computer program that simulates an M/Ek/1 queue.
#  Here, Ek is an Erlangrandom variable with k phases.

#b) Based on this program, plot Pn against n when k = 4 and rho= 5/6. 
# This means that the overall service rate of the queue is 6 and the arrival rate is 5.
# Also, find the expected number in the system. How do these results compare with your M/M/1 results in (3)?

def Erlang(k, Mu):
    t = sum([Exponential(1/(Mu*k)) for i in range(k)])
    return t

def M_Ek_1(K):
    #all  parameters
    simulation_time_in_seconds = 500  # simulation time in seconds
    Lambda = 5  # arrival rate  (/second)
    Mu = 6     # service rate (/second)
    rho = Lambda/Mu   # utilization 
    queue = Queue() #  Queue
    number_customer = int(Poisson(Lambda)*60*60) # total number of customers arrived within in one hour
    
   
    inter_arrival_time = [] # inter arrival time of each customer 
    for i in range(number_customer):
        t = (Exponential(1/Lambda))
        if i == 0:
            inter_arrival_time.append(0)
        else:
            inter_arrival_time.append(t)
    
    
    arrival_time = [] #arrival time of each customer
    for i in range(number_customer):
        
        if i == 0:
            arrival_time.append(0.00)
        else:
            arrival_time.append(arrival_time[i-1]+inter_arrival_time[i])
    arrival_time  = list(map(lambda x: round(x,2) , arrival_time))


    service_time = []  # service time of each customer
    for i in range(number_customer):
        t= Erlang(K, Mu)
        t=round(t,2)
        service_time.append(t)
    
    idle = True # flags that indate wether server is busy
    N = [] #number of customer in system at each time point
    W_Q = [0 for i in range(number_customer)] # waiting time of each customer in Queue
    finished_customer = 0 # counter of finished customer
    temp_service_time = list(service_time) # copy of service time and decrement temp service time when customer is in server
    t = 0.00  # start from 0 second

    # run simulation
    while t <= simulation_time_in_seconds:

        print("simulation at {} seconds".format(t))
        
        # check which customer arrives 
        for k in range(number_customer):
            if  arrival_time[k] == t:
                queue.put(k)
                

         #  if server is in idle and customer leave queue and enter server
        if not queue.empty() and idle :
            customer_in_server = queue.get()
            idle = False

        # if server is busy
        if not idle:
            # increase waiting time of each customer in queue
            for customer in list(queue.queue):
                W_Q[customer] = round(W_Q[customer]+0.01,2)
            
            # decrease service time of customer in server
            if temp_service_time[customer_in_server] >= 0.01:
                temp_service_time[customer_in_server] = round(temp_service_time[customer_in_server]-0.01,2)  
            
            # finished customer departure server 
            if temp_service_time[customer_in_server] == 0.00:
                idle = True
                finished_customer+=1 # count finished customers
        
        # number of customer in Queue and Server at each time point

        n = len(list(queue.queue)) + (1 if not idle else 0)
        N.append(n)

        # add time point to list
        t = round(t +0.01, 2)

    print("Simulation Done")

    #plot pn vs  n 
    counter = Counter(N)
    n=[]
    p_n= []
    counter =dict(sorted(counter.items(), key = lambda x:x[0]))
    for key, val in counter.items():
        n.append(key)
        p_n.append(val/len(N))
    plt.plot(n,p_n, label = "Simulation")
    plt.xlabel("n")
    plt.ylabel("P_n")
    plt.grid()
    plt.title("P_n vs n for M/Ek/1 queue k ={}".format(K))
    plt.show()

    # Expected number of customer in system
    E_N = list(map(lambda x: x[0]*x[1], list(zip(n,p_n))))
    E_N= sum(E_N)


    #Expected waiting delay within queue of each customer in second
    E_W_Q = []
    for customer in range(finished_customer):
        E_W_Q.append(W_Q[customer])
    counter = Counter(E_W_Q)
    w_q = []
    p_w_q = []
    for key, val in counter.items():
        w_q.append(key)
        p_w_q.append(val/len(E_W_Q))
    E_WQ = list(map(lambda x:(x[0]*x[1]), list(zip(w_q,p_w_q))))
    E_WQ = sum(E_WQ)
    
    # Expected Service time of each customer in second
    E_S_T = []
    for customer in range(finished_customer):
        E_S_T.append(service_time[customer])
    counter = Counter(E_S_T)
    s_t = []
    p_s_t = []
    for key, val in counter.items():
        s_t.append(key)
        p_s_t.append(val/len(E_S_T))
    E_ST = list(map(lambda x:(x[0]*x[1]), list(zip(s_t,p_s_t))))
    E_ST = sum(E_ST)
    
    # Expected delay of system in second
    E_T = E_ST + E_WQ

    print( "Expected Delay of system is {} seconds".format(round(E_T,3)))
    print("Expected number of customer in system is {}".format(round(E_N,2)))


#(c) Plot the expected number in the system for different values of the utilization when k = 40.
# Make sure to keep the service rate of the queue to be 6 and vary the arrival rate from 1 to 5.9. 
# Also plot the expected number in the system in an M/D/1 queue from the analysis in class (for a similar range) 
# and compare the results with your simulation. What does this tell you and why?

# return expected number of customer in M/Ek/1 queque with different arrival rate
def EN_M_Ek_1(Lambda, K=40):
    simulation_time_in_seconds = 500  # simulation time in seconds
    Mu = 6     # service rate (/second)
    rho = Lambda/Mu   # utilization 
    queue = Queue() #  Queue
    number_customer = int(Poisson(Lambda)*60*60) # total number of customers arrived within in one hour
    
   
    inter_arrival_time = [] # inter arrival time of each customer 
    for i in range(number_customer):
        t = (Exponential(1/Lambda))
        if i == 0:
            inter_arrival_time.append(0)
        else:
            inter_arrival_time.append(t)
    
    
    arrival_time = [] #arrival time of each customer
    for i in range(number_customer):
        
        if i == 0:
            arrival_time.append(0.0)
        else:
            arrival_time.append(arrival_time[i-1]+inter_arrival_time[i])
    arrival_time  = list(map(lambda x: round(x,1) , arrival_time))


    service_time = []  # service time of each customer
    for i in range(number_customer):
        t= Erlang(K, Mu)
        t=round(t,1)
        service_time.append(t)
    
    idle = True # flags that indate wether server is busy
    N = [] #number of customer in system at each time point
    finished_customer = 0 # counter of finished customer
    t = 0.0  # start from 0 second

    # run simulation
    while t <= simulation_time_in_seconds:
        
        # check which customer arrives 
        for k in range(number_customer):
            if  arrival_time[k] == t:
                queue.put(k)
                

         #  if server is in idle and customer leave queue and enter server
        if not queue.empty() and idle :
            customer_in_server = queue.get()
            idle = False

        # if server is busy
        if not idle:
            
            # decrease service time of customer in server
            if service_time[customer_in_server] >= 0.1:
                service_time[customer_in_server] = round(service_time[customer_in_server]-0.1,1)  
            
            # finished customer departure server 
            if service_time[customer_in_server] == 0.0:
                idle = True
                finished_customer+=1 # count finished customers
        
        # number of customer in Queue and Server at each time point

        n = len(list(queue.queue)) + (1 if not idle else 0)
        N.append(n)

        # add time point to list
        t = round(t +0.1, 1)


    # Expected number of customer in system
    counter = Counter(N)
    n=[]
    p_n= []
    counter =dict(sorted(counter.items(), key = lambda x:x[0]))
    for key, val in counter.items():
        n.append(key)
        p_n.append(val/len(N))
    E_N = list(map(lambda x: x[0]*x[1], list(zip(n,p_n))))
    E_N= round(sum(E_N),2)
    
    return E_N


def plot_M_Ek_1_M_D_1():
    
    E_N1 = [] # store expected number in M/Ek/1 queue 
    E_N2 = [] # store expected number in M/D/1 queue 
    rho = []
    for Lambda in np.arange(1,6, 0.1):
        Lambda = round(Lambda,1)
        Rho = Lambda/6
        E_N1.append(EN_M_Ek_1(Lambda))
        E_N2.append((Rho/(1-Rho))*(1-Rho/2))
        rho.append(Rho)
        print("simulation at rho {}".format(Lambda))
    
    # plot rho vs E_N

    plt.plot(rho, E_N1, label = "M/Ek/1")
    plt.plot(rho, E_N2, label = "M/D/1")
    plt.xlabel("rho")
    plt.ylabel("E[N]")
    plt.grid()
    plt.legend()
    plt.title("Expected Number of System E[N] vs Utilization rho")
    plt.show()
    


plot_Prob_Uniform()

plot_Pro_Exp_Poisson()

MM_1_Queue()

M_Ek_1(4)

plot_M_Ek_1_M_D_1()