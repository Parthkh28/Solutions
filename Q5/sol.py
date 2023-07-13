import pandas as pd

# Read the Excel file
df = pd.read_excel('TimeSeries.xlsx')

# Sort the data by Bot and Start Time
df.sort_values(['Bot', 'Start Time'], inplace=True)

# Initialize variables
current_bot = None
current_start = None
current_end = None
work_periods = []

# Iterate over the rows
for _, row in df.iterrows():
    bot = row['Bot']
    start_time = row['Start Time']
    end_time = row['End Time']

    if current_bot is None:
        current_bot = bot
        current_start = start_time
        current_end = end_time
    elif bot == current_bot and start_time <= current_end:
        # Update the current end time if the current task is within the previous task period
        current_end = max(current_end, end_time)
    else:
        # Add the current work period to the list
        work_periods.append((current_bot, current_start, current_end))

        # Start a new work period
        current_bot = bot
        current_start = start_time
        current_end = end_time

# Add the last work period to the list
work_periods.append((current_bot, current_start, current_end))

# Convert the list of work periods to a DataFrame
work_periods_df = pd.DataFrame(work_periods, columns=['Bot', 'Start Time', 'End Time'])

# Merge the activities for each work period
result = pd.merge(work_periods_df, df, on=['Bot', 'Start Time', 'End Time'], how='left')
result = result.groupby(['Bot', 'Start Time', 'End Time'])['Activity'].apply(list).reset_index()

# Print the result
print(result)
