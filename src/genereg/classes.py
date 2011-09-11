
import numpy as num
import matplotlib.pyplot as plt
import copy
import networkx as nx
import probes

print_enable=True

class probeable_obj ():
    def __init__ (self):
        self.probes = []
    def attach (self,probe):
        if probe in self.probes:
            print "This probe is already attached."
        else:
            self.probes.append(probe)
    
    def populate_probes (self,subroutine):
        for probe in self.probes:
            if probe.subroutine == subroutine:
                measured = probe.function(self)
                print measured
                probe.data = num.append(probe.data,measured)
                
                
class network(object, probeable_obj):
    '''
    Network Class
    
    Input Arguments
        adjacency_matrix
        maskm
        state_vec  
    '''
    def __init__ (self,adjacency_matrix,mask,score,function,state_vec=None):
        probeable_obj.__init__(self)
        self.adjacency=adjacency_matrix
        self.n_nodes= num.size(adjacency_matrix,0)
        self.mask=mask
        if state_vec == None:
            state_vec= (num.random.random((self.n_nodes,self.n_nodes))< 0.5 )*1.0
        self.state=num.array([state_vec])
        self.equilibria=num.zeros(2**self.n_nodes)
        self.orbits = num.zeros(2**self.n_nodes)
        self.score = 0
        self.mama = []
        self.children = []
        self.scorer = score
        self.function = function
    
    def print_id(self):
        '''
        Prints out an identification of the network.
        Prints:
            Id
            Mothers
            Children
            Orbits
            Score
            Adjacency matrix
            sTate
            masK
        '''
        print "This network is : "+str(id(self))+"."
        print "Nodes: "+str(self.n_nodes)
        print "Score: "+str(self.score)
        print "Its mothers are: "
        print "   "+str(id(self.mother))
        print "Its children are: "
        for child in self.children:
            print "   "+str(id(child))
        print "It has the following adjacency matrix: "
        print self.adjacency
        print "The following are the masks for each node: "
        for (num,node) in enumerate(self.mask):
            print str(num)+" th node : "+str(node)
        print "The following are the states with respect to time "
        for (t,state) in enumerate(self.state):
            print "t= "+str(t)+" : "+str(node)
        print "The scorer is : "
        print self.scorer
            
        
    def show_graph(self,type='circular'):
        '''
        Visualizes the network with the help of networkx class generated from the
        adjacency matrix.
        '''

        nx_image = nx.DiGraph(self.adjacency)
        if type is 'circular':
            nx.draw_circular(nx_image)
        if type is 'random':
            nx.draw_random(nx_image)
        if type is 'graphviz':
            nx.draw_graphviz(nx_image)
        if type is 'normal':
            nx.draw(self.nx,pos=nx.spring_layout(nx_image))
        plt.show()


    def advance(self,times,starter_state=None):
        '''
        Advances the state in the phase space a given number of times.
        If a starter state is given, the initial condition is taken as the given state.
        If not, the last state is used instead.
        Input Arguments
            times -> the number of iterations to be taken.
            starter_state -> the initial state to be used
        '''
                
        # it no initial state is given, the last state is the initial state.
        
        if starter_state == None:
            starter_state = self.state[-1]
            
        
        # Could have preallocated, but 
        # Premature pre-optimization is the root of all evil.
        
        for counter in range(times):
            newstate = self.function(self)
            self.state=num.append(self.state,[newstate],axis=0)
            
        self.populate_probes(probes.advance)
            
    def plot_state(self,last=20):
        '''
        Plots the last 20 states as a black and white strips vertically.
        The vertical axis is time, whereas each strip is a single state.
        Input Arguments
            last -> the number of states that will be plotted 
        '''
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        # Future Modification 
        # May show a 'color' based on the whole state vector, easier for us to see states. 
        
        plt.imshow(self.state[-last:],cmap=plt.cm.binary,interpolation='nearest')
        
        # Wont go on unless the Window is closed.
        
        plt.show()


    def plot_equilibria(self):
        
        # Take the state vector, convert the list of arrays into a 2d array, then show it as an image
        # Black and white. 
        
        # Future Modification 
        # May show a 'color' based on the whole state vector, easier for us to see states. 
        if self.n_nodes % 2 == 0:
            jumper = 2**(self.n_nodes/2)
            im_matrix = num.zeros((jumper,jumper))
            for ctr,offset in enumerate(num.multiply(range(jumper,jumper))):
                im_matrix[ctr,:] = self.equilibria[offset:jumper+offset]
        
        if self.n_nodes % 2 == 1:
            jumper = 2**(self.n_nodes/2+1)
            im_matrix = num.zeros((jumper/2,jumper))
            for ctr,offset in enumerate(num.multiply(range(jumper/2),jumper)):
                im_matrix[ctr,:] = self.equilibria[offset:jumper+offset]
        
        plt.imshow(im_matrix,cmap=plt.cm.gray,interpolation='nearest')
        
        # Wont go on unless the Window is closed.
        
        plt.grid()
        plt.colorbar()
        plt.show()
        
    def hamming_distance_of_state(self,state_vector):
        '''
        Returns the Hamming distance of the specified vector to the state vectors that
        are available.
        Input Arguments:
            state_vector -> the vector that we'd like to calculate the Hamming distance to.
        '''
        return num.array(num.abs(state_vector-self.state)).sum(axis=1)
    
    def plot_hamming_distance_of_state(self,state_vector):
        '''
        Plots the Hamming distance of the specified vector to the state vectors that
        are available.
            state_vector -> the vector that we'd like to plot the Hamming distance to.
        '''
        plt.plot(self.hamming_distance_of_state(state_vector))
        plt.show()           
           
    def search_equilibrium(self,chaos_limit,starter_state,orbit_extraction=False):
        '''
        Searches for an equilibrium point, or a limit cycle. 
        Returns the state vector, or the state vector list, if the equilibrium is a limit cycle.
        If no equilibrium is found, returns False.
        Input Arguments:
            starter_state -> the initial state vector that the state will evolve on.
            chaos_limit -> the degree that an orbit will be considered as chaotic.
                The calculation will stop when this point is reached.
            orbit_extraction -> True when every individual orbit is recorded with its degree.
        '''
        
        #flushes states
        
        self.state = num.array([starter_state])
        
        #Advances chaos limit times.
        #self.advance(chaos_limit)
        
        # A memory of chaos limit is created, preallocation.
        
        #memory = num.zeros((chaos_limit,self.n_nodes))
        
        memory = num.array([[None]*self.n_nodes]*chaos_limit)
        
        # to the first memory block, the initial state is written. 
        
        memory_ctr = 0
        
        while (memory_ctr < chaos_limit):
            
            memory [memory_ctr] = self.state[-1]
            #advance once , last state will be a new one 

            self.advance(1,starter_state)
            
            # VERY INEFFICIENT EXTREMELY EXTRAVAGANT!!!
            # BUT WORKS.
            # We'd like to remove tolist s
            
            
            # All matrices are converted into lists.
            memory_as_list = memory.tolist()
            last_state_as_list = self.state.tolist()[-1]
            
            # if this particular state we are concerned with is present in the memory 
            if last_state_as_list in memory_as_list:
                # Where in the memory is this particular state?
                where = memory_as_list.index(last_state_as_list)
                # If We'd like to extract the orbit out, for all states in the memory, 
                for state in memory[0:where]:
                    # Convert the state to a list
                    state_as_list = state.tolist()
                    # Finds the decimal representation of the binary number
                    location_in_equilibrium = int(reduce(lambda s, x: s*2 + x, state_as_list))
                    # Memory_ctr is the present number of iteration, whereas Where is the last identical state
                    self.equilibria[location_in_equilibrium] = memory_ctr-where+1
                    # Extract orbits, if it was requested to do so.
                    if orbit_extraction == True:
                        self.orbits[location_in_equilibrium] = memory [:memory_ctr]
                return (memory [:memory_ctr+1],memory_ctr-where+1)
            memory_ctr += 1
        self.populate_probes(probes.search_equilibrium)
            
    def populate_equilibria(self,normalize=1):
        '''
        Creates all possible initial conditions by listing all possible 2^n boolean states.
        Then runs populate_equilibrium for each of them.
            populate_equilibrium returns orbits and-or degrees of the orbits.
        Gives scores to each of the networks, depending on the degree of the orbit each initial condition
        rests on.
        Input Arguments:
            normalize -> normalizes the scores to the value given.
        '''
 
        # Creates all possible initial conditions by listing all possible integers from 0 to 2^n_node-1
        # Converts them all to binaries, fills them all with zeroes such that they are all in the
        # form of 000111010 rather than 111010. Then creates a list out of them.
        
        state_numbers_decimal = range(0,num.power(2,self.n_nodes))
        binspace = [list((bin(k)[2:].zfill(self.n_nodes))) for k in state_numbers_decimal]
        
        # But this list has elements of strings. We convert all of the elements to integers
        
        int_binspace=[[int(i) for i in k] for k in binspace] 
        
        for state in int_binspace:
            self.search_equilibrium(100,state)  
        
        self.score = self.scorer(self)
        self.populate_probes(probes.populate_equilibria)
        
    def degree(self):
        sum=[]
        for row in self.adjacency:
            sum.append(num.sum(row))
        return num.mean(sum)
    
    def mutant(self, mutated_obj=('Both',1), rule=None, howmany=1):
        '''
        Will result in mutation
        Returns mutated network.
        
        Arranges the identification of the newcomer.
        Input Arguments:
            mutated_obj -> A tuple is fed, the first argument of the tuple determines the nature of the 
            mutation, whereas the second argument determines number of mutations inflicted on each round.
            rule -> If possible, a rule for mutation will be implemented.
            howmany -> The number of mutants that will be returned for each call. 
        '''
        
        mutant_list = []
        
        for mutant_ctr in range(0,howmany):
            
            mutated_network = copy.copy(self)
            mutant_adj = copy.copy(mutated_network.adjacency)
            mutant_mask = copy.copy(mutated_network.mask)
            
            if (mutated_obj[0] == 'Both' or mutated_obj[0] == 'Connections'):
                num.random.seed()
                random_i = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                num.random.seed()
                random_j = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                for ith_row in random_i:
                    for jth_column in random_j:
                        if mutant_adj[ith_row][jth_column] == 1:
                            mutant_adj[ith_row][jth_column] = 0
                        elif mutant_adj[ith_row][jth_column] == 0:
                            mutant_adj[ith_row][jth_column] = 1
                        
            
            if (mutated_obj[0] == 'Both' or mutated_obj[0] == 'Mask'):
                num.random.seed()
                random_i = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                num.random.seed()
                random_j = num.random.randint(0, self.n_nodes-1, size=mutated_obj[1])
                for ith_row in random_i:
                    for jth_column in random_j:
                        if mutant_mask[ith_row][jth_column] == 1:
                            mutant_mask[ith_row][jth_column] = 0
                        elif mutant_mask[ith_row][jth_column] == 0:
                            mutant_mask[ith_row][jth_column] = 1
                        
            mutated_network.adjacency = mutant_adj
            mutated_network.mask = mutant_mask
            
            ##
            # Records the fact that self is the mama of the mutant.
            # Has no children, et cetera.
            
            mutated_network.mama = self
            mutated_network.children = []
            mutated_network.nx=nx.DiGraph(mutated_network.adjacency)
            
            ##
            # Records that self has a mutant child somewhere
            
            self.children.append(mutated_network)
            mutant_list.append(mutated_network) 
            
        return mutant_list
    
