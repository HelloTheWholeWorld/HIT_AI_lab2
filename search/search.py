# coding=UTF-8
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

class GraphSearch(object):
    '''
    1-4问的搜索算法
    '''
    def __init__(self, problem, data_structure, have_cost=False, heuristic=nullHeuristic):
        '''
        初始化函数

        args:
            problem: 问题对象
            data_structure: 问题使用的数据结构
            have_cost: 是否有代价函数
            heuristic: 启发函数
        '''
        self.problem = problem
        self.data_structure = data_structure
        self.have_cost = have_cost
        self.heuristic = heuristic

    def graph_search(self):
        '''
        搜索函数
        
        returns:
            if successfully get to goal state : return actions list
            else : return None list
        '''
        open_list = self.data_structure()  # 初始化Open表

        if self.have_cost:
            # push的为((state,action),cost) utils定义的数据结构pop时不返回cost=
            open_list.push((self.problem.getStartState(), []), self.heuristic(self.problem.getStartState(), self.problem))
        else:
            open_list.push((self.problem.getStartState(), []))  # Open表中为二元组(状态,到达该状态的actions)

        closed_list = []
        while True:
            if open_list.isEmpty(): 
                return [] 
            state, actions = open_list.pop()
            
            if self.problem.isGoalState(state):  # 如果当前状态是目标状态,则搜索成功,返回操作序列actions
                return actions       

            if state not in closed_list:
                closed_list.append(state)
                for successor_state, action, cost in self.problem.getSuccessors(state):
                    if self.have_cost:
                        open_list.push((successor_state, actions+[action]), self.problem.getCostOfActions(actions+[action]) + self.heuristic(successor_state, self.problem))
                    else:
                        open_list.push((successor_state, actions+[action]))  # 用+防止actions为空


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    dfs = GraphSearch(problem, util.Stack)
    return dfs.graph_search()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    bfs = GraphSearch(problem, util.Queue)
    return bfs.graph_search()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    ucs = GraphSearch(problem, util.PriorityQueue, True)
    return ucs.graph_search()

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    astar = GraphSearch(problem, util.PriorityQueue, True, heuristic)
    return astar.graph_search()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
