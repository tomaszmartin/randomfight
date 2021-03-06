import datetime as dt

from bs4 import BeautifulSoup
import pandas as pd

from app.parsers import sherdog


def test_events_list_parsing(sherdog_events_list):
    page_content, page_url = sherdog_events_list
    links = sherdog.extract_events_links(page_content, page_url)
    actuall = [
        "http://www.sherdog.com/events/247-FC-Brawl-In-The-Burgh-4-86700",
        "http://www.sherdog.com/events/247-FC-Brawl-in-the-Burgh-5-87932",
        "http://www.sherdog.com/events/ACA-114-Omielanczuk-vs-Johnson-87933",
        "http://www.sherdog.com/events/ACA-YE-14-ACA-Young-Eagles-87882",
        "http://www.sherdog.com/events/ADW-UAE-Warriors-14-87837",
        "http://www.sherdog.com/events/AFC-2-Arena-Fight-Championship-2-87968",
        "http://www.sherdog.com/events/AFC-3-Guerrero-vs-Figuera-87998",
        "http://www.sherdog.com/events/AFC-Almighty-Fighting-Championship-18-87939",
        "http://www.sherdog.com/events/AFC-Ascendancy-Fighting-Championship-22-87917",
        "http://www.sherdog.com/events/AFL-1-Quito-88058",
        "http://www.sherdog.com/events/AKA-Rite-Of-Passage-12-87881",
        "http://www.sherdog.com/events/ALMMA-187-Bull-Terror-Challenge-88077",
        "http://www.sherdog.com/events/AUFC-Arabic-Ultimate-Fighting-Championship-29-88075",
        "http://www.sherdog.com/events/Adventure-Fighters-Tournament-AFT-24-88107",
        "http://www.sherdog.com/events/Adventure-Fighters-Tournament-AFT-25-88160",
        "http://www.sherdog.com/events/Aleksey-Raevskiy-Promotion-KPF-Kingdom-Professional-Fight-Selection-5-87746",
        "http://www.sherdog.com/events/Arena-Global-Arena-Global-9-88031",
        "http://www.sherdog.com/events/BFL-9-88105",
        "http://www.sherdog.com/events/BSC-1-Reis-vs-Briseo-88111",
        "http://www.sherdog.com/events/Babilon-MMA-18-Revenge-88023",
        "http://www.sherdog.com/events/Bellator-253-Caldwell-vs-McKee-87801",
        "http://www.sherdog.com/events/Bellator-254-Macfarlane-vs-Velasquez-87904",
        "http://www.sherdog.com/events/Bout-Bout-41-88080",
        "http://www.sherdog.com/events/Brave-CF-45-Brave-Combat-Federation-45-87869",
        "http://www.sherdog.com/events/CFC-8-Corumba-Fight-Combat-8-88103",
        "http://www.sherdog.com/events/CFFC-88-Cage-Fury-Fighting-Championships-88-88008",
        "http://www.sherdog.com/events/CFFC-89-Cage-Fury-Fighting-Championships-89-88009",
        "http://www.sherdog.com/events/CFN-Colisao-Fight-Night-4-88229",
        "http://www.sherdog.com/events/CG-28-Celtic-Gladiator-28-Lockdown-Throwdown-87784",
        "http://www.sherdog.com/events/CLFC-Cage-Legacy-14-87749",
        "http://www.sherdog.com/events/CW-117-Cage-Warriors-117-The-Trilogy-Strikes-Back-1-82741",
        "http://www.sherdog.com/events/CW-118-Cage-Warriors-118-The-Trilogy-Strikes-Back-2-82743",
        "http://www.sherdog.com/events/CW-119-Cage-Warriors-119-The-Trilogy-Strikes-Back-3-87754",
        "http://www.sherdog.com/events/CW-38-Clan-Wars-38-88032",
        "http://www.sherdog.com/events/Caged-Aggression-29-Determination-Day-1-87687",
        "http://www.sherdog.com/events/Caged-Aggression-29-Determination-Day-2-87688",
        "http://www.sherdog.com/events/Caged-Steel-26-Caged-Steel-Fighting-Championship-26-87258",
        "http://www.sherdog.com/events/Caray-MMA-Boxing-Temporada-2-MMA-Fights-4-88082",
        "http://www.sherdog.com/events/Coastal-Combat-8-10037-MMA-Action-on-the-Sunshine-Coast-88026",
        "http://www.sherdog.com/events/Colosseum-MMA-Battle-of-Champions-16-88005",
        "http://www.sherdog.com/events/Combat-Night-Combat-Night-Pro-19-86057",
        "http://www.sherdog.com/events/DCS-63-Thanksgiving-Throwdown-2-Night-1-88187",
        "http://www.sherdog.com/events/DCS-64-Thanksgiving-Throwdown-2-Night-2-88188",
        "http://www.sherdog.com/events/DFC-11-Diamondback-Fighting-Championship-11-86033",
        "http://www.sherdog.com/events/DFL-2-Torres-vs-Medina-88096",
        "http://www.sherdog.com/events/DMF-DM-Fight-1-88079",
        "http://www.sherdog.com/events/Dana-Whites-Contender-Series-Contender-Series-2020-Week-10-86534",
        "http://www.sherdog.com/events/Dazn-Joshua-vs-Pulev-88161",
        "http://www.sherdog.com/events/Double-G-FC-5-Double-G-Fighting-Championship-87937",
        "http://www.sherdog.com/events/EFC-30-Eagle-Fighting-Championship-30-88025",
        "http://www.sherdog.com/events/EFC-Global-EFC-Global-8-88033",
        "http://www.sherdog.com/events/EMMA-Eternal-MMA-55-87885",
        "http://www.sherdog.com/events/Endo-Athletics-JiuJitsu-Pro-7-86718",
        "http://www.sherdog.com/events/Evolution-Championship-The-Dark-Cage-87947",
        "http://www.sherdog.com/events/FAC-5-Fighting-Alliance-Championship-88204",
        "http://www.sherdog.com/events/FAC-6-Fighting-Alliance-Championship-88205",
        "http://www.sherdog.com/events/FEN-31-Rutkowski-vs-Zielinski-2-87871",
        "http://www.sherdog.com/events/FFC-44-Basurto-vs-Ribovics-86732",
        "http://www.sherdog.com/events/FFC-FMR-Fighting-Championship-Selection-5-88027",
        "http://www.sherdog.com/events/FMD-Full-Metal-Dojo-Fight-Circus-Vol-2-87883",
        "http://www.sherdog.com/events/FMMA-8-Fame-MMA-87787",
        "http://www.sherdog.com/events/FMMAU-Kharkiv-MMA-Cup-88095",
        "http://www.sherdog.com/events/FNC-Armagedon-4-Final-87887",
        "http://www.sherdog.com/events/Fair-Fight-Promotion-Fair-Fight-13-Road-to-One-88109",
        "http://www.sherdog.com/events/Fight-Club-Den-Haag-Akira-FC-2-87946",
        "http://www.sherdog.com/events/Fight-Masters-Selection-12-88018",
        "http://www.sherdog.com/events/Fighting-Force-Promotions-Force-4-McMahon-vs-Thornton-87931",
        "http://www.sherdog.com/events/Flogger-Series-FS-6-88283",
        "http://www.sherdog.com/events/Forze-MMA-1-Josiane-vs-Quezia-88081",
        "http://www.sherdog.com/events/Fury-FC-43-Fury-Fighting-Championship-43-85321",
        "http://www.sherdog.com/events/GAMMA-Canarias-Pro-Fight-87890",
        "http://www.sherdog.com/events/GFC-04-Gentlemanflower-Fighting-Championship-04-88016",
        "http://www.sherdog.com/events/GLFC-17-Global-Legion-FC-17Miami-88130",
        "http://www.sherdog.com/events/GMC-30-German-MMA-Championship-30-86538",
        "http://www.sherdog.com/events/Ghazni-MMA-Ghazni-MMA-1-88274",
        "http://www.sherdog.com/events/Gold-Rush-Gold-Rush-7-88083",
        "http://www.sherdog.com/events/Grachan-Grachan-46-88175",
        "http://www.sherdog.com/events/HRMMA-Hardrock-MMA-117-88037",
        "http://www.sherdog.com/events/Home-Fight-Championship-HFC-1-87579",
        "http://www.sherdog.com/events/Honor-FC-14-Honor-Fighting-Championship-14-87892",
        "http://www.sherdog.com/events/Horus-Fight-Combat-HFC-KLB-Vs-Javali-86684",
        "http://www.sherdog.com/events/IFMMA-International-Fighting-MMA-15-88241",
        "http://www.sherdog.com/events/Impact-Promotions-Beatdown-at-the-Beach-15-87785",
        "http://www.sherdog.com/events/Invicta-FC-43-King-vs-Harrison-87485",
        "http://www.sherdog.com/events/JFC-2-Junior-Fighting-Championship-2-87930",
        "http://www.sherdog.com/events/KFC-2-King-Fighting-Championship-2-88278",
        "http://www.sherdog.com/events/KSW-56-Materla-vs-Soldic-87766",
        "http://www.sherdog.com/events/LFA-95-Pereira-vs-Powell-87902",
        "http://www.sherdog.com/events/LFA-96-Mendonca-vs-Dagvadorj-87955",
        "http://www.sherdog.com/events/LFC-3-Lions-Fighting-Championship-3-88006",
        "http://www.sherdog.com/events/LFC-Limo-Fight-Championship-21-88291",
        "http://www.sherdog.com/events/Lux-Fight-League-Lux-011-88010",
        "http://www.sherdog.com/events/MADA-Madabattle-Martial-Arts-Festival-2-88021",
        "http://www.sherdog.com/events/MF-Mega-Fight-Champions-2-88056",
        "http://www.sherdog.com/events/MMA-Battle-Arena-Battle-Arena-86716",
        "http://www.sherdog.com/events/MMA-Battle-Arena-Battle-Arena-86717",
        "http://www.sherdog.com/events/MMA-Berlin-Tournament-65-86720",
        "http://www.sherdog.com/events/MMA-Series-20-Time-of-New-Heroes-12-87928",
        "http://www.sherdog.com/events/MMA-Series-21-Krasnaya-Polyana-87929",
        "http://www.sherdog.com/events/MMA-Series-22-Fighting-Championship-Pankration-88088",
        "http://www.sherdog.com/events/MMAX-FC-Fight-Night-2-88004",
        "http://www.sherdog.com/events/Mannheimer-Hafenkeilerei-Mannheim-Harbor-Brawl-9-86722",
        "http://www.sherdog.com/events/NCP-Pankration-National-Championship-31-87722",
        "http://www.sherdog.com/events/NFC-128-National-Fighting-Championship-128-88243",
        "http://www.sherdog.com/events/NFC-26-Naiza-Fighter-Championship-26-88028",
        "http://www.sherdog.com/events/NFG-16-Mortal-Combat-87941",
        "http://www.sherdog.com/events/O-Rei-da-Luta-2-87984",
        "http://www.sherdog.com/events/OC-Oplot-Challenge-111-88078",
        "http://www.sherdog.com/events/OCL-Ohio-Combat-League-8-88030",
        "http://www.sherdog.com/events/OFC-1-Original-Fighting-Championship-1-88233",
        "http://www.sherdog.com/events/OFC-10-Estela-vs-Blasco-87893",
        "http://www.sherdog.com/events/OFC-2020-88128",
        "http://www.sherdog.com/events/OSE-Dmitriy-Zhidkov-Memorial-2020-88036",
        "http://www.sherdog.com/events/Oktagon-MMA-Oktagon-18-87886",
        "http://www.sherdog.com/events/Oktagon-MMA-Oktagon-19-88129",
        "http://www.sherdog.com/events/One-Championship-Big-Bang-2-86181",
        "http://www.sherdog.com/events/One-Championship-Big-Bang-86179",
        "http://www.sherdog.com/events/One-Championship-Collision-Course-2-88137",
        "http://www.sherdog.com/events/One-Championship-Inside-the-Matrix-3-87966",
        "http://www.sherdog.com/events/One-Championship-Inside-the-Matrix-4-87967",
        "http://www.sherdog.com/events/One-Championship-TBA-88180",
        "http://www.sherdog.com/events/One-Pride-MMA-Fight-Night-39-The-Real-Fight-88295",
        "http://www.sherdog.com/events/Opolscy-Wojownicy-5-Bitwa-nad-Odra-87747",
        "http://www.sherdog.com/events/PF-Pyramid-Fights-16-88173",
        "http://www.sherdog.com/events/PIK-Promoterskaya-International-Company-86775",
        "http://www.sherdog.com/events/PPC-12-Kratos-Cup-88281",
        "http://www.sherdog.com/events/Pasaje-Combat-2-Vacacela-vs-Castro-87999",
        "http://www.sherdog.com/events/Perviy-Club-Fight-Show-46-88282",
        "http://www.sherdog.com/events/Productora-One-Live-Fight-Night-87889",
        "http://www.sherdog.com/events/R2-Combat-Live-1-87861",
        "http://www.sherdog.com/events/RCC-Intro-10-88019",
        "http://www.sherdog.com/events/RCF-13-Red-City-Fights-13-Selection-4-88035",
        "http://www.sherdog.com/events/RECIFIGHT-4-CAPITO-vs-ALEXSANDRO-88285",
        "http://www.sherdog.com/events/RITC-Rage-in-the-Cage-OKC-77-88174",
        "http://www.sherdog.com/events/RV-Eventos-Jatoba-Fight-Striker-MMA-87942",
        "http://www.sherdog.com/events/Revelation-FC-Revelation-Fighting-Championship-6-87856",
        "http://www.sherdog.com/events/Rizin-FF-Rizin-25-87884",
        "http://www.sherdog.com/events/Rough-Fight-League-Storm-Surge-3-88176",
        "http://www.sherdog.com/events/SFC-Legacy-of-Sparta-Bantamweight-Grand-Prix-88234",
        "http://www.sherdog.com/events/SFC-Sombra-Fight-Champions-18-87810",
        "http://www.sherdog.com/events/SFL-54-Siberian-Fighting-League-54-Battle-1-88120",
        "http://www.sherdog.com/events/SFMMA-Superfight-MMA-15-88034",
        "http://www.sherdog.com/events/SFT-Standout-Fighting-Tournament-24-Cabecao-vs-Jacare-87813",
        "http://www.sherdog.com/events/SFT-Standout-Fighting-Tournament-25-Predador-vs-Viana-87814",
        "http://www.sherdog.com/events/SFT-Standout-Fighting-Tournament-26-Camelo-vs-Clebinho-87815",
        "http://www.sherdog.com/events/Shooto-Brazil-Shooto-Brazil-104-88166",
        "http://www.sherdog.com/events/Shooto-Brazil-Shooto-Brazil-105-88165",
        "http://www.sherdog.com/events/Shooto-Professional-Shooto-2020-Vol-7-87891",
        "http://www.sherdog.com/events/Square-Ring-Promotions-Island-Fights-65-88167",
        "http://www.sherdog.com/events/Superior-Challenge-21-Stockholm-84597",
        "http://www.sherdog.com/events/TF-Terral-Fight-8-87641",
        "http://www.sherdog.com/events/TFS-Mix-Fight-Gala-31-Fight-Club-4-87739",
        "http://www.sherdog.com/events/The-Battle-Championship-Road-to-AFL-87944",
        "http://www.sherdog.com/events/Time-to-Shine-Time-to-Rise-4-87748",
        "http://www.sherdog.com/events/Titan-FC-65-Graves-vs-Jasse-87909",
        "http://www.sherdog.com/events/ToM-7-Time-of-Masters-7-86719",
        "http://www.sherdog.com/events/ToM-Time-of-Masters-Independence-Day-88017",
        "http://www.sherdog.com/events/Tuva-MMA-Federation-Tuva-MMA-Cup-87965",
        "http://www.sherdog.com/events/UFC-255-Figueiredo-vs-Perez-87312",
        "http://www.sherdog.com/events/UFC-256-Figueiredo-vs-Moreno-87401",
        "http://www.sherdog.com/events/UFC-257-McGregor-vs-Poirier-2-87798",
        "http://www.sherdog.com/events/UFC-Fight-Night-182-Felder-vs-dos-Anjos-87393",
        "http://www.sherdog.com/events/UFC-Fight-Night-183-Thompson-vs-Neal-87646",
        "http://www.sherdog.com/events/UFC-Fight-Night-184-Holloway-vs-Kattar-87759",
        "http://www.sherdog.com/events/UFC-Fight-Night-Jan-20-88171",
        "http://www.sherdog.com/events/UFC-Fight-Night-Jan-30-87765",
        "http://www.sherdog.com/events/UFC-on-ESPN-18-Smith-vs-Clark-87392",
        "http://www.sherdog.com/events/UFC-on-ESPN-19-Hermansson-vs-Vettori-87402",
        "http://www.sherdog.com/events/UFL-4-Ultimate-Fight-League-4-81927",
        "http://www.sherdog.com/events/UFN-23-Urban-Fight-Night-23-88020",
        "http://www.sherdog.com/events/UMMA-All-Russian-MMA-Championship-2020-Day-1-87938",
        "http://www.sherdog.com/events/UMMA-All-Russian-MMA-Championship-2020-Day-2-87945",
        "http://www.sherdog.com/events/UWC-Mexico-24-Friday-the-13th-87980",
        "http://www.sherdog.com/events/Ultimate-Battle-Grounds-5-Winter-Flurries-88168",
        "http://www.sherdog.com/events/Versus-FC-Muay-Thai-and-MMA-Qualifier-88007",
        "http://www.sherdog.com/events/WDFC-14-Warriors-Den-FC-14-87786",
        "http://www.sherdog.com/events/WEF-95-ProfFight-40-88086",
        "http://www.sherdog.com/events/WLMMA-We-Love-MMA-59-86545",
        "http://www.sherdog.com/events/WSF-Vale-Tudo-Sem-Regras-VTR-MMA-88029",
        "http://www.sherdog.com/events/WSF-World-Sensacional-Fight-6-88024",
        "http://www.sherdog.com/events/XFC-46-State-Of-Origin-88085",
        "http://www.sherdog.com/events/YFC-11-Yantzaza-Fighting-Championship-11-88057",
        "http://www.sherdog.com/events/ZFC-5-Zeus-Fighting-Championship-5-87478",
        "http://www.sherdog.com/events/iFF-3-iKon-Fighting-Federation-3-88014",
        "http://www.sherdog.com/events/iFF-4-iKon-Fighting-Federation-4-88182",
    ]
    assert links == actuall


