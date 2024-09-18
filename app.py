from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Set your RapidAPI key here
RAPIDAPI_KEY = ""

# Team to ID mapping
TEAM_ID_MAPPING = {
    'Arizona Cardinals': 22, 'Atlanta Falcons': 1, 'Baltimore Ravens': 33, 'Buffalo Bills': 2,
    'Carolina Panthers': 29, 'Chicago Bears': 3, 'Cincinnati Bengals': 4, 'Cleveland Browns': 5,
    'Dallas Cowboys': 6, 'Denver Broncos': 7, 'Detroit Lions': 8, 'Green Bay Packers': 9,
    'Houston Texans': 34, 'Indianapolis Colts': 11, 'Jacksonville Jaguars': 30, 'Kansas City Chiefs': 12,
    'Las Vegas Raiders': 13, 'Los Angeles Chargers': 24, 'Los Angeles Rams': 14, 'Miami Dolphins': 15,
    'Minnesota Vikings': 16, 'New England Patriots': 17, 'New Orleans Saints': 18, 'New York Giants': 19,
    'New York Jets': 20, 'Philadelphia Eagles': 21, 'Pittsburgh Steelers': 23, 'San Francisco 49ers': 25,
    'Seattle Seahawks': 26, 'Tampa Bay Buccaneers': 27, 'Tennessee Titans': 10, 'Washington Commanders': 28
}

def get_matchups(team_a, team_b, year):
    url = "https://nfl-api-data.p.rapidapi.com/nfl-events"
    querystring = {"year": str(year)}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    return {}

def get_team_stats(team_id, year):
    url = "https://nfl-api-data.p.rapidapi.com/nfl-team-statistics"
    querystring = {"year": 2024, "id": team_id}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    return {}

def get_team_details(team_id):
    url = "https://nfl-api-data.p.rapidapi.com/nfl-team-info"
    querystring = {"id": team_id}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "nfl-api-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    return {}

@app.route('/')
def index():
    nfl_teams = [
        'Arizona Cardinals', 'Atlanta Falcons', 'Baltimore Ravens', 'Buffalo Bills',
        'Carolina Panthers', 'Chicago Bears', 'Cincinnati Bengals', 'Cleveland Browns',
        'Dallas Cowboys', 'Denver Broncos', 'Detroit Lions', 'Green Bay Packers',
        'Houston Texans', 'Indianapolis Colts', 'Jacksonville Jaguars', 'Kansas City Chiefs',
        'Las Vegas Raiders', 'Los Angeles Chargers', 'Los Angeles Rams', 'Miami Dolphins',
        'Minnesota Vikings', 'New England Patriots', 'New Orleans Saints', 'New York Giants',
        'New York Jets', 'Philadelphia Eagles', 'Pittsburgh Steelers', 'San Francisco 49ers',
        'Seattle Seahawks', 'Tampa Bay Buccaneers', 'Tennessee Titans', 'Washington Commanders'
    ]
    return render_template('index.html', nfl_teams=nfl_teams)

