import sqlite3
import subprocess

def get_connection():
    return sqlite3.connect("golfers.db")


def get_golfer_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM golfers WHERE name = ?", (name,))
    golfer = c.fetchone()
    conn.close()
    return golfer


def run_ollama(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "phi3:mini"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace"
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
        pass

    if not weaknesses:
        weaknesses = ["fine-tuning and advanced scoring strategy"]

    return weaknesses


def classify_skill_tier(handicap):
    if handicap <= 5:
        return "Advanced / Competitive Player"
    elif handicap <= 15:
        return "Intermediate Player"
    else:
        return "Developing / High Handicap Player"


def ask_golf_ai():
    name = input("Enter golfer's name: ")
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

    user_question = input("\nWhat do you want to ask your AI coach?\n> ")

    prompt = f"""
You are a professional golf performance coach AI.

Using the structured data below, provide detailed,
constructive, and encouraging coaching advice.

Golfer Data:
{context}

Answer this golfer question clearly and specifically:
"{user_question}"

Keep the response concise (under 400 words).
"""

    print("\nThinking...\n")
    answer = run_ollama(prompt)

    print("\nAI Coach Response:\n")
    print(answer)


def generate_practice_plan():
    name = input("Enter golfer's name for practice plan: ")
    golfer = get_golfer_by_name(name)

    if not golfer:
        print("Golfer not found! Add them first.")
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
You are a professional golf performance coach.

Generate a realistic 7-day golf training plan.

STRICT REQUIREMENTS:
- Each day must NOT exceed 2 hours total training time.
- Each day should include 2–4 drills.
- Include estimated time per drill.
- Clearly label Day 1 through Day 7.
- Keep total response under 500 words.
- Make the plan realistic for an amateur golfer.

Golfer Data:
{context}
"""

    print("\nGenerating 7-Day Practice Plan...\n")
    plan = run_ollama(prompt)

    print("\nPersonalized Practice Plan:\n")
    print(plan)


def generate_performance_audit():
    name = input("Enter golfer's name for performance audit: ")
    golfer = get_golfer_by_name(name)

    if not golfer:
        print("Golfer not found! Add them first.")
        return

    _, name, handicap, driving_distance, putts, gir, approach = golfer

    weaknesses = detect_weaknesses(handicap, driving_distance, putts, gir, approach)
    skill_tier = classify_skill_tier(handicap)

    priority_ranking = weaknesses[:3]

    context = f"""
Golfer Name: {name}
Skill Tier (Rule-Based Classification): {skill_tier}
Handicap: {handicap}
Driving Distance: {driving_distance} yards
Average Putts per Hole: {putts}
Greens in Regulation: {gir}%
Approach Accuracy: {approach}%

Identified Weakness Areas:
{", ".join(weaknesses)}

Top Development Priorities:
{", ".join(priority_ranking)}
"""

    prompt = f"""
You are a professional golf performance analyst.

Generate a structured Performance Audit Report.

Include:

1. Skill Tier Explanation
2. Primary Strength
3. Primary Limitation
4. Scoring Risk Factor
5. Course Type Suitability
6. Development Priority Explanation
7. Estimated Scoring Improvement Potential

Be analytical and professional.
Keep response under 500 words.

Golfer Data:
{context}
"""

    print("\nGenerating Performance Audit Report...\n")
    report = run_ollama(prompt)

    print("\nPerformance Audit Report:\n")
    print(report)
