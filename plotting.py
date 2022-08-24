import matplotlib.pyplot as plt
import numpy



def plot_score(xpoints,ypoints):
    plt.plot(xpoints,ypoints,'o')
    plt.xlabel("Iteration no")
    plt.ylabel("Score")
    plt.show()