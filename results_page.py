import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def display_team_results(results_df):
    """
    Display team results in a well-aligned graphical format with headers and grouped roles.

    :param results_df: DataFrame with columns ['Team', 'Role', 'Name']
    """
    # Define team colors
    team_colors = {
        'BD': '#E57373',  # Red
        'FIN': '#64B5F6',  # Blue
        'MKT': '#81C784',  # Green
        'NPO': '#CE93D8',  # Purple
        'STRAT': '#9575CD'  # Dark Purple
    }

    # Unique teams and layout
    teams = results_df['Team'].unique()
    num_teams = len(teams)
    cols = 2  # Number of columns for display
    rows = (num_teams + 1) // cols

    # Create figure and axes
    fig, axes = plt.subplots(rows, cols, figsize=(8, rows * 2.5))
    axes = axes.flatten()

    # Loop through teams and plot their data
    for idx, team in enumerate(teams):
        ax = axes[idx]
        ax.axis('off')  # Hide axes

        # Add team header
        header_color = team_colors.get(team, '#D3D3D3')  # Default to grey if team not in dict
        ax.add_patch(FancyBboxPatch(
            (0.1, 0.85), 0.5, 0.15,  # Adjusted width to 0.8 and centered by starting at 0.1
            boxstyle="round,pad=0.05", fc=header_color, ec="none"
        ))
        ax.text(0.35, 0.89, team, fontsize=18, fontweight='bold', color='white', ha='center', va='center')

        # Get members of the team
        team_data = results_df[results_df['Team'] == team]
        roles = team_data.groupby('Role')['Name'].apply(list)

        # Display each role and its members with consistent spacing
        y_pos = 0.7
        for role, members in roles.items():
            ax.text(0.05, y_pos, f"{role}:", fontsize=12, fontweight='bold', ha='left', va='top')
            for member in members:
                ax.text(0.17, y_pos, member, fontsize=11, ha='left', va='top')
                y_pos -= 0.1
            y_pos -= 0.04  # Add spacing between roles

    # Remove unused axes
    for ax in axes[num_teams:]:
        ax.axis('off')

    # Adjust layout to reduce overlapping
    plt.tight_layout(pad=0.5)
    plt.show()
