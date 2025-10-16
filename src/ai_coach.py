import sqlite3
import subprocess
import json

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
        ["ollama", "run", "phi3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    response, _ = process.communicate(input=prompt)
    return response.strip()

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
    """

    user_question = input("\nWhat do you want to ask your AI coach? (e.g., 'How can I improve my short game?')\n> ")

    prompt = f"""
    You are a professional golf performance coach AI.
    Here is the golfer’s data:
    {context}

    Using this data, provide detailed, constructive, and encouraging advice to improve their performance.
    Answer the following question from the golfer:
    "{user_question}"
    """

    print("\n Thinking...\n")
    answer = run_ollama(prompt)
    print(" AI Coach Response:\n")
    print(answer)

if __name__ == "__main__":
    ask_golf_ai()
