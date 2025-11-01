import itertools

with open("649all.txt", "w") as f:
    for combo in itertools.combinations(range(1, 50), 6):
        f.write(", ".join(map(str, combo)) + "\n")