def format_instructors(instructors):
    """Format a list of instructor names."""
    instructor_names = [instructor.name for instructor in instructors]
    if len(instructor_names) == 1:
        return instructor_names[0]
    elif len(instructor_names) == 2:
        return " and ".join(instructor_names)
    else:
        return ", ".join(instructor_names[:-1]) + ", and " + instructor_names[-1]
    