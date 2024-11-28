''' 
Most important factors of algorithm:
1. Weights
2. Loss formula for role placement (deteremines what factors merit people getting position they want)


'''

import pandas as pd
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value

# WEIGHTS

# Define weights for score, ABA semester, and year
score_weight = 2   # Weight for score
team_pref_weight = 1  # Weight for team preference
role_pref_weight = 1  # Weight for role preference
semester_weight = 1  # Weight for ABA Semester
year_weight = 1  # Weight for Year




# DataFrame Setup

# Load the CSV file
file_path = 'data.csv'  # Update with your file path if needed
data = pd.read_csv(file_path)

# Parse data into a usable format for optimization
candidates = data[['Name', 'Team Preference', 'Role Preference', 'Score', 'ABA Semester', 'Year']]
# Remove all spaces after commas in the 'Team Preference' column
candidates['Team Preference'] = candidates['Team Preference'].str.replace(' ', '', regex=False)

team_list = ['BD', 'FIN', 'MKT', 'NPO', 'STRAT']
role_list = ['PM', 'SC', 'RC']

# Normalize ABA Semester and Year for weighting purposes (optional)
max_semester = candidates['ABA Semester'].max()
max_year = candidates['Year'].max()

candidates['ABA Semester Norm'] = candidates['ABA Semester'] / max_semester
candidates['Year Norm'] = candidates['Year'] / max_year




# LP Problem setup

# Create decision variables for assigning candidates to teams and roles
assignment = LpVariable.dicts(
    "Assign", 
    ((name, team, role) for name in candidates['Name']
     for team in team_list
     for role in role_list), 
    cat="Binary"
)

# Create the optimization problem
prob = LpProblem("Team_Assignment_Problem", LpMaximize)

# Objective function: Maximize the preferences and use scores for tie-breaking
# Preference scoring: 3 points for 1st preference, 2 for 2nd, 1 for 3rd
team_preference_points = {
    team: {name: (3 - preferences.index(team)) if team in preferences else -1
           for name, preferences in zip(candidates['Name'], candidates['Team Preference'].str.split(','))}
    for team in team_list
}

# Calculate role preference points with normalized weights
role_preference_points = {
    role: {
        name: (
            1 if role == role_pref else  # No loss for preferred role
            -10 * aba_norm * year_norm if role_pref == 'PM' and role == 'SC' else  # Small loss for PM prefers SC
            -100 * aba_norm * year_norm if role_pref == 'PM' and role == 'RC' else  # Huge loss for PM prefers RC
            -100 * aba_norm * year_norm if role_pref == 'SC' and role == 'PM' else  # Huge loss for SC prefers PM
            -10 * aba_norm * year_norm if role_pref == 'SC' and role == 'RC' else  # Small loss for SC prefers RC
            -100 * aba_norm * year_norm if role_pref == 'RC' else  # Huge loss for RC prefers any other role
            0  # Default penalty
        )
        for name, role_pref, aba_norm, year_norm in zip(
            candidates['Name'],
            candidates['Role Preference'],
            candidates['ABA Semester Norm'],
            candidates['Year Norm']
        )
    }
    for role in role_list
}

# Objective Function
prob += lpSum(
    assignment[(name, team, role)] *
    (
        score_weight * float(score) +
        # semester_weight * candidates.loc[candidates['Name'] == name, 'ABA Semester Norm'].values[0] +
        # year_weight * candidates.loc[candidates['Name'] == name, 'Year Norm'].values[0] +
        team_pref_weight * team_preference_points[team][name] +
        role_pref_weight * role_preference_points[role][name]
    )
    for name, score in zip(candidates['Name'], candidates['Score'])
    for team in team_list
    for role in role_list
)

# Constraints for roles: Each team must have 2 PMs and 2 SCs
for team in team_list:
    prob += lpSum(assignment[(name, team, 'PM')] for name in candidates['Name']) == 2, f"PM_Constraint_{team}"
    prob += lpSum(assignment[(name, team, 'SC')] for name in candidates['Name']) == 2, f"SC_Constraint_{team}"
    # prob += lpSum(assignment[(name, team, 'RC')] for name in candidates['Name']) <= 2, f"Max_RC_Constraint_{team}"

# Ensure everyone is assigned to exactly one team and one role
for name in candidates['Name']:
    prob += lpSum(assignment[(name, team, role)] for team in team_list for role in role_list) == 1, f"One_Choice_Per_Candidate_{name}"

# Solve the problem
prob.solve()

# Parse results and display them
assignments = []

for index, row in candidates.iterrows():
    name = row['Name']
    team_preferences = row['Team Preference'].split(',')
    role_preference = row['Role Preference']
    
    for team in team_list:
        for role in role_list:
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
                    "Got Preferred Role": role_match
                })

# Create a DataFrame to display the assignments
assignments_df = pd.DataFrame(assignments)
assignments_df = assignments_df.sort_values(by=['Team', 'Role'], ascending=[True, True])

print(assignments_df)

# Output the result to a CSV file
# output_file = 'Team_Assignments.csv'
# assignments_df.to_csv(output_file, index=False)
# print(f"Team assignments have been saved to {output_file}.")