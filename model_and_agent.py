
from multiprocessing.spawn import prepare
import matplotlib.pyplot as plt
import numpy as np
from game import BLOCK_SIZE, SnakeGame

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

    qtable = np.zeros((32,24,3))
    # qtable = np.zeros((768,3))
    ## rewards
    ## bigger by 2 set the bounderies equal to -10
    rewards = np.zeros((32,24))
    rewards = np.pad(rewards,pad_width=1,mode='constant',constant_values=-10)

    ## reward for apple

    rewards[int(apple[0] // BLOCK_SIZE)][int(apple[1] // BLOCK_SIZE)] = 10

    ## make the snake tail -10

    for square in snake[1:]:
        rewards[int(square[0] // BLOCK_SIZE)][int(square[1] // BLOCK_SIZE)] = -10

    
    return qtable,rewards

def get_state(self, game):
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

GAME = SnakeGame()
EPISODES = 100
qtable,rewards = prepare_enviroment(GAME)

## learning rate
alpha = 0.001

## discount rate is big because we want long term rewards
gamma = 0.9  

snake = GAME._get_snake_idxs()
apple = GAME._get_food()

## 32 * 24 and 3 actions
##qtable = np.zeros((32,24,3))
# qtable = np.zeros((768,3))


## actions | 0 , 1 , 2
actions = ['straight','left','right']


print(repr(rewards))