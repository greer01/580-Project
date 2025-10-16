import random 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from db import get_all_golfers

def plot_histograms(golfers):
    distances = [g['driving_distance'] for g in golfers] 
    plt.hist(distances, bins=10, color='skyblue', edgecolor='black')
    plt.title("Driving Distance Distribution")
    plt.xlabel("Driving Distance (yards)")
    plt.ylabel("Number of Golfers")
    plt.grid(True, linestyle="--", alpha= 0.6)
    plt.show()

def plot_scatter(golfers):
    distances = [g['driving_distance'] for g in golfers]
    gir = [g['gir'] for g in golfers]
    plt.scatter(distances, gir, color="green", alpha=0.7)
    plt.title("Driving Distance vs GIR %")
    plt.xlabel("Driving Distance (yards)")
    plt.ylabel("GIR (%)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

def plot_radar(golfer):
    labels = ["Driving", "Putting", "GIR", "Approach", "Handicap"]
    values = [
        golfer["driving_distance"] / 30,
        max(0, 5 - golfer["putts_per_hole"]),
        golfer["gir"] / 10,
        golfer["approach_accuracy"] / 10,
        max(0, 10 - golfer["handicap"] / 2)
    ]
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="darkorange", linewidth=2)
    ax.fill(angles, values, color="orange", alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 10)
    ax.set_title(f"{golfer['name']}'s Skill Radar", size=14)
    plt.show()

if __name__ == "__main__":
    golfers = get_all_golfers()
    
    if len(golfers) == 0:
        print("No golfer data available to visualize. Add some golfers first.")
    else:
        df = pd.DataFrame(golfers)

        plot_histograms(golfers)
        plot_scatter(golfers)
        plot_radar(random.choice(golfers))
