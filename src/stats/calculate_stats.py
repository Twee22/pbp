from src.config_files.config import fip_constant

def calculate_stats(profile):
    """Calculates AVG, OBP, SLG, OPS, IFH%, BABIP"""
    if profile["AB"]:
        profile["AVG"] = profile["Hits"] / profile["AB"]
    if (profile["AB"] + profile["BB"] + profile["HBP"] + profile["SF"]):
        profile["OBP"] = (profile["Hits"] + profile["BB"] + profile["HBP"]) / (profile["AB"] + 
            profile["BB"] + profile["HBP"] + profile["SF"])
    if profile["AB"]:
        profile["SLG"] = (profile["1B"] + 2 * profile["2B"] + 3 * profile["3B"] + 
            4 * profile["HR"]) / profile["AB"]
    profile["OPS"] = profile["OBP"] + profile["SLG"]
    if profile["IFH"] + profile["IFHO"]:
        profile["IFHP"] = profile["IFH"] * 100 / (profile["IFH"] + profile["IFHO"])
    total = (profile["Location"]["1"] + profile["Location"]["2"] + profile["Location"]["3"] +
            profile["Location"]["4"] + profile["Location"]["5"] + profile["Location"]["6"] +
            profile["Location"]["7"] + profile["Location"]["8"] + profile["Location"]["9"] +
            profile["Location"]["78"] + profile["Location"]["89"])
    if total:
        profile["BABIP"] = profile["Hits"] / total
        if profile["BABIP"] > 1:
            profile["BABIP"] = 1
    if profile["Outs"]:
        profile["Innings"] = profile["Outs"] // 3 + ((profile["Outs"] % 3) * 0.1)
        profile["K/9"] = profile["K"] / profile["Outs"]
        profile["K%"] = profile["K"] / profile["PA"] * 100
        profile["BB/9"] = profile["BB"] / profile["Outs"]
        profile["BB%"] = profile["BB"] / profile["PA"] * 100
        profile["FIP"] = ((13*profile["HR"]) + (3*(profile["BB"]+profile["HBP"])) - (2*profile["K"])) / (profile["Outs"]/3) + fip_constant

    return profile