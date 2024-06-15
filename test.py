def grade_evaluation(grade):
    match grade:
        case "A" | "B":
            print("Excellent or Good job!")
        case "C":
            print("Well done")
        case "D":
            print("You passed")
        case "F":
            print("Better try again")
        case _:
            print("This is either A or another grade that's not specifically handled")

# Example usage
grade = "B"
grade_evaluation(grade)  # Prints: Excellent or Good job!


