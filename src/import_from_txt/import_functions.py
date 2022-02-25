import re

from os.path import isfile

from copy import deepcopy

from src.player_profile.player import create_profile, check_data_point

def get_players(team_name, year_from_list, year):
    """Import roster from text documents """


    doc_name = "data/" + team_name + "/" + year + "/" + team_name + "_team_" + year +".txt"
    profiles = []

    with open(doc_name, "r") as f:

        line = f.readline()
        order = get_order(line)

        line = f.readline()
        while line:
            split_line = []

            if line:
                for p in line.split():
                    p = p.strip()
                    if p:
                        split_line.append(p)

            '''if len(split_line) < 5:
                line = f.readline()
                continue'''

            profile = create_profile()
            profile["year"] = year_from_list

            counter = 0
            for data_point in order:
                if check_data_point(data_point):
                    try:
                        profile[data_point] = split_line[counter]
                        counter += 1
                    except:
                        continue

            profile = fill_empty_sections_profile(profile)

            if "/" in profile["position"] and "p" in profile["position"].lower():
                for sepearted_position in profile["position"].split('/'):
                    new_profile = deepcopy(profile)
                    new_profile["position"] = sepearted_position
                    profiles.append(new_profile)
            else:
                profiles.append(profile)

            line = f.readline()

    for profile in profiles:
        get_official_statistics(profile, team_name, year_from_list, year)

    return profiles

