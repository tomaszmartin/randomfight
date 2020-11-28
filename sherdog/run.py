"""Responsible for sequencing fights data in time."""
import copy
import time
from datetime import datetime as dt
from typing import List, Dict
import pandas as pd

pd.options.mode.chained_assignment = None


class Sequencer(object):
    """Transforms fights stats into sequences of pre fight stats."""

    def __init__(self):
        self.data = None

    def fit(self, data):
        """
        Saves data for future transformation.
        :param data: raw data
        :return:
        """
        self.data = self.enrich(data)

    @staticmethod
    def enrich(raw):
        """
        Creates a data about fights from fighter and opponents perspective
        :param raw: fights data
        :return: fights data from fighter and opponents perspective
        """
        data = pd.DataFrame(raw)
        opponent = pd.DataFrame(raw)
        data["id"] = data["fighter"] + data["opponent"] + data["title"]
        opponent.rename(
            columns={"fighter": "opponent", "opponent": "fighter"}, inplace=True
        )
        opponent["result"] = "loss"
        data = data.append(opponent)
        data = data.sort_values(by=["fighter"])

        return data

    @staticmethod
    def parse_date(x):
        return dt.strptime(x, "%Y-%m-%d").date()

    def create_empty_stat(self, current_fight):
        return {
            "id": current_fight["id"],
            "date": self.parse_date(current_fight["date"]),
            "location": current_fight["location"],
            "organization": current_fight["organization"],
            "title": current_fight["title"],
            "fighter": {
                "started": current_fight["date"],
                "id": current_fight["fighter"],
                "history": {
                    "win": {
                        "total": 0.0,
                        "decision": 0.0,
                        "submission": 0.0,
                        "knockout": 0.0,
                    },
                    "loss": {
                        "total": 0.0,
                        "decision": 0.0,
                        "submission": 0.0,
                        "knockout": 0.0,
                    },
                    "since_last_fight": 0,
                    "fights": 0.0,
                    "time": 0.0,
                    "positions": 0.0,
                },
                "streak": {"win": 0.0, "loss": 0.0},
            },
            "result": current_fight["result"],
            "method": current_fight["method"],
            "details": current_fight["details"],
        }

    def create_stat(
        self,
        current_stat=None,
        previous_stat=None,
        current_fight=None,
        previous_fight=None,
    ):
        current_stat["id"] = current_fight["id"]
        current_stat["date"] = self.parse_date(current_fight["date"])
        for key in ["location", "result", "method", "details", "organization", "title"]:
            current_stat[key] = current_fight[key]

        # Add result from past fight
        result = previous_fight["result"].lower()
        current_stat["fighter"]["history"][result]["total"] += 1.0
        if result == "win":
            current_stat["fighter"]["streak"]["win"] += 1.0
            current_stat["fighter"]["streak"]["loss"] = 0.0
        else:
            current_stat["fighter"]["streak"]["loss"] += 1.0
            current_stat["fighter"]["streak"]["win"] = 0.0
        # Increase results and method scores
        method = "decision"
        knockout_flags = ["ko", "punches", "knockout", "cut", "towel", "kick"]
        for flag in knockout_flags:
            if flag in str(previous_fight["method"]):
                method = "knockout"
        submission_flags = [
            "sub",
            "mata",
            "armbar",
            "choke",
            "isaac",
            "tapout",
            "ubmission",
            "forfeit",
        ]
        for flag in submission_flags:
            if flag in str(previous_fight["method"]):
                method = "submission"
        current_stat["fighter"]["history"][result][method] += 1.0

        # Add stats
        current_stat["fighter"]["history"]["since_last_fight"] = (
            current_stat["date"] - previous_stat["date"]
        ).days
        current_stat["fighter"]["history"]["fights"] += 1.0
        if float(previous_fight["time"]) < 0:
            previous_fight["time"] = 5.0
        current_stat["fighter"]["history"]["time"] += float(previous_fight["time"])
        current_stat["fighter"]["history"]["positions"] += float(
            previous_fight["position"]
        )

        return current_stat

    def get_fights_for_fighter(self, fighter) -> List[Dict]:
        """
        Extracts all fights for a given fighter.
        :param fighter: fighter's id or name
        :return: given fighter's fights
        """
        fights = self.data[self.data["fighter"] == fighter]
        fights_list = fights.T.to_dict().values()
        # Sort fights from oldest to newest
        result = sorted(fights_list, key=lambda x: self.parse_date(x["date"]))
        return result

    def get_fighters(self) -> List[str]:
        """
        Extracts a list of fighters names.
        :return: fighters names
        """
        return self.data["fighter"].unique().tolist()

    def build_stats(self, fights):
        """
        Creates a list of data points in time, based on fighter's fights.
        :param fights: fighter's fights
        :return: enhanced data about fighter
        """
        stats = []
        for i, current_fight in enumerate(fights, 0):
            if i == 0:
                current_stat = self.create_empty_stat(current_fight)
            else:
                # Combine information form previous fights
                current_stat = copy.deepcopy(stats[i - 1])
                previous_stat = copy.deepcopy(stats[i - 1])
                previous_fight = copy.deepcopy(fights[i - 1])
                # Update stats with current information
                current_stat = self.create_stat(
                    current_stat=current_stat,
                    previous_stat=previous_stat,
                    current_fight=current_fight,
                    previous_fight=previous_fight,
                )
            stats.append(current_stat)

        return stats

    @staticmethod
    def exchange(data):
        result = []
        ids = list(set([point["id"] for point in data]))
        start = time.time()
        for i, idx in enumerate(ids):
            if i % 1000 == 0:
                print(
                    "Exchanging data {} from {} in {:.2f}".format(
                        i, len(ids), time.time() - start
                    )
                )
                start = time.time()
            pair = []
            for current in data:
                if current["id"] == idx:
                    pair.append(current)
            if len(pair) == 2:
                fighter, opponent = pair
                fighter["opponent"] = opponent["fighter"]
                opponent["opponent"] = fighter["fighter"]
                # Append new data points
                result.append(fighter)
                result.append(opponent)
            else:
                print("Error exchanging {}".format(i))

        return result

    def transform(self):
        """Transforms fight stats into sequences."""
        transformed = []
        fighters = self.get_fighters()
        start = time.time()
        for i, fighter in enumerate(fighters):
            if i % 1000 == 0:
                print(
                    "Working on {} fighter out of {} in {:.2f}".format(
                        i, len(fighters), time.time() - start
                    )
                )
                start = time.time()
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            transformed.extend(current)
        return transformed

    def fit_transform(self, data):
        """Transforms fight stats into sequences."""
        self.fit(data)
        return self.transform()