@app.route('/get_matchups', methods=['POST'])
def get_matchups_for_teams():
    team_a = request.form['team_a']
    team_b = request.form['team_b']

    all_matchups = []

    # Get matchups for the last 5 years
    for year in range(2019, 2024):
        matchups_data = get_matchups(team_a, team_b, year)
        if 'events' in matchups_data:
            for event in matchups_data['events']:
                competitors = event['competitions'][0]['competitors']
                teams_involved = [competitors[0]['team']['displayName'], competitors[1]['team']['displayName']]

                if team_a in teams_involved and team_b in teams_involved:
                    winner = next(c['team']['displayName'] for c in competitors if c['winner'])
                    winner_color = next(c['team']['color'] for c in competitors if c['winner'])
                    winner_logo = next(c['team']['logo'] for c in competitors if c['winner'])
                    score = f"{competitors[0]['score']} - {competitors[1]['score']}"
                    leaders = event['competitions'][0]['leaders']

                    passing = leaders[0]['leaders'][0]
                    rushing = leaders[1]['leaders'][0]
                    receiving = leaders[2]['leaders'][0]

                    date = datetime.strptime(event['date'], '%Y-%m-%dT%H:%MZ').strftime('%B %d, %Y')

                    matchup_info = {
                        'winner': winner,
                        'score': score,
                        'passing': {
                            'name': passing['athlete']['displayName'],
                            'stats': passing['displayValue'],
                            'image': passing['athlete']['headshot']
                        },
                        'rushing': {
                            'name': rushing['athlete']['displayName'],
                            'stats': rushing['displayValue'],
                            'image': rushing['athlete']['headshot']
                        },
                        'receiving': {
                            'name': receiving['athlete']['displayName'],
                            'stats': receiving['displayValue'],
                            'image': receiving['athlete']['headshot']
                        },
                        'date': date,
                        'winner_color': f"#{winner_color}",
                        'winner_logo': winner_logo
                    }
                    all_matchups.append(matchup_info)

    return jsonify(all_matchups)

@app.route('/get_team_stats', methods=['POST'])
def get_team_stats_route():
    team_a = request.form['team_a']
    team_b = request.form['team_b']

    # Get team IDs from the mapping
    team_a_id = TEAM_ID_MAPPING.get(team_a)
    team_b_id = TEAM_ID_MAPPING.get(team_b)

    if not team_a_id or not team_b_id:
        return jsonify({"error": "Invalid team names provided"}), 400

    # Get stats for both teams
    team_a_stats = get_team_stats(team_a_id, 2024)
    team_b_stats = get_team_stats(team_b_id, 2024)

    team_a_info = get_team_details(team_a_id)
    team_b_info = get_team_details(team_b_id)

    def extract_stats(team_stats, team_info):
        if 'statistics' in team_stats:
            stats = team_stats['statistics']['splits'].get('categories', [])
            extracted_stats = {
                'PassingYards': None,
                'PassingTouchdowns': None,
                'RdzPct': None,
                'ForcedFumbles': None,
                'Interceptions': None,
                'TotalSacks': None,
                'QBRating': None,
                'GamesPlayed': None,
                'TotalYards': None,
                'TeamColor': None
            }

            for category in stats:
                for stat in category['stats']:
                    if stat['name'] == 'passingYards':
                        extracted_stats['PassingYards'] = stat['displayValue']
                    elif stat['name'] == 'passingTouchdowns':
                        extracted_stats['PassingTouchdowns'] = stat['displayValue']
                    elif stat['name'] == 'completionPct':
                        extracted_stats['RdzPct'] = stat['displayValue']
                    elif stat['name'] == 'fumblesForced':
                        extracted_stats['ForcedFumbles'] = stat['displayValue']
                    elif stat['name'] == 'interceptions':
                        extracted_stats['Interceptions'] = stat['displayValue']
                    elif stat['name'] == 'sacks':
                        extracted_stats['TotalSacks'] = stat['displayValue']
                    elif stat['name'] == 'quarterbackRating':
                        extracted_stats['QBRating'] = stat['displayValue']
                    elif stat['name'] == 'gamesPlayed':
                        extracted_stats['GamesPlayed'] = stat['displayValue']
                    elif stat['name'] == 'totalYards':
                        extracted_stats['TotalYards'] = stat['displayValue']

            
            # Ensure 'teaminfo' exists in the response
            if 'teaminfo' in team_info:
                team_info = team_info['teaminfo']
                #Safely get the team color using get() method
                extracted_stats['TeamColor'] = team_info.get('color', None)  # color is in hex, e.g., "a40227"

            return extracted_stats

        return {}

    # Extract stats for both teams
    team_a_extracted_stats = extract_stats(team_a_stats, team_a_info)
    team_b_extracted_stats = extract_stats(team_b_stats, team_b_info)

    return jsonify({'team_a_stats': team_a_extracted_stats, 'team_b_stats': team_b_extracted_stats})



if __name__ == '__main__':
    app.run(debug=True)
