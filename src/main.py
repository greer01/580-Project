import requests
import json
import urllib.parse

# API KEYS
FINDER_API_KEY = "9fbeaacc43msh87084e1bed4d7b9p1867f7jsnca540e78c690"  # Golf Course Finder API (RapidAPI)
GOLFCOURSE_API_KEY = "D42GSYCEPK2422NCRGGV3LOWNA"  # GolfCourseAPI.com Key

# Type Any Place
def get_lat_lon_from_place():
    place = input("\n📍 Enter the city/town and state (e.g., 'Saxonburg, PA'): ")
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote_plus(place)}&format=json"

    try:
        response = requests.get(url, headers={"User-Agent": "golf-course-matcher"})
        data = response.json()

        if not data:
            print("❌ Could not find that location. Please try again.")
            return get_lat_lon_from_place()

        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        print(f"✅ Found location: {lat}, {lon}")
        return lat, lon
    except Exception as e:
        print(f"❌ Error fetching location: {e}")
        return get_lat_lon_from_place()

# API Helper
def find_courses(lat, lon, radius):
    response = requests.get(
        f"https://golf-course-finder.p.rapidapi.com/api/golf-clubs/?miles={radius}&latitude={lat}&longitude={lon}",
        headers={
            "x-rapidapi-key": FINDER_API_KEY,
            "x-rapidapi-host": "golf-course-finder.p.rapidapi.com"
        }
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❗ Error: {response.status_code} - Unable to retrieve nearby courses.")
        return []

# Match Color + Reasoning Function
def get_match_color(handicap, driving_distance, slope, yardage):
    explanations = []

    # Determine Slope Match
    if slope == "Info not available":
        slope_color = "🟨"
        explanations.append("Slope rating info missing")
    else:
        slope = float(slope)
        expected_slope = (120 if handicap <= 5 else 115 if handicap <= 15 else 105 if handicap <= 25 else 100)

        if (0 <= handicap <= 5 and 120 <= slope <= 135) or \
           (6 <= handicap <= 15 and 115 <= slope <= 130) or \
           (16 <= handicap <= 25 and 105 <= slope <= 120) or \
           (handicap >= 26 and slope < 110):
            slope_color = "🟩"
            explanations.append("Slope matches your expected range for your handicap")
        elif abs(slope - expected_slope) <= 10:
            slope_color = "🟨"
            explanations.append("Slope slightly harder/easier than expected for your handicap")
        else:
            slope_color = "🟥"
            explanations.append("Slope much harder/easier than expected for your handicap")

    # Determine Yardage Match
    if yardage == "Info not available":
        yardage_color = "🟨"
        explanations.append("Yardage info missing")
    else:
        yardage = float(yardage)
        expected_yardage = (6600 if driving_distance >= 280 else 6200 if driving_distance >= 240 else 5800)

        if (driving_distance >= 280 and yardage >= 6600) or \
           (240 <= driving_distance < 280 and 6200 <= yardage <= 6600) or \
           (200 <= driving_distance < 240 and 5800 <= yardage <= 6200) or \
           (driving_distance < 200 and yardage <= 5800):
            yardage_color = "🟩"
            explanations.append("Yardage matches your driving distance")
        elif abs(yardage - expected_yardage) <= 200:
            yardage_color = "🟨"
            explanations.append("Yardage slightly longer/shorter than ideal for your driving distance")
        else:
            yardage_color = "🟥"
            explanations.append("Yardage badly mismatched for your driving distance")

    # Final Color Decision
    if slope_color == "🟥" or yardage_color == "🟥":
        final_color = "🟥"
    elif slope_color == "🟨" or yardage_color == "🟨":
        final_color = "🟨"
    else:
        final_color = "🟩"

    return final_color, explanations

# MAIN PROGRAM START
LAT, LON = get_lat_lon_from_place()

RADIUS = int(input("\n📏 Enter search radius in miles (e.g., 10): "))
handicap = int(input("🎯 Enter your handicap (e.g., 15): "))
driving_distance = int(input("🏌️ Enter your average driving distance in yards (e.g., 250): "))

nearby_courses = find_courses(LAT, LON, RADIUS)

if not nearby_courses:
    print("❌ No courses found. Expanding radius to 30 miles...")
    RADIUS = 30
    nearby_courses = find_courses(LAT, LON, RADIUS)

if not nearby_courses:
    print("❌ No courses found even after expanding. Try a different location.")
    exit()

# Search and Match Courses
print("\n🏌️ Nearby Golf Courses with Match Scores:\n")

any_successful = False

for course in nearby_courses:
    club_name = course.get('club_name')
    country = course.get('country')

    if not club_name or country != "United States of America":
        continue

    search_query = urllib.parse.quote_plus(club_name)
    golfcourse_url = f"https://api.golfcourseapi.com/v1/search?search_query={search_query}"
    headers = {
        "Authorization": f"Key {GOLFCOURSE_API_KEY}"
    }

    response = requests.get(golfcourse_url, headers=headers)

    if response.status_code != 200:
        continue

    courses = response.json().get('courses', [])
    if not courses:
        continue

    for course in courses:
        club_name = course.get('club_name', "Unknown Club")
        course_name = course.get('course_name', "Unknown Course")
        location = course.get('location', {})
        address = location.get('address', "Address not available")

        male_tees = course.get('tees', {}).get('male', [])
        
        if male_tees:
            tee_info = male_tees[0]
            yardage = tee_info.get('total_yards', "Info not available")
            slope = tee_info.get('slope_rating', "Info not available")
            course_rating = tee_info.get('course_rating', "Info not available")
            holes = tee_info.get('number_of_holes', "Info not available")
        else:
            continue  # Skip if no yardage/slope info

        match_color, explanations = get_match_color(handicap, driving_distance, slope, yardage)

        # === Display the course details
        print(f"🏌️ Club Name: {club_name}")
        print(f"🎯 Course Name: {course_name}")
        print(f"📍 Address: {address}")
        print(f"🕳️ Holes: {holes}")
        print(f"📏 Yardage: {yardage}")
        print(f"📐 Slope Rating: {slope}")
        print(f"🏅 Course Rating: {course_rating}")
        print(f"🎯 Match Quality: {match_color}")
        print(f"📝 Reasoning:")
        for reason in explanations:
            print(f"   - {reason}")
        print("-" * 50)

        any_successful = True
        break  # Only show first match

if not any_successful:
    print("❌ No detailed info found for any nearby courses.")
