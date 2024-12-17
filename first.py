print('hello world')

more_fruits = ["apple", "banana", "cherry", "date", "fig", "grape"]

# Getting a slice
first_three = more_fruits[:3]       # Elements from the start up to index 3 (not included)
middle_two = more_fruits[2:4]       # Elements from index 2 to 4 (not included)
last_two = more_fruits[-2:]         # The last two elements

print("First three fruits:", first_three)
print("Middle two fruits:", middle_two)
print("Last two fruits:", last_two)

numbers = [1, 2, 3, 4, 5]
squares = [x ** 2 for x in numbers]

print("Original numbers:", numbers)
print("Squares:", squares)

numbers = [1, 2, 3, 4, 5, 6]
evens = [x for x in numbers if x % 2 == 0]

print("Even numbers:", evens)

names = ["Alice", "Bob", "Charlie", 'aa']
scores = [85, 90, 78,88]

combined = list(zip(names, scores))
print("Combined list:", combined)


nested_list = [[1, 2, 3], [4, 5], [6, 7, 8]]

# Flattened list
flattened = [item for sublist in nested_list for item in sublist]
print("Flattened list:", flattened)


items = ["apple", "banana", "cherry"]

# Using enumerate to get index and value
for index, value in enumerate(items):
    print(f"Item {index}: {value}")


# Check if all elements are positive
numbers = [-1, 1, 2, 3, 4, 5]
all_positive = all(x > 0 for x in numbers)

# Check if any element is negative
any_negative = any(x < 0 for x in numbers)

print("All positive:", all_positive)
print("Any negative:", any_negative)


from collections import Counter

# List of fruits with duplicates
fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Count occurrences of each fruit
fruit_counts = Counter(fruits)

print("Fruit counts:", fruit_counts)


from itertools import chain

# Nested list
nested_list = [[1, 2, 3], [4, 5], [6, 7, 8]]

# Flattened list using chain
flattened_list = list(chain(*nested_list))

print("Flattened list:", flattened_list)


# List with duplicates
numbers = [1, 2, 2, 3, 4, 4, 5]

# Convert to a set to remove duplicates
unique_numbers = list(set(numbers))

print("Unique numbers:", unique_numbers)


from itertools import zip_longest

# Unequal lists
names = ["Alice", "Bob", "Charlie"]
scores = [85, 90]

# Zip with default fill value
combined = list(zip_longest(names, scores, fillvalue="No Score"))

print("Combined with fill values:", combined)




with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a new file.")

with open("output.txt", "a") as file:
    file.write("\nAdding more content.")


import json

data = {"name": "Alice", "age": 25, "city": "New York"}

# Write JSON data to a file
with open("data.json", "w") as file:
    json.dump(data, file)