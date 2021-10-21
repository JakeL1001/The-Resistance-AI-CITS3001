import itertools
from agent import Agent
import random

class BasicBayes(Agent):
    """
    self.worlds stores a dictionary of all possible worlds, where each key is a tuple of the a combinations players in the world, 
                assuming the players of whose names are in the tuple are both spies, and the value is the likelihood of that world being the real world.
                eg. if (1,2): 0.4, then there is a 40% chance of the real world having players 1 and 2 as spies.
    self.spy_count stores a dict of how many spies are in a game in regards to how many players are in the game, eg a game with 5 players has 2 spies
    """

    def __init__(self, name='BasicBayes'): # Initialises the agent
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
        self.mission_Number = 0 # The index of the current mission number, for indentifying how many betrayals are required
        
        if self.spy_count[number_of_players] == 2: # Creates the combination of worlds for a game containing 2 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    if not self.is_spy() and x == self.player_number or y == self.player_number:
                        pass # Used to ignore worlds in which the player is a spy, as they do not need to be accounted for
                    else:
                        self.worlds[(x,y)] = 0
        elif self.spy_count[number_of_players] == 3: # Creates the worlds for a game of 3 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number):
                            pass
                        else:
                            self.worlds[(x,y,z)] = 0
        elif self.spy_count[number_of_players] == 4: # Creates the worlds for a game of 4 spies
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        for w in range(z+1, number_of_players):
                            if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number or w == self.player_number):
                                pass
                            else:
                                self.worlds[(x,y,z,w)] = 0

        # set the starting chance of a world being true to the same value
        startingChance = 1/len(self.worlds) # Gives each world the same chance of being true, which is 1/number of worlds
        for key, value in self.worlds.items(): 
                self.worlds[key] = startingChance

    def is_spy(self): # returns True iff the agent is a spy
        return self.player_number in self.spy_list

    def calculate_probabilities(self):
        # Calculate the probability of each player being a spy, return as a dict of {player_id: probability}
        orderedProbs = {} # Includes the agent as suspicion of 0, may not be viable for a spy to think itself as not suspicious
        for x in range(self.number_of_players):
            temp = []
            if (x != self.player_number or self.is_spy()) and self.number_of_players-1 != self.player_number:
                for key, value in self.worlds.items(): # Loops through all worlds in which a player exists as a spy
                    if x in key:
                        temp.append(value)
                orderedProbs[x] = (sum(temp) / len(temp)) # Averages the suspicion of each player in the worlds in which they are spies
            else:
                orderedProbs[x] = 0 # Sets own suspicion to 0
        orderedProbs = {x: y for x, y in sorted(orderedProbs.items(), key=lambda item: item[1], reverse=True)} # Sorts the list in descending order of suspicion
        total = 0
        for agents, suspicion in orderedProbs.items(): # Loop through each player's suspicion scores
            total += suspicion
        average = total/len(orderedProbs) # Calculates the average suspicion of all players in the game
        return orderedProbs, average


    def propose_mission(self, team_size, betrayals_required = 1): # Calculate the probability of each player being a spy, then select the "team_size" lowest suspicion players
        team = []
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion
        probabilities = list(probabilities)
        if self.is_spy(): # If the agent is a spy, choose a team most likely to pass the vote, but still contain a spy
            spiesSelected = 0
            for x in range(len(probabilities)-1, 0, -1): # looping backwards over the list, find the first spy (least suspicious, and add them to the team)
                if probabilities[x] in self.spy_list and spiesSelected < betrayals_required: # Ensure that the number of spies selected is less than the number of spies required
                    team.append(probabilities[x]) # Add the spy to the mission
                    spiesSelected += 1 # Increment the number of spies selected, If the number of spies selected is equal to the number of betrayals required, then do not select more spies
            for x in range(team_size - spiesSelected+1): # for the remaining number of players required, add the next least suspicious players to the team, more likely to suceed vote
                if probabilities[x] not in self.spy_list and len(team) < team_size-1:
                    team.append(probabilities[x])
        else: # If the agent is not a spy, choose a team with the least suspicion, least chance of containing a spy
            probabilities.reverse() # Reverse the list so that the first element is the least likely to be a spy
            for x in range(team_size):
                team.append(probabilities[x])
        random.shuffle(team) # Shuffle the team so that the spy is not always last, so that opponents can't model us based off of team proposal order
        return team

    def vote(self, mission, proposer): # Returns decision on whether or not to vote for a mission. Resistance want high confidence of no spies, spies want a mission that will fail
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        probabilities, average = self.calculate_probabilities() # returns list of agents in descending order of suspicion

        if not self.is_spy(): # If Resistance, deny missions with suspicious proposers or mission members
            if list(probabilities.keys()).index(proposer) < self.spy_count[self.number_of_players] - 1: # If the proposer is in the top "number of spies" index of the suspicion list, deny mission
                return False
            else:   # If any agents in mission are in top "number of spies" index of the suspicion list, deny mission
                for x in mission:
                    if list(probabilities.keys()).index(x) < self.spy_count[self.number_of_players] - 1: # If the index is within the top number of spots in the suspicion list that there are spies, deny mission
                        return False
                return True # If no reason to vote no, vote yes
        else: # If the agent is a spy, pass mission with spys on them, but not too suspicious, as it may incriminate yourself
            if probabilities.get(proposer) > average: # If the proposer is more suspicious than average, then vote no
                return False
            else:
                for x in mission:
                    if probabilities.get(x) > average: # if any mission members are more suspicious than average, then vote no
                        return False
                if sorted(mission) == sorted(self.spy_list): # If entire spy team is on mission, vote no
                    return False
                return True

    def vote_outcome(self, mission, proposer, votes): 
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        #nothing to do here
        pass

    def betray(self, mission, proposer): # True or False bsed on whether you wan't to betray the mission or not. BasicBayes always betrays
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        return True

    def mission_outcome(self, mission, proposer, betrayals, mission_success): # Update suspicion of players based on outcome of the mission
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

                # total is the total number of combinations that a mission could end in
                # each agent either passes the mission (True), or fails the mission (False)
                # e.g. for a mission with 3 agents, the possible outcomes are:
                # (True, True, True), (True, True, False), (True, False, True), (True, False, False), (False, True, True), (False, True, False), (False, False, True), (False, False, False)
                total = list(itertools.product([True, False], repeat = len(mission)))
                
                # the chance of failing a mission is the number of combinations divided by the total
                fail_chance[combination] = len(comb)/len(total)

                # sum the product of P(C) and P(F|C) to get P(F)
                total_fail += fail_chance[combination] * self.worlds[combination]
                
            for combination in fail_chance: # update the worlds based on the new P(F) values
                try:
                    self.worlds[combination] = fail_chance[combination] * self.worlds[combination] / total_fail
                except ZeroDivisionError:
                    self.worlds[combination] = 0

        self.mission_Number += 1

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
        # Outputs result of each game to csv, used for testing performance of the agent.
        # Commented out from Code for final submission and tournament play
        pass
        """
        if self.name == 'BasicBayesRandom':
            if self.is_spy():
                if spies_win:
                    with open('BasicBayesRandom.csv','a') as fd:
                        fd.write('{} players,I was spy,Won\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesRandom.csv','a') as fd:
                        fd.write('{} players,I was spy,Lost\n'.format(self.number_of_players))
            else:
                if spies_win:
                    with open('BasicBayesRandom.csv','a') as fd:
                        fd.write('{} players,I was not spy,Lost\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesRandom.csv','a') as fd:
                        fd.write('{} players,I was not spy,Won\n'.format(self.number_of_players))
                        
        elif self.name == 'BasicBayesBasic':
            if self.is_spy():
                if spies_win:
                    with open('BasicBayesBasic.csv','a') as fd:
                        fd.write('{} players,I was spy,Won\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesBasic.csv','a') as fd:
                        fd.write('{} players,I was spy,Lost\n'.format(self.number_of_players))
            else:
                if spies_win:
                    with open('BasicBayesBasic.csv','a') as fd:
                        fd.write('{} players,I was not spy,Lost\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesBasic.csv','a') as fd:
                        fd.write('{} players,I was not spy,Won\n'.format(self.number_of_players))
        
        elif self.name == 'BasicBayesJond':
            if self.is_spy():
                if spies_win:
                    with open('BasicBayesJond.csv','a') as fd:
                        fd.write('{} players,I was spy,Won\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesJond.csv','a') as fd:
                        fd.write('{} players,I was spy,Lost\n'.format(self.number_of_players))
            else:
                if spies_win:
                    with open('BasicBayesJond.csv','a') as fd:
                        fd.write('{} players,I was not spy,Lost\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesJond.csv','a') as fd:
                        fd.write('{} players,I was not spy,Won\n'.format(self.number_of_players))
        
        elif self.name == 'BasicBayesCombination':
            if self.is_spy():
                if spies_win:
                    with open('BasicBayesCombination.csv','a') as fd:
                        fd.write('{} players,I was spy,Won\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesCombination.csv','a') as fd:
                        fd.write('{} players,I was spy,Lost\n'.format(self.number_of_players))
            else:
                if spies_win:
                    with open('BasicBayesCombination.csv','a') as fd:
                        fd.write('{} players,I was not spy,Lost\n'.format(self.number_of_players))
                else:
                    with open('BasicBayesCombination.csv','a') as fd:
                        fd.write('{} players,I was not spy,Won\n'.format(self.number_of_players))
        """

