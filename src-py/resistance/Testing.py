from random_agent import RandomAgent
from BasicBayes import BasicBayes
from agent2 import Agent2
from BayesJond import BayesJond
from game import Game
import random
import pandas as pd
from multiprocessing import Process


# agents = [RandomAgent(name='r1'), 
#         RandomAgent(name='r2'),  
#         RandomAgent(name='r3'),  
#         # RandomAgent(name='r4'),  
#         RandomAgent(name='r5'),  
#         RandomAgent(name='r6'),  
#         RandomAgent(name='r7'),
#         Agent1(name="TEST")]



# agents = [Agent1(name='TEST'), 
#         Agent2(name='r2'),  
#         RandomAgent(name='r3'),  
#         # RandomAgent(name='r4'),  
#         RandomAgent(name='r5'),  
#         RandomAgent(name='r6'),  
#         RandomAgent(name='r7'),
#         BayesJond(name="r8")]


# agents = [BayesJond(name='r1'), 
#         BayesJond(name='r2'),  
#         BayesJond(name='r3'),  
#         # RandomAgent(name='r4'),  
#         BayesJond(name='r5'),  
#         BayesJond(name='r6'),  
#         BayesJond(name='r7'),
#         BayesJond(name="TEST")]


# agents = [Agent1(name='r1'), 
#         Agent1(name='r2'),  
#         Agent1(name='r3'),  
#         # RandomAgent(name='r4'),  
#         Agent1(name='r5'),  
#         Agent1(name='r6'),  
#         BasicBayes(name='r7'),
#         BasicBayes(name="TEST")]

# agents = [Agent2(name='r1'), 
#         Agent2(name='r2'),  
#         Agent2(name='r3'),  
#         # RandomAgent(name='r4'),  
#         Agent2(name='r5'),  
#         Agent2(name='r6'),  
#         Agent2(name='r7'),
#         Agent2(name="TEST")]        

# game = Game(agents)
# game.play()
# print(game.missions_lost)
agents = [RandomAgent(name='r1'), 
                RandomAgent(name='r2'),  
                RandomAgent(name='r3'),  
                # RandomAgent(name='r4'),  
                RandomAgent(name='r5'),  
                RandomAgent(name='r6'),  
                RandomAgent(name='r7'),
                BasicBayes(name="TEST")]


if __name__ == "__main__":
    Basic = [BasicBayes(name='basic1'),
            BasicBayes(name='basic2'),  
            BasicBayes(name='basic3'),    
            BasicBayes(name='basic4'),  
            BasicBayes(name='basic5'),  
            BasicBayes(name='basic6'),
            BasicBayes(name="basic7"),
            BasicBayes(name="basic8"),
            BasicBayes(name="basic9")]
    
    Jond = [BayesJond(name='jond1'),
            BayesJond(name='jond2'),
            BayesJond(name='jond3'),
            BayesJond(name='jond4'),
            BayesJond(name='jond5'),
            BayesJond(name='jond6'),
            BayesJond(name="jond7"),
            BayesJond(name="jond8"),
            BayesJond(name="jond9")]
    
    Random = [RandomAgent(name='random1'),
            RandomAgent(name='random2'),
            RandomAgent(name='random3'),
            RandomAgent(name='random4'),
            RandomAgent(name='random5'),
            RandomAgent(name='random6'),
            RandomAgent(name="random7"),
            RandomAgent(name="random8"),
            RandomAgent(name="random9")]
    
    Combination = [RandomAgent(name='random1'),
                BasicBayes(name='basic1'),
                BayesJond(name='jond1'),
                RandomAgent(name='random2'),
                BasicBayes(name='basic2'),
                BayesJond(name='jond2'),
                RandomAgent(name='random3'),
                BasicBayes(name='basic3'),
                BayesJond(name='jond3'),]
        
    agentsToTest = ["BasicBayes", "BayesJond"]
    opponentlist = [Random, Basic, Jond, Combination]
    # opponentlisttostring = {Random: "Random", Basic: "Basic", Jond: "Jond", Combination: "Combination"}
    opponentstringtolist = {'Random': Random, 'Basic': Basic, 'Jond': Jond, 'Combination': Combination}
    
    games = 1
    
    for subject in agentsToTest: #Tests BasicBayes and BayesJond
        for opponentstring in opponentstringtolist: # Tests against Random, Basic, Jond, and Combination
            opponents = opponentstringtolist[opponentstring]
            for x in range(5,11): # Tests game size between 5 and 10 inclusive
                print("Testing " + subject + " against " + opponentstring + " with " + str(x) + " agents")
                if opponentstring == "Combination": # Randomizes the combination of agents
                    random.shuffle(opponents)
                agents = opponents[:x-1]
                agents.append(eval(subject)(name=subject + opponentstring)) # Adds the subject to the agents list
                for i in range(games): # Tests each combination 20,000 times
                    game = Game(agents)
                    game.play()


        # df = pd.read_csv('outcomes.csv')
        # df = df.reset_index()

        # df.columns = ['Role', 'Win']
        # total_wins = df[df['Win'] == 'Won']
        # spy_wins = df[df['Role'] == 'I was spy' ]
        # games_as_spy = spy_wins['Win'].count()
        # spy_wins = spy_wins[spy_wins['Win'] == 'Won']

        # res_wins = df[df['Role'] == 'I was not spy' ]
        # games_as_res = res_wins['Win'].count()
        # res_wins = res_wins[res_wins['Win'] == 'Won']

        # wins = total_wins['Win'].count()
        # total_winrate =  (spy_wins['Win'].count() + res_wins['Win'].count()) / (games_as_res + games_as_spy)
        # spy_winrate = spy_wins['Win'].count()/games_as_spy
        # res_winrate = res_wins['Win'].count()/games_as_res
        # print('Total winrate was:', total_winrate)
        # print('Spy winrate was:', spy_winrate)
        # print('Resistance winrate was:', res_winrate)
