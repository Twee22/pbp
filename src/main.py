from src.input.input_functions import get_user_input
from src.import_from_txt.import_functions import get_players, get_play_by_play_data
from src.stats.calculate_stats import calculate_stats
from src.breakdown.breakdown_data import breakdown_data
from src.output_functions.output_data import output_data

def main():
    # Get user inputs
    user_input = get_user_input()
    team_name = user_input["team_name"]
    year_for_roster = user_input["year"]
    list_of_years = user_input["list_from_years"]
    what_format_output = user_input["what_format_output"]
    how_many_pa_to_appear = user_input["how_many_pa_to_appear"]
    years_seperated_or_together = user_input["years_seperated_or_together"]
    
    # Get team list
    if years_seperated_or_together == "together":
        profiles = get_players(team_name, year_for_roster, year_for_roster)
    else:
        profiles = []
        for year_from_list in list_of_years:
            profiles += get_players(team_name, year_from_list, year_for_roster)

    # Get play_by_play data
    if years_seperated_or_together == "together":
        play_by_play_data = {}
        data = []
        for year in list_of_years:
            tmp_data = get_play_by_play_data(team_name, year)
            for d in tmp_data:
                data.append(d)
        play_by_play_data.update({year_for_roster: data})
    else:
        play_by_play_data = {}
        for year in list_of_years:
            data = get_play_by_play_data(team_name, year)
            play_by_play_data.update({year: data})

    # Scrape play_by_play data
    for profile in profiles:
        if not "P" in profile["position"]:
            name = profile["name"].lower()
            check = False
            for line in play_by_play_data[profile["year"]]:
                line = line.lower()
                if "top of" in line or "bottom of" in line:
                    if "opposition" in line:
                        check = False
                    else:
                        check = True
                elif check:
                    if name[:7] in line:
                        profile = breakdown_data(profile, line) 
                '''for word in words[:2]:
                    if name[:7] in word and not check:
                        profile = breakdown_data(profile, line)
                        check = True'''
            profile = calculate_stats(profile)
        elif "P" in profile["position"]:
            player_check = False
            inning_check = False
            for line in play_by_play_data[profile["year"]]:
                line = line.lower()
                if "game_start_point" in line:
                    player_check = False
                if ("starting pitcher" in line) and profile["name"].lower() in line:
                    player_check = True
                if "top of" in line or "bottom of" in line:
                    if "opposition" in line:
                        inning_check = True
                    else:
                        inning_check = False
                elif inning_check:
                    if "now in to pitch" in line:
                        if profile["name"].lower() in line.split('replacing')[0]:
                            player_check = True
                        else:
                            player_check = False
                    elif player_check:
                        profile = breakdown_data(profile, line)
            profile = calculate_stats(profile)
            
    # Output data
    check = output_data(profiles, team_name, year_for_roster, list_of_years, what_format_output, how_many_pa_to_appear, years_seperated_or_together)

    if not check:
        print("An error has occured with outputting the data")