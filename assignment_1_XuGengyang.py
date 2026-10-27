# Name: XuGengyang
# Assignment One

"""Assignment One: Turtle Drawing, QA Bot and Simple Calculator.

Run: python3 "assignment 1_XuGengyang.py"
Main menu: 1 = drawing, 2 = QA Bot, 3 = calculator, 0 = exit.
Drawing menu: 1 = squares, 2 = stars, 3 = triangles, 4 = combined pattern.
Drawings appear stroke by stroke, with a visible moving turtle.
Close the drawing window to return to the drawing menu.
Only Python's standard library is used.
"""

import colorsys
import math
import re


# Animation controls: 1 is slowest and 10 is fastest. Keep the speed above 0.
DRAWING_SPEED = 4
FRAME_DELAY_MS = 10


def draw_shape(pen, shape, radius, rotation, centre=(0, 0)):
    """Draw a centred shape; radius is the distance to an outer corner."""
    angle = math.radians(rotation)
    pen.penup()
    pen.goto(centre[0] + radius * math.cos(angle),
             centre[1] + radius * math.sin(angle))

    if shape == "star":
        # A star connects every second corner of a regular pentagon.
        length = 2 * radius * math.sin(2 * math.pi / 5)
        pen.setheading(rotation - 162)
        pen.pendown()
        for point in range(5):
            pen.forward(length)
            pen.right(144)
    else:
        sides = 4 if shape == "square" else 3
        length = 2 * radius * math.sin(math.pi / sides)
        pen.setheading(rotation + 90 + 180 / sides)
        pen.pendown()
        for side in range(sides):
            pen.forward(length)
            pen.left(360 / sides)


def draw_pattern(pen, screen, choice):
    """Use nested for loops and change the colour, length and rotation."""
    if choice == "1":
        shape = "square"
    elif choice == "2":
        shape = "star"
    elif choice == "3":
        shape = "triangle"
    else:
        shape = "square"

    pen.pensize(1.5)
    for step in range(40):
        # Increasing radius also increases the length of each drawn edge.
        radius = 24 + step * 4.5
        colour = colorsys.hsv_to_rgb(step / 40, 0.72, 1.0)
        pen.pencolor(colour)
        draw_shape(pen, shape, radius, 45 + step * 6)
        screen.update()

    if choice == "4":
        # Add an inner ring of triangles and an outer ring of stars.
        for step in range(24):
            angle = step * 15
            radians = math.radians(angle)
            pen.pencolor(colorsys.hsv_to_rgb(step / 24, 0.55, 1.0))
            centre = (233 * math.cos(radians), 233 * math.sin(radians))
            draw_shape(pen, "triangle", 9 + step % 3 * 2, angle, centre)
            centre = (278 * math.cos(radians), 278 * math.sin(radians))
            draw_shape(pen, "star", 8 + step % 4 * 2, angle + 90, centre)
            screen.update()

        pen.pencolor("#FFE6A0")
        pen.pensize(3)
        draw_shape(pen, "star", 22, 90)
        screen.update()


def show_drawing(choice):
    """Open a fresh window each time, so drawings can be selected repeatedly."""
    try:
        import tkinter as tk
        import turtle
    except ImportError:
        print("Drawing needs Python's tkinter and turtle modules.")
        return

    try:
        root = tk.Tk()
    except tk.TclError:
        print("Drawing needs a graphical desktop. No window could be opened.")
        print("Returning to the drawing menu.")
        return

    try:
        titles = {"1": "SQUARE PATTERN", "2": "FIVE-POINTED STAR PATTERN",
                  "3": "TRIANGLE PATTERN", "4": "SPECTRUM GARDEN"}
        root.title("XuGengyang - Assignment One - " + titles[choice])
        root.resizable(False, False)
        canvas = tk.Canvas(root, width=900, height=740, highlightthickness=0)
        canvas.pack()
        # A separate canvas avoids reusing a previously closed Turtle window.
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor("#091425")
        screen.colormode(1.0)
        screen.tracer(0, 0)
        pen = turtle.RawTurtle(screen)
        pen.hideturtle()
        pen.speed(0)

        pen.penup()
        pen.goto(0, 323)
        pen.color("#F3F6FF")
        pen.write(titles[choice], align="center", font=("Arial", 21, "bold"))
        pen.goto(0, 302)
        pen.color("#9AB2CE")
        pen.write("Watch the turtle draw each line | Colours and lengths change",
                  align="center", font=("Arial", 10, "normal"))
        pen.goto(0, -326)
        pen.write("When finished, click the picture to return to the drawing menu.",
                  align="center", font=("Arial", 11, "normal"))
        pen.goto(0, -348)
        pen.write("XuGengyang | Assignment One", align="center",
                  font=("Arial", 10, "normal"))

        # Show the labels immediately, then animate every drawing movement.
        # tracer(1) is essential: tracer(0) would disable stroke animation.
        screen.update()
        pen.penup()
        pen.goto(0, 0)
        pen.shape("turtle")
        pen.shapesize(0.65, 0.65)
        pen.speed(DRAWING_SPEED)
        pen.showturtle()
        screen.tracer(1, FRAME_DELAY_MS)
        print("Drawing step by step. Close the window at any time to return.")
        draw_pattern(pen, screen, choice)
        pen.hideturtle()
        screen.update()
        print("Drawing complete. Take a screenshot, then click the picture.")
        screen.onclick(lambda x, y: root.destroy())
        root.mainloop()
    except (turtle.Terminator, tk.TclError):
        print("Drawing window closed. Returning to the drawing menu.")
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass  # The user may already have closed the window.


