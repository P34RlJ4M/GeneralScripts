# Define the tag path
tagPath = "[default]TestHistorical/Humidity 1"

# Define the date range (past hour)
end = system.date.now()
start = system.date.addHours(end, -1)

# Query the tag history
history = system.tag.queryTagHistory(
    paths=[tagPath],
    startDate=start,
    endDate=end,
    returnFormat='Wide',
    includeBoundingValues=True
)

# Dictionary to store duration for each value (in milliseconds)
valueDurations = {}

# Iterate through the history to calculate durations
for i in range(history.getRowCount()):
    value = history.getValueAt(i, 1)  # Column 1 is the tag value
    timestamp = history.getValueAt(i, 0)  # Column 0 is the timestamp

    # Calculate duration until next value change (or end time)
    if i < history.getRowCount() - 1:
        nextTimestamp = history.getValueAt(i + 1, 0)
        duration = nextTimestamp.getTime() - timestamp.getTime()
    else:
        # Last value extends to the end time
        duration = end.getTime() - timestamp.getTime()

    # Add duration to the value's total
    if value in valueDurations:
        valueDurations[value] += duration
    else:
        valueDurations[value] = duration

# Print results
print
"Duration for each value over the past hour:"
print
"-" * 80

totalDuration = 0
for value, duration in valueDurations.items():
    durationSeconds = duration / 1000.0
    durationMinutes = durationSeconds / 60.0
    totalDuration += duration

    print
    "Value: %s" % str(value)
    print
    "  Duration: %.2f seconds (%.2f minutes)" % (durationSeconds, durationMinutes)
    print
    "-" * 80

# Verify total
totalSeconds = totalDuration / 1000.0
totalMinutes = totalSeconds / 60.0
print
"Total Duration: %.2f seconds (%.2f minutes)" % (totalSeconds, totalMinutes)