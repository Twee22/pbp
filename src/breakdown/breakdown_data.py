import re

def breakdown_data(profile, point):
    """Get data extracted from one line of play_by_play"""
    # HITS
    # single
    extra_base_hit_checker = False
    if re.search("singled", point):
        profile["AB"] += 1
        profile["PA"] += 1
        profile["Hits"] += 1
        profile["1B"] += 1
    # double
    elif re.search("doubled", point):
        profile["AB"] += 1
        profile["PA"] += 1
        profile["Hits"] += 1
        profile["XBH"] += 1
        profile["2B"] += 1
        extra_base_hit_checker = True
    # triple
    elif re.search("tripled", point):
        profile["AB"] += 1
        profile["PA"] += 1
        profile["Hits"] += 1
        profile["XBH"] += 1
        profile["3B"] += 1
        extra_base_hit_checker = True
    # home run
    elif re.search("homered|hit a home run|hit a homer", point):
        profile["AB"] += 1
        profile["PA"] += 1
        profile["Hits"] += 1
        profile["XBH"] += 1
        profile["HR"] += 1
        extra_base_hit_checker = True
    # WALKS
    elif re.search("reached on a walk|walked", point):
        profile["PA"] += 1
        profile["BB"] += 1
    # HIT BY PITCH
    elif re.search("hit by pitch|hbp", point):
        profile["PA"] += 1
        profile["HBP"] += 1
    # OUTS
    # Double play
    elif re.search("double play", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Outs"] += 2
        profile["DP"] += 1
        if re.search("ground", point):
            profile["Type"]["GB"] += 1
            profile["IFHO"] += 1
            profile["IFH"] -= 1
    # Triple Play
    elif re.search("triple play", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Outs"] += 3
        profile["TP"] += 1
        if re.search("ground", point):
            profile["Type"]["GB"] += 1
            profile["IFHO"] += 1
            profile["IFH"] -= 1
    # Strike outs
    elif re.search("struck out looking", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["K"] += 1
        profile["KL"] += 1
        profile["Outs"] += 1
    elif re.search("struck out swinging", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["K"] += 1
        profile["KS"] += 1
        profile["Outs"] += 1
    # Ground Outs
    elif re.search("grounded out", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Type"]["GB"] += 1
        profile["IFHO"] += 1
        profile["IFH"] -= 1
        profile["Outs"] += 1
    # Line Outs
    elif re.search("lined", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Type"]["LD"] += 1
        profile["Outs"] += 1
    # Fly outs
    elif re.search("flied out|flew out", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Type"]["FB"] += 1
        profile["Outs"] += 1
    # Pop Outs
    elif re.search("popped out", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["Type"]["PF"] += 1
        profile["Outs"] += 1
    #Errors
    elif re.search("e[1-9]", point) or (re.search("error", point) and not re.search("previous entered error", point)):
        if re.search("reached", point):
            profile["PA"] += 1
            profile["AB"] += 1
            profile["ROE"] += 1
            if re.search("bobble", point) or re.search("misplayed grounder", point):
                profile["Type"]["GB"] += 1
            elif re.search("wild throw", point):
                pass
            elif re.search("missed catch", point):
                pass
            elif re.search("dropped fly", point):
                profile["Type"]["FB"] += 1
            elif re.search("dropped popup", point):
                profile["Type"]["PF"] += 1
    #SacFly
    elif re.search("sacrifice fly", point):
        profile["PA"] += 1
        profile["SF"] += 1
        profile["Type"]["FB"] += 1
        profile["Outs"] += 1
    #Fielder's Choice
    elif re.search("fielder's choice", point) and not re.search("bunt", point):
        profile["PA"] += 1
        profile["AB"] += 1
        profile["FC"] += 1
        profile["Type"]["GB"] += 1
        profile["Outs"] += 1
    #Bunts
    elif re.search("bunt", point):
        profile["PA"] += 1
        profile["Type"]["Bunt"] += 1
        profile["Outs"] += 1
        if re.search("sacrifice bunt", point):
            profile["Bunt"]["SAC"] += 1
        elif re.search("out at first", point):
            profile["AB"] += 1
            profile["Bunt"]["Out"] += 1
        elif re.search(r"\(e[1-9]\)", point):
            profile["ROE"] += 1
            profile["Bunt"]["Error"] += 1
            profile["IFHO"] += 1
        elif re.search("reached", point):
            profile["AB"] += 1
            profile["Bunt"]["Safe"] += 1
            profile["Hits"] += 1
            profile["1B"] += 1
            profile["IFH"] += 1
    #Stolen Base
    elif re.search("stole", point):
        profile["SB"] += 1
        if re.search("stole second", point):
            profile["SB2"] += 1
        elif re.search("stole third", point):
            profile["SB3"] += 1
        elif re.search("stole home", point):
            profile["SB4"] += 1
    elif re.search("caught stealing", point):
        profile["CS"] += 1

    profile = get_location(profile, point, extra_base_check = extra_base_hit_checker)

    return profile

def get_location(profile, point, extra_base_check = False):
    """Gets location from line"""

    # This checks for substitutions
    if re.search("to", point) and re.search("for", point):
        return profile

    # Removes "Advanced to base"
    point = re.sub("advanced to", "", point)

    if re.search("to pitcher", point) or re.search("by p ", point):
        profile["Location"]["1"] += 1
        if extra_base_check:
            profile["XBHLocation"]["1"] += 1
    elif re.search("to catcher", point) or re.search("by c ", point):
        profile["Location"]["2"] += 1
        if extra_base_check:
            profile["XBHLocation"]["2"] += 1
    elif re.search("to 1b|to first", point) or re.search("by 1b|by first", point):
        profile["Location"]["3"] += 1
        profile["IFH"] += 1
        if extra_base_check:
            profile["XBHLocation"]["3"] += 1
    elif re.search("to 2b|to second", point) or re.search("by 2b|by second", point):
        profile["Location"]["4"] += 1
        profile["IFH"] += 1
        if extra_base_check:
            profile["XBHLocation"]["4"] += 1
    elif re.search("to 3b|to third|by 3b|by third", point):
        profile["Location"]["5"] += 1
        profile["IFH"] += 1
        if extra_base_check:
            profile["XBHLocation"]["5"] += 1
    elif re.search("to short|to ss", point) or re.search("by short|by ss", point):
        profile["Location"]["6"] += 1
        profile["IFH"] += 1
        if extra_base_check:
            profile["XBHLocation"]["6"] += 1
    elif re.search("to lf|to left |to deep left|to shallow left|down the LF line|over the left field fence|by lf|by left field|through the left side", point):
        profile["Location"]["7"] += 1
        if extra_base_check:
            profile["XBHLocation"]["7"] += 1
    elif re.search("to cf|to center |to deep center|to shallow center|over the center field fence|by cf|by center field|up the middle", point):
        profile["Location"]["8"] += 1
        if extra_base_check:
            profile["XBHLocation"]["8"] += 1
    elif re.search("to rf|to right |to deep right|to shallow right|down the RF line|over the right field fence|by rf|by right field|through the right side", point):
        profile["Location"]["9"] += 1
        if extra_base_check:
            profile["XBHLocation"]["9"] += 1
    elif re.search("to right center|to deep right-center|to shallow right-center", point):
        profile["Location"]["89"] += 1
        if extra_base_check:
            profile["XBHLocation"]["89"] += 1
    elif re.search("to left center|to deep left-center|to shallow left_center", point):
        profile["Location"]["78"] += 1
        if extra_base_check:
            profile["XBHLocation"]["89"] += 1
    else:
        index = point.find('(')
        if index != -1 and index != len(point) - 1:
            location = point[index + 1]
            if location.isnumeric() and location != "0":
                profile["Location"][location] += 1
                if location in ["3", "4", "5", "6"]:
                    profile["IFH"] += 1
    return profile