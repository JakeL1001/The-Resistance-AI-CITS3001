from agent import Agent
import random

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
        self.spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4}
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list
        self.worlds = {}
        
        # print(number_of_players)
        # print(player_number)
        if self.spy_count[number_of_players] == 2:
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    if not self.is_spy() and x == self.player_number or y == self.player_number:
                        self.worlds[(x,y)] = "INVALID"
                    else:
                        self.worlds[(x,y)] = "VALID"
        elif self.spy_count[number_of_players] == 3:
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number):
                            self.worlds[(x,y,z)] = "INVALID"
                        else:
                            self.worlds[(x,y,z)] = "VALID"
        elif self.spy_count[number_of_players] == 4:
            for x in range(number_of_players):
                for y in range(x+1, number_of_players):
                    for z in range(y+1, number_of_players):
                        for w in range(z+1, number_of_players):
                            if not self.is_spy() and (x == self.player_number or y == self.player_number or z == self.player_number or w == self.player_number):
                                self.worlds[(x,y,z,w)] = "INVALID"
                            else:
                                self.worlds[(x,y,z,w)] = "VALID"

        temp = self.worlds.copy()
        for key, value in self.worlds.items():
            if value == "INVALID":
                temp.pop(key)
        self.worlds = temp.copy()
        startingChance = 1/len(self.worlds)
        for key, value in self.worlds.items():
                self.worlds[key] = startingChance
        
        print(self.worlds)
        self.order_worlds()
        
    def order_worlds(self):
        self.worlds = {x: y for x, y in sorted(self.worlds.items(), key=lambda item: item[1], reverse=True)}
        # Re-orders the list of agents in descending order of most likely to be spies, so first element is most likely to be spy
        # list(self.probabilities)[0] would return the first element of the list of suspicion, which is the player with the highest suspicion

    def is_spy(self): # returns True iff the agent is a spy
        return self.player_number in self.spy_list

    def propose_missionTEST(self, team_size, betrayals_required = 1): # Must select mission based off internal knowledge, If spy, put spies on team, if resistance, put not spies on team
        # Select players with least chance of being spy (to include self or not?)
        # Include self means that 1 guaranteed resistance, but can draw more heat if mission fails, other resistance may suspect us of being a spy, can test
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        self.order_probabilities() # Ensure that all players are in order of suspicion
        teamHelper = list(self.probabilities)
        
        team = []
        if self.is_spy(): # TODO remember to use betrayals_required
            # loop through list of players in order of suspicion, find the last player who is a spy, and put them on the team, least likely to be voted against by resistance
            # Choose so that spies win
            spiesSelected = 0
            for x in range(len(teamHelper)-1, 0, -1):
                # print(x)
                if teamHelper[x] in self.spy_list and spiesSelected < betrayals_required:
                    team.append(teamHelper[x])
                    spiesSelected += 1
            for x in range(team_size - spiesSelected):
                if teamHelper[x] not in self.spy_list and len(team) < team_size-1:
                    team.append(teamHelper[x])
            # print("LEAST SUSPICIOUS SPY = ", leastSusSpy)
            # team.append(leastSusSpy)
        else:
            # Choose so that resistance wins, select least suspicious members
            teamHelper.reverse() # Reverse the list so that the first element is the least likely to be voted against by resistance
            for x in range(team_size):
                team.append(teamHelper[x]) # TODO decide if we want to include ourselves in every team or not
        random.shuffle(team) # Shuffle the team so that the spy is not always last, so that opponents can't model us based off of team proposal order
        print("I selected team: ", team, team_size, " \n")
        return team

    def propose_mission(self, team_size, betrayals_required = 1):
        team = []
        
        return team
        
    def vote(self, mission, proposer): # If proposer is suspected spy, be careful of voting yes, if members of mission are suspected spies, vote no
        # CheckAllChance() return list of players in order of suspicion, if any players are too suspicious, vote no
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        return random.random()<0.5

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
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        By default, spies will betray 30% of the time. 
        '''
        if self.is_spy():
            return random.random()<0.3

    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        # Update internal perception of players
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
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
        pass