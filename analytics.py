import pandas as pd


class Analytics:

    def __init__(self, roadmap):
        self.roadmap = roadmap

    def create_dataframe(self):

        data = []

        for skill in self.roadmap:
            data.append(skill.to_dict())

        return pd.DataFrame(data)

    def summary(self):

        df = self.create_dataframe()

        total = len(df)
        completed = int(df["completed"].sum())
        remaining = total - completed

        print("\n===== Summary =====")
        print(f"Total Skills     : {total}")
        print(f"Completed Skills : {completed}")
        print(f"Remaining Skills : {remaining}")

    def category_summary(self):

        df = self.create_dataframe()

        print("\n===== Skills by Category =====")
        print(df.groupby("category")["name"].count())

    def difficulty_summary(self):

        df = self.create_dataframe()

        print("\n===== Difficulty Levels =====")
        print(df["difficulty"].value_counts())

    def completed_skills(self):

        df = self.create_dataframe()

        return int(df["completed"].sum())

    def remaining_skills(self):

        df = self.create_dataframe()

        return len(df) - int(df["completed"].sum())

    def progress_percentage(self):

        df = self.create_dataframe()

        if len(df) == 0:
            return 0

        return round((df["completed"].sum() / len(df)) * 100, 2)