class family(object, probeable_obj):
    '''
    Family Class.
    A class that will have a single family of networks, a genetic algorithm 
    will be run within a family. The macro parameters of a group of network, 
    though may also be reached from a list of networks, will be housed in a 
    family in a more structured manner.
    '''
    
    def __init__ (self):
        probeable_obj.__init__(self)
        self.network_list = []
        self.wildtype_list = [] 
        self.scores = num.array([])
        self.scores_history = []
    
    def add_to_family(self, network):
        '''
        This method will add a network to the specified family.
        network -> The network that is to be appended to the family.
        '''
        
        
        if network in self.network_list:
            print "The network that you're trying to add to the family is already a member."
            print "Please clone the individual and append the clone."
            return False
        
        self.network_list.append(network)
        return True
            
    def plot_scores(self):
             
        plt.plot(self.scores)
        
        # Wont go on unless the Window is closed.
        plt.show()
        
    def populate_wildtype(self,wildtype_threshold):
        '''
        Finds the wild types in a family and populates the list wildtype_list with them.
        Input Arguments
            wildtype_threshold -> a threshold for the score of he individual in order to attend
            the wildtype club.
        '''
        if len(self.scores) == 0:
            if print_enable:
                print "Warning: Equilibria not found."
                print "Populating equilibria ..."
            self.populate_equilibria_in_family()
            if print_enable:
                print "    Done!"
        
        print "Checking individuals in this family by their scores"
        for network in self.network_list:
            if network.score == 0:
                if print_enable:
                    print "Warning: Network "+str(network)+" has no information on its equilibrium"
                    print "Now calculating its equilibria..."
                network.populate_equilibria()
                if print_enable:    
                    print "    Done!"
                
            if network.score < wildtype_threshold:
                if print_enable:
                    print "Network "+str(id(network))+" is wild."
                self.wildtype_list.append(network)
        
        self.populate_probes(probes.populate_wildtype)
        return True
    
    def populate_equilibria_in_family(self):
        '''
        If the family has individuals, it goes to each individual and finds the equilibria 
        for all possible initial conditions they may face. The orbits and scores are 
        assigned to each one of them.
        '''
        
        if len(self.network_list) == 0:
            print "Warning: There is nobody in this family."
            print "Please adopt individuals."
            return False
            
        self.scores = num.zeros(len(self.network_list))
        
        for id,network in enumerate(self.network_list): 
            if print_enable:
                print "("+str(id+1)+"/"+str(len(self.network_list))+") Populating equilibrium for: "+str(network)
            network.populate_equilibria()
            self.scores[id] = network.score
        self.populate_probes(probes.populate_equilibria_in_family)
            
    def genetic_iteration(self,score_threshold,mutant_recipe=('Both',1),howmany_gntc=1):
        '''
        Runs one iteration of the genetic algorithm.
        It finds wildtypes of the family, mutates them, populates the family with mutants
        and assasinates as much of it has mutated. 
        '''
        if self.wildtype_list != []:
            self.wildtype_list = []
        if print_enable:
            print "Determining wildtypes"
        self.populate_wildtype(score_threshold)
        if print_enable:
            print str(len(self.wildtype_list))+"wild individuals"
        kill_count = len(self.wildtype_list)
        family_count = len(self.network_list)
        
        #    Prepare a vector that has ones for each to be killed, zeroes for all remain.
        #    and permute its elements randomly.
        
        array = [1]*kill_count+[0]*(family_count-kill_count)
 
        random_kill_list = num.random.permutation(array)
        
        #    Tag each element as None for those who'll be killed
        
        for number,to_be_killed in enumerate(random_kill_list):
            if to_be_killed == 1:
                if print_enable:
                    print str(self.network_list[number])+" is killed with score"+str(self.network_list[number].score) 
                self.network_list[number] = None
                
        #    If there are ones that are killed, populate the remaining gaps with mutated wildtypes.
        counter_wt = 0
        
        for network_ctr,all_networks in enumerate(self.network_list):
            if all_networks == None:
                if print_enable:
                    print "mutating network "+str(self.wildtype_list[counter_wt])
                self.network_list[network_ctr] = self.wildtype_list[counter_wt].mutant(mutated_obj=mutant_recipe,howmany=howmany_gntc)[0]
                if print_enable:    
                    print "finding equilibria of the new network "+str(self.network_list[network_ctr])
                self.network_list[network_ctr].populate_equilibria()
                self.scores[network_ctr] = self.network_list[network_ctr].score
                counter_wt = counter_wt +1
                
        self.scores_history = num.append(self.scores_history,self.scores)
        self.populate_probes(probes.genetic_iteration)
        return self.scores
        

    def genetic_algorithm(self,howmany=5,*args,**kwargs):
        """
        The wrapper for consecutive genetic iterations.
        """
        self.populate_equilibria_in_family()
        
        for ctr in range(howmany[0]):
            meanscore = self.scores.mean()
            if print_enable:
                print "Iteration "+str(ctr)+" Mean Score is: "+str(meanscore)
            self.genetic_iteration(meanscore,howmany[1])
        self.populate_probes(probes.genetic_algorithm)

