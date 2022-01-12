from src.config_files.config import disclaimer_1, disclaimer_2, color_1, color_2, color_3
from src.player_profile.player import create_profile
from src.stats.calculate_stats import calculate_stats
from src.output_functions.output_helper_functions import create_team_profile

def output_profile_to_html(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together):
    
    doc_name = "data/" + team_name + "/" + year_for_roster + "/" + team_name + "_batting_" + year_for_report + "_report.html"

    f = open(doc_name,'w')

    html_output = get_html_output(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together)

    f.write(html_output)
    
    return True

def get_html_output(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together):
    
    html_output = """<!DOCTYPE html>
    <html>
        {{style_sheet}}
        <body>
            {{team_profile}}
            <br>
            {{player_profiles}}
            <br>
            {{disclaimer}}
        </body>
    </html>"""

    style_sheet = get_style_sheet(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together)   
    html_output = html_output.replace("{{style_sheet}}", style_sheet)

    team_profile = get_team_profile(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together)
    html_output = html_output.replace("{{team_profile}}", team_profile)

    player_profiles = get_player_profiles(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together)
    html_output = html_output.replace("{{player_profiles}}", player_profiles)

    disclaimer = get_disclaimer()
    html_output = html_output.replace("{{disclaimer}}", disclaimer)

    return html_output

def get_style_sheet(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together):
    style_sheet = """
    <style>
    .spray-container {
        display: flex;
        justify-content: center;
    }
    .container {
        position: relative;
        text-align: center;
        color: black;
        padding: 30px;
    }
    .leftfield {
        position: absolute;
        top: 38%;
        left: 10%;
    }
    .leftcentre {
        position: absolute;
        top: 30%;
        left: 22%;
    }
    .centrefield {
        position: absolute;
        top: 25%;
        left: 43%;
    }
    .rightcentre {
        position: absolute;
        top: 30%;
        left: 67%;
    }
    .rightfield {
        position: absolute;
        top: 38%;
        left: 78%;
    }
    .thirdbase {
        position: absolute;
        top: 57%;
        left: 18%;
    }
    .shortstop {
        position: absolute;
        top: 48%;
        left: 27%;
    }
    .secondbase {
        position: absolute;
        top: 48%;
        left: 57%;
    }
    .firstbase {
        position: absolute;
        top: 57%;
        left: 66%;
    }
    .pitcher {
        position: absolute;
        top: 60%;
        left: 43%;
    }
    .catcher {
        position: absolute;
        top: 88%;
        left: 43%;
    }
    .image_name {
        position: absolute;
        top: 100%;
        left: 30%
    }
    img {
        width: 280;
        height: 400;
    }
    body {
        font-family:verdana;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    table, td {
        border: 1px solid black;
    }
    @media print {
        .new-page {
            page-break-before: always;
        }
    }
    </style>
    """

    return style_sheet

def get_team_profile(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together):

    team_profile = create_team_profile(profiles)
    team_profile_pitching = create_team_profile(profiles, pitching=True)
    message = """
    <p class=\"new-page\">
        {{team_name}}: Hitting
        <br>
        Years: {{year_for_report}}
        <br>
        {{profile}}
    <p class=\"new-page\">
        {{team_name}}: Pitching
        <br>
        Years: {{year_for_report}}
        <br>
        {{profile_pitching}}
    """
    message = message.replace("{{team_name}}", team_name.replace("_", " ").title())
    message = message.replace("{{year_for_report}}", year_for_report)
    message = message.replace("{{profile}}", format_profile_to_html(team_profile))
    message = message.replace("{{profile_pitching}}", format_profile_to_html(team_profile_pitching))
    return message
    

def get_player_profiles(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear, years_seperated_or_together):

    message = str()

    for profile in profiles:
        player_html = str()
        if profile["PA"] >= how_many_pa_to_appear:
            player_html += "<p class=\"new-page\">#{} {} {}<br>".format(profile["number"], profile["f_name"].replace("_", " "), profile["name"].replace("_", " "))
            if years_seperated_or_together == "seperated":
                player_html += "Year: {}<br>".format(profile["year"])
            if profile["class"].strip():
                player_html += "CL: {} ".format(profile["class"])
            if profile["position"].strip():
                player_html += "POS: {} ".format(profile["position"])
            if profile["b_t"].strip():
                player_html += "B/T: {} ".format(profile["b_t"])
            if profile["height"].strip():
                player_html += "Height: {} ".format(profile["height"])
            if profile["weight"].strip():
                player_html += "Weight: {} ".format(profile["weight"])
            player_html += "<br>"

            player_html += format_profile_to_html(profile)

            message += player_html

    return message


