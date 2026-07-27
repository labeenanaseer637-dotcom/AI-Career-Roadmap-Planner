import csv
from skill import Skill


class CareerPath:

    def __init__(self, file_name):
        self.file_name = file_name


    def get_careers(self):

        careers = []

        with open(self.file_name, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["career"] not in careers:
                    careers.append(row["career"])

        return careers



    def generate_roadmap(self, career_name, user=None):

        roadmap = []

        with open(self.file_name, "r") as file:

            reader = csv.DictReader(file)


            for row in reader:

                if row["career"] == career_name:


                    # Personalization logic

                    if user:


                        if user.programming_experience == "Beginner":

                            if row["difficulty"] == "Hard":
                                continue


                        if user.study_hours < 2:

                            if row["difficulty"] == "Hard":
                                continue



                    skill = Skill(
                        row["skill"],
                        row["category"],
                        row["difficulty"]
                    )


                    roadmap.append(skill)


        return roadmap