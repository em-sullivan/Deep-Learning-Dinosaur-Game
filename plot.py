import numpy as np
import matplotlib.pyplot as plt

# Open results file as a file object
f = open("Saved_Models/mod-resultsb.txt", "r")
# Return a list with each index a line of the file
lines = f.readlines()

generations = []
highest_scores = []
average_scores = []

# Extract the generations, highest scores, and average scores, and store them in individual lists
# Also convert each string to an integer or float
for i in lines:
    generations.append(int(i.split(',')[0]))
    highest_scores.append(int(i.split(',')[1]))
    average_scores.append(float(i.split(',')[2].rstrip("\n"))) # Get rid of any trailing newline characters

# Safely close the file
f.close()

num_gens = np.max(generations)

# print(generations)
# print(highest_scores)
# print(average_scores)

# Plot the data
x = np.array(generations)
y1 = np.array(average_scores)
y2 = np.array(highest_scores)

plt.plot(x, y1)
plt.plot(x, y2,
    color='red',
    linewidth=1.0)

plt.legend(['Average Score', 'Highest Score'])
plt.title("testb (" + str(num_gens) + " generations)")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.grid()
plt.show()