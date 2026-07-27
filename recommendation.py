class RecommendationEngine:


    def filter_by_level(self, roadmap, current_level):

        filtered = []

        for skill in roadmap:

            if current_level == "Beginner":

                if skill.difficulty in ["Easy", "Medium"]:
                    filtered.append(skill)


            elif current_level == "Intermediate":

                if skill.difficulty != "Hard":
                    filtered.append(skill)


            else:
                filtered.append(skill)


        return filtered



    def match_interest(self, roadmap, interests):

        if not interests:
            return roadmap


        interests = interests.lower()

        matched = []

        for skill in roadmap:

            if interests in skill.category.lower():
                matched.append(skill)

            else:
                matched.append(skill)


        return matched



    def adjust_for_time(self, roadmap, study_hours):

        if study_hours < 2:

            roadmap = [
                skill for skill in roadmap
                if skill.difficulty != "Hard"
            ]


        return roadmap



    def prioritize_learning_style(self, roadmap, learning_style):

        # Future expansion:
        # Video based learning
        # Project based learning
        # Reading based learning

        return roadmap



    def recommend(self, user, roadmap):

        roadmap = self.filter_by_level(
            roadmap,
            user.current_level
        )


        roadmap = self.match_interest(
            roadmap,
            user.interests
        )


        roadmap = self.adjust_for_time(
            roadmap,
            user.study_hours
        )


        roadmap = self.prioritize_learning_style(
            roadmap,
            user.learning_style
        )


        return roadmap