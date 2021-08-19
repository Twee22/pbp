from src.input.input_functions import format_user_input
from src.import_from_txt.import_functions import get_order, fill_empty_sections_profile
from src.player_profile.player import create_profile, check_data_point
from src.stats.calculate_stats import calculate_stats
from src.breakdown.breakdown_data import get_location, breakdown_data
from src.output_functions.output_helper_functions import create_string_list_of_years, combine_player_profiles, add_profiles_together

def test_user_input():
    print("Testing user_input function")
    test_user_input = format_user_input("team_name", "2019", "2017 2018 2019 2020", "pdf", "0", "together")
    assert test_user_input["team_name"] == "team_name"
    assert test_user_input["year"] == "2019"
    assert test_user_input["list_from_years"] == ["2017", "2018", "2019", "2020"]
    assert test_user_input["what_format_output"] == "pdf"
    assert test_user_input["how_many_pa_to_appear"] == 0
    assert test_user_input["years_seperated_or_together"] == "together"
    test_user_input = format_user_input("test", "2019", "2019", "pdf", "NOT_A_NUMBER", "NOT_A_VIABLE_INPUT")
    assert test_user_input["how_many_pa_to_appear"] == 0
    assert test_user_input["years_seperated_or_together"] == "seperated"

def test_get_order():
    print("Testing get_order function")
    test_output = get_order("name number class")
    assert test_output == ['name', 'number', 'class']

def test_fill_empty_sections_profile():
    print("Testing fill_empty_sections_profile")
    points = ["name", "number", "f_name", "class", "position", "b_t", "height", "weight"]
    profile = {}
    for point in points:
        profile.update({point: ""})
    profile = fill_empty_sections_profile(profile)
    for point in points:
        assert profile[point] == "Not Found"

def test_create_profile():
    print("Testing create_profile")
    profile = create_profile()
    assert profile == {"name": "",
            "number": 0, "f_name": 0,
            "class": 0, "position": 0, "b_t": 0,
            "height": 0, "weight": 0, "year": 0,
            "AVG": 0, "OBP": 0, "SLG": 0, "OPS": 0, "BABIP": 0,
            "AB": 0, "PA": 0,
            "Hits": 0, "XBH": 0, "1B": 0, "2B": 0, "3B": 0, "HR": 0,
            "BB": 0, "HBP": 0, 
            "K": 0, "KL": 0, "KS": 0, 
            "ROE": 0, "SF": 0, "FC": 0,
            "IFH": 0, "IFHO": 0, "IFHP": 0,
            "SB": 0, "CS": 0, "SB2": 0, "SB3": 0, "SB4": 0,
            "Bunt": {"Safe": 0, "Error": 0, "Out": 0, "SAC": 0},
            "Location": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "78": 0, "89": 0},
            "Type": {"GB": 0, "LD": 0, "FB": 0, "PF": 0, "Bunt": 0}
    }

def test_check_data_point():
    print("Testing check_data_point")
    assert check_data_point("name")
    assert not check_data_point("not_valid")

def test_calculate_stats():
    print("Testing calculate_stats")
    test_profile = create_profile()

    test_profile = calculate_stats(test_profile)
    assert test_profile["AVG"] == 0
    assert test_profile["OBP"] == 0
    assert test_profile["SLG"] == 0
    assert test_profile["OPS"] == 0
    assert test_profile["IFHP"] == 0
    assert test_profile["BABIP"] == 0

    test_profile["AB"] = 5
    test_profile["Hits"] = 2
    test_profile["BB"] = 1
    test_profile["HBP"] = 3
    test_profile["SF"] = 4
    test_profile["1B"] = 1
    test_profile["HR"] = 1
    test_profile["IFH"] = 1
    test_profile["IFHO"] = 3
    test_profile["Location"]["89"] = 4

    test_profile = calculate_stats(test_profile)
    assert test_profile["AVG"] == 0.4
    assert test_profile["OBP"] == 6/13
    assert test_profile["SLG"] == 1
    assert test_profile["OPS"] == 1 + (6 / 13)
    assert test_profile["IFHP"] == 25
    assert test_profile["BABIP"] == 0.5

