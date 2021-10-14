import itertools
from agent import Agent
import random
import csv

class Agent1(Agent): #TODO Rename based on algorithm used
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

    def __init__(self, name='BayesAgent1'): # Initialises the agent. # TODO change name
        self.name = name

    def new_game(self, number_of_players, player_number, spy_list): # I think we can leave as is
        # Could set each players starting chance of being a spy, based on number of players, and number of spies
        # Do i update my own probability as other agents would see me, or keep my probability at 0 becuase it is known i am not a spy?
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        print("New game: ", number_of_players, player_number, spy_list) # Prints all relavent information about the game, good for debugging
        self.spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4} # Returns the number of spies in a game of a relavent size eg a game with 9 players, self.spy_count[9] returns 3
        self.number_of_players = number_of_players # The number of players in the game
        self.player_number = player_number # The agent's player number
        self.spy_list = spy_list # The list of spy indexes, empty if the agent is not a spy
        self.worlds = {} # Stores the worlds and their probabilities, will be updated as the game progresses
        
        # print(number_of_players)
        # print(player_number)
        if self.spy_count[number_of_players] == 2: # Creates the worlds for a game of 2 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    if not self.is_spy() and x == self.player_number or y == self.player_number:
                        self.worlds[(x,y)] = "INVALID" # Used to remove worlds in which the player is a spy, as they are not needed to be accounted for
                    else:
                        self.worlds[(x,y)] = "VALID"
        elif self.spy_count[number_of_players] == 3: # Creates the worlds for a game of 3 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number):
                            self.worlds[(x,y,z)] = "INVALID"
                        else:
                            self.worlds[(x,y,z)] = "VALID"
        elif self.spy_count[number_of_players] == 4: # Creates the worlds for a game of 4 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        for w in range(z+1, number_of_players):
                            if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number or w == self.player_number):
                                self.worlds[(x,y,z,w)] = "INVALID"
                            else:
                                self.worlds[(x,y,z,w)] = "VALID"

        # update the list of worlds to remove invalid worlds
        temp = self.worlds.copy()
        for key, value in self.worlds.items():
            if value == "INVALID":
                temp.pop(key)
        self.worlds = temp.copy()

        # set the starting chance of a world being true to the same value
        startingChance = 1/len(self.worlds)
        for key, value in self.worlds.items(): 
                self.worlds[key] = startingChance
        
        print(self.worlds)
        self.order_worlds() # orders the worlds in descending order of most likely to be spies, so first element is most likely to be spy
        
    def order_worlds(self):
        self.worlds = {x: y for x, y in sorted(self.worlds.items(), key=lambda item: item[1], reverse=True)}
        # Re-orders the list of agents in descending order of most likely to be spies, so first element is most likely to be spy
        # list(self.probabilities)[0] would return the first element of the list of suspicion, which is the player with the highest suspicion

    def is_spy(self): # returns True iff the agent is a spy
        return self.player_number in self.spy_list

    def calculate_probabilities(self):
        # Calculate the probability of each player being a spy, return as a dict of {player_id: probability}

        orderedProbs = {} # Includes the agent as suspicion of 0, may not be viable for a spy to think itself as not suspicious
        for x in range(self.number_of_players):
            temp = []
            if x != self.player_number or self.is_spy():
                for key, value in self.worlds.items(): # Loops through all worlds in which a player exists as a spy
                    if x in key:
                        temp.append(value)
                orderedProbs[x] = (sum(temp) / len(temp)) # Averages the suspicion of each player in the worlds in which they are spies
            else:
                orderedProbs[x] = 0 # Sets own suspicion to 0
            
        orderedProbs = {x: y for x, y in sorted(orderedProbs.items(), key=lambda item: item[1], reverse=True)} # Sorts the list in descending order of suspicion
        total = 0
        for agents, suspicion in orderedProbs.items():
            total += suspicion
        average = total/len(orderedProbs)
        print('average suspiciousness is:', average)
        print(orderedProbs)
        return orderedProbs, average


    def propose_mission(self, team_size, betrayals_required = 1): # Calculate the probability of each player being a spy, then select the "team_size" lowest people
        team = []
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion
        probabilities = list(probabilities)
        print(probabilities)
        if self.is_spy(): # If the agent is a spy, choose a team most likely to pass the vote, but still contain a spy
            spiesSelected = 0
            for x in range(len(probabilities)-1, 0, -1): # looping backwards over the list, find the first spy (least suspicious, and add them to the team)
                if probabilities[x] in self.spy_list and spiesSelected < betrayals_required and probabilities[x] != self.player_number: # Check that least suspicious player is not the agent, and that the number of spies selected is less than the number of spies required
                    team.append(probabilities[x])
                    spiesSelected += 1 # Increment the number of spies selected, If the number of spies selected is equal to the number of betrayals required, then do not select more spies
            for x in range(team_size - spiesSelected+1): # for the remaining number of players required, add the next least suspicious players to the team, more likely to suceed vote
                if probabilities[x] not in self.spy_list and len(team) < team_size-1:
                    team.append(probabilities[x])
        else: # If the agent is not a spy, choose a team with the least suspicion, least chance of containing a spy
            probabilities.reverse() # Reverse the list so that the first element is the least likely to be a spy
            for x in range(team_size+1):
                team.append(probabilities[x]) # TODO decide if we want to include ourselves in every team or not
        random.shuffle(team) # Shuffle the team so that the spy is not always last, so that opponents can't model us based off of team proposal order
        print("I selected team: ", team, team_size, " \n")
        return team

    def vote(self, mission, proposer): # If proposer is suspected spy, be careful of voting yes, if members of mission are suspected spies, vote no
        # RESTISTANCE
            # Could maybe only vote if all agents are in bottom half of suspicion list.
            # Do NOT vote if any members are most suspicious, or if the proposer is most suspicious
        # SPY
            # COULD implement voting no if it will incriminate you to unsafe levels
            # If the team contains less suspicious spies, vote yes, if the spy is very suspicious, vote no, as it may incriminate yourself
            # If you are on the team, vote yes unless it will greatly incrimiate you if you betray
            # If we vote no with no spies on the team, that's suspicious, so vote yes
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        #probabilities, average = list(self.calculate_probabilities()) # returns list of agents in descending order of suspicion
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion
        # mission = random.sample(range(1, 7), 3)
        # probabilities = random.sample(range(0, 7), 7)
        # print(probabilities)
        print("I am voting on mission: ", mission, proposer)
        print("Probabilities ", probabilities)
        # TODO parameter sweep of cut-offs to vote yes or no, eg how suspicious do we vote no against or yes against, 
        # TODO do we vote based on position or on actual likelihood of being a spy

        if not self.is_spy(): # If Resistance, deny missions with suspicious proposers or mission members
            if list(probabilities.keys()).index(proposer) < self.spy_count[self.number_of_players] - 1: # If the proposer is in the top "number of spies" index of the suspicion list, deny mission
                print("I am voting no, proposer bad")
                return False
            else:   # If any agents in mission are in top "number of spies" index of the suspicion list, deny mission
                for x in mission:
                    if list(probabilities.keys()).index(x) < self.spy_count[self.number_of_players] - 1: # If the index is within the top number of spots in the suspicion list that there are spies, deny mission
                        print("I am voting no")
                        return False
                print("I am voting yes") # If mission and proposer pass the suspicion test, vote yes
                return True
        else: # If the agent is a spy, pass mission with spys on them, but not too suspicious, as it may incriminate yourself
            #if probabilities.index(proposer) == 0: # If the proposer is the most suspicious player, deny mission
            if probabilities.get(proposer) > average: # If the proposer is more suspicious than average, then vote no
                print("I am voting no, proposer bad, too suspicious1")
                return False
            else:
                for x in mission:
                    # if probabilities.index(x) < 2: # if one of the 2 most suspicious players is on the mission, deny mission
                    # if probabilities.index(x) == 0: # if the most suspicious player is on the mission, deny mission
                    if probabilities.get(x) > average: # if the most suspicious player is on the mission, deny mission
                        print("I am voting no, mission bad, too suspicious2")
                        return False
                if sorted(mission) == sorted(self.spy_list):
                    print("I am voting no, mission bad, contains only spies"), # If mission of only spies, would be incriminating, deny mission
                    return False
                print("I am voting yes")
                return True

    def vote_outcome(self, mission, proposer, votes): # If people voted yes and mission failed, they could be spies, if people voted no and mission failed, they could be resistance
        # Update internal perception of players,
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        #nothing to do here
        pass

    def betray(self, mission, proposer): # Beware of betraying if already have or other spies on the same team
        # Could calculate if betrayal would increase the agents suspicion to bad levels
        # If number of spies in the mission is less than required to betray the mission, do not betray
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if self.is_spy():
            return True

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        # Update internal perception of players
        # TODO missions can still suceed with a betrayal
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        # if the mission fails, then the world probabilities can be updated
        if betrayals != 0:
            fail_chance = self.worlds.copy() # this dictionary will store the P(F|C) values
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
                #print(combination)
                #print('combinations are')
                #print(comb)

                # total is the total number of combinations that a mission could end in
                # each agent either passes the mission (True), or fails the mission (False)
                # e.g. for a mission with 3 agents, the possible outcomes are:
                # (True, True, True), (True, True, False), (True, False, True), (True, False, False), (False, True, True), (False, True, False), (False, False, True), (False, False, False)
                total = list(itertools.product([True, False], repeat = len(mission)))
                #print('permuations are', len(total))
                #print(total)
                # the chance of failing a mission is the number of combinations divided by the total
                fail_chance[combination] = len(comb)/len(total)
                # sum the product of P(C) and P(F|C) to get P(F)
                total_fail += fail_chance[combination] * self.worlds[combination]
            temp_world = self.worlds.copy()
            for combination in fail_chance:
                # temp_world[combination] = fail_chance[combination] * self.worlds[combination] / total_fail
                self.worlds[combination] = fail_chance[combination] * self.worlds[combination] / total_fail
        #else:
        #    fail_chance = 0
        #    total_fail = 0
        #    temp_world = 0
            

        #print(self.worlds)
        #print(fail_chance)
        #print(total_fail)
        #print(temp_world)
        #nothing to do here
        pass

    def round_outcome(self, rounds_complete, missions_failed): # Could implement if missions_failed == 2, and Agent is spy, always fail mission, as will always result in win
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the number of missions (0-3) that have failed.
        '''
        #nothing to do here
        pass
    
    def game_outcome(self, spies_win, spies): # Could save info about the spies for future games?
        # if an agent is performing similar actions to seen in previous games, then this could be used to deduce spy identities
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        #nothing to do here
        
        print('I was spy?', self.is_spy())
        if self.is_spy():
            if not spies_win:
                print("I won!")
                with open('outcomes.csv','a') as fd:
                    fd.write('I was spy,Won\n')
            else:
                print("I lost")
                with open('outcomes.csv','a') as fd:
                    fd.write('I was spy,Lost\n')
        else:
            if not spies_win:
                print("I lost")
                with open('outcomes.csv','a') as fd:
                    fd.write('I was not spy,Lost\n')
            else:
                print("I won!")
                with open('outcomes.csv','a') as fd:
                    fd.write('I was not spy,Won\n')
        pass

# print('scenario 1')
# a = Agent1
# Agent1.new_game(a, 8, 0, [])
# Agent1.mission_outcome(a, [1, 2, 3], 2, 1, False)

# print('scenario 2')
# Agent1.new_game(a, 6, 0, [])
# Agent1.mission_outcome(a, [1, 2], 2, 2, False)

#mission = [0, 1, 2]
#total = list(itertools.product([True, False], repeat = len(mission)))
#print(total)