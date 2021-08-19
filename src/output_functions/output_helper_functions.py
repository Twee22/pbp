from src.player_profile.player import create_profile
from src.stats.calculate_stats import calculate_stats


def create_string_list_of_years(list_of_years):
    """Creates a string listing the years"""
    string_list_of_years = ""
    for year in list_of_years:
        string_list_of_years += year + "_"
    string_list_of_years = string_list_of_years[:-1]
    return string_list_of_years

def combine_player_profiles(profiles):
    """Combines player profiles from across years"""
    combined_profile = []
    for profile in profiles:
        check = False
        for c_profile in combined_profile:
            if c_profile["number"] == profile["number"] and c_profile["name"] == profile["name"] and c_profile["position"] == profile["position"]:
                c_profile = add_profiles_together(c_profile, profile)
                check = True
        if not check:
            combined_profile.append(profile)
    return combined_profile

def add_profiles_together(profile1, profile2):
    """Takes 2 profiles as input, returns the profiles combined. """
    for key in profile1:
        if isinstance(profile1[key], int):
            profile1[key] = profile1[key] + profile2[key]
        elif isinstance(profile1[key], dict):
            for key2 in profile1[key]:
                profile1[key][key2] = profile1[key][key2] + profile2[key][key2]
    return profile1


def create_team_profile(profiles, pitching=False):
    
    team_profile = {}
    team_profile = create_profile()

    for profile in profiles:
        if not pitching:
            if "P" not in str(profile["position"]):
                team_profile = profile_merge(team_profile, profile)
        elif pitching:
            if "P" in str(profile["position"]):
                team_profile = profile_merge(team_profile, profile)

    if pitching:
        team_profile["name"] = "team_pitching"
        team_profile["position"] = "P"
    elif not pitching:
        team_profile["name"] = "team_hitting"
    
    team_profile = calculate_stats(team_profile)
    
    return team_profile


def profile_merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                profile_merge(a[key], b[key], path + [str(key)])
            elif not isinstance(a[key], str) and not isinstance(b[key], str):
                a[key] = a[key] + b[key]
        else:
            a[key] = b[key]
    return a