def test_get_location():
    print("Testing get_location")
    profile = create_profile()
    
    profile = get_location(profile, "R Santamaria singled to pitcher")
    assert profile["Location"]["1"] == 1

    profile = get_location(profile, "J. Angelopul singled to catcher, bunt (0-0).")
    assert profile["Location"]["2"] == 1

    profile = get_location(profile, "P. Giglio grounded out to 1b unassisted (0-0).")
    assert profile["Location"]["3"] == 1
    assert profile["IFH"] == 1
    profile = get_location(profile, "J. Gay to 1b for O. Romero.	7	5")
    assert profile["Location"]["3"] == 1 
    profile = get_location(profile, "P. Giglio singled to first base (0-0)")
    assert profile["Location"]["3"] == 2

    profile = get_location(profile, "C. Hughes grounded out to 2b (0-0)")
    assert profile["Location"]["4"] == 1
    assert profile["IFH"] == 3
    profile = get_location(profile, "T. Erzen to 2b for E. Hildebran.")
    assert profile["Location"]["4"] == 1 
    profile = get_location(profile, "G. Hammer singled to second base (1-0 B)")
    assert profile["Location"]["4"] == 2

    profile = get_location(profile, "B. Ryan grounded out to 3b.")
    assert profile["Location"]["5"] == 1
    assert profile["IFH"] == 5
    profile = get_location(profile, "C. Ratliff to 3b for Rocco Arguto.")
    assert profile["Location"]["5"] == 1 
    profile = get_location(profile, "L. Bistrup singled to third base;")
    assert profile["Location"]["5"] == 2

    profile = get_location(profile, "T. Schuetz singled to shortstop")
    assert profile["Location"]["6"] == 1
    assert profile["IFH"] == 7
    profile = get_location(profile, "J. Nakagawa to ss for J. Martinez.")
    assert profile["Location"]["6"] == 1 
    profile = get_location(profile, "B. Galindo grounded out to ss.")
    assert profile["Location"]["6"] == 2

    profile = get_location(profile, "N. Nintze flied out to lf.")
    assert profile["Location"]["7"] == 1
    assert profile["IFH"] == 8
    profile = get_location(profile, "J. Angelopul to lf for P. Giglio.")
    assert profile["Location"]["7"] == 1 
    profile = get_location(profile, "Castillo,D doubled to left field")
    assert profile["Location"]["7"] == 2

    profile = get_location(profile, "N. Nintze flied out to cf (2-2 KBSB).")
    assert profile["Location"]["8"] == 1
    assert profile["IFH"] == 8
    profile = get_location(profile, "G. Bell to cf for N. Nintze.")
    assert profile["Location"]["8"] == 1 
    profile = get_location(profile, "B. Feist singled to center field")
    assert profile["Location"]["8"] == 2

    profile = get_location(profile, "D. Solis flied out to rf.")
    assert profile["Location"]["9"] == 1
    assert profile["IFH"] == 8
    profile = get_location(profile, "J. Hernandez to rf for P. Giglio.")
    assert profile["Location"]["9"] == 1 
    profile = get_location(profile, "N. Nintze singled to right field")
    assert profile["Location"]["9"] == 2

    profile = get_location(profile, "B. Ipson doubled to left center.")
    assert profile["Location"]["78"] == 1
    assert profile["IFH"] == 8

    profile = get_location(profile, "J. Hernandez singled to right center.")
    assert profile["Location"]["89"] == 1
    assert profile["IFH"] == 8

