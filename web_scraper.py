import requests 
import re
from bs4 import BeautifulSoup

class Error(Exception):
    pass

class YearDoesNotExistError(Error):
    pass

class SchoolDoesNotExistError(Error):
    pass

schools = [
        {"name": "Ferrum College",
        "school_name": "ferrum_college",
        "year": "2020",
        "url_part_1": "https://www.ferrumpanthers.com/",
        "url_part_2": "sports/bsb/2019-20/schedule",
        "initial_scrape_type": "aspx",
        "final_scrape_type": "stats/tabs"
        },
        {"name": "Antelope Valley",
        "school_name": "antelope_valley",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=19071",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Aquinas",
        "school_name": "aquinas",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1615",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Arizona Christian",
        "school_name": "arizona_christian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=17740",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Asbury",
        "school_name": "asbury",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=8291",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Ave Maria",
        "school_name": "ave_maria",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=15387",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Avila",
        "school_name": "avila",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1617&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Avila",
        "school_name": "avila",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1617",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Avila",
        "school_name": "avila",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1617&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bacone",
        "school_name": "bacone",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1619",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Baker",
        "school_name": "baker",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1620",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bellevue",
        "school_name": "bellevue",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1623",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Benedictine",
        "school_name": "benedictine",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1624",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Benedictine Mesa",
        "school_name": "benedictine_mesa",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20728",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bethany",
        "school_name": "bethany",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1628",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bethel",
        "school_name": "bethel",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1629",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bethel Tenn",
        "school_name": "bethel_tenn",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1828",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Blue Mountain",
        "school_name": "blue_mountain",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=17743",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bluefield",
        "school_name": "bluefield",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1632",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Brescia",
        "school_name": "brescia",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1633",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Brewton Parker",
        "school_name": "brewton_parker",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1635",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Briar Cliff",
        "school_name": "briar_cliff",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1637",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "British Columbia",
        "school_name": "british_columbia",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1799",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bryan",
        "school_name": "bryan",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1636",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Calumet St Joseph",
        "school_name": "calumet_st_joseph",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1640",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Campbellsville",
        "school_name": "campbellsville",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1641",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Central Baptist",
        "school_name": "central_baptist",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=15388",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Central Christian",
        "school_name": "central_christian",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1644&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Central Christian",
        "school_name": "central_christian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1644",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Central Christian",
        "school_name": "central_christian",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1644&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Central Methodist",
        "school_name": "central_methodist",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1645",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Clarke",
        "school_name": "clarke",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=8289",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Cleary",
        "school_name": "cleary",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21009",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "College of Idaho",
        "school_name": "college_of_idaho",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1612",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "College of the Ozarks",
        "school_name": "college_of_the_ozarks",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1646",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Columbia",
        "school_name": "columbia",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20727",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Columbia",
        "school_name": "columbia",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=20727",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Columbia International",
        "school_name": "columbia_international",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21285",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Concordia",
        "school_name": "concordia",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1651",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Concordia Neb",
        "school_name": "concordia_neb",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1652",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Cornerstone",
        "school_name": "cornerstone",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=18999",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Crowleys Ridge",
        "school_name": "crowleys_ridge",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20736",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Culver Stockton",
        "school_name": "culver_stockton",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1655",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Cumberland",
        "school_name": "cumberland",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1657",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Cumberlands",
        "school_name": "cumberlands",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1656",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Dakota State",
        "school_name": "dakota_state",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1658",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Dakota Wesleyan",
        "school_name": "dakota_wesleyan",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1659",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Doane",
        "school_name": "doane",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1662",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Dordt",
        "school_name": "dordt",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1663",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Edward Waters",
        "school_name": "edward_waters",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1665",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Evangel",
        "school_name": "evangel",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1668",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Faulkner",
        "school_name": "faulkner",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1669",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Fisher",
        "school_name": "fisher",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1672",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Florida Memorial",
        "school_name": "florida_memorial",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1671",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Florida National",
        "school_name": "florida_national",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21178",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Freed Hardeman",
        "school_name": "freed_hardeman",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1673",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Friends",
        "school_name": "friends",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1674",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Georgetown",
        "school_name": "georgetown",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1676",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Georgia Gwinnett",
        "school_name": "georgia_gwinnett",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=18986",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Goshen",
        "school_name": "goshen",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1678",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Grace",
        "school_name": "grace",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1679",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Graceland",
        "school_name": "graceland",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1680",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Grand View",
        "school_name": "grand_view",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1682",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Hannibal LaGrange",
        "school_name": "hannibal_lagrange",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1683",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Harris Stowe State",
        "school_name": "harris_stowe_state",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1684",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Hastings",
        "school_name": "hastings",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1685",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Hope International",
        "school_name": "hope_international",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20599",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Houston Victoria",
        "school_name": "houston_victoria",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=8288",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Huntington",
        "school_name": "huntington",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1688",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Huston Tillotson",
        "school_name": "huston_tillotson",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1691",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Indiana Tech",
        "school_name": "indiana_tech",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1692",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Indiana Wesleyan",
        "school_name": "indiana_wesleyan",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1694",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "IU Kokomo",
        "school_name": "iu_kokomo",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21006",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "IU South Bend",
        "school_name": "iu_south_bend",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20598",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "IU Southeast",
        "school_name": "iu_southeast",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1696",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Jamestown",
        "school_name": "jamestown",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1699",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Jarvis Christian",
        "school_name": "jarvis_christian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=18985",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Judson",
        "school_name": "judson",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1701",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Kansas Wesleyan",
        "school_name": "kansas_wesleyan",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2019&team=1702",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Kansas Wesleyan",
        "school_name": "kansas_wesleyan",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1702",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Kansas Wesleyan",
        "school_name": "kansas_wesleyan",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1702&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Keiser University",
        "school_name": "keiser_university",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1740",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Kentucky Christian",
        "school_name": "kentucky_christian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21010",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "La Sierra",
        "school_name": "la_sierra",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=15602",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lawrence Tech",
        "school_name": "lawrence_tech",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20729",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lewis Clark State",
        "school_name": "lewis_clark_state",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1707",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lincoln",
        "school_name": "lincoln",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21177",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lincoln Christian",
        "school_name": "lincoln_christian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=19201",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lindsey Wilson",
        "school_name": "lindsey_wilson",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1711",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lourdes",
        "school_name": "lourdes",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=18711",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Loyola",
        "school_name": "loyola",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1709",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "LSU Alexandria",
        "school_name": "lsu_alexandria",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=8293",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "LSU Shreveport",
        "school_name": "lsu_shreveport",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=8293",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Lyon",
        "school_name": "lyon",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1713",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Madonna",
        "school_name": "madonna",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1715",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Marian",
        "school_name": "marian",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1717",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Martin Methodist",
        "school_name": "martin_methodist",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1719",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Marymount California",
        "school_name": "marymount_california",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=20601",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mayville State",
        "school_name": "mayville_state",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1720",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "McPherson",
        "school_name": "mcpherson",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=17742&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "McPherson",
        "school_name": "mcpherson",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=17742",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "McPherson",
        "school_name": "mcpherson",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=17742",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Menlo",
        "school_name": "menlo",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=9101",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Michigan Dearborn",
        "school_name": "michigan_dearborn",
        "year": "2020",
        "url": "https://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21008",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Peru State College",
        "school_name": "peru_state_college",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1755",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Crowleys Ridge",
        "school_name": "crowleys_ridge",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2019&team=20736",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Truett McConnell",
        "school_name": "truett_mcconnell",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=15389&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Truett McConnell",
        "school_name": "truett_mcconnell",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=15389&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Nazarene",
        "school_name": "mid_america_nazarene",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=1723",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Nazarene",
        "school_name": "mid_america_nazarene",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1723",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas AM Texarkana",
        "school_name": "texas_am_texarkana",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=20603&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas AM Texarkana",
        "school_name": "texas_am_texarkana",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=20603&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas AM Texarkana",
        "school_name": "texas_am_texarkana",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=20603&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Jarvis Christian",
        "school_name": "jarvis_christian",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=18985&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Jarvis Christian",
        "school_name": "jarvis_christian",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=18985&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Jarvis Christian",
        "school_name": "jarvis_christian",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=18985&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "St Mary",
        "school_name": "st_mary",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1765",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "St Mary",
        "school_name": "st_mary",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1765&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "St Mary",
        "school_name": "st_mary",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1765&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "St Mary",
        "school_name": "st_mary",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1765&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "St Mary",
        "school_name": "st_mary",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1765&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Christian",
        "school_name": "mid_america_christian",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1856",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Christian",
        "school_name": "mid_america_christian",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1856&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Christian",
        "school_name": "mid_america_christian",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1856&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Mid America Christian",
        "school_name": "mid_america_christian",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1856&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Panhandle State",
        "school_name": "oklahoma_panhandle_state",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2020&team=21007",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Panhandle State",
        "school_name": "oklahoma_panhandle_state",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=21007",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bethany",
        "school_name": "bethany",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1628&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Bethany",
        "school_name": "bethany",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1628&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Science And Arts",
        "school_name": "science_and_arts",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1798&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Science And Arts",
        "school_name": "science_and_arts",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1798&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Science And Arts",
        "school_name": "science_and_arts",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1798&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Science And Arts",
        "school_name": "science_and_arts",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1798",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma City",
        "school_name": "oklahoma_city",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1748&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma City",
        "school_name": "oklahoma_city",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1748&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma City",
        "school_name": "oklahoma_city",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1748&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma City",
        "school_name": "oklahoma_city",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1748&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Wesleyan",
        "school_name": "oklahoma_wesleyan",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1749",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Wesleyan",
        "school_name": "oklahoma_wesleyan",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1749&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Wesleyan",
        "school_name": "oklahoma_wesleyan",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1749&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Oklahoma Wesleyan",
        "school_name": "oklahoma_wesleyan",
        "year": "2018",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1749&sea=NAIMBA_2018",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwest",
        "school_name": "southwest",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1648&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwest",
        "school_name": "southwest",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1648&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern",
        "school_name": "southwestern",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2019&team=21005",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern",
        "school_name": "southwestern",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=21005&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern",
        "school_name": "southwestern",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=21005&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "SAGU",
        "school_name": "sagu",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1778&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "SAGU",
        "school_name": "sagu",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1778&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "SAGU",
        "school_name": "sagu",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1778&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "York",
        "school_name": "york",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2019&team=1827",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "York",
        "school_name": "york",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1827&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "York",
        "school_name": "york",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1827&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Sterling",
        "school_name": "sterling",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1782",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Sterling",
        "school_name": "sterling",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1782&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Sterling",
        "school_name": "sterling",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1782&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Tabor",
        "school_name": "tabor",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1783&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Tabor",
        "school_name": "tabor",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1783&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Tabor",
        "school_name": "tabor",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1783&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Wayland Baptist",
        "school_name": "wayland_baptist",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=1817",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern Christian",
        "school_name": "southwestern_christian",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=19070&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern Christian",
        "school_name": "southwestern_christian",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=19070&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southwestern Christian",
        "school_name": "southwestern_christian",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=19070&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Ottawa",
        "school_name": "ottawa",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1752&sea=NAIMBA_2019",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Ottawa",
        "school_name": "ottawa",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1752&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Ottawa",
        "school_name": "ottawa",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1752&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas Wesleyan",
        "school_name": "texas_wesleyan",
        "year": "2019",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2019&team=1787",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas Wesleyan",
        "school_name": "texas_wesleyan",
        "year": "2020",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1787&sea=NAIMBA_2020",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Texas Wesleyan",
        "school_name": "texas_wesleyan",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&team=1787&sea=NAIMBA_2021",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        },
        {"name": "Southeastern",
        "school_name": "southeastern",
        "year": "2021",
        "url": "http://www.dakstats.com/WebSync/Pages/Team/TeamSchedule.aspx?association=10&sg=MBA&sea=NAIMBA_2021&team=9105",
        "initial_scrape_type": "dakstats",
        "final_scrape_type": "dakstats"
        }
        ]

def get_user_input():
    school_name = input("Which school do you want to get data from?\n")
    year = input("Which year do you want to get information for?\n")

    user_input = {}
    user_input["school_name"] = school_name
    user_input["year"] = year

    return user_input

def get_school(user_input):
    check_if_school_exists = False
    for school in schools:
        if school["name"].lower() == user_input["school_name"].lower():
            check_if_school_exists = True
            if school["year"] == user_input["year"]:
                return school
    if check_if_school_exists:
        raise YearDoesNotExistError("This year does not exist for this school. Please add it to the database")
    else:
        raise SchoolDoesNotExistError("This School does not exist in the database. Please add it")

def get_pages_to_scrape_aspx(school):
    URL = school["url_part_1"] + school["url_part_2"]

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(URL, headers=headers)
    text = r.text

    links = re.findall(r'href=".*\.xml"', text)

    return links

def get_pages_to_scrape_dakstats(school):
    URL = school["url"]

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(URL, headers=headers, verify=False)
    text = r.text

    links = re.findall(r'ShowWebcastPopup[^\s]+;', text)

    return links

def scrape_pages_stats_tabs(school, pages_to_scrape):
    
    print("Scraping data for", school["name"])

    file_destination = "data/" + school["school_name"] + "/" + school["year"] + "/" + school["school_name"] + "_batting_" + school["year"] + ".txt"
    open(file_destination, "w").close

    for page in pages_to_scrape:
        start = page.find("\"") + 1
        end = page.find("\"", start+1)
        link = school["url_part_1"][:-1] + page[start:end]
        
        print("Processing:", link)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(link, headers=headers)

        soup = BeautifulSoup(r.content, 'html.parser')

        results = soup.find_all("div", attrs={'data-module':"stats/tabs", "data-type":"secondary"}) 

        play_by_play_text = ""

        for res in results:
            play_by_play_text += res.text.strip()

        play_by_play_text = re.sub(r"\s+\n\s+", "\n", play_by_play_text)
        play_by_play_text = re.sub(r"[ \t]+", " ", play_by_play_text)
        play_by_play_text = re.sub(r"\nTop of", " Top of", play_by_play_text)
        play_by_play_text = re.sub(r"\nBottom of", " Bottom of", play_by_play_text)

        with open(file_destination, "a") as file:
            file.write(play_by_play_text)

    print("Complete")

    return True

def scrape_pages_dakstats(school, pages_to_scrape):

    print("Scraping data for", school["name"])

    file_destination = "data/" + school["school_name"] + "/" + school["year"] + "/" + school["school_name"] + "_batting_" + school["year"] + ".txt"
    open(file_destination, "w").close

    for page in pages_to_scrape:

        seperated_page = page.split(",")

        seasonID = seperated_page[3][1:-3]
        sg = seperated_page[1][1:-1]
        compID = seperated_page[2][1:-1]

        print("Processing: seasonID = {} sg = {} compID = {}".format(seasonID, sg, compID))

        link = "https://www.dakstats.com/WebSync/Pages/GameBook/GameBookData.aspx?sg={}&compID={}&sea={}".format(sg, compID, seasonID)

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(link, headers=headers, verify=False)

        soup = BeautifulSoup(r.content, 'html.parser')

        results = soup.find_all("td")                 

        play_by_play_text = ""
        home_or_away = "NOT_DEFINED"
        team_name_short = school["name"].split("_")[0].lower()
        team_name_abreviated =  " " + "".join(x[0] for x in school["name"].split("_")).lower() + " "
        team_name_longest = max(school["name"].split(" "), key=len)
        if len(team_name_short) > 4:
            team_name_short = team_name_short[0:3]

        for res in results:
            text = res.text
            if re.search("Starting Lineup", text):
                if home_or_away == "NOT_DEFINED":
                    if school["name"] in text or team_name_short in text or team_name_abreviated in text or team_name_longest in text:
                        home_or_away = "AWAY"
                    else:
                        home_or_away = "HOME"
                
                    play_by_play_text += "GAME_START_POINT\n"

                player_name = text.split(',')[-1]
                player_name = player_name.strip()[:-1]   

                if school["name"] in text:
                    play_by_play_text += school["name"] + " Starting Pitcher: " + player_name + "\n"
                else: 
                    play_by_play_text += "OPPOSITION Starting Pitcher: " + player_name + "\n"

            if re.search("Top|Bottom", text):
                if home_or_away == "HOME":  
                    if re.search("Bottom of", text):
                        text = text.replace("Bottom of", school["name"] + " Bottom of", 1)
                    elif re.search("Top of", text):
                        text = text.replace("Top of", "OPPOSITION Top of", 1)
                elif home_or_away == "AWAY":
                    if re.search("Top of", text):
                        text = text.replace("Top of", school["name"] + " Top of", 1)
                    elif re.search("Bottom of", text):
                        text = text.replace("Bottom of", "OPPOSITION Bottom of", 1)
                else:
                    pass

                text = text.replace("- ", "\n", 1)
                text = text.replace(". ", "\n")

                play_by_play_text += text
                play_by_play_text += "\n"

        play_by_play_text +=  "GAME_END_POINT\n"
            
        with open(file_destination, "a") as file:
            file.write(play_by_play_text)

    print("Complete")

    return True

def scrape():
    user_input = get_user_input()
    school = get_school(user_input)

    if school["initial_scrape_type"] == "aspx":
        pages_to_scrape = get_pages_to_scrape_aspx(school)
    elif school["initial_scrape_type"] == "dakstats":
        pages_to_scrape = get_pages_to_scrape_dakstats(school)
    else:
        print("This school has not been calibrated for the initial scraping process")
        return False

    if school["final_scrape_type"] == "stats/tabs":
        check = scrape_pages_stats_tabs(school, pages_to_scrape)
    elif school["final_scrape_type"] == "dakstats":
        check = scrape_pages_dakstats(school, pages_to_scrape)
    else:
        print("This school has not been calibrated for the final scraping process")
        return False

    if not check:
        print("An error occured with outputting the data")

if __name__ == "__main__":
    scrape()