def getValueDurations(tagPath, hours=1):
    """
    Get the duration for each value of a tag over a specified time period.

    Args:
        tagPath (str): The full tag path (e.g., "[default]TestHistorical/Humidity 1")
        hours (int/float): Number of hours to look back (default: 1)

    Returns:
        dict: Dictionary with values as keys and durations (in milliseconds) as values
    """

    # Define the date range
    end = system.date.now()
    start = system.date.addHours(end, -hours)

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

    return valueDurations


def printValueDurations(tagPath, hours=1):
    """
    Print the duration for each value of a tag over a specified time period.

    Args:
        tagPath (str): The full tag path (e.g., "[default]TestHistorical/Humidity 1")
        hours (int/float): Number of hours to look back (default: 1)
    """

    # Get the durations
    valueDurations = getValueDurations(tagPath, hours)

    # Print results
    print
    "Duration for each value over the past %.1f hour(s) for tag: %s" % (hours, tagPath)
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
