import random
from db import add_golfer

def generate_synthetic_data(num_golfers=50):
    first_names = [
        "Logan", "Alex", "Jordan", "Taylor", "Chris", "Riley", "Morgan", "Jamie",
        "Drew", "Casey", "Sam", "Cameron", "Jesse", "Blake", "Skyler", "Devon",
        "Harper", "Reese", "Peyton", "Rowan"
    ]

    for _ in range(num_golfers):
        name = random.choice(first_names) + " " + random.choice(["Smith", "Johnson", "Brown", "Lee", "Garcia", "Miller"])
        hanidcap = round(random.uniform(0,25), 1)
        driving_distance = random.randint(200, 320)
        gir = random.randint(30,80)
        putts_per_hole = round(random.uniform(1.6, 2.5), 2)
        approach_accuracy = random.randint(40, 85)

        add_golfer(name, hanidcap, driving_distance, putts_per_hole, gir, approach_accuracy)

        print(f" Added: {name} (HCP: {hanidcap}, Drive: {driving_distance} yds, GIR: {gir}%, Putts/Hole: {putts_per_hole}, App Acc: {approach_accuracy}%)")

if __name__ == "__main__":
    generate_synthetic_data()
