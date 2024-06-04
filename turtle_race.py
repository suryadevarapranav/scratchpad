import turtle
import time
import random

# define the constants for the dimensions of the game window
WIDTH, HEIGHT = 700, 600

# list of possible colors that could be assigned to the turtles.
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'black', 'purple', 'pink', 'brown', 'cyan']


def get_number_of_racers():
    """
	let the player be allowed to enter the number of turtle racers.
	check if the input is a valid number i.e. b/w 2 & 10.
	Returns:
		int: The number of racers.
	"""
    racers = 0
    while True:
        racers = input('Enter the number of racers (2 - 10): ')
        if racers.isdigit():  # Check if the input is numeric
            racers = int(racers)
        else:
            print('Input is not numeric... Try Again!')
            continue

        # Check if the number is within the valid range
        if 2 <= racers <= 10:
            return racers
        else:
            print('Number not in range 2-10. Try Again!')


def race(colors):
    """
	Conduct the turtle race.
	Args:
		colors (list): List of colors assigned to the turtles.
	Returns:
		str: The color of the winning turtle.
	"""
    # Create turtles with the given colors
    turtles = create_turtles(colors)

    while True:
        for racer in turtles:
            # Move the turtle forward by a random distance
            distance = random.randrange(1, 20)
            racer.forward(distance)

            # Check if the turtle has crossed the finish line
            x, y = racer.pos()
            if y >= HEIGHT // 2 - 10:
                return colors[turtles.index(racer)]  # Return the color of the winning turtle


def create_turtles(colors):
    """
	Create turtle objects for each racer.
	Args:
		colors (list): List of colors for the turtles.
	Returns:
		list: List of turtle objects.
	"""
    turtles = []
    # Calculate the spacing between the turtles
    spacingx = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        racer = turtle.Turtle()  # Create a new turtle
        racer.color(color)  # Set the turtle color
        racer.shape('turtle')  # Set the turtle shape
        racer.left(90)  # Point the turtle upwards
        racer.penup()  # Lift the pen to avoid drawing lines
        # Position the turtle at the starting line
        racer.setpos(-WIDTH // 2 + (i + 1) * spacingx, -HEIGHT // 2 + 20)
        racer.pendown()  # Put the pen down to start drawing
        turtles.append(racer)

    return turtles


def init_turtle():
    """
	Initialize the turtle screen.
	"""
    screen = turtle.Screen()  # Create a screen object
    screen.setup(WIDTH, HEIGHT)  # Set up the screen dimensions
    screen.title('Turtle Racing!')  # Set the screen title


# get the input number of turtle racers
racers = get_number_of_racers()

# Initialize the turtle game screen
# init_turtle()
# not working on mac but runs on this url: https://pythonsandbox.com/turtle until 8 turtles, 9, 10 some get cut off screen.

# Shuffle the colors and select the number of colors needed for the racers
random.shuffle(COLORS)
colors = COLORS[:racers]

# Conduct the race and determine the winner
winner = race(colors)
print("The winner is the turtle with color:", winner)

# Wait for a few seconds before closing the program
time.sleep(5)