def test_empty_events_list_parsing():
    links = sherdog.extract_events_links("", "")
    actuall = []
    assert links == actuall


def test_event_parsing(sherdog_event):
    page_content, page_url = sherdog_event
    event_data = sherdog.extract_event_data(page_content, page_url)
    assert event_data == {
        "title": "UFC 214 Cormier vs. Jones 2",
        "organization": "Ultimate Fighting Championship (UFC)",
        "date": dt.date(2017, 7, 29),
        "location": "Honda Center / Anaheim / California / United States",
        "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
    }


def test_main_fight_parsing(sherdog_event):
    page_content, _ = sherdog_event
    soup = BeautifulSoup(page_content, "lxml")
    fights = sherdog._extract_main_fight_from_event(soup)
    assert fights == {
        "method": "no contest",
        "details": "overturned by csac",
        "result": "nc",
        "rounds": 3,
        "time": 13.016666666666666,
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "position": 1,
    }


def test_other_fights_parsing(sherdog_event):
    page_content, _ = sherdog_event
    soup = BeautifulSoup(page_content, "lxml")
    fights = sherdog._extract_other_fights_from_event(soup)
    assert fights == [
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 5,
            "time": 25.0,
            "fighter": "http://www.sherdog.com/fighter/Tyron-Woodley-42605",
            "opponent": "http://www.sherdog.com/fighter/Demian-Maia-14637",
            "position": 2,
        },
        {
            "method": "tko",
            "details": "knees",
            "result": "win",
            "rounds": 3,
            "time": 11.933333333333334,
            "fighter": "http://www.sherdog.com/fighter/Cristiane-Justino-14477",
            "opponent": "http://www.sherdog.com/fighter/Tonya-Evinger-18248",
            "position": 3,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Robbie-Lawler-2245",
            "opponent": "http://www.sherdog.com/fighter/Donald-Cerrone-15105",
            "position": 4,
        },
        {
            "method": "ko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 0.7,
            "fighter": "http://www.sherdog.com/fighter/Volkan-Oezdemir-58503",
            "opponent": "http://www.sherdog.com/fighter/Jimi-Manuwa-37528",
            "position": 5,
        },
        {
            "method": "tko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 4.566666666666666,
            "fighter": "http://www.sherdog.com/fighter/Ricardo-Lamas-32051",
            "opponent": "http://www.sherdog.com/fighter/Jason-Knight-44957",
            "position": 6,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aljamain-Sterling-66313",
            "opponent": "http://www.sherdog.com/fighter/Renan-Barao-23156",
            "position": 7,
        },
        {
            "method": "submission",
            "details": "guillotine choke",
            "result": "win",
            "rounds": 3,
            "time": 12.983333333333334,
            "fighter": "http://www.sherdog.com/fighter/Brian-Ortega-65310",
            "opponent": "http://www.sherdog.com/fighter/Renato-Carneiro-61700",
            "position": 8,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Calvin-Kattar-23782",
            "opponent": "http://www.sherdog.com/fighter/Andre-Fili-58385",
            "position": 9,
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aleksandra-Albu-144949",
            "opponent": "http://www.sherdog.com/fighter/Kailin-Curran-62703",
            "position": 10,
        },
        {
            "method": "decision",
            "details": "split",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Jarred-Brooks-174665",
            "opponent": "http://www.sherdog.com/fighter/Eric-Shelton-86414",
            "position": 11,
        },
        {
            "method": "ko",
            "details": "punch",
            "result": "win",
            "rounds": 1,
            "time": 3.066666666666667,
            "fighter": "http://www.sherdog.com/fighter/Drew-Dober-23982",
            "opponent": "http://www.sherdog.com/fighter/Joshua-Burkman-10003",
            "position": 12,
        },
    ]


