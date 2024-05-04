def format_dancers(dancers):
    """Format a list of dancer names."""
    dancer_names = [dancer.name for dancer in dancers]
    if len(dancer_names) == 1:
        return dancer_names[0]
    elif len(dancer_names) == 2:
        return " and ".join(dancer_names)
    else:
        return ", ".join(dancer_names[:-1]) + ", and " + dancer_names[-1]
    