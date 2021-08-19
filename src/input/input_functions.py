
def get_user_input():
    """Gets all required input from the user. This should be the only time that user input is requrired."""

    team_name = input("which team's data do you want?\n")
    if team_name == "test":
        return get_test_values()

    year = input("Which year's roster do you want data on?\n")
    list_from_years = input("Enter a list of the years that you want data from seperated by spaces\n")
    what_format_output = input("What format output do you want?\n")
    how_many_pa_to_appear = input("How many plate appearances does a play need to be outputted?\n")
    if " " in list_from_years:
        years_seperated_or_together = input("Should a player get a sheet for each year or should the data be consolidated? Enter 'seperated' or 'together'.\n")
    else:
        years_seperated_or_together = "separated"

    user_input = format_user_input(team_name, year, list_from_years, what_format_output, how_many_pa_to_appear, years_seperated_or_together)

    return user_input

def format_user_input(team_name, year, list_from_years, what_format_output, how_many_pa_to_appear, years_seperated_or_together):
    """Format user input into usable form"""

    list_from_years = list_from_years.split(" ")

    user_input = {}
    user_input["team_name"] = team_name.lower().replace(" ", "_")
    user_input["year"] = year
    user_input["list_from_years"] = list_from_years
    user_input["what_format_output"] = what_format_output
    
    try:
        user_input["how_many_pa_to_appear"] = int(how_many_pa_to_appear)
    except:
        user_input["how_many_pa_to_appear"] = 0

    if years_seperated_or_together not in ["together", "seperated"]:
        user_input["years_seperated_or_together"] = "seperated"
    else:
        user_input["years_seperated_or_together"] = years_seperated_or_together

    return user_input

def get_test_values():
    with open("test_inputs.txt", "r") as f:
        values = f.readlines()

    team_name = values[0].strip()
    year = values[1].strip()
    list_from_years = values[2].strip()
    what_format_output = values[3].strip()
    how_many_pa_to_appear = values[4].strip()
    years_seperated_or_together = values[5].strip()

    user_input = format_user_input(team_name, year, list_from_years, what_format_output, how_many_pa_to_appear, years_seperated_or_together)

    return user_input