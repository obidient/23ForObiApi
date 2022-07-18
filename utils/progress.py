

def calculate_progress_percentage(current_value, total_value=23):
    try:
        return int(100 * (current_value / total_value))
    except ZeroDivisionError:
        return 0