def test_fights_parsing(sherdog_event):
    page_content, page_url = sherdog_event
    fights = sherdog.extract_fights(page_content, page_url)
    assert fights == [
        {
            "method": "no contest",
            "details": "overturned by csac",
            "result": "nc",
            "rounds": 3,
            "time": 13.016666666666666,
            "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
            "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
            "position": 1,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "3cda3aefbd92cf77156efcd4bbbd0723",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 5,
            "time": 25.0,
            "fighter": "http://www.sherdog.com/fighter/Tyron-Woodley-42605",
            "opponent": "http://www.sherdog.com/fighter/Demian-Maia-14637",
            "position": 2,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "125e438263086c8f3d0f469a815720ff",
        },
        {
            "method": "tko",
            "details": "knees",
            "result": "win",
            "rounds": 3,
            "time": 11.933333333333334,
            "fighter": "http://www.sherdog.com/fighter/Cristiane-Justino-14477",
            "opponent": "http://www.sherdog.com/fighter/Tonya-Evinger-18248",
            "position": 3,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "4da8792140df9e0c36ea83f18611b25b",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Robbie-Lawler-2245",
            "opponent": "http://www.sherdog.com/fighter/Donald-Cerrone-15105",
            "position": 4,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "a6456a74295f38e27b6cbacbd521bceb",
        },
        {
            "method": "ko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 0.7,
            "fighter": "http://www.sherdog.com/fighter/Volkan-Oezdemir-58503",
            "opponent": "http://www.sherdog.com/fighter/Jimi-Manuwa-37528",
            "position": 5,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "64e4b168f12b54fa952d1f955312f3b6",
        },
        {
            "method": "tko",
            "details": "punches",
            "result": "win",
            "rounds": 1,
            "time": 4.566666666666666,
            "fighter": "http://www.sherdog.com/fighter/Ricardo-Lamas-32051",
            "opponent": "http://www.sherdog.com/fighter/Jason-Knight-44957",
            "position": 6,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "97f54afbfa1c0ba3bbb5a92e0592f808",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aljamain-Sterling-66313",
            "opponent": "http://www.sherdog.com/fighter/Renan-Barao-23156",
            "position": 7,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "02ddcea5da241841b429dfa7b43597c6",
        },
        {
            "method": "submission",
            "details": "guillotine choke",
            "result": "win",
            "rounds": 3,
            "time": 12.983333333333334,
            "fighter": "http://www.sherdog.com/fighter/Brian-Ortega-65310",
            "opponent": "http://www.sherdog.com/fighter/Renato-Carneiro-61700",
            "position": 8,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "baf70455b161fe5f6e2c1878c0b5c4e2",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Calvin-Kattar-23782",
            "opponent": "http://www.sherdog.com/fighter/Andre-Fili-58385",
            "position": 9,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "fa391e5f03b8f341b58e79206d753047",
        },
        {
            "method": "decision",
            "details": "unanimous",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Aleksandra-Albu-144949",
            "opponent": "http://www.sherdog.com/fighter/Kailin-Curran-62703",
            "position": 10,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "dabc81a4aa934403839f391fbdaefd34",
        },
        {
            "method": "decision",
            "details": "split",
            "result": "win",
            "rounds": 3,
            "time": 15.0,
            "fighter": "http://www.sherdog.com/fighter/Jarred-Brooks-174665",
            "opponent": "http://www.sherdog.com/fighter/Eric-Shelton-86414",
            "position": 11,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "8328f6dc4410e35e850facf4dfc1f29b",
        },
        {
            "method": "ko",
            "details": "punch",
            "result": "win",
            "rounds": 1,
            "time": 3.066666666666667,
            "fighter": "http://www.sherdog.com/fighter/Drew-Dober-23982",
            "opponent": "http://www.sherdog.com/fighter/Joshua-Burkman-10003",
            "position": 12,
            "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
            "title": "UFC 214 Cormier vs. Jones 2",
            "organization": "Ultimate Fighting Championship (UFC)",
            "date": dt.date(2017, 7, 29),
            "location": "Honda Center / Anaheim / California / United States",
            "id": "f5ba70e3ad5338b4fddc69380632dbad",
        },
    ]


