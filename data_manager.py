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

     directory = os.path.dirname(self.file_name)

     if directory:
        os.makedirs(directory, exist_ok=True)

     if not os.path.exists(self.file_name):

        with open(
            self.file_name,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.fields
            )

            writer.writeheader()
    def save_user(self, user):
        
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

      ids = []

      with open(self.file_name, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:

            user_id = row.get("user_id", "").strip()

            if user_id.startswith("AI"):

                try:
                    number = int(user_id[2:])
                    ids.append(number)

                except ValueError:
                    pass

        next_id = max(ids) + 1 if ids else 1

        new_id = f"AI{next_id:03d}"
 
        print("🆕 GENERATED USER ID:", new_id)
        return new_id
    def save_progress(self, user_id, roadmap):
      os.makedirs("data", exist_ok=True)
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

     print("🔎 Looking for USER ID:", repr(user_id))

     with open(self.file_name, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:

            stored_id = row["user_id"].strip()

            print("📁 Stored USER ID:", repr(stored_id))

            if stored_id == str(user_id).strip():

                print("✅ USER FOUND:", stored_id)

                return User(
                    row["user_id"].strip(),
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
                    int(row["verification_code"])
                    if row["verification_code"] else None
                )

     print("❌ USER NOT FOUND:", repr(user_id))
     return None  
    def load_user_by_credentials(self, name, password):
      self.create_file_if_not_exists()
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
       self.create_file_if_not_exists()
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
      self.create_file_if_not_exists()
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
     self.create_file_if_not_exists()
     with open(self.file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["email"] == email:

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
    def delete_user(self, user_id):
     self.create_file_if_not_exists()

     users = []

     with open(self.file_name, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["user_id"] != str(user_id):

                users.append(row)

     with open(self.file_name, "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=self.fields)

        writer.writeheader()

        writer.writerows(users)

    def delete_progress(self, user_id):

     progress_file = "data/progress.csv"

     if not os.path.exists(progress_file):
        return

     rows = []

     with open(
        progress_file,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("user_id", "").strip() != str(user_id).strip():
                rows.append(row)

     with open(
        progress_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "user_id",
            "skill_name",
            "completed"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in rows:

            writer.writerow({
                "user_id": row.get("user_id", ""),
                "skill_name": row.get(
                    "skill_name",
                    row.get("skill", "")
                ),
                "completed": row.get("completed", "")
            })