def test_breakdown_data():
    print("Testing breakdown_data")

    profile = create_profile()
    profile = breakdown_data(profile, "J. Manzano singled to right field")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["1B"] == 1
    assert profile["Hits"] == 1
    assert profile["Location"]["9"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "J. Manzano doubled to right field")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["2B"] == 1
    assert profile["Hits"] == 1
    assert profile["XBH"] == 1
    assert profile["Location"]["9"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "C. Marshall tripled to center field")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["3B"] == 1
    assert profile["Hits"] == 1
    assert profile["XBH"] == 1
    assert profile["Location"]["8"] == 1

    # Might want more tests for HRs
    profile = create_profile()
    profile = breakdown_data(profile, "L. Soole homered to right field")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["HR"] == 1
    assert profile["Hits"] == 1
    assert profile["XBH"] == 1
    assert profile["Location"]["9"] == 1

    # Might want more to Walks
    profile = create_profile()
    profile = breakdown_data(profile, "J. Kistaitis walked")
    assert profile["PA"] == 1
    assert profile["BB"] == 1

    # Might want more for HBP
    profile = create_profile()
    profile = breakdown_data(profile, "J. Gay hit by pitch")
    assert profile["PA"] == 1
    assert profile["HBP"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "L. Bistrup struck out looking")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["K"] == 1
    assert profile["KL"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "D. Adame struck out swinging")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["K"] == 1
    assert profile["KS"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "L. Soole grounded out to 2b.	6	2")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["Type"]["GB"] == 1
    assert profile["Location"]["4"] == 1
    assert profile["IFHO"] == 1
    assert profile["IFH"] == 0

    profile = create_profile()
    profile = breakdown_data(profile, "C. Peters lined out to cf (1-0 B).")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["Type"]["LD"] == 1
    assert profile["Location"]["8"] == 1

    # Need more for fly out
    profile = create_profile()
    profile = breakdown_data(profile, "J. Hernandez flied out to rf")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["Type"]["FB"] == 1
    assert profile["Location"]["9"] == 1

    # Need more for errors
    profile = create_profile()
    profile = breakdown_data(profile, "E. Hildebran reached on an error by 1b")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["ROE"] == 1

    # Need sac fly tracking

    profile = create_profile()
    profile = breakdown_data(profile, "E. Hildebran reached on a fielder's choice (0-0)")
    assert profile["PA"] == 1
    assert profile["AB"] == 1
    assert profile["FC"] == 1
    assert profile["Type"]["GB"] == 1

    # Need bunts

    profile = create_profile()
    profile = breakdown_data(profile, "D. Solis stole second")
    assert profile["SB"] == 1
    assert profile["SB2"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "L. Bistrup stole third")
    assert profile["SB"] == 1
    assert profile["SB3"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "W. Dixon stole home.")
    assert profile["SB"] == 1
    assert profile["SB4"] == 1

    profile = create_profile()
    profile = breakdown_data(profile, "J. Shapiro out at second p to 3b to 2b, caught stealing.")
    assert profile["CS"] == 1

def test_output_helper_functions():
    print("Testing output_helper_functions")
    test_add_profiles_together()
    test_combine_player_profiles()
    test_create_string_list_of_years()

def test_add_profiles_together():
    profile1 = create_profile()
    profile2 = create_profile()
    
    profile1["number"] = "1"
    profile2["number"] = "1"
    profile1["AB"] = 4
    profile2["AB"] = 3
    profile2["BB"] = 5
    profile1["Location"]["1"] = 1
    profile2["Location"]["1"] = 2
    profile1["Type"]["GB"] = 6
    profile2["Type"]["GB"] = 7
    
    profile = add_profiles_together(profile1, profile2)

    assert profile["number"] == "1"
    assert profile["AB"] == 7
    assert profile["BB"] == 5
    assert profile["Location"]["1"] == 3
    assert profile["Type"]["GB"] == 13

def test_combine_player_profiles():
    profile1 = create_profile()
    profile2 = create_profile()
    
    profile1["number"] = "1"
    profile2["number"] = "1"
    profile1["AB"] = 4
    profile2["AB"] = 3
    profile2["BB"] = 5
    profile1["Location"]["1"] = 1
    profile2["Location"]["1"] = 2
    profile1["Type"]["GB"] = 6
    profile2["Type"]["GB"] = 7

    profiles = [profile1, profile2]

    profiles = combine_player_profiles(profiles)

    assert len(profiles) == 1
    assert profiles[0]["number"] == "1"


def test_create_string_list_of_years():
    list_of_years = ["2017", "2018", "2019", "2020"]
    assert create_string_list_of_years(list_of_years) == "2017_2018_2019_2020"

def unit_test():
    print("Begin testing")
    # tests for input
    test_user_input()
    # tests for import_from_txt
    test_get_order()
    test_fill_empty_sections_profile()
    # tests for player_profile
    test_create_profile()
    test_check_data_point()
    # tests for stats
    test_calculate_stats()
    # tests for breakdown
    test_get_location()
    test_breakdown_data()
    # tests for output_fuctions
    test_output_helper_functions()

    print("Success")

if __name__ == "__main__":
    unit_test()
