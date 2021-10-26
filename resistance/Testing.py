from random_agent import RandomAgent
from BasicBayes import BasicBayes
from agent2 import Agent2
from BayesJond import BayesJond
from game import Game
import random
import pandas as pd
from multiprocessing import Process

def loopgames(subject, opponentstring, x, opponents, games):
    print("Testing " + subject + " against " + opponentstring + " with " + str(x) + " agents")
    if opponentstring == "Combination": # Randomizes the combination of agents
        random.shuffle(opponents)
    agents = opponents[:x-1]
    agents.append(eval(subject)(name=subject + opponentstring)) # Adds the subject to the agents list
    for i in range(games): # Tests each combination 20,000 times
        game = Game(agents)
        game.play()

def loopgames2(opponentstringtolist, opponentstring, games, subject):
    opponents = opponentstringtolist[opponentstring]
    # subject = subject + "Agent" # ONLY NEEDED FOR TESTING THE RANDOM AGENT uncomment when testing random agent
    for x in range(5,11): # Tests game size between 5 and 10 inclusive
        print("Testing " + subject + " against " + opponentstring + " with " + str(x) + " agents")
        if opponentstring == "Combination": # Randomizes the combination of agents
            random.shuffle(opponents)
        agents = opponents[:x-1]
        agents.append(eval(subject)(name=subject + opponentstring)) # Adds the subject to the agents list
        for i in range(games): # Tests each combination 20,000 times
            game = Game(agents)
            game.play()

if __name__ == "__main__":
    Basic = [BasicBayes(name='basic1'), # Creates team of BasicBayes opposing agents, up to 9 players, creating a team of 10
            BasicBayes(name='basic2'),  
            BasicBayes(name='basic3'),    
            BasicBayes(name='basic4'),  
            BasicBayes(name='basic5'),  
            BasicBayes(name='basic6'),
            BasicBayes(name="basic7"),
            BasicBayes(name="basic8"),
            BasicBayes(name="basic9")]
    
    Jond = [BayesJond(name='jond1'), # Creates team of BayesJond opposing agents, up to 9 players, creating a team of 10
            BayesJond(name='jond2'),
            BayesJond(name='jond3'),
            BayesJond(name='jond4'),
            BayesJond(name='jond5'),
            BayesJond(name='jond6'),
            BayesJond(name="jond7"),
            BayesJond(name="jond8"),
            BayesJond(name="jond9")]
    
    Random = [RandomAgent(name='random1'), # Creates team of RandomAgent opposing agents, up to 9 players, creating a team of 10
            RandomAgent(name='random2'),
            RandomAgent(name='random3'),
            RandomAgent(name='random4'),
            RandomAgent(name='random5'),
            RandomAgent(name='random6'),
            RandomAgent(name="random7"),
            RandomAgent(name="random8"),
            RandomAgent(name="random9")]
    
    Combination = [RandomAgent(name='random1'), # Creates team of a combination of the other opposing agents, up to 9 players, creating a team of 10
                BasicBayes(name='basic1'),
                BayesJond(name='jond1'),
                RandomAgent(name='random2'),
                BasicBayes(name='basic2'),
                BayesJond(name='jond2'),
                RandomAgent(name='random3'),
                BasicBayes(name='basic3'),
                BayesJond(name='jond3'),]
        
    agentsToTest = ["BasicBayes", "BayesJond"] # List of agents to test
    # agentsToTest = ["Random"] # Test separately to compare results
    opponentlist = [Random, Basic, Jond, Combination] # List of teams to test each agent against
    opponentstringtolist = {'Random': Random, 'Basic': Basic, 'Jond': Jond, 'Combination': Combination} 
    
    games = 20000   # Number of games for each agent to verse each type of team for each size of game. eg for 2 agents vs 4 teams with between 5-10 players and 20,000 games, 
                    # there will be a total of 960,000 test games played
    
    for subject in agentsToTest: #Tests BasicBayes and BayesJond
        processes = []
        for opponentstring in opponentstringtolist: # Tests against Random, Basic, Jond, and Combination
            p = Process(target=loopgames2, args=(opponentstringtolist, opponentstring, games, subject)) # Uses multiprocessing to run much faster, each thread tests an opposing team
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
            
    '''
    REMEMBER, BEFORE RUNNING, UNCOMMMENT THE LAST FUNCITON IN THE EACH OF THE BASICBAYES AND BAYESJOND AGENTS, OR NO CSV OF RESULTS WILL BE MADE
    '''
