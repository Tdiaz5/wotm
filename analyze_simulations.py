import pickle
import matplotlib.pyplot as plt

filename = "scintillator_simulations.pkl"

f = open(filename, 'rb')
all_events_1, all_events_2 = pickle.load(f)
f.close()

n_events = len(all_events_1)

for i in range(len(all_events_1)):
    plt.plot(all_events_1[i])
    plt.title(f"Event {i}/{n_events}")
    plt.draw()
    plt.pause(0.1)
    plt.clf()