
import matplotlib.pyplot as plt
import numpy as np
from game import BLOCK_SIZE, SnakeGame
from collections import namedtuple
from enum import Enum
import random

from plotting import plot_score

Point = namedtuple('Point', 'x, y')

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

    ## 32 * 24 and 3 actions
    qtable = np.zeros((24,32,3))
    # qtable = np.zeros((768,3))
    
    ## rewards
    ## bigger by 2 set the bounderies equal to -10
    rewards = np.zeros((24,32))


    ## reward for apple
    ## are they reverted ??/
    x_OX =  int(apple[0] // BLOCK_SIZE)
    y_OY = int(apple[1] // BLOCK_SIZE)
    ## ASTA E COORDONATA FARA PADDING
    rewards[y_OY][x_OX] = 10

    ## make the snake tail -10

    ## am inversat si aici pentru ca x sunt coloanele si y liniile
    ## SI ASTEA LA FEL FARA PADDING SUNT COORDONATELE
    for square in snake[1:]:
        rewards[int(square[1] // BLOCK_SIZE)][int(square[0] // BLOCK_SIZE)] = -10


    rewards = np.pad(rewards,pad_width=1,mode='constant',constant_values=-10)
    
    return qtable,rewards


# [danger_straight,danger_left,danger_right,
# moving_left,moving_right,moving_up,moving_down,
# food_left,food_right,food_up,food_down]
def get_state_complex(self, game):
        head = game.snake[0]

        ## w.r.t the direction of motion

        left  = Point(head.x - 20, head.y)
        right  = Point(head.x + 20, head.y)
        up  = Point(head.x, head.y - 20)
        down  = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(right)) or 
            (dir_l and game.is_collision(left)) or 
            (dir_u and game.is_collision(up)) or 
            (dir_d and game.is_collision(down)),

            # Danger right
            (dir_u and game.is_collision(right)) or 
            (dir_d and game.is_collision(left)) or 
            (dir_l and game.is_collision(up)) or 
            (dir_r and game.is_collision(down)),

            # Danger left
            (dir_d and game.is_collision(right)) or 
            (dir_u and game.is_collision(left)) or 
            (dir_r and game.is_collision(up)) or 
            (dir_l and game.is_collision(down)),
            
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


## X SI Y SUNT INVERSATE  ??? 
## X e coloana y e linia
def get_state_easy(game):
    return Point(int(game.head.y // BLOCK_SIZE),int(game.head.x // BLOCK_SIZE))

'''
Use a epsilon greedy alg to allow for exploration of new paths that at first seem not to get a good future reward

return action
[1,0,0] -> straight
[0,1,0] -> right
[0,0,1] -> left

Take the best action 90% of times so epsilon is 0.9
'''
def get_action(epsilon,old_state):
    # random moves: tradeoff exploration / exploitation

    move = [0,0,0]

    ## if qtable is empty for that state do a random action
    if np.random.random() > epsilon or np.array_equal(qtable[old_state[0],old_state[1]],np.array([0,0,0])):
         ## get random action
        move_idx = random.randint(0, 2)
        move[move_idx] = 1
    else:
        ## get the best action
        ## should take the max of the array and make it 1
        ## dar daca e negativ ?? sa iau in modul
        print(np.argmax(qtable[old_state[0],old_state[1]]))
        print(qtable[old_state[0],old_state[1]])

        move[np.argmax(qtable[old_state[0],old_state[1]])] = 1

    return move


GAME = SnakeGame()
EPISODES = 500
qtable,rewards = prepare_enviroment(GAME)

## learning rate
alpha = 0.5

## discount rate is big because we want long term rewards
gamma = 1.0  

## percentage of time we take the best action considering the qtable
epsilon = 0.9

snake = GAME._get_snake_idxs()
apple = GAME._get_food()



iteration_for_plotting  = []
score_for_plotting = []

for i in range(EPISODES):
    ## jocul abia a pornit la linia 107
    game_over = False
    GAME.reset()
    while not game_over:

        old_state = get_state_easy(GAME)
        ## ? problema aici ?? 
        action = get_action(epsilon,old_state)
        reward,game_over,score = GAME.play_step(action)
        new_state = get_state_easy(GAME)

        print("Reward is:",reward)
        (m,n,p) = np.shape(qtable)
        
        if new_state[0] == m or new_state[1] == n:
            game_over = True
            break

        ## sau mai usor fac eu corelarea direct
        '''
            action == [1,0,0] -> 0 
            action == [0,1,0] -> 1
            action == [0,0,1] -> 2

        '''

        action_idx = 0 

        if np.array_equal(action,np.array([1,0,0])):
            action_idx = 0
        elif np.array_equal(action,np.array([0,1,0])):
            action_idx = 1
        elif np.array_equal(action,np.array([0,0,1])):
            action_idx = 2
        else:
            raise Exception()


        qtable[old_state[0],old_state[1],action_idx] += alpha * (reward + gamma * np.max(qtable[new_state[0],new_state[1]]) - qtable[old_state[0],old_state[1],action_idx])
        
    iteration_for_plotting += [i]
    score_for_plotting += [score] 

plot_score(iteration_for_plotting,score_for_plotting)
np.save('qtable.npy',qtable)
    