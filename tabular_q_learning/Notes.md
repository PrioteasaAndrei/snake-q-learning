### Notes on reinforcement learning

Learning method based on maximizing imediate rewards attributed to actions.
Q learning is trial and error.

## Agent

The agent recieves the game as a parameter

The agent can do:
    explotation = look into the Q table and select max value action
    exploration = act randomly -> explore new states

OBS : stochaestic = random distribution

    ## Bellman equation:
    ~ base of dynamic programming

Tu esti la t+1 aici nu la t 

Q'(st,at) = Q(st,at) + alpha * (reward_t + gamma * max(Q(st+1,a)) - Q(st,at))

gamma = discount factor ( 0 <= gamma <= 1 ) 
    | gamma == 0 -> myopic ; consider only current rewards
    | gamma == 1 -> long term reward

alpha = learning rate 0 <= alpha <= 1
    | how much new information ovverides old information
    | 0 -> only use prior knowledge
    | 1 -> only use current info , no history
    | usually let it be 0.1 

max Q(st+1, a) = maximum future reward than can be obtained from st+1

### Moves

straight, left and right w.r.t direction of movement

### States

Neighbouring cells:

[danger_straight,danger_left,danger_right,
moving_left,moving_right,moving_up,moving_down,
food_left,food_right,food_up,food_down]

-- all boolean

Varianta simpla : 
    state = casuta in care se afla capul sarpelui

Varianta complexa:
    state = 
            [danger_straight,danger_left,danger_right,
            moving_left,moving_right,moving_up,moving_down,
            food_left,food_right,food_up,food_down]
