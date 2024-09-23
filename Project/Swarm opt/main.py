import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from pso import City, PSO, create_distance_matrix
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('medium.csv', header=None)

# Extract the first and second columns as numpy arrays
x = df.iloc[:, 0].to_numpy()
y = df.iloc[:, 1].to_numpy()

# Create a numpy array of shape (n, 2) where n is the number of cities
coords = np.stack((x, y), axis=1)

# Create a list of City objects from the coordinates
cities = [City(x, y) for x, y in coords]

# Create a distance matrix using the City objects
distance_matrix = create_distance_matrix(cities)


class PSOGUI:
    def __init__(self, master, cities):
        self.cities = cities
        master.title("PSO Configuration")
        master.geometry("400x250")

        # Create labels and entry fields
        iter_label = ttk.Label(master, text="Iterations:")
        iter_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.iter_entry = ttk.Entry(master)
        self.iter_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        pop_size_label = ttk.Label(master, text="Population Size:")
        pop_size_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.pop_size_entry = ttk.Entry(master)
        self.pop_size_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        pbest_prob_label = ttk.Label(master, text="Pbest Probability:")
        pbest_prob_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.pbest_prob_entry = ttk.Entry(master)
        self.pbest_prob_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        gbest_prob_label = ttk.Label(master, text="Gbest Probability:")
        gbest_prob_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.gbest_prob_entry = ttk.Entry(master)
        self.gbest_prob_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Create submit button
        submit_button = ttk.Button(master, text="Create PSO", command=self.create_pso)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_pso(self):
        iterations = int(self.iter_entry.get())
        population_size = int(self.pop_size_entry.get())
        pbest_probability = float(self.pbest_prob_entry.get())
        gbest_probability = float(self.gbest_prob_entry.get())

        # Assuming the PSO class is imported and instantiated as pso
        pso = PSO(iterations=iterations, population_size=population_size, pbest_probability=pbest_probability,
                  gbest_probability=gbest_probability, cities=cities)
        pso.run()

        # Store pso as a local variable
        self.pso = pso

        print(f'cost: {self.pso.gbest.pbest_cost}\t| gbest: {self.pso.gbest.pbest}')

        x_list, y_list = [], []
        for city in self.pso.gbest.pbest:
            x_list.append(city.x)
            y_list.append(city.y)
        x_list.append(self.pso.gbest.pbest[0].x)
        y_list.append(self.pso.gbest.pbest[0].y)
        fig = plt.figure(1)
        fig.suptitle('pso TSP')

        plt.plot(x_list, y_list, 'ro')
        plt.plot(x_list, y_list)
        plt.show(block=True)


def main():
    root = tk.Tk()
    app = PSOGUI(root, cities)
    root.mainloop()


if __name__ == "__main__":
    main()