def drawing_menu():
    while True:
        print("\n--- Drawing Menu ---")
        print("1. Squares")
        print("2. Five-pointed stars")
        print("3. Triangles")
        print("4. Colourful combined pattern")
        print("0. Back to main menu")
        choice = input("Choose a drawing (0-4): ").strip()
        if choice == "0":
            return
        elif choice in ("1", "2", "3", "4"):
            show_drawing(choice)
        else:
            print("Invalid choice. Please enter 0, 1, 2, 3, or 4.")


def get_bot_answer(question):
    """Match the five required keywords using if / elif / else."""
    # Match whole words: 'ai' should not accidentally match 'rain' or 'email'.
    words = re.findall(r"[a-z]+", question.lower())
    if not question.strip():
        return "Please type a question."
    elif "hku" in words:
        return "HKU stands for The University of Hong Kong."
    elif "robot" in words or "robots" in words:
        return ("A robot is a programmable machine that can perform tasks "
                "automatically or under human control.")
    elif "jetson" in words:
        return ("Jetson Nano is an NVIDIA embedded computer designed for "
                "AI and robotics projects.")
    elif "ai" in words or "artificial intelligence" in question.lower():
        return ("AI stands for Artificial Intelligence. It helps computers "
                "perform tasks such as learning, recognizing images, "
                "and understanding language.")
    elif "human" in words or "humans" in words:
        return ("A human is a person. Humans can think, communicate and "
                "create; they also design and guide AI systems.")
    else:
        return ("Sorry, I don't understand yet. Please ask about "
                "HKU, robot, jetson, ai, or human.")


def qa_bot():
    print("\n--- Question Answering Bot ---")
    print("Topics: HKU, robot, jetson, ai, human")
    print("Ask about one topic at a time. Example: What is Jetson Nano?")
    print("Enter 0 or back to return to the main menu.")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in ("0", "back", "exit", "quit", "bye"):
            print("Bot: Returning to the main menu.")
            return
        else:
            print("Bot:", get_bot_answer(question))


def read_number(prompt):
    """Keep asking after invalid input; 'back' cancels the calculator."""
    while True:
        text = input(prompt).strip()
        if text.lower() == "back":
            return None
        try:
            number = float(text)
            if math.isfinite(number):
                return number
            print("Please enter a finite number.")
        except ValueError:
            print("Invalid number. Try again, or type back to return.")


def calculator():
    while True:
        print("\n--- Simple Calculator ---")
        print("Operators: + (add), - (subtract), * (multiply), / (divide)")
        print("Enter 0 here, or type back at any prompt, to return to the main menu.")
        operator = input("Choose an operator (+, -, *, /): ").strip()
        if operator.lower() in ("0", "back"):
            return
        elif operator not in ("+", "-", "*", "/"):
            print("Invalid operator. Choose +, -, *, or /.")
            continue

        first = read_number("Enter the first number: ")
        if first is None:
            return
        second = read_number("Enter the second number: ")
        if second is None:
            return

        if operator == "+":
            result = first + second
        elif operator == "-":
            result = first - second
        elif operator == "*":
            result = first * second
        else:
            if second == 0:
                print("Cannot divide by zero. Please try another calculation.")
                continue
            result = first / second

        if math.isfinite(result):
            print("Result: {:g} {} {:g} = {:g}".format(
                first, operator, second, result))
        else:
            print("The result is too large. Please try smaller numbers.")


def main():
    print("Assignment One - XuGengyang")
    while True:
        print("\n--- Main Menu ---")
        print("1. Turtle Drawing")
        print("2. QA Bot")
        print("3. Simple Calculator")
        print("0. Exit")
        choice = input("Choose a function (0-3): ").strip()
        if choice == "1":
            drawing_menu()
        elif choice == "2":
            qa_bot()
        elif choice == "3":
            calculator()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 0, 1, 2, or 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
