import fastf1
from fastf1.ergast import Ergast

input_Season = input("Enter the F1 season (e.g., 2025): ")
input_Round = input("Enter the current round number (e.g., 19): ")

Season = input_Season
Round = input_Round


def get_drivers_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=Season, round=Round)
    return standings.content[0]

def calculate_max_points_for_remaining_season():
    points_for_sprint = 8 + 25
    points_for_conventional = 25

    events = fastf1.get_event_schedule(Season, backend='ergast')
    events = events[events['RoundNumber'] >= Round]
    sprint_events = len(events.loc[events['EventFormat'] == 'sprint_shootout'])
    convertional_events = len(events.loc[events['EventFormat'] == 'conventional'])

    sprint_points = sprint_events * points_for_sprint
    conventional_points = convertional_events * points_for_conventional

    return sprint_points + conventional_points

def calculate_who_can_win(driver_standings, max_points):
    leader_points = int(driver_standings.loc[0]['points'])

    for i, _ in enumerate(driver_standings.iterrows()):
        driver = driver_standings.loc[i]
        driver_max_points = int(driver["points"]) + max_points
        can_win = 'No' if driver_max_points < leader_points else 'Yes'

        print(f"{driver['position']}: {driver['givenName'] + ' ' + driver['familyName']}, "
              f"Current points: {driver['points']}, "
              f"Theoretical max points: {driver_max_points}, "
              f"Can win: {can_win}")

driver_standings = get_drivers_standings()
points = calculate_max_points_for_remaining_season()
calculate_who_can_win(driver_standings, points)