def get_disclaimer():

    message = """
    <br>
    {{disclaimer_1}}
    <br>
    {{disclaimer_2}}
    """
    message = message.replace("{{disclaimer_1}}", disclaimer_1)
    message = message.replace("{{disclaimer_2}}", disclaimer_2)
    return message

def format_profile_to_html(profile):
    
    html_profile = ""

    if "P" in str(profile["position"]) and profile["Official_Statistics_Exist_Pitching"] == True:
        html_profile += """
        <h>Official Pitching Statistics:</h>
        <table>
            <tr>
                <td>ERA: {:.2f}</td>
                <td>W: {}</td>
                <td>L: {}</td>
                <td>GP: {}</td>
                <td>GS: {}</td>
                <td>CG: {}</td>
                <td>SHO: {}</td>
                <td>CBO: {}</td>
                <td>SV: {}</td>
            </tr>
            <tr>
                <td>IP: {:.1f}</td>
                <td>H: {}</td>
                <td>R: {}</td>
                <td>ER: {}</td>
                <td>BB: {}</td>
                <td>SO: {}</td>
                <td>2B: {}</td>
                <td>3B: {}</td>
                <td>HR: {}</td>
            </tr>
            <tr>
                <td>TBF: {}</td>
                <td>B/Avg: {:.3f}</td>
                <td>WP: {}</td>
                <td>HBP: {}</td>
                <td>BK: {}</td>
                <td>SFA: {}</td>
                <td>SHA: {}</td>
                <td></td>
                <td></td>
            </tr>
        </table>
        """.format(profile["Official_Statistics_Pitching"]["ERA"],
                        profile["Official_Statistics_Pitching"]["W"], profile["Official_Statistics_Pitching"]["L"],
                        profile["Official_Statistics_Pitching"]["GP"], profile["Official_Statistics_Pitching"]["GS"],
                        profile["Official_Statistics_Pitching"]["CG"], profile["Official_Statistics_Pitching"]["SHO"],
                        profile["Official_Statistics_Pitching"]["CBO"], profile["Official_Statistics_Pitching"]["SV"],
                        profile["Official_Statistics_Pitching"]["IP"], profile["Official_Statistics_Pitching"]["H"],
                        profile["Official_Statistics_Pitching"]["R"], profile["Official_Statistics_Pitching"]["ER"],
                        profile["Official_Statistics_Pitching"]["BB"], profile["Official_Statistics_Pitching"]["S0"],
                        profile["Official_Statistics_Pitching"]["2B"], profile["Official_Statistics_Pitching"]["3B"],
                        profile["Official_Statistics_Pitching"]["HR"], profile["Official_Statistics_Pitching"]["TBF"],
                        profile["Official_Statistics_Pitching"]["B/Avg"], profile["Official_Statistics_Pitching"]["WP"],
                        profile["Official_Statistics_Pitching"]["HBP"], profile["Official_Statistics_Pitching"]["BK"],
                        profile["Official_Statistics_Pitching"]["SFA"], profile["Official_Statistics_Pitching"]["SHA"])
    elif not "P" in str(profile["position"]) and profile["Official_Statistics_Exist_Batting"] == True:
        html_profile += """
        <h>Official Hitting Statistics:</h>
        <table>
            <tr>
                <td>GP: {}</td>
                <td>GS: {}</td>
                <td>AVG: {:.3f}</td>
                <td>AB: {}</td>
                <td>R: {}</td>
                <td>H: {}</td>
                <td>2B: {}</td>
                <td>3B: {}</td>
                <td>HR: {}</td>
            </tr>
            <tr>
                <td>RBI: {}</td>
                <td>TB: {}</td>
                <td>SLG: {:.3f}</td>
                <td>BB: {}</td>
                <td>HBP: {}</td>
                <td>SO: {}</td>
                <td>GDP: {}</td>
                <td>OBP: {:.3f}</td>
                <td>SF: {}</td>
            </tr>
            <tr>
                <td>SH: {}</td>
                <td>SB: {}</td>
                <td>SBA: {}</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        </table>
        """.format(profile["Official_Statistics_Batting"]["GP"], profile["Official_Statistics_Batting"]["GS"],
                        profile["Official_Statistics_Batting"]["AVG"], profile["Official_Statistics_Batting"]["AB"],
                        profile["Official_Statistics_Batting"]["R"], profile["Official_Statistics_Batting"]["H"],
                        profile["Official_Statistics_Batting"]["2B"], profile["Official_Statistics_Batting"]["3B"],
                        profile["Official_Statistics_Batting"]["HR"], profile["Official_Statistics_Batting"]["RBI"],
                        profile["Official_Statistics_Batting"]["TB"], profile["Official_Statistics_Batting"]["SLG"],
                        profile["Official_Statistics_Batting"]["BB"], profile["Official_Statistics_Batting"]["HBP"],
                        profile["Official_Statistics_Batting"]["SO"], profile["Official_Statistics_Batting"]["GDP"] ,
                        profile["Official_Statistics_Batting"]["OBP"], profile["Official_Statistics_Batting"]["SF"],
                        profile["Official_Statistics_Batting"]["SH"], profile["Official_Statistics_Batting"]["SB"],
                        profile["Official_Statistics_Batting"]["SBA"]
        )

    html_profile += "<h>Confirmable Statistics:</h><table>"

    if "P" in str(profile["position"]):
        html_profile += """    
            <tr>
                <td>FIP: {:.3f}</td>
                <td>AVGa: {:.3f}</td>
                <td>OBPa: {:.3f}</td>
                <td>SLGa: {:.3f}</td>
                <td>OPSa: {:.3f}</td>
                <td>K%: {:.2f}%</td>
                <td>BB%: {:.2f}%</td>
            </tr>
        """.format(profile["FIP"], profile["AVG"], profile["OBP"], profile["SLG"], 
            profile["OPS"], profile["K%"], profile["BB%"])
    else:
        html_profile += """    
            <tr>
                <td>AVG: {:.3f}</td>
                <td>OBP: {:.3f}</td>
                <td>SLG: {:.3f}</td>
                <td>OPS: {:.3f}</td>
                <td>BABIP: {:.3f}</td>
                <td></td>
                <td></td>
            </tr>
        """.format(profile["AVG"], profile["OBP"], profile["SLG"], profile["OPS"], profile["BABIP"])

    html_profile += """
        <tr>
            <td>PA: {}</td>
            <td>AB: {}</td>
            <td>Hits: {}</td>
            <td>Walks: {}</td>
            <td>HBP: {}</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>XBH: {}</td>
            <td>1B: {}</td>
            <td>2B: {}</td>
            <td>3B: {}</td>
            <td>HR: {}</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Strikeouts: {}</td> 
            <td>Looking: {}</td>
            <td>Swinging: {}</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>ROE: {}</td>
            <td>SF: {}</td>
            <td>FC: {}</td>
            <td>DP: {}</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>IFH: {}</td>
            <td>IFHO: {}</td>
            IFHpercentage
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Steal Attempts: {}</td>
            <td>SB: {}</td>
            <td>CS: {}</td>
            steal_percentage
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>SB2: {}</td>
            <td>SB3: {}</td>
            <td>SB4: {}</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Bunts:</td>
            <td>Safe: {}</td>
            <td>Errors: {}</td>
            <td>Outs: {}</td>
            <td>Sacrifice: {}</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Location:</td>
            <td>1: {}</td>
            <td>2: {}</td>
            <td>3: {}</td>
            <td>4: {}</td>
            <td>5: {}</td>
            <td>6: {}</td>
        </tr>
        <tr>
            <td>7: {}</td>
            <td>8: {}</td>
            <td>9: {}</td>
            <td>78: {}</td>
            <td>89: {}</td>
            <td></td>
            <td></td>
        </tr>
        location_percentage
        <tr>
            <td>Hit Type:</td>
            <td>GB: {}</td>
            <td>LD: {}</td>
            <td>FB: {}</td>
            <td>PF: {}</td>
            <td>Bunt: {}</td>
            <td></td>
        </tr>
        type_percentage
        </table>
    spray_chart 
    </p>
    """.format(
        profile["PA"], profile["AB"], profile["Hits"], profile["BB"], profile["HBP"],
        profile["XBH"], profile["1B"], profile["2B"], profile["3B"], profile["HR"],
        profile["K"], profile["KL"], profile["KS"],
        profile["ROE"], profile["SF"], profile["FC"], profile["DP"],
        profile["IFH"], profile["IFHO"],
        profile["SB"] + profile["CS"], profile["SB"], profile["CS"],
        profile["SB2"], profile["SB3"], profile["SB4"],
        profile["Bunt"]["Safe"], profile["Bunt"]["Error"], profile["Bunt"]["Out"], profile["Bunt"]["SAC"],
        profile["Location"]["1"], profile["Location"]["2"], profile["Location"]["3"], profile["Location"]["4"], 
        profile["Location"]["5"], profile["Location"]["6"], profile["Location"]["7"], profile["Location"]["8"], 
        profile["Location"]["9"], profile["Location"]["78"], profile["Location"]["89"], 
        profile["Type"]["GB"], profile["Type"]["LD"], profile["Type"]["FB"], 
        profile["Type"]["PF"], profile["Type"]["Bunt"]
        )

    if profile["IFH"] + profile["IFHO"]:
        html_profile = html_profile.replace("IFHpercentage", "<td>IFHP: {:.2f}%</td>".format(profile["IFHP"]))
    else:
        html_profile = html_profile.replace("IFHpercentage", "<td></td>")

    if profile["SB"] + profile["CS"]:
        html_profile = html_profile.replace("steal_percentage", "<td>Steal Percentage: {:.2f}%</td>".format(profile["SB"] * 100/(profile["SB"]+profile["CS"])))
    else:
        html_profile = html_profile.replace("steal_percentage", "<td></td>")

    total = (profile["Location"]["1"] + profile["Location"]["2"] + profile["Location"]["3"] + 
                        profile["Location"]["4"] + profile["Location"]["5"] + profile["Location"]["6"] + 
                        profile["Location"]["7"] + profile["Location"]["8"] + profile["Location"]["9"] +
                        profile["Location"]["78"] + profile["Location"]["89"])
    if total:
        html_profile = html_profile.replace("location_percentage", """
        <tr>
            <td>Location Percentages:</td>
            <td>1: {:.2f}%</td>
            <td>2: {:.2f}%</td>
            <td>3: {:.2f}%</td>
            <td>4: {:.2f}%</td>
            <td>5: {:.2f}%</td>
            <td>6: {:.2f}%</td>
        </tr>
        <tr>
            <td>7: {:.2f}%</td>
            <td>8: {:.2f}%</td>
            <td>9: {:.2f}%</td>
            <td>78: {:.2f}%</td>
            <td>89: {:.2f}%</td>
            <td></td>
            <td></td>
        </tr>""".format(
            profile["Location"]["1"]/total*100, profile["Location"]["2"]/total*100,
            profile["Location"]["3"]/total*100, profile["Location"]["4"]/total*100, 
            profile["Location"]["5"]/total*100, profile["Location"]["6"]/total*100,
            profile["Location"]["7"]/total*100, profile["Location"]["8"]/total*100, 
            profile["Location"]["9"]/total*100, profile["Location"]["78"]/total*100,
            profile["Location"]["89"]/total*100))
        html_profile = html_profile.replace("spray_chart", create_spray_chart(profile, total))
    else:
        html_profile = html_profile.replace("location_percentage", "")
        html_profile = html_profile.replace("spray_chart", "")

    total = profile["Type"]["GB"] + profile["Type"]["LD"] + profile["Type"]["FB"] + profile["Type"]["PF"] + profile["Type"]["Bunt"]
    if total:
        html_profile = html_profile.replace("type_percentage", """
        <tr>
            <td>Type percentages:</td>
            <td>GB: {:.2f}%</td>
            <td>LD: {:.2f}%</td>
            <td>FB: {:.2f}%</td>
            <td>PF: {:.2f}%</td>
            <td>Bunt: {:.2f}%</td>
            <td></td>
        </tr>""".format(
            profile["Type"]["GB"]/total*100, profile["Type"]["LD"]/total*100, 
            profile["Type"]["FB"]/total*100, profile["Type"]["PF"]/total*100, 
            profile["Type"]["Bunt"]/total*100))
    else:
        html_profile = html_profile.replace("type_percentage", "")


    return html_profile

