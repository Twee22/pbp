from src.config_files.config import disclaimer_1, disclaimer_2

def output_profile_to_text(profiles, team_name, year_for_roster, year_for_report, how_many_pa_to_appear):
    doc_name = "data/" + team_name + "/" + year_for_roster + "/" + team_name + "_batting_" + year_for_report + "_report.txt"
    with open(doc_name, "w") as f:
        for profile in profiles:
            if profile["PA"] >= how_many_pa_to_appear:
                f.write("#{} {} {}\n".format(profile["number"], profile["f_name"], profile["name"]))
                f.write("Year: {}\n".format(profile["year"]))
                f.write("CL: {} POS: {} B/T: {} HT: {} WT: {}\n".format(profile["class"], profile["position"], profile["b_t"], profile["height"], profile["weight"]))
                f.write("AVG: {:.3f} OBP: {:.3f} SLG: {:.3f} OPS: {:.3f} BABIP: {:.3f}\n".format(profile["AVG"], profile["OBP"], profile["SLG"], profile["OPS"], profile["BABIP"]))
                f.write("PA: {} AB: {} Hits: {} Walks: {} HBP: {}\n".format(profile["PA"], profile["AB"], profile["Hits"], profile["BB"], profile["HBP"]))
                f.write("XBH: {} 1B: {} 2B: {} 3B: {} HR: {}\n".format(profile["XBH"], profile["1B"], profile["2B"], profile["3B"], profile["HR"]))
                f.write("Strikeouts: {} Looking: {} Swinging: {}\n".format(profile["K"], profile["KL"], profile["KS"]))
                f.write("ROE: {} SF: {} FC:{}\n".format(profile["ROE"], profile["SF"], profile["FC"]))
                if profile["IFH"] + profile["IFHO"]:
                    f.write("IFH: {} IFHO: {} IFHP: {:.3f}%\n".format(profile["IFH"], profile["IFHO"], profile["IFHP"]))
                else:
                    f.write("IFH: {} IFHO: {}\n".format(profile["IFH"], profile["IFHO"]))
                if profile["SB"] + profile["CS"]:
                    f.write("Steal Attempts: {} SB: {} CS: {} Steal Percentage: {:.2f}%\n".format(profile["SB"]+profile["CS"], profile["SB"], profile["CS"],
                        profile["SB"] * 100/(profile["SB"]+profile["CS"])))
                    f.write("SB2: {} SB3: {} SB4: {}\n".format(profile["SB2"], profile["SB3"], profile["SB4"]))
                f.write("Bunts: Safe: {} Errors: {} Outs:{} Sacrifice: {}\n".format(profile["Bunt"]["Safe"], 
                    profile["Bunt"]["Error"], profile["Bunt"]["Out"], profile["Bunt"]["SAC"]))
                f.write("Location: 1:{} 2:{} 3:{} 4:{} 5:{} 6:{} 7:{} 8:{} 9:{} 78:{} 89:{}\n".format(profile["Location"]["1"], 
                    profile["Location"]["2"], profile["Location"]["3"], profile["Location"]["4"],
                    profile["Location"]["5"], profile["Location"]["6"], profile["Location"]["7"], 
                    profile["Location"]["8"], profile["Location"]["9"], profile["Location"]["78"],
                    profile["Location"]["89"]))
                total = (profile["Location"]["1"] + profile["Location"]["2"] + profile["Location"]["3"] + 
                        profile["Location"]["4"] + profile["Location"]["5"] + profile["Location"]["6"] + 
                        profile["Location"]["7"] + profile["Location"]["8"] + profile["Location"]["9"] +
                        profile["Location"]["78"] + profile["Location"]["89"])
                if total:
                    f.write("Location Percentages: 1:{:.2f}% 2:{:.2f}% 3:{:.2f}% 4:{:.2f}% 5:{:.2f}% 6:{:.2f}% 7:{:.2f}% 8:{:.2f}% 9:{:.2f}% 78:{:.2f}% 89:{:.2f}%\n".format(
                        profile["Location"]["1"]/total*100, profile["Location"]["2"]/total*100,
                        profile["Location"]["3"]/total*100, profile["Location"]["4"]/total*100, 
                        profile["Location"]["5"]/total*100, profile["Location"]["6"]/total*100,
                        profile["Location"]["7"]/total*100, profile["Location"]["8"]/total*100, 
                        profile["Location"]["9"]/total*100, profile["Location"]["78"]/total*100,
                        profile["Location"]["89"]/total*100))
                f.write("Hit Type: GB: {} LD: {} FB: {} PF:{} Bunt: {}\n".format(profile["Type"]["GB"], 
                        profile["Type"]["LD"], profile["Type"]["FB"], profile["Type"]["PF"], profile["Type"]["Bunt"]))
                total = profile["Type"]["GB"] + profile["Type"]["LD"] + profile["Type"]["FB"] + profile["Type"]["PF"] + profile["Type"]["Bunt"]
                if total:
                    f.write("Type percentages: GB: {:.2f}% LD: {:.2f}% FB: {:.2f}% PF: {:.2f}% Bunt:{:.2f}%\n".format(profile["Type"]["GB"]/total*100, profile["Type"]["LD"]/total*100, 
                        profile["Type"]["FB"]/total*100, profile["Type"]["PF"]/total*100, profile["Type"]["Bunt"]/total*100))
                f.write("\n\n\n")

        f.write("{}\n".format(disclaimer_1))
        f.write("{}\n".format(disclaimer_2))

    return True