class Cumulator(Sequencer):
    def __init__(self):
        super().__init__()
        self.transformed = []

    def fit(self, data):
        """Saves the data for transformation."""
        self.data = pd.DataFrame(data)
        self.data["fighterid"] = self.data["fighter"].apply(lambda x: x["id"])
        self.data = self.data.sort_values(by="date")

    def get_fighters(self):
        """Returns a list of fighter's names."""
        fighter_ids = self.data["fighter"].apply(lambda x: x["id"])
        return fighter_ids.unique().tolist()  # ['/fighter/Georges-St-Pierre-3500']

    def get_fights_for_fighter(self, name):
        """Extracts all fights for a specific fighter."""
        fights = self.data[self.data["fighterid"] == name]
        fights_list = fights.T.to_dict().values()
        # Sort fights from oldest to earliest
        result = sorted(fights_list, key=lambda x: x["date"])
        return result

    def build_stats(self, fights):
        """Build cumulative stats for fighter."""
        stats = []
        raw = {
            "win": {
                "win": {
                    "total": 0.0,
                    "decision": 0.0,
                    "submission": 0.0,
                    "knockout": 0.0,
                },
                "loss": {
                    "total": 0.0,
                    "decision": 0.0,
                    "submission": 0.0,
                    "knockout": 0.0,
                },
            },
            "loss": {
                "win": {
                    "total": 0.0,
                    "decision": 0.0,
                    "submission": 0.0,
                    "knockout": 0.0,
                },
                "loss": {
                    "total": 0.0,
                    "decision": 0.0,
                    "submission": 0.0,
                    "knockout": 0.0,
                },
            },
        }
        for i, fight in enumerate(fights):
            fight = copy.deepcopy(fight)
            if i == 0:
                fight["fighter"]["cumulative"] = raw
                stats.append(fight)
            else:
                fight["fighter"]["cumulative"] = copy.deepcopy(
                    stats[i - 1]["fighter"]["cumulative"]
                )
                previous_stat = stats[i - 1]
                placement = previous_stat["result"].lower()
                for result in ["win", "loss"]:
                    for method in fight["opponent"]["history"][result].keys():
                        fight["fighter"]["cumulative"][placement][result][
                            method
                        ] += previous_stat["opponent"]["history"][result][method]
                stats.append(fight)

        return stats

    def transform(self):
        """Transforms fight stats into sequences."""
        fighters = self.get_fighters()
        start = time.time()
        num_of_fighters = len(fighters)
        for i, fighter in enumerate(fighters):
            if i % 1000 == 0:
                print(
                    "Transformed {} out of {} stats for {:.2f} seconds".format(
                        i, num_of_fighters, time.time() - start
                    )
                )
                start = time.time()
            fights = self.get_fights_for_fighter(fighter)
            current = self.build_stats(fights)
            self.transformed.extend(current)  # not append!
        return self.transformed


if __name__ == "__main__":
    transformer = Sequencer()
    # Calculate pre-fight stats
    # data = pd.read_csv('data/data.csv')
    # data = data[data['result'].isin(['win', 'loss'])]
    # transformed = transformer.fit_transform(data)
    # frame = pd.DataFrame.from_records(transformed)
    # frame.to_json('data/step1.json')

    # Exchange stats
    # transformed = pd.read_json('data/step1.json').to_dict('records')
    # exchanged = transformer.exchange(transformed)
    # final = pd.DataFrame.from_records(exchanged)
    # final.to_json('data/step2.json')

    # Calculate cumulative stats
    transformer = Cumulator()
    data = pd.read_json("data/step2.json")
    transformed = transformer.fit_transform(data)
    transformed_df = pd.DataFrame.from_records(transformed)
    transformed_df.to_json("data/step3.json")

    # Exchange stats
    transformed = pd.read_json("data/step3.json").to_dict("records")
    exchanged = transformer.exchange(transformed)
    final = pd.DataFrame.from_records(exchanged)
    final.to_json("data/final.json")
