import pickle
from tkinter import N
import matplotlib.pyplot as plt

filename = "1000events_1MeV_realscale"

path = "data_files/"
format = ".pkl"

f = open(path + filename + format, 'rb')
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
n_events = len(all_events_1)

# with open(path + filename + '_rebinned' + format, 'wb') as f:
#     pickle.dump(events_1_rebinned, f)

for i in range(len(all_events_1)):
    plt.bar([4 * i for i in range(len(events_1_rebinned[i]))], events_1_rebinned[i], width=4, align="center")
    # plt.title(f"Event {i}/{n_events}")
    plt.title("Simulation of a 1 MeV muon detection")
    plt.xlim(0, 200)
    plt.xlabel("time (ns)")
    plt.ylabel("photon count")
    plt.show()