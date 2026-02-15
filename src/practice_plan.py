import subprocess

def generate_practice_plan(golfer_data):
    """
    Generate a 7-day strcutued golf practice plan using AI based on golfer statistics. 
    """

    name = golfer_data["name"]
    handicap = golfer_data["handicap"]
    driving = golfer_data["driving_distance"]
    gir = golfer_data["gir"]
    putting = golfer_data["putting_average"]
    approach = golfer_data["approach_accuracy"]

    prompt = f"""
You are an expericenced professional golf coacg.

Creat a detailed 7-day strucutred practice plan for the following golfer

Golfer Profile:
Name: {name}
Handicap: {handicap}
Average Driving Distance: {driving} yards
Greens in Regulation: {gir}%
Putting Average: {putting} strokes
Approach Accuracy: {approach}%

Instructions:
- Indeitify weakest areas.
- Create a realistic 7-day plan.
- Include drills, repetitions, and focus goals.
- Keep tone professional and constructuive.
- Be consise but structured.
- Format clearly by Day 1 through Day 7.
"""
    
    process = subprocess.Popen(
        ["ollama", "run", "phi3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    output, _ = process.communicate(prompt)
    return output
