import sqlite3
import subprocess
import time

# Database Setup
def get_connection():
    return sqlite3.connect("golfers.db")

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS golfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            handicap REAL,
            driving_distance REAL,
            putts_per_hole REAL,
            gir REAL,
            approach_accuracy REAL
        )
    """)
    conn.commit()
    conn.close()

def add_golfer(name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO golfers (name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, handicap, driving_distance, putts_per_hole, gir, approach_accuracy))
    conn.commit()
    conn.close()

def get_all_golfers():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers")
    golfers = c.fetchall()
    conn.close()
    return golfers

def get_golfer_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers WHERE name = ?", (name,))
    golfer = c.fetchone()
    conn.close()
    return golfer


# Course Recomendation
def recommend_course_type(golfer):
    if len(golfer) == 7:
        _, name, handicap, driving_distance, putts, gir, approach = golfer
    else:
        name, handicap, driving_distance, putts, gir, approach = golfer

    reasoning = []

    if driving_distance >= 280:
        course_type = "Championship-level course (long and challenging)"
        reasoning.append("You hit long drives, so longer par-4s and par-5s suit your game.")
    elif 240 <= driving_distance < 280:
        course_type = "Balanced course (mix of distance and precision)"
        reasoning.append("Your distance allows you to handle moderate-length courses while focusing on approach accuracy.")
    else:
        course_type = "Short, strategic course (for accuracy and control)"
        reasoning.append("Shorter courses let you focus on consistency and positioning off the tee.")

    if handicap <= 8:
        reasoning.append("You’re a low-handicap player who benefits from tougher layouts with faster greens.")
    elif handicap <= 18:
        reasoning.append("You’re improving, so mid-difficulty layouts that reward consistency are ideal.")
    else:
        reasoning.append("Forgiving fairways and less penal rough will help you enjoy and improve your game.")

    if gir > 65 or approach > 70:
        reasoning.append("High GIR and approach accuracy suggest you’ll enjoy courses that challenge pin placement and distance control.")
    elif gir < 50:
        reasoning.append("Courses with larger greens and open approaches will support your improvement in GIR percentage.")

    if putts < 1.8:
        reasoning.append("Fast, contoured greens will test your advanced putting skills.")
    elif putts > 2.0:
        reasoning.append("Courses with slower greens will allow you to build confidence in putting.")

    print(f"\n Recommended Course Type for {name}: {course_type}")
    print("\nReasoning:")
    for r in reasoning:
        print(f" • {r}")


# AI COACH
def run_ollama(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "phi3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    output, error = process.communicate(input=prompt)
    if error:
        print(f" Error: {error}")
    return output.strip()

def ask_ai_coach():
    print("\n--- AI Golf Coach ---")
    name = input("Enter golfer's name (or 'b' to go back): ")
    if name.lower() == 'b':
        return

    golfer = get_golfer_by_name(name)
    if not golfer:
        print("Golfer not found. Please add them first.")
        return

    _, name, handicap, driving_distance, putts, gir, approach = golfer

    context = f"""
    Golfer Name: {name}
    Handicap: {handicap}
    Driving Distance: {driving_distance} yards
    Average Putts per Hole: {putts}
    Greens in Regulation: {gir}%
    Approach Accuracy: {approach}%
    """

    user_question = input("\nAsk your AI golf coach a question (or 'b' to go back):\n> ")
    if user_question.lower() == 'b':
        return

    prompt = f"""
    You are a concise and analytical golf performance AI coach.
    Use the golfer's performance metrics to provide specific, data-driven improvement advice.
    Avoid introductions or sign-offs.
    Respond in 2–4 sentences with a direct, professional tone.

    Golfer data:
    {context}

    Question: {user_question}
    """

    print("\nThinking...\n")
    answer = run_ollama(prompt)
    print("AI Coach Response:\n")
    print(answer)


# Main 
def main():
    create_table()

    while True:
        print("\n=== Golf Performance Analyzer ===")
        print("1.  Add Golfer")
        print("2.  List Golfers")
        print("3.  Recommend Course Type")
        print("4.  Ask AI Coach")
        print("5.  Quit")

        choice = input("\nSelect an option (1–5): ").strip()

        if choice == "1":
            print("\n--- Add Golfer ---")
            name = input("Enter golfer's name (or 'b' to go back): ")
            if name.lower() == 'b':
                continue
            try:
                handicap = float(input("Handicap: "))
                driving_distance = float(input("Average driving distance (yards): "))
                putts = float(input("Average putts per hole: "))
                gir = float(input("Greens in regulation (%): "))
                approach_accuracy = float(input("Approach accuracy (%): "))
            except ValueError:
                print("Invalid input — please enter numeric values.")
                continue

            add_golfer(name, handicap, driving_distance, putts, gir, approach_accuracy)
            print(f"\n Golfer {name} added successfully!")

        elif choice == "2":
            print("\n--- Stored Golfers ---")
            golfers = get_all_golfers()
            if golfers:
                for g in golfers:
                    print(f"{g[0]}. {g[1]} (HCP: {g[2]}, Dist: {g[3]} yds, GIR: {g[5]}%)")
            else:
                print("No golfers found.")

        elif choice == "3":
            golfers = get_all_golfers()
            if not golfers:
                print("No golfers found.")
                continue
            print("\nSelect a golfer by ID:")
            for g in golfers:
                print(f"{g[0]}. {g[1]}")
            try:
                golfer_id = int(input("Enter ID (or 0 to go back): "))
            except ValueError:
                print("Invalid input.")
                continue
            if golfer_id == 0:
                continue
            selected = [g for g in golfers if g[0] == golfer_id]
            if selected:
                recommend_course_type(selected[0])
            else:
                print("Invalid selection.")

        elif choice == "4":
            ask_ai_coach()

        elif choice == "5":
            print("\nGoodbye! ")
            break

        else:
            print("Invalid option — please enter 1–5.")

if __name__ == "__main__":
    main()
