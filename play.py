import wordlebot as wb
color_id = {'G': 2, 'Y': 1, 'B': 0}
controls = ['Q', 'q', 'r', 'R']
colors = ['G', 'g', 'y', 'Y', 'b', 'B']
bot = wb.WordleBot()
print(f"Welcome to WordleBot! R=restart. Q=quit. Input your guess and its pattern [G, Y, B]. \n")
guess = ""
while True:
    while(guess not in controls and len(guess) != 5):
        guess = input("Guess/R/Q: ")
    if guess.upper() == "Q":
        break
    if guess.upper() == "R":
        print(f"New game! \n")
        bot.restart()
        while(guess not in controls and len(guess) != 5):
            guess = input("Guess/R/Q: ")
    pattern = []
    for i in range(5):
        color = '0'
        while (color not in colors):
            color = input(f"\tColor {i+1}: ")[0]
        pattern.append(color_id[color.upper()])
    bot.observe(guess, tuple(pattern))
    guess = color = ""