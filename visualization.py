import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import os

class Visualization:

    def __init__(self, roadmap):
        self.roadmap = roadmap

    def create_dataframe(self):

        data = []

        for skill in self.roadmap:
            data.append(skill.to_dict())

        return pd.DataFrame(data)

    def progress_pie_chart(self):

      df = self.create_dataframe()

      completed = df["completed"].sum()
      remaining = len(df) - completed

      labels = ["Completed", "Remaining"]
      values = [completed, remaining]

      plt.figure(figsize=(6,6))

      plt.pie(values, labels=labels, autopct="%1.1f%%")
      plt.title("Skill Progress")

      os.makedirs("static/charts", exist_ok=True)

      plt.savefig("static/charts/progress_pie.png")

      plt.close()
    def category_bar_chart(self):

        df = self.create_dataframe()

        category_count = df.groupby("category")["name"].count()

        plt.figure(figsize=(8,5))

        plt.bar(
            category_count.index,
            category_count.values
        )

        plt.title("Skills by Category")
        plt.xlabel("Category")
        plt.ylabel("Number of Skills")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("static/charts/category_bar.png")

        plt.close()

    def difficulty_chart(self):

        df = self.create_dataframe()

        difficulty = df["difficulty"].value_counts()

        plt.figure(figsize=(6,4))

        plt.bar(
            difficulty.index,
            difficulty.values
        )

        plt.title("Difficulty Distribution")
        plt.xlabel("Difficulty")
        plt.ylabel("Skills")

        plt.savefig("static/charts/difficulty.png")

        plt.close()