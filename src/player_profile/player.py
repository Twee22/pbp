def create_profile():
    """Creates a dictionary that is then used to monitor player stats"""
    profile = {"name": "",
                "number": 0, "f_name": 0,
                "class": 0, "position": 0, "b_t": 0,
                "height": 0, "weight": 0, "year": 0,
                "AVG": 0, "OBP": 0, "SLG": 0, "OPS": 0, "BABIP": 0,
                "AB": 0, "PA": 0,
                "Hits": 0, "XBH": 0, "1B": 0, "2B": 0, "3B": 0, "HR": 0,
                "BB": 0, "HBP": 0, 
                "K": 0, "KL": 0, "KS": 0, 
                "ROE": 0, "SF": 0, "FC": 0, "DP": 0, "TP": 0,
                "IFH": 0, "IFHO": 0, "IFHP": 0,
                "SB": 0, "CS": 0, "SB2": 0, "SB3": 0, "SB4": 0,
                "Bunt": {"Safe": 0, "Error": 0, "Out": 0, "SAC": 0},
                "Location": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, 
                        "8": 0, "9": 0, "78": 0, "89": 0},
                "XBHLocation": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, 
                        "8": 0, "9": 0, "78": 0, "89": 0},
                "Type": {"GB": 0, "LD": 0, "FB": 0, "PF": 0, "Bunt": 0},
                "Outs": 0,
                "Innings": 0, "K/9": 0, "K%": 0, "BB/9": 0, "BB%":0, 
                "FIP": 0,
                "Official_Statistics_Pitching": {"ERA": 0, "W": 0, "L": 0, "GP": 0, "GS": 0, "CG": 0, "SHO": 0,
                        "CBO": 0, "SV": 0, "IP": 0, "H": 0, "R": 0, "ER": 0, "BB": 0, "SO": 0, "2B": 0, 
                        "3B": 0, "HR": 0, "TBF": 0, "B/Avg": 0, "WP": 0, "HBP": 0, "BK": 0, "SFA": 0, "SHA": 0},
                "Official_Statistics_Batting": {"GP": 0, "GS": 0, "AVG": 0, "AB": 0, "R": 0, "H": 0, "2B": 0, "3B": 0, 
                        "HR": 0, "RBI": 0, "TB": 0, "SLG%": 0, "BB": 0, "HBP": 0, "SO": 0, "GDP": 0, 
                        "OB%": 0, "SF": 0, "SH": 0, "SB": 0, "SBA": 0},
                "Official_Statistics_Exist_Batting": False, "Official_Statistics_Exist_Pitching": False
    }
    return profile

def check_data_point(data_point):
        """Checks that a string represents an item in the player profile"""
        # Currently only checks for information gotten from the roster
        allowed_points = ["name", "number", "f_name", "class", "position", "b_t", "height", "weight"]
        if data_point in allowed_points:
                return True     
        else:
                return False