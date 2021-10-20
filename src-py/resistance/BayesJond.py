import itertools
from agent import Agent
import random

# IMPLEMENT EXPERT RULES
# TODO Keep in mind mission sizes vs number of agents, always will have a spy if not on mission DONE 
# TODO Avoid failing with more spies than required number of betrayals Done
# TODO Spies always fail after 2 missions have failed, will guarantee a win Done
# TODO Always vote no if not on mission Done


class BayesJond(Agent): #TODO Rename based on algorithm used
    """
    All players should start with equal chance of being spy, IF resistance in game of 5 players, each other player has a 50% chance of being a spy, 
    as it is 2/4 chance of being a spy if we are not included in the count. This should be kept in mind and update when playing as spy too, as it can help avoid detection
    
    self.worlds stores a dictionary of all possible worlds, where each key is a tuple of the a combinations players in the world, 
                assuming the players of whose names are in the tuple are both spies, and the value is the likelihood of that world being the real world.
                eg. if (1,2): 0.4, then there is a 40% chance of the real world having players 1 and 2 as spies.
    self.number_of_players stores an int of the number of players in the game
    self.player_number stores an int of the player number of this agent
    self.spy_list stores a list of ints of the player indexes of the spies in the game
    self.spy_count stores a dict of how many spies are in a game in regards to how many players are in the game, eg a game with 5 players has 2 spies
    """

    def __init__(self, name='Bayes Jond 007'): # Initialises the agent. # TODO change name
        self.name = name

    def new_game(self, number_of_players, player_number, spy_list): 
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4} # Returns the number of spies in a game of a relavent size eg a game with 9 players, self.spy_count[9] returns 3
        self.number_of_players = number_of_players # The number of players in the game
        self.player_number = player_number # The agent's player number
        self.spy_list = spy_list # The list of spy indexes, empty if the agent is not a spy
        self.worlds = {} # Stores the worlds and their probabilities, will be updated as the game progresses
        self.votecount = 0 # Stores the number of failed votes
        self.mission_Number = 0 # The index of the current mission number, for indentifying how many betrayals are required
        self.spy_score = 0 # The number of points that the spies have, 3 == win for spies
        
        if self.spy_count[number_of_players] == 2: # Creates the worlds for a game of 2 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    self.worlds[(x,y)] = "VALID"
        elif self.spy_count[number_of_players] == 3: # Creates the worlds for a game of 3 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        self.worlds[(x,y,z)] = "VALID"
        elif self.spy_count[number_of_players] == 4: # Creates the worlds for a game of 4 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        for w in range(z+1, number_of_players):
                            self.worlds[(x,y,z,w)] = "VALID"


        # set the starting chance of a world being true to the same value
        startingChance = 1/len(self.worlds)
        for key, value in self.worlds.items(): 
                self.worlds[key] = startingChance

    def is_spy(self): # returns True iff the agent is a spy
        return self.player_number in self.spy_list

    def calculate_probabilities(self):
        '''
        calculates and sorts the suspiciousness of each player using values from self.worlds
        returns a dictionary mapping suspiciousness to player numbers and the average suspiciousness
        '''

        orderedProbs = {} # dictionary to populate
        for x in range(self.number_of_players): # Loop throuhg all players
            temp = [] # list to hold probabilities of worlds containing player x
            for key, value in self.worlds.items(): # Loops through all worlds
                if x in key: 
                    temp.append(value) 
            orderedProbs[x] = (sum(temp) / len(temp)) # Averages the suspicion of each player in the worlds in which they are spies
            
        orderedProbs = {x: y for x, y in sorted(orderedProbs.items(), key=lambda item: item[1], reverse=True)} # Sorts the list in descending order of suspicion
        total = 0 # variable used to calculate average suspiciousness
        for agents, suspicion in orderedProbs.items():
            total += suspicion
        average = total/len(orderedProbs)
        return orderedProbs, average

    def propose_mission(self, team_size, betrayals_required = 1): # Calculate the probability of each player being a spy, then select the "team_size" lowest people
        '''
        team_size is the required mission size
        betrayals_required is the number of betrayals needed for the mission to fail
        '''
        team = []
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion
        probabilities = list(probabilities) # get only the keys of the dictionary

        # EXPERT RULES: Always include self in proposition
        team.append(self.player_number)
        team_size -= 1
        
        
        if self.is_spy(): # If the agent is a spy, choose a team most likely to pass the vote, but still contain a spy
            # EXPERT RULES: self is already selected
            spiesSelected = 1
            for x in range(len(probabilities)-1, 0, -1): # looping backwards over the list, find the first spy (least suspicious, and add them to the team)
                # Check that least suspicious player is not the agent, and that the number of spies selected is less than the number of spies required
                # Check that agent is not adding itself again
                if probabilities[x] in self.spy_list and spiesSelected < betrayals_required and probabilities[x] != self.player_number: 
                    team.append(probabilities[x])
                    spiesSelected += 1 # Increment the number of spies selected, If the number of spies selected is equal to the number of betrayals required, then do not select more spies
            for x in range(team_size - spiesSelected+1): # for the remaining number of players required, add the next least suspicious players to the team, more likely to suceed vote
                if probabilities[x] not in self.spy_list and len(team) < team_size + 1 and probabilities[x] != self.player_number:
                    team.append(probabilities[x])
        else: # If the agent is not a spy, choose a team with the least suspicion, least chance of containing a spy
            probabilities.reverse() # Reverse the list so that the first element is the least likely to be a spy
            for x in range(team_size):
                if probabilities[x] != self.player_number:
                    team.append(probabilities[x]) 
        random.shuffle(team) # Shuffle the team so that the spy is not always last, so that opponents can't model us based off of team proposal order
        return team

    def vote(self, mission, proposer): # If proposer is suspected spy, be careful of voting yes, if members of mission are suspected spies, vote no
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion

        # EXPERT RULES
        # Always accept the final mission proposal, as voting no is not helpful for spies or resistance
        if self.votecount == 4:
            return True
        
        if not self.is_spy(): # If Resistance, deny missions with suspicious proposers or mission members
            # EXPERT RULES
            # If you are not in a mission with the number of players on the mission equal to the number of resistance members
            # then the mission is guaranteed to have a spy, so deny mission
            if len(mission) == (self.number_of_players - self.spy_count[self.number_of_players]) and self.player_number not in mission:
                return False
            # EXPERT RULES
            # Trust players that cannot be spies, assume they will make informed decisions
            if probabilities.get(proposer) == 0: 
                return True
            if probabilities.get(proposer) > average: # If the proposer is more suspicious than average, deny mission
                return False
            else:   
                for x in mission:
                    if probabilities.get(x) > average: # If any agents in mission are more suspicious, deny mission
                        return False
                # If mission and proposer pass the suspicion test, vote yes
                return True
        else: # If the agent is a spy, pass mission with spys on them, but not too suspicious, as it may incriminate yourself
            if probabilities.get(proposer) > average: # If the proposer is more suspicious than average, then vote no
                return False
            else:
                for x in mission:
                    if probabilities.get(x) > average: # if a player on the mission is more suspicious than average, deny mission
                        return False
                if sorted(mission) == sorted(self.spy_list):
                    # If mission of only spies, would be incriminating, deny mission
                    return False
                return True

    def vote_outcome(self, mission, proposer, votes): # use to keep track of how many votes have failed
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a list of players that voted in favour of the mission
        No return value is required or expected.
        '''
        yes = 0
        no = 0

        if len(votes) >= self.number_of_players/2: # increment if the vote fails
            self.votecount += 1
        else: # reset if the vote succeeds
            self.votecount = 0
        pass

    def betray(self, mission, proposer): 
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        
        if self.is_spy():
            Spies_in_mission = 0
            # Check the number of spies in the mission
            for x in mission: 
                if x in self.spy_list:
                    Spies_in_mission += 1
            # If 2 missions have alreay failed, always betray the mission if there are enough spies
            if self.spy_score == 2 and self.fails_required[self.number_of_players][self.mission_Number-1] <= Spies_in_mission:
                return True
            # If there are enough spies to betray the mission, choose to betray
            if self.fails_required[self.number_of_players][self.mission_Number-1] <= Spies_in_mission:
                return True
            else:
                return False
        else:
            return False

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        # Update internal perception of worlds
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        # if there was at least 1 betrayal, the worlds probabilities can be updated
        if betrayals != 0:
            fail_chance = self.worlds.copy() # this dictionary will store the P(F|W) values
            total_fail = 0
            # iterate through all the worlds
            for combination in fail_chance:
                # overlap is the agents in both the mission and current combination
                overlap = set(combination)&set(mission)

                # comb is the combinations of which agents could have chosen to betray
                # e.g. if we know that there were 2 betrayals, and overlap was [0, 1, 2],
                #      then the possible betrayal outcomes are:
                #      (0, 1), (0, 2) and (1, 2)
                comb = list(itertools.combinations(overlap, betrayals))

                # total is the total number of combinations that a mission could end in
                # each agent either passes the mission (True), or fails the mission (False)
                # e.g. for a mission with 3 agents, the possible outcomes are:
                # (True, True, True), (True, True, False), (True, False, True), (True, False, False), (False, True, True), (False, True, False), (False, False, True), (False, False, False)
                total = list(itertools.product([True, False], repeat = len(mission)))
                
                # the chance of failing a mission is the number of combinations divided by the total
                fail_chance[combination] = len(comb)/len(total)
                
                # sum the product of P(C) and P(F|C) to get P(F)
                total_fail += fail_chance[combination] * self.worlds[combination]
            
            for combination in fail_chance: # set the world probabilities to the newly calculated values
                self.worlds[combination] = fail_chance[combination] * self.worlds[combination] / total_fail
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the number of missions (0-3) that have failed.
        '''
        #nothing to do here
        pass
    
    def game_outcome(self, spies_win, spies): 
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        if self.name == 'TEST':
            if self.is_spy():
                if spies_win:
                    #if self.name == "TEST": print("I won!")
                    with open('outcomes.csv','a') as fd:
                        fd.write('I was spy,Won\n')
                else:
                    #if self.name == "TEST": print("I lost")
                    with open('outcomes.csv','a') as fd:
                        fd.write('I was spy,Lost\n')
            else:
                if spies_win:
                    #if self.name == "TEST": print("I lost")
                    with open('outcomes.csv','a') as fd:
                        fd.write('I was not spy,Lost\n')
                else:
                    #if self.name == "TEST": print("I won!")
                    with open('outcomes.csv','a') as fd:
                        fd.write('I was not spy,Won\n')
        pass
