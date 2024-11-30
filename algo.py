import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value

class TeamAssignmentOptimizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.team_list = ['BD', 'FIN', 'MKT', 'NPO', 'STRAT']
        self.role_list = ['PM', 'SC', 'RC']
        self.prob = LpProblem("Team_Assignment_Problem", LpMaximize)
        self.assignments = []
        # self.weights = {
        #     'score_weight': 1,
        #     'team_pref_weight': 1,
        #     'role_pref_weight': 1,
        #     'semester_weight': 1,
        #     'year_weight': 1,
        # }
        self.assignment_vars = None
        self.prepare_data()


    def prepare_data(self):
        # Normalize data and clean team preferences
        self.data['Team Preference'] = self.data['Team Preference'].str.replace(' ', '', regex=False)
        max_semester = self.data['ABA Semester'].max()
        max_year = self.data['School Year'].max()
        self.data['ABA Semester Norm'] = self.data['ABA Semester'] / max_semester
        self.data['School Year Norm'] = self.data['School Year'] / max_year

    def solve(self, weights):

        # LP Problem setup

        # Define weights for score, ABA semester, and year
        score_weight = 1   # Weight for score
        team_pref_weight = 1  # Weight for team preference
        role_pref_weight = 1  # Weight for role preference
        semester_weight = 1  # Weight for ABA Semester
        year_weight = 1  # Weight for Year

        # Create decision variables for assigning self.data to teams and roles
        assignment = LpVariable.dicts(
            "Assign", 
            ((name, team, role) for name in self.data['Name']
            for team in self.team_list
            for role in self.role_list), 
            cat="Binary"
        )

        # Create the optimization problem
        prob = LpProblem("Team_Assignment_Problem", LpMaximize)

        # Objective function: Maximize the preferences and use scores for tie-breaking
        # Preference scoring: 3 points for 1st preference, 2 for 2nd, 1 for 3rd
        team_preference_points = {
            team: {name: (3 - preferences.index(team)) * score / 5 if team in preferences else -1
                for name, preferences, score in zip(self.data['Name'], self.data['Team Preference'].str.split(','), self.data['Score'])}
            for team in self.team_list
        }

        # Calculate role preference points with normalized weights
        role_preference_points = {
            role: {
                name: (
                    1 if role == role_pref else  # No loss for preferred role
                    -5 * score * aba_norm * year_norm if role_pref == 'PM' and role == 'SC' else  # Small loss for PM prefers SC
                    -100 * aba_norm * year_norm if role_pref == 'PM' and role == 'RC' else  # Huge loss for PM prefers RC
                    -100 * aba_norm * year_norm if role_pref == 'SC' and role == 'PM' else  # Huge loss for SC prefers PM
                    -5 * score * aba_norm * year_norm if role_pref == 'SC' and role == 'RC' else  # Small loss for SC prefers RC
                    -100 * aba_norm * year_norm if role_pref == 'RC' else  # Huge loss for RC prefers any other role
                    0  # Default penalty
                )
                for name, role_pref, score, aba_norm, year_norm in zip(
                    self.data['Name'],
                    self.data['Role Preference'],
                    self.data['Score'],
                    self.data['ABA Semester Norm'],
                    self.data['School Year Norm']
                )
            }
            for role in self.role_list
        }

        # Objective Function
        prob += lpSum(
            assignment[(name, team, role)] *
            (
                #score_weight * float(score) +
                # semester_weight * self.data.loc[self.data['Name'] == name, 'ABA Semester Norm'].values[0] +
                # year_weight * self.data.loc[self.data['Name'] == name, 'School Year Norm'].values[0] +
                team_pref_weight * team_preference_points[team][name] +
                role_pref_weight * role_preference_points[role][name]
            )
            for name, score in zip(self.data['Name'], self.data['Score'])
            for team in self.team_list
            for role in self.role_list
        )

        # Constraints for roles: Each team must have 2 PMs and 2 SCs
        for team in self.team_list:
            prob += lpSum(assignment[(name, team, 'PM')] for name in self.data['Name']) == 2, f"PM_Constraint_{team}"
            prob += lpSum(assignment[(name, team, 'SC')] for name in self.data['Name']) == 2, f"SC_Constraint_{team}"
            prob += lpSum(assignment[(name, team, 'RC')] for name in self.data['Name']) <= 3, f"Max_RC_Constraint_{team}"


        # Ensure everyone is assigned to exactly one team and one role
        for name in self.data['Name']:
            prob += lpSum(assignment[(name, team, role)] for team in self.team_list for role in self.role_list) == 1, f"One_Choice_Per_Candidate_{name}"

        # Solve the problem
        prob.solve()

        # Parse results and display them
        assignments = []

        for index, row in self.data.iterrows():
            name = row['Name']
            team_preferences = row['Team Preference'].split(',')
            role_preference = row['Role Preference']
            
            for team in self.team_list:
                for role in self.role_list:
                    if value(assignment[(name, team, role)]) == 1:
                        # Determine the ranking of the assigned team (1st, 2nd, 3rd, or No Preference)
                        if team in team_preferences:
                            team_rank = team_preferences.index(team) + 1
                        else:
                            team_rank = "No Preference"
                        
                        # Determine if the assigned role is the preferred role
                        role_match = "Yes" if role == role_preference else "No"
                        
                        # Add the assignment details to the list
                        assignments.append({
                            "Name": name,
                            "Team": team,
                            "Role": role,
                            "Team Rank": f"{team_rank}{'st' if team_rank == 1 else 'nd' if team_rank == 2 else 'rd' if team_rank == 3 else ''}",
                            "Preferred Role": role_match
                        })

        # Create a DataFrame to display the assignments
        assignments_df = pd.DataFrame(assignments)

        # Define a custom sort order for the Role column
        role_order = ["PM", "SC", "RC"]
        assignments_df['Role'] = pd.Categorical(assignments_df['Role'], categories=role_order, ordered=True)

        # Sort by Team and then by the custom Role order
        assignments_df = assignments_df.sort_values(by=['Team', 'Role'], ascending=[True, True])
        
        return assignments_df