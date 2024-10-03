# Mad Libs Generator

# Asking the user for inputs
noun1 = input("Enter a noun: ")
adjective1 = input("Enter an adjective: ")
verb1 = input("Enter a verb: ")
noun2 = input("Enter another noun: ")
adjective2 = input("Enter another adjective: ")
verb2 = input("Enter another verb: ")

# Creating the story
story = f"Once upon a time, there was a {adjective1} {noun1} who loved to {verb1}. \
One day, the {noun1} found a {adjective2} {noun2} and decided to {verb2} it. \
And they lived happily ever after!"

# Printing the story
print("\nHere is your Mad Libs story:")
print(story)
