# Imports 
from db import get_all_golfers, get_connection

def analyze_golfer_performance(golfer):
    # Analyzes a single golfer's performance and provides feedback
    id, name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy = golfer

    feedback = [f" Performance Analysis for {name}:"]
    feedback.append(f"Handicap: {handicap}")
    feedback.append(f"Driving Distance: {driving_distance} yards")
    feedback.append(f"Putts per Hole: {putts_per_hole}")
    feedback.append(f"Green in Regulation (GIR): {gir}%")
    feedback.append(f"Approach Accuracy: {approach_accuracy}%\n")


    # For Driving Distance
    if driving_distance < 230:
        feedback.append(" Your Driving distance is a little below average. Work on swing speed and good contact for longer drives.")
    elif 230 <= driving_distance < 270: 
        feedback.append(" You have an average driving distance. Focus more on accuracy off of the tee to produce lower scores.")
    else:
        feedback.append(" Excellent driving distance! Make sure your short game is as good as your long game.")

    # Greens in Reg 
    if gir < 40:
        feedback.append (" Green in regulation is low. your short game needs some work. Focus on club selection and distance control.")
    elif 40 <= gir < 65:
        feedback.append(" Your GIR is solid. Work on approach shots and accuracy to give yourself more birdie opportunities.")
    else:
        feedback.append(" Excellent GIR percentage! You are hitting a lot of greens. Keep it up! You can also focus on more accuracy to the hole to give yourself more birdie chances to upgrade your game even more.")

    # Putting 
    if putts_per_hole > 2.2:
        feedback.append(" Your putting could use some improvement. Practice lag putting and short putts to lower your scores.")
    elif 1.8 <= putts_per_hole <= 2.2:
        feedback.append(" Your putting is steady. Focus on reading greens and speed control to make more putts.")
    else:
        feedback.append(" Elite putting performance, keep it up to keep saving those strokes on the greens!")

    # Handicap Feedback
    if handicap > 15:
        feedback.append(" Your handicap indicates you are a beginner. Focus on fundamentals and course management to improve.")
    elif 8 < handicap <= 15:
        feedback.append(" You are a solid player. Work on consistency and short game to lower your scores.")
    else:
        feedback.append(" low handicap continue to focus on precison and strategy to contiue to level up your game")

    return "\n".join(feedback)

def run_analysis():
    # runs analysis for all golfers in the database
    golfers = get_all_golfers()
    for golfer in golfers:
        print(analyze_golfer_performance(golfer))
        print ("-" * 50)

if __name__ == "__main__":
    run_analysis()
