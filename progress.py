import csv
import os
class ProgressTracker:

    def __init__(self, roadmap, file_name="data/progress.csv"):

     self.roadmap = roadmap
     self.file_name = file_name
     self.fields = ["user_id", "skill", "completed"]
     self.create_file()
    def create_file(self):

      if not os.path.exists(self.file_name):

        with open(self.file_name, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(self.fields) 
    def complete_skill(self, skill_name):

        for skill in self.roadmap:

            if skill.name.lower() == skill_name.lower():
                skill.set_completed(True)
                return True

        return False

    def completed_skills(self):

        count = 0

        for skill in self.roadmap:

            if skill.completed:
                count += 1

        return count

    def remaining_skills(self):

        return len(self.roadmap) - self.completed_skills()

    def progress_percentage(self):

      total = len(self.roadmap)

      if total == 0:
              return 0

      completed = self.completed_skills()

      percentage = (completed / total) * 100

      return round(percentage, 2)

    def display_progress(self):

        print("\n========== Progress ==========")
        print(f"Completed : {self.completed_skills()}")
        print(f"Remaining : {self.remaining_skills()}")
        print(f"Progress  : {self.progress_percentage():.2f}%")
    def search_skill(self, keyword):

      results = []

      keyword = keyword.lower()

      for skill in self.roadmap:

        if keyword in skill.name.lower():

            results.append(skill)

      return results    
    def save_progress(self, user_id):

      rows = []

      if os.path.exists(self.file_name):

        with open(self.file_name, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["user_id"] != str(user_id):

                    rows.append(row)

      for skill in self.roadmap:

        rows.append({

            "user_id": user_id,

            "skill": skill.name,

            "completed": skill.completed

        })

      with open(self.file_name, "w", newline="") as file:

        writer = csv.DictWriter(

            file,

            fieldnames=self.fields

        )

        writer.writeheader()

        writer.writerows(rows)
    def load_progress(self, user_id):

     if not os.path.exists(self.file_name):

        return

     with open(self.file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["user_id"] == str(user_id):

                for skill in self.roadmap:

                    if skill.name == row["skill"]:

                        skill.completed = (
                            row["completed"] == "True"
                        )    