def create_spray_chart(profile, total):
    
    message = """
    <div class="spray-container">
        <div class="container">
            <img src=\"/home/ilan/Documents/code/play_by_play/images/spray_chart_base_2.png\" alt=\"Image not found\" width=\"350\" height=\"500\">
            <div class="leftfield">{:.2f}%</div>
            <div class="leftcentre">{}</div>
            <div class="centrefield">{:.2f}%</div>
            <div class="rightcentre">{}</div>
            <div class="rightfield">{:.2f}%</div>
            <div class="thirdbase">{:.2f}%</div>
            <div class="shortstop">{:.2f}%</div>
            <div class="secondbase">{:.2f}%</div>
            <div class="firstbase">{:.2f}%</div>
            <div class="pitcher">{:.2f}%</div>
            <div class="catcher">{:.2f}%</div>
            <div class="image_name">Overall Spray Chart</div>
        </div>
    """.format(profile["Location"]["7"]/total*100, format_gaps(profile["Location"]["78"]/total*100),
            profile["Location"]["8"]/total*100, format_gaps(profile["Location"]["89"]/total*100), 
            profile["Location"]["9"]/total*100, profile["Location"]["5"]/total*100,
            profile["Location"]["6"]/total*100, profile["Location"]["4"]/total*100, 
            profile["Location"]["3"]/total*100, profile["Location"]["2"]/total*100,
            profile["Location"]["1"]/total*100)
    
    total = (profile["XBHLocation"]["1"] + profile["XBHLocation"]["2"] + profile["XBHLocation"]["3"] + 
            profile["XBHLocation"]["4"] + profile["XBHLocation"]["5"] + profile["XBHLocation"]["6"] + 
            profile["XBHLocation"]["7"] + profile["XBHLocation"]["8"] + profile["XBHLocation"]["9"] + 
            profile["XBHLocation"]["78"] + profile["XBHLocation"]["89"])

    if total:
        message += """
            <div class="container">
                <img src=\"/home/ilan/Documents/code/play_by_play/images/spray_chart_base_2.png\" alt=\"Image not found\" width=\"350\" height=\"500\">
                <div class="leftfield">{:.2f}%</div>
                <div class="leftcentre">{}</div>
                <div class="centrefield">{:.2f}%</div>
                <div class="rightcentre">{}</div>
                <div class="rightfield">{:.2f}%</div>
                <div class="thirdbase">{:.2f}%</div>
                <div class="shortstop">{:.2f}%</div>
                <div class="secondbase">{:.2f}%</div>
                <div class="firstbase">{:.2f}%</div>
                <div class="pitcher">{:.2f}%</div>
                <div class="catcher">{:.2f}%</div>
                <div class="image_name">Spray Chart for XBHs</div>
            </div>
        </div>
        """.format(profile["XBHLocation"]["7"]/total*100, format_gaps(profile["XBHLocation"]["78"]/total*100),
                profile["XBHLocation"]["8"]/total*100, format_gaps(profile["XBHLocation"]["89"]/total*100), 
                profile["XBHLocation"]["9"]/total*100, profile["XBHLocation"]["5"]/total*100,
                profile["XBHLocation"]["6"]/total*100, profile["XBHLocation"]["4"]/total*100, 
                profile["XBHLocation"]["3"]/total*100, profile["XBHLocation"]["2"]/total*100,
                profile["XBHLocation"]["1"]/total*100)
    else:
        message += """
        </div>
        """
        
    return message

def format_gaps(input_number):
    if input_number == 0:
        return ''
    else:
        return "{:.2f}%".format(input_number)