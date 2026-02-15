import sqlite3
import subprocess

# Connect to SQLite
def get_connection():
    return sqlite3.connect("golfers.db")

# Fetch golfer data by name
def get_golfer_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers WHERE name = ?", (name,))
    golfer = c.fetchone()
    conn.close()
    return golfer

# Run Ollama locally (using Phi-3 for faster responses)
def run_ollama(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "phi3:mini"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    response, _ = process.communicate(input=prompt)
    return response.strip()

def detect_weaknesses(handicap, driving_distance, putts, gir, approach):
    weaknesses = []

    try:
        if gir < 50:
            weaknesses.append("approach play and green targeting")

        if putts > 2:
            weaknesses.append("putting consistency and distance control")

        if approach < 60:
            weaknesses.append("iron accuracy")

        if driving_distance < 240:
            weaknesses.append("driving power and tee shot optimization")

        if handicap > 15:
            weaknesses.append("overall course management and consistency")

    except TypeError:
        # In case any values are None
        pass

    if not weaknesses:
        weaknesses = ["fine-tuning and advanced scoring strategy"]

    return weaknesses

# AI Coach Interaction
def ask_golf_ai():
    name = input("Enter golfer's name: ")
    golfer = get_golfer_by_name(name)

    if not golfer:
        print("Golfer not found! Make sure you’ve added them first.")
        return

    # unpack golfer data
    _, name, handicap, driving_distance, putts, gir, approach = golfer

    # Build the context
    context = f"""
    Golfer Name: {name}
    Handicap: {handicap}
    Driving Distance: {driving_distance} yards
    Average Putts per Hole: {putts}
    Greens in Regulation: {gir}%
    Approach Accuracy: {approach}%

    Primary Weakness Areas:
    {", ".join(detect_weaknesses) if isinstance(detect_weaknesses, list) else "general improvement focus"}
    """

    user_question = input("\nWhat do you want to ask your AI coach? (e.g., 'How can I improve my short game?')\n> ")

    prompt = f"""
    You are a professional golf performance coach AI.
    Here is the golfer’s data:
    {context}

    Using this data, provide detailed, constructive, and encouraging advice to improve their performance.
    Answer the following golfer question clearly and specifically:
    "{user_question}"
    """

    print("\n Thinking...\n")
    answer = run_ollama(prompt)
    print(" AI Coach Response:\n")
    print(answer)

def generate_practice_plan():
    name = input("Enter golfer's name for practice plan: ")
    golfer = get_golfer_by_name(name)

    if not golfer:
        print("Golfer not found! Make sure you’ve added them first.")
        return

    _, name, handicap, driving_distance, putts, gir, approach = golfer

    weaknesses = detect_weaknesses(handicap, driving_distance, putts, gir, approach)

    context = f"""
Golfer Name: {name}
Handicap: {handicap}
Driving Distance: {driving_distance} yards
Average Putts per Hole: {putts}
Greens in Regulation: {gir}%
Approach Accuracy: {approach}%

Primary Weakness Areas:
{", ".join(weaknesses)}
"""

    prompt = f"""
You are an experienced professional golf coach.

Generate a realistic 7-day golf training plan for this golfer.

STRICT REQUIREMENTS:
- Each day must NOT exceed 2 hours total training time.
- Each day should include 2–4 drills.
- Clearly label each day (Day 1 through Day 7).
- For each drill, include estimated time (e.g., 20 minutes).
- Keep total output under 500 words.
- Make the plan realistic for an amateur golfer.


Golfer Data:
{context}
"""

    print("\n Generating 7-Day Practice Plan...\n")
    plan = run_ollama(prompt)

    print("Personalized Practice Plan:\n")
    print(plan)
    
if __name__ == "__main__":
    ask_golf_ai()
