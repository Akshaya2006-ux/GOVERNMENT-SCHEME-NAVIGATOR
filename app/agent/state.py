class AgentState:

    def __init__(self, user_query=""):

        self.user_query = user_query

        self.user_profile = {
            "age": None,
            "gender": None,
            "state": None,
            "occupation": None,
            "income": None,
            "category": None
        }

        self.goal = None

        self.observations = []

        self.actions_taken = []

        self.candidate_schemes = []

        self.eligible_schemes = []

        self.final_answer = None

    def add_observation(self, observation):
        self.observations.append(observation)

    def add_action(self, action):
        self.actions_taken.append(action)

    def update_profile(self, key, value):
        self.user_profile[key] = value

    def show_state(self):

        print("\n========== AGENT STATE ==========")

        print("User Query:", self.user_query)

        print("\nUser Profile:")
        for key, value in self.user_profile.items():
            print(f"  {key}: {value}")

        print("\nGoal:", self.goal)

        print("\nActions Taken:")
        for action in self.actions_taken:
            print(" ", action)

        print("\nObservations:")
        for observation in self.observations:
            print(" ", observation)

        print("=================================\n")