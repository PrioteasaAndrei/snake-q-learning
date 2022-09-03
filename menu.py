import os

value = input("Select which agent to use:\n1-Deep Q Learning\n2-Tabular Q Learning\nSelect:")

if value == '1':
    print("You selected Deep Q Learning Agent")
    os.system('cmd /k "python Deep_Q/agent.py"')
elif value == '2':
    print("You selected Tabular Q Learning Agent")
    os.system('cmd /k "python tabular_q_learning/model_and_agent.py"')