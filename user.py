class User:
    def __init__(self, user_id, name, age, education, career_goal, study_hours,password,current_level,
       programming_experience,
        interests,
        learning_style, email, verified=False, verification_code=None):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.education = education
        self.career_goal = career_goal
        self.study_hours = study_hours
        self.password = password
        self.current_level = current_level
        self.programming_experience = programming_experience
        self.interests = interests
        self.learning_style = learning_style
        self.email = email
        self.verified = verified
        self.verification_code = verification_code

    def display_profile(self):
        print("\n----- User Profile -----")
        print(f"ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Education: {self.education}")
        print(f"Career Goal: {self.career_goal}")
        print(f"Study Hours per Day: {self.study_hours}")
        print(f"Current Level: {self.current_level}")
        print(f"Programming Experience: {self.programming_experience}")
        print(f"Interests: {self.interests}")
        print(f"Learning Style: {self.learning_style}")    
    def update_profile(self, name, age, education, career_goal, study_hours):
      self.name = name
      self.age = age
      self.education = education
      self.career_goal = career_goal
      self.study_hours = study_hours    
    def to_dict(self):
      return {
        "user_id": self.user_id,
        "name": self.name,
        "age": self.age,
        "education": self.education,
        "career_goal": self.career_goal,
        "study_hours": self.study_hours,
        "password": self.password,
        "current_level": self.current_level,
        "programming_experience": self.programming_experience,
        "interests": self.interests,
        "learning_style": self.learning_style,
        "email": self.email,
        "verified": self.verified,
        "verification_code": self.verification_code }  
