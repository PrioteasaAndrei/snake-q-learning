
from turtle import distance
import matplotlib.pyplot as plt
import numpy as np
from game import BLOCK_SIZE, SnakeGame
from collections import namedtuple
from enum import Enum
import random

from plotting import plot_score

Point = namedtuple('Point', 'x, y')

## learning rate
alpha = 0.1

## discount rate is big because we want long term rewards
gamma = 0.9

## percentage of time we take the best action considering the qtable
epsilon = 1.0


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    

def prepare_enviroment(game):
    snake = game._get_snake_idxs()
    apple = game._get_food()

    def check_integrity_snake(snake):
        for square in snake:
            if square[0] % BLOCK_SIZE != 0.0 or square[1] % BLOCK_SIZE != 0.0:
                raise Exception()

    check_integrity_snake(snake)

    if apple[0] % BLOCK_SIZE != 0.0 or apple[1] % BLOCK_SIZE != 0.0:
        raise Exception()
   
   ##  dictionary 
   
   ## key : str(state)
    qtable = {}

    ## populate qtable 

    boolean_vals = [0,1]

    ## -> 2 ^ 12 states = 4096 states which is ok
    states = []

    for s1 in boolean_vals:
        for s2 in boolean_vals:
            for s3 in boolean_vals:
                for s4 in boolean_vals:
                    for s5 in boolean_vals:
                        for s6 in boolean_vals:
                            for s7 in boolean_vals:
                                for s8 in boolean_vals:
                                    for s9 in boolean_vals:
                                        for s10 in boolean_vals:
                                            for s11 in boolean_vals:
                                                states.append(np.array([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11]))


    ## 1110011110101 : [0.5,1.2,3.3]
    ## key is state : val for 100 010 and 001
    for state in states:
        qtable[str(state)] = np.array([0,0,0],dtype=float)    
    

    ## Use experience learning for better results
    ## history will be set to [] after every match
    history = []

    return qtable,history



def get_state_easy(game):
    return Point(int(game.head.y // BLOCK_SIZE),int(game.head.x // BLOCK_SIZE))

'''

    returns a len 11 boolean array 

'''
def get_state( game):
    head = game.snake[0]
    point_l = Point(head.x - 20, head.y)
    point_r = Point(head.x + 20, head.y)
    point_u = Point(head.x, head.y - 20)
    point_d = Point(head.x, head.y + 20)
    
    dir_l = game.direction == Direction.LEFT
    dir_r = game.direction == Direction.RIGHT
    dir_u = game.direction == Direction.UP
    dir_d = game.direction == Direction.DOWN

    state = [
        # Danger straight
        (dir_r and game.is_collision(point_r)) or 
        (dir_l and game.is_collision(point_l)) or 
        (dir_u and game.is_collision(point_u)) or 
        (dir_d and game.is_collision(point_d)),

        # Danger right
        (dir_u and game.is_collision(point_r)) or 
        (dir_d and game.is_collision(point_l)) or 
        (dir_l and game.is_collision(point_u)) or 
        (dir_r and game.is_collision(point_d)),

        # Danger left
        (dir_d and game.is_collision(point_r)) or 
        (dir_u and game.is_collision(point_l)) or 
        (dir_r and game.is_collision(point_u)) or 
        (dir_l and game.is_collision(point_d)),
        
        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,
        
        # Food location 
        game.food.x < game.head.x,  # food left
        game.food.x > game.head.x,  # food right
        game.food.y < game.head.y,  # food up
        game.food.y > game.head.y  # food down
        ]

    return np.array(state, dtype=int)




def distance_to_apple(x_food,y_food,x_head,y_head):
    return np.abs(x_head - x_food) + np.abs(y_head - y_food)
    

## reason == True -> snake died
## reason == False -> snake still alive / caught an apple 
def update_qtable(qtable,reason):
    reverse_history = history[::-1]
    for i,h in enumerate(reverse_history[:-1]):
        if reason == True:
            ## snake died
            h_state = reverse_history[0]['state']
            h_action = reverse_history[0]['action']
            action_index = action_to_index(h_action)
            reward = -1
            qtable[str(h_state)][action_idx] = alpha * qtable[str(h_state)][action_idx] + ( 1 - alpha) * reward
        else:
            ## current state
            current_state = h['state']
            current_food = h['apple']
            current_head = h['head']

            ## prev state
            prev_state = reverse_history[i+1]['state']
            prev_act = reverse_history[i+1]['action']
            prev_food = reverse_history[i+1]['apple']
            prev_head = reverse_history[i+1]['head']

            ## if snake ate food or is closer reward is 1
            if prev_food != current_food:
                reward = 1
            ## works in px because we only do division for conversion
            elif distance_to_apple(current_food[0],current_food[1],current_head[0],current_head[1]) < distance_to_apple(prev_food[0],prev_food[1],prev_head[0],prev_head[1]):
                reward = 1
            else:
                ## further from the food
                reward = -1

            qtable[str(prev_state)][action_to_index(prev_act)] = alpha * (qtable[str(prev_state)][action_to_index(prev_act)]) + (1-alpha) * (reward + gamma * np.max(qtable[str(current_state)]))


def action_to_index(action):
    if np.array_equal(np.array([1,0,0]),action):
        return 0
    elif np.array_equal(np.array([0,1,0]),action):
        return 1
    elif np.array_equal(np.array([0,0,1]),action):
        return 2

'''
Use a epsilon greedy alg to allow for exploration of new paths that at first seem not to get a good future reward

return action
[1,0,0] -> straight
[0,1,0] -> right
[0,0,1] -> left

Take the best action 90% of times so epsilon is 0.9
'''
def get_action(old_state,epoch):
    # random moves: tradeoff exploration / exploitation
    move = [0,0,0]

    if np.random.random() < epsilon:
         ## get random action
        # print("HERERERER")
        move_idx = random.randint(0, 2)
        move[move_idx] = 1
    else:
        ## get the best action
        ## should take the max of the array and make it 1
        arr = qtable[str(old_state)]
        move[np.argmax(arr)] = 1

    history.append({
    'state': old_state,
    'action': move,
    ## in px coord
    'apple': (GAME.food.x,GAME.food.y),
    ## in px coord
    'head': (GAME.head.x,GAME.head.y)
    })

    return move


GAME = SnakeGame()
EPISODES = 500
qtable,history = prepare_enviroment(GAME)

iteration_for_plotting  = []
score_for_plotting = []

for i in range(EPISODES):
    game_over = False
    GAME.reset()
    history = [] 

    if i % 50 == 0:
        epsilon -= 0.1
        print("New epsilon is:",epsilon)

    if epsilon < 0.0 :
        epsilon = 0.0

    while not game_over:

        old_state = get_state(GAME)
        action = get_action(old_state,i)

        reward,game_over,score = GAME.play_step(action)

        new_state = get_state(GAME)

        '''
            action == [1,0,0] -> 0 
            action == [0,1,0] -> 1
            action == [0,0,1] -> 2

        '''
        action_idx = action_to_index(action)
        qtable[str(old_state)][action_idx] += alpha * (reward + gamma * np.max(qtable[str(new_state)]) - qtable[str(old_state)][action_idx])

        ##update_qtable(qtable,game_over)

    iteration_for_plotting += [i]
    score_for_plotting += [score] 


plot_score(iteration_for_plotting,score_for_plotting)
# np.save('qtable.npy',qtable)