def test_empty_webiste_fights_parsing():
    fights = sherdog.extract_fights(None, "")
    assert len(fights) == 0


def test_fighter_parsing(sherdog_fighter):
    page_content, page_url = sherdog_fighter
    fighter = sherdog.extract_fighter_info(page_content, page_url)
    assert fighter == {
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "birth": dt.date(1987, 7, 19),
        "height": 6.4,
        "association": "Jackson-Wink MMA",
        "nationality": "United States",
    }


def test_opponent_parsing(sherdog_opponent):
    page_content, page_url = sherdog_opponent
    fighter = sherdog.extract_fighter_info(page_content, page_url)
    assert fighter == {
        "fighter": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "birth": dt.date(1979, 3, 20),
        "height": 5.11,
        "association": "American Kickboxing Academy",
        "nationality": "United States",
    }


def test_combining_fight_and_fighters(sherdog_event, sherdog_fighter, sherdog_opponent):
    fighter = sherdog.extract_fighter_info(*sherdog_fighter)
    opponent = sherdog.extract_fighter_info(*sherdog_opponent)
    fights = sherdog.extract_fights(*sherdog_event)
    fighters = pd.DataFrame([fighter, opponent])
    result = sherdog.combine_data(pd.DataFrame(fights[:1]), fighters)
    actuall = result.to_dict("records")[0]
    assert actuall == {
        "method": "no contest",
        "details": "overturned by csac",
        "result": "nc",
        "rounds": 3,
        "time": 13.016666666666666,
        "fighter": "http://www.sherdog.com/fighter/Jon-Jones-27944",
        "opponent": "http://www.sherdog.com/fighter/Daniel-Cormier-52311",
        "position": 1,
        "url": "http://www.sherdog.com/events/UFC-214-Cormier-vs-Jones-2-57825",
        "title": "UFC 214 Cormier vs. Jones 2",
        "organization": "Ultimate Fighting Championship (UFC)",
        "date": dt.date(2017, 7, 29),
        "location": "Honda Center / Anaheim / California / United States",
        "id": "3cda3aefbd92cf77156efcd4bbbd0723",
        "fighter birth": dt.date(1987, 7, 19),
        "fighter height": 6.4,
        "fighter association": "Jackson-Wink MMA",
        "fighter nationality": "United States",
        "opponent birth": dt.date(1979, 3, 20),
        "opponent height": 5.11,
        "opponent association": "American Kickboxing Academy",
        "opponent nationality": "United States",
    }


