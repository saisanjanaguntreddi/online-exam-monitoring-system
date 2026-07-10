warning_count = 0


def add_warning():

    global warning_count

    warning_count += 1

    print(f"WARNING {warning_count}")

    return warning_count


def get_warning_count():

    return warning_count