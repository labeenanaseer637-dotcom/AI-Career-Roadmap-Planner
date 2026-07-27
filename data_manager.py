import csv
import os
from user import User


class DataManager:

    def __init__(self, file_name):
        self.file_name = file_name
        self.fields = [
            "user_id",
            "name",
            "age",
            "education",
            "career_goal",
            "study_hours",
            "password",
            "current_level",
            "programming_experience",
            "interests",
            "learning_style",
            "email",
            "verified",
            "verification_code"]
    def create_file_if_not_exists(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()
    def save_user(self, user):
        self.create_file_if_not_exists()
        with open(self.file_name, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(user.to_dict())
    def load_users(self):
        self.create_file_if_not_exists()
        users = []
        with open(self.file_name, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    row["user_id"],
                    row["name"],
                    int(row["age"]),
                    row["education"],
                    row["career_goal"],
                    float(row["study_hours"]),
                    row["password"],
                    row["current_level"],
                    row["programming_experience"],
                    row["interests"],
                    row["learning_style"], 
                    row["email"],
                    row["verified"] == "True",
                    int(row["verification_code"]) if row["verification_code"] else None)
                users.append(user)
        return users
    def get_next_id(self):
      self.create_file_if_not_exists()
      with open(self.file_name, "r", newline="") as file:
        reader = csv.DictReader(file)
        ids = []
        for row in reader:
            user_id = row["user_id"].strip()
            if not user_id:
                continue
            if user_id.startswith("AI"):
                try:
                    number = int(user_id[2:])
                    ids.append(number)
                except ValueError:
                    continue
        next_id = max(ids) + 1 if ids else 1
        return f"AI{next_id:03d}"
    def save_progress(self, user_id, roadmap):
      with open("data/progress.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["user_id", "skill_name", "completed"])
        for skill in roadmap:
            writer.writerow([
                user_id,
                skill.name,
                skill.completed
            ])
    def load_progress(self, user_id):
        progress = {}
        try:
          with open("data/progress.csv","r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user_id"] == user_id:
                    progress[row["skill_name"]] = (
                        row["completed"] == "True"
                    )
        except FileNotFoundError:
          pass
        return progress            
    def load_user_by_id(self, user_id):
       self.create_file_if_not_exists()
       with open(self.file_name, "r", newline="") as file:
          reader = csv.DictReader(file)
          for row in reader:
            if row["user_id"] == user_id:
                return User(
                    row["user_id"],
                    row["name"],
                    int(row["age"]),
                    row["education"],
                    row["career_goal"],
                    float(row["study_hours"]),
                    row["password"],
                    row["current_level"],
                    row["programming_experience"],
                    row["interests"],
                    row["learning_style"], row["email"],
                    row["verified"] == "True",
                    int(row["verification_code"]) if row["verification_code"] else None)
          return None  
    def load_user_by_credentials(self, name, password):
      with open(self.file_name, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["name"] == name and row["password"] == password:
                return User(
                    row["user_id"],
                    row["name"],
                    int(row["age"]),
                    row["education"],
                    row["career_goal"],
                    float(row["study_hours"]),
                    row["password"],
                    row["current_level"],
                    row["programming_experience"],
                    row["interests"],
                    row["learning_style"] ,row["email"],  row["verified"] == "True",  int(row["verification_code"]) if row["verification_code"] else None
                )
      return None
    def update_user(self, updated_user):
       users = []
       with open(self.file_name, "r", newline="") as file:
         reader = csv.DictReader(file)
         for row in reader:
            if row["user_id"] == updated_user.user_id:
                row["name"] = updated_user.name
                row["age"] = updated_user.age
                row["education"] = updated_user.education
                row["career_goal"] = updated_user.career_goal
                row["study_hours"] = updated_user.study_hours
                row["password"] = updated_user.password
                row["email"] = updated_user.email
                row["verified"] = updated_user.verified
                row["verification_code"] = updated_user.verification_code
                row["current_level"] = updated_user.current_level
                row["programming_experience"] = updated_user.programming_experience
                row["interests"] = updated_user.interests
                row["learning_style"] = updated_user.learning_style
            users.append(row)
       with open(self.file_name, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=self.fields)
        writer.writeheader()
        writer.writerows(users)  
    def load_user_by_name(self, name):

      with open(self.file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["name"] == name:

                return User(
                    row["user_id"],
                    row["name"],
                    int(row["age"]),
                    row["education"],
                    row["career_goal"],
                    float(row["study_hours"]),
                    row["password"],
                    row["current_level"],
                    row["programming_experience"],
                    row["interests"],
                    row["learning_style"],
                    row["email"],
                    row["verified"] == "True",
                    int(row["verification_code"]) if row["verification_code"] else None
                )
        return None        
    def load_user_by_email(self, email):

     with open(self.file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["email"] == email:

                return row

     return None