def test_void_main_fighter():
    html = """
    <div class="fighter right_side" itemprop="performer" itemscope="" itemtype="http://schema.org/Person">
        <a href="javascript:void();" itemprop="url">
            <img itemprop="image" src="/image_crop/72/72/_images/fighter_small_default.jpg" 
                 alt="Unknown Fighter" title="Unknown Fighter">
        </a>
        <h3>
        <a href="javascript:void();"><span itemprop="name">Unknown Fighter</span></a>
        </h3>
        <span class="final_result loss">loss</span>
        <span class="record"> -  -  <em>(Win - Loss - Draw)</em> </span>
    </div>
    """
    soup = BeautifulSoup(html, "lxml")
    assert sherdog._extract_fighter_id(soup) == "Unknown Fighter"


def test_void_other_fighter():
    html = """
    <td class="text_left col_fc_upcoming" itemprop="performer" itemscope="" itemtype="http://schema.org/Person">
        <meta itemprop="image" content="/image_crop/44/44/_images/fighter_small_default.jpg">
        <img height="44" width="44" class="lazy" src="/image_crop/44/44/_images/fighter_small_default.jpg" 
             data-original="/image_crop/44/44/_images/fighter_small_default.jpg" 
             alt="Unknown Fighter" title="Unknown Fighter">
        <div class="fighter_result_data">
            <a itemprop="url" href="javascript:void();"><span itemprop="name">Unknown Fighter</span></a><br>
            <span class="final_result loss">loss</span>
        </div>
    </td>
    """
    soup = BeautifulSoup(html, "lxml")
    assert sherdog._extract_fighter_id(soup) == "Unknown Fighter"