def get_official_statistics(profile, team_name, year_from_list, year):
    doc_name = "data/" + team_name + "/" + year_from_list + "/" + team_name + "_official_statistics_" + year_from_list +".txt"
    if int(year_from_list) <= 2021:
        try:
            # Try statement ensures that format is consistent
            
            if not isfile(doc_name):
                return 
            
            with open(doc_name, "r") as f:

                line = f.readline()
                check = False
                while line:
                    
                    line = line.lower()

                    if not check and "p" in profile["position"].lower() and "pitching" in line:
                        check = True
                        
                    elif not check and "p" not in profile["position"].lower() and "batting" in line:
                        check = True

                    elif check and ("pitching" in line or "batting" in line or "fielding" in line):
                        check = False
                    
                    elif check and profile["name"].lower() in line:

                        split_line = line.split("\t")
                        if "p" in profile["position"].lower():
                            profile["Official_Statistics_Pitching"]["ERA"] = float(split_line[1])
                            profile["Official_Statistics_Pitching"]["W"] = int(split_line[2])
                            profile["Official_Statistics_Pitching"]["L"] = int(split_line[3])
                            profile["Official_Statistics_Pitching"]["GP"] = int(split_line[4])
                            profile["Official_Statistics_Pitching"]["GS"] = int(split_line[5])
                            profile["Official_Statistics_Pitching"]["CG"] = int(split_line[6])
                            profile["Official_Statistics_Pitching"]["SHO"] = int(split_line[7])
                            profile["Official_Statistics_Pitching"]["CBO"] = int(split_line[8])
                            profile["Official_Statistics_Pitching"]["SV"] = int(split_line[9])
                            profile["Official_Statistics_Pitching"]["IP"] = float(split_line[10])
                            profile["Official_Statistics_Pitching"]["H"] = int(split_line[11])
                            profile["Official_Statistics_Pitching"]["R"] = int(split_line[12])
                            profile["Official_Statistics_Pitching"]["ER"] = int(split_line[13])
                            profile["Official_Statistics_Pitching"]["BB"] = int(split_line[14])
                            profile["Official_Statistics_Pitching"]["S0"] = int(split_line[15])
                            profile["Official_Statistics_Pitching"]["2B"] = int(split_line[16])
                            profile["Official_Statistics_Pitching"]["3B"] = int(split_line[17])
                            profile["Official_Statistics_Pitching"]["HR"] = int(split_line[18])
                            profile["Official_Statistics_Pitching"]["TBF"] = int(split_line[19])
                            profile["Official_Statistics_Pitching"]["B/Avg"] = float(split_line[20])
                            profile["Official_Statistics_Pitching"]["WP"] = int(split_line[21])
                            profile["Official_Statistics_Pitching"]["HBP"] = int(split_line[22])
                            profile["Official_Statistics_Pitching"]["BK"] = int(split_line[23])
                            profile["Official_Statistics_Pitching"]["SFA"] = int(split_line[24])
                            profile["Official_Statistics_Pitching"]["SHA"] = int(split_line[25])

                            profile["Official_Statistics_Exist_Pitching"] = True
                        elif "p" not in profile["position"].lower():
                            profile["Official_Statistics_Batting"]["GP"] = int(split_line[1])
                            profile["Official_Statistics_Batting"]["GS"] = int(split_line[2])
                            profile["Official_Statistics_Batting"]["AVG"] = float(split_line[3])
                            profile["Official_Statistics_Batting"]["AB"] = int(split_line[4])
                            profile["Official_Statistics_Batting"]["R"] = int(split_line[5])
                            profile["Official_Statistics_Batting"]["H"] = int(split_line[6])
                            profile["Official_Statistics_Batting"]["2B"] = int(split_line[7])
                            profile["Official_Statistics_Batting"]["3B"] = int(split_line[8])
                            profile["Official_Statistics_Batting"]["HR"] = int(split_line[9])
                            profile["Official_Statistics_Batting"]["RBI"] = int(split_line[10])
                            profile["Official_Statistics_Batting"]["TB"] = int(split_line[11])
                            profile["Official_Statistics_Batting"]["SLG"] = float(split_line[12])
                            profile["Official_Statistics_Batting"]["BB"] = int(split_line[13])
                            profile["Official_Statistics_Batting"]["HBP"] = int(split_line[14])
                            profile["Official_Statistics_Batting"]["SO"] = int(split_line[15])
                            profile["Official_Statistics_Batting"]["GDP"] = int(split_line[16])
                            profile["Official_Statistics_Batting"]["OBP"] = float(split_line[17])
                            profile["Official_Statistics_Batting"]["SF"] = int(split_line[18])
                            profile["Official_Statistics_Batting"]["SH"] = int(split_line[19])
                            profile["Official_Statistics_Batting"]["SB"] = int(split_line[20])
                            profile["Official_Statistics_Batting"]["SBA"] = int(split_line[21])
                            
                            profile["Official_Statistics_Exist_Batting"] = True

                    line = f.readline()
        except Exception as e:
            pass
    else:
        try:
            
            if not isfile(doc_name):
                return 
            
            with open(doc_name, "r") as f:

                line = f.readline()
                current_stats = "NOTHING"
                while line:
                    
                    line = line.lower()
                    
                    if "extended hitting" in line:
                        current_stats = "extended hitting"
                    elif "hitting" in line:
                        current_stats = "hitting"
                    elif "pitching" in line:
                        current_stats = "pitching"
                    elif "fielding" in line:
                        current_stats = "fielding"
                        
                    if profile["name"].lower() in line:
                        split_line = line.strip().split("\t")
                        if current_stats == "hitting":

                            #G	AB	R	H	2B	3B	HR	RBI	BB	K	SB	CS	AVG	OBP	SLG
                            profile["Official_Statistics_Batting"]["GP"] = int(split_line[4]) if split_line[4].isdigit() else 0
                            profile["Official_Statistics_Batting"]["AB"] = int(split_line[5]) if split_line[5].isdigit() else 0
                            profile["Official_Statistics_Batting"]["R"] = int(split_line[6]) if split_line[6].isdigit() else 0
                            profile["Official_Statistics_Batting"]["H"] = int(split_line[7]) if split_line[7].isdigit() else 0
                            profile["Official_Statistics_Batting"]["2B"] = int(split_line[8]) if split_line[8].isdigit() else 0
                            profile["Official_Statistics_Batting"]["3B"] = int(split_line[9]) if split_line[9].isdigit() else 0
                            profile["Official_Statistics_Batting"]["HR"] = int(split_line[10]) if split_line[10].isdigit() else 0
                            profile["Official_Statistics_Batting"]["RBI"] = int(split_line[11]) if split_line[11].isdigit() else 0
                            profile["Official_Statistics_Batting"]["BB"] = int(split_line[12]) if split_line[12].isdigit() else 0
                            profile["Official_Statistics_Batting"]["K"] = int(split_line[13]) if split_line[13].isdigit() else 0
                            profile["Official_Statistics_Batting"]["SB"] = int(split_line[14]) if split_line[14].isdigit() else 0
                            profile["Official_Statistics_Batting"]["CS"] = int(split_line[15]) if split_line[15].isdigit() else 0
                            profile["Official_Statistics_Batting"]["AVG"] = float(split_line[16]) if is_float(split_line[16]) else 0
                            profile["Official_Statistics_Batting"]["OBP"] = float(split_line[17]) if is_float(split_line[17]) else 0
                            profile["Official_Statistics_Batting"]["SLG"] = float(split_line[18]) if is_float(split_line[18]) else 0
                            
                            profile["Official_Statistics_Exist_Batting"] = True

                        elif current_stats == "extended hitting":
                            #G	HBP	SF	SH	TB	XBH	HDP	GO	FO	GO/FO	PA
                            profile["Official_Statistics_Batting"]["HBP"] = int(split_line[5]) if split_line[5].isdigit() else 0
                            profile["Official_Statistics_Batting"]["SF"] = int(split_line[6]) if split_line[6].isdigit() else 0
                            profile["Official_Statistics_Batting"]["SH"] = int(split_line[7]) if split_line[7].isdigit() else 0
                            profile["Official_Statistics_Batting"]["TB"] = int(split_line[8]) if split_line[8].isdigit() else 0
                            profile["Official_Statistics_Batting"]["XBH"] = int(split_line[9]) if split_line[9].isdigit() else 0
                            profile["Official_Statistics_Batting"]["HDP"] = int(split_line[10]) if split_line[10].isdigit() else 0
                            profile["Official_Statistics_Batting"]["GO"] = int(split_line[11]) if split_line[11].isdigit() else 0
                            profile["Official_Statistics_Batting"]["FO"] = int(split_line[12]) if split_line[12].isdigit() else 0
                            profile["Official_Statistics_Batting"]["GO/FO"] = float(split_line[13]) if is_float(split_line[13]) else 0
                            profile["Official_Statistics_Batting"]["PA"] = int(split_line[14]) if split_line[14].isdigit() else 0
                            
                            profile["Official_Statistics_Exist_Batting"] = True
                        elif current_stats == "pitching":
                            #APP	GS	W	L	SV	CG	IP	H	R	ER	BB	K	K/9	HR	ERA
                            profile["Official_Statistics_Pitching"]["APP"] = int(split_line[4]) if split_line[4].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["GS"] = int(split_line[5]) if split_line[5].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["W"] = int(split_line[6]) if split_line[6].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["L"] = int(split_line[7]) if split_line[7].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["SV"] = int(split_line[8]) if split_line[8].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["CG"] = int(split_line[9]) if split_line[9].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["IP"] = float(split_line[10]) if is_float(split_line[10]) else 0
                            profile["Official_Statistics_Pitching"]["H"] = int(split_line[11]) if split_line[11].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["R"] = int(split_line[12]) if split_line[12].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["ER"] = int(split_line[13]) if split_line[13].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["BB"] = int(split_line[14]) if split_line[14].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["K"] = int(split_line[15]) if split_line[15].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["K/9"] = float(split_line[16]) if is_float(split_line[16]) else 0
                            profile["Official_Statistics_Pitching"]["HR"] = int(split_line[17]) if split_line[17].isdigit() else 0
                            profile["Official_Statistics_Pitching"]["ERA"] = float(split_line[18]) if is_float(split_line[18]) else 0

                            profile["Official_Statistics_Exist_Pitching"] = True
                    
                    line = f.readline()
        except Exception as e:
            print(current_stats, str(e))

