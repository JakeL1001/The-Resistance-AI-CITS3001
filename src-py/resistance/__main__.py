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

def loopgames(NO_GAMES):
                print("looping")
                
if __name__ == "__main__":


        df = pd.DataFrame(list())
        df.to_csv('outcomes.csv')

        NO_GAMES = 100

        # processes = []
        # for i in range(5,11): # Runs 6 processes, each testing a different number of agents (DIFFERENT NUMBER OF PLAYERS NOT YET IMPLEMENTED)
        #         print(i)
        #         p = Process(target=loopgames, args=(NO_GAMES,))
        #         processes.append(p)
        #         p.start()
        # for p in processes:
        #         p.join()

        # for p in range(7,8):
        #         print(p)
        #         agents = []
        #         for x in range(1,p):
        #                 agents.append(RandomAgent(name="r{}".format(str(x))))
        #         agents.append(BayesJond(name="TEST"))
        #         random.shuffle(agents)
        #         print(agents)
        #         for i in range(NO_GAMES):
        #                 game = Game(agents)
        #                 game.play()

        
        agents1 = [BasicBayes(name='r1'), 
                                BasicBayes(name='r2'),  
                                BasicBayes(name='r3'),  
                                # RandomAgent(name='r4'),  
                                BasicBayes(name='r4'),  
                                BasicBayes(name='r5'),  
                                BasicBayes(name='r6'),
                                BasicBayes(name="r7"),
                                BasicBayes(name="r8"),
                                BasicBayes(name="r9")]
        agents2 = [Agent2(name='r1'),
                                Agent2(name='r2'),
                                Agent2(name='r3'),
                                # RandomAgent(name='r4'),
                                Agent2(name='r4'),
                                Agent2(name='r5'),
                                Agent2(name='r6'),
                                Agent2(name="r7"),
                                Agent2(name="r8"),
                                Agent2(name="r9")]
        agentsr = [RandomAgent(name='r1'),
                                RandomAgent(name='r2'),
                                RandomAgent(name='r3'),
                                # RandomAgent(name='r4'),
                                RandomAgent(name='r4'),
                                RandomAgent(name='r5'),
                                RandomAgent(name='r6'),
                                RandomAgent(name="r7"),
                                RandomAgent(name="r8"),
                                RandomAgent(name="r9")]
        
        agentcombos = [agents1, agents2, agentsr]
        for x in agentcombos:
                print(x)
                for p in range(5,11):
                        print(p)
                        agents = x[:p-1]
                        agents.append(BayesJond(name="TEST"))
                        print(agents)
                        random.shuffle(x)
                        for i in range(NO_GAMES):
                                game = Game(agents)
                                game.play()
                
                
        # agents = [RandomAgent(name='r1'), 
        #         RandomAgent(name='r2'),  
        #         RandomAgent(name='r3'),  
        #         RandomAgent(name='r4'),
        #         BasicBayes(name="TEST")]

        # for i in range(NO_GAMES):
        #         # print(i)
        #         game = Game(agents)
        #         game.play()



        df = pd.read_csv('outcomes.csv')
        df = df.reset_index()

        df.columns = ['Role', 'Win']
        total_wins = df[df['Win'] == 'Won']
        spy_wins = df[df['Role'] == 'I was spy' ]
        games_as_spy = spy_wins['Win'].count()
        spy_wins = spy_wins[spy_wins['Win'] == 'Won']

        res_wins = df[df['Role'] == 'I was not spy' ]
        games_as_res = res_wins['Win'].count()
        res_wins = res_wins[res_wins['Win'] == 'Won']

        wins = total_wins['Win'].count()
        total_winrate =  (spy_wins['Win'].count() + res_wins['Win'].count()) / (games_as_res + games_as_spy)
        spy_winrate = spy_wins['Win'].count()/games_as_spy
        res_winrate = res_wins['Win'].count()/games_as_res
        print('Total winrate was:', total_winrate)
        print('Spy winrate was:', spy_winrate)
        print('Resistance winrate was:', res_winrate)
