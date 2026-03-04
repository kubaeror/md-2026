with open("common/national_focus/md2026_ukr_focus.txt", "r") as f:
    lines = f.readlines()

# find the last "}" which was the original close, ignoring the new lines we just appended
original_content = "".join(lines)
