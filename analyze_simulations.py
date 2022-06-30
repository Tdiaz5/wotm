import pickle
from tkinter import N
import matplotlib.pyplot as plt

filename = "1000events_1MeV.pkl"

f = open(filename, 'rb')
all_events_1, all_events_2 = pickle.load(f)
f.close()

def rebin(events, factor):
    new_events = []
    index = 0

    while index < len(events):
        new_bin = 0

        for i in range(factor):
            new_bin += events[index]
            index += 1
        
        new_events.append(new_bin)

    return new_events

events_1_rebinned = [rebin(event, 20) for event in all_events_1]
print(len(events_1_rebinned[0]))

n_events = len(all_events_1)

for i in range(len(all_events_1)):
    plt.bar([i for i in range(len(events_1_rebinned[i]))], events_1_rebinned[i])
    plt.title(f"Event {i}/{n_events}")
    plt.show()