from src.output_functions.output_to_txt import output_profile_to_text
from src.output_functions.output_helper_functions import combine_player_profiles, create_string_list_of_years
from src.output_functions.output_to_xlsx import output_profile_to_xlsx
from src.output_functions.output_to_html import output_profile_to_html
from src.output_functions.output_to_pdf import output_profile_to_pdf

def  output_data(profiles, team_name, year_for_roster, list_of_years, what_format_output, how_many_pa_to_appear, years_seperated_or_together):
    """Outputs data in the formats required"""

    check = True 
    str_list_of_years = create_string_list_of_years(list_of_years) 

    if years_seperated_or_together == "together":
        profiles = combine_player_profiles(profiles) 

    if what_format_output == "txt" or not what_format_output:
        check = check and output_profile_to_text(profiles, team_name, year_for_roster, str_list_of_years, how_many_pa_to_appear)

    if what_format_output == "xlsx" or not what_format_output:
        check = check and output_profile_to_xlsx(profiles, team_name, year_for_roster, str_list_of_years, how_many_pa_to_appear)

    if what_format_output == "html" or not what_format_output:
        check = check and output_profile_to_html(profiles, team_name, year_for_roster, str_list_of_years, how_many_pa_to_appear, years_seperated_or_together)

    if what_format_output == "pdf" or not what_format_output:
        check = check and output_profile_to_html(profiles, team_name, year_for_roster, str_list_of_years, how_many_pa_to_appear, years_seperated_or_together)
        check = check and output_profile_to_pdf(profiles, team_name, year_for_roster, str_list_of_years, how_many_pa_to_appear)

    

    return check