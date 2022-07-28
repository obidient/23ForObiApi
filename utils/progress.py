from bigfastapi.models import user_models


def calculate_progress_percentage(current_value, total_value=23):
    try:
        return int(100 * (current_value / total_value))
    except ZeroDivisionError:
        return 0


def top_contributors_in_a_village(voters_obj):
    check_list = []
    for contributor in voters_obj:
        check_list.append(contributor.delivered_by)

    dict_check_list = {}
    for name in check_list:
        dict_check_list[name] = dict_check_list.get(name, 0) + 1

    # sort the dict by value in descending order
    sorted_dict = sorted(dict_check_list.items(), key=lambda kv: kv[1], reverse=True)

    # return key of top 5 contributors
    return [x[0] for x in sorted_dict[:5]]