def get_order(line):
    """Seperates 'name number class' into ['name', 'number', 'class']"""
    order = line[:-1].split(" ")
    return order

def fill_empty_sections_profile(profile):
    """Fills empty parts of the player profile with 'Not Found' """
    points = ["name", "number", "f_name", "class", "position", "b_t", "height", "weight"]
    for point in points:
        if not profile[point]:
            profile[point] = "  "
    return profile


def get_play_by_play_data(team_name, year):
    """Gets play by play data from txt document """
    doc_name = "data/" + team_name + "/" + year + "/" +  team_name + "_batting_" + year + ".txt"
    with open(doc_name, "r") as f:
        lines = f.readlines()
        '''tmp = f.readlines()
        lines = []
        check = True
        team_name_short = team_name.split("_")[0].lower()
        team_name_abreviated =  " " + "".join(x[0] for x in team_name.split("_")).lower() + " "
        team_name_longest = max(team_name.split(" "), key=len)
        if len(team_name_short) > 4:
            team_name_short = team_name_short[0:3]
        for line in tmp:
            line = line.lower().replace(",", "")
            if check and re.search("(top/bottom) of [0-9]", line):
                if not re.search(team_name_short, line) and not re.search(team_name_abreviated, line) and not re.search(team_name_longest, line):
                    check = False
            elif not check and re.search("(top/bottom) of [0-9]", line):
                if re.search(team_name_short, line) or re.search(team_name_abreviated, line) or re.search(team_name_longest, line):
                    check = True
            elif check:
                if ";" in line:
                    for l in line.split(";"):
                        lines.append(l)
                else:
                    lines.append(line)'''
    return lines

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
