Q learning based snake agent using tabular q learning

## Rewards

Snake eats the apple : 1p
Snake gets closer to the apple: 1p
Snake hits itself or obstacle or gets away from the apple : -1

## Actions

Continue direction of movement: [1,0,0]
Go right w.r.t direction of motion: [0,1,0]
Go left w.r.t direction of motion: [0,0,1]

## States

Boolean array made of 11 elements:
### Danger straight
### Danger right w.r.t direction of motion
### Danger left w.r.t direction of motion
### 4 Move directions
### food left of head
### food right of head
### food up of head
### food down of head

Qtable is a python dict with str(state) as key and a numpy array with 3 elements as value, a q value for each action

states : 2^11 = 2048
actions: 3
Qtable entries: 6144

## Parameters

gamma = 0.9 
    we want a long term reward
alpha = 0.1
    we want o learn slowly
epsilon = 0.1
    becomes 0 after 300 games


## Experience replay

I hold a history of states and actions without their coresponding q values.

## Tabular Q learning vs Deep Q learning

### Tabular             ### Deep

small #states           large #states and action spaces

small #actions          can handle continuos inputs

discrete states         prety slow

pretty fast             needs to write to the disk 

qtable can              experience learning is advised in order to randomize the sequential data training
be kept in 
memory


## Analysis

The model needs about 400 games before any visible result are seen
Max score: 40
Adding fixed obstacles requires the agent to train over 1600 iterations in order to score above 10
