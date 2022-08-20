### Notes on reinforcement learning

Learning method based on maximizing imediate rewards attributed to actions.

### Rewards

Eat apple = 10 p
Die = -10 p or #steps > 100 * len(snake) -10p 
    | no progress proportional with the length of the snake
Move without hitting the wall or diying = 0p



### Moves

straight, left and right w.r.t direction of movement

### States

Neighbouring cells:

[danger_straight,danger_left,danger_right,
moving_left,moving_right,moving_up,moving_down,
food_left,food_right,food_up,food_down]

-- all boolean