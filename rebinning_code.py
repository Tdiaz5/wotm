import pickle
from tkinter import N
import matplotlib.pyplot as plt

# ------------- PARAMETERS TO EDIT -----------------
filename = "1000events_1MeV_realscale"
path = "data_files/"
format = ".pkl"
rebinning_factor = 20
# --------------------------------------------------

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

events_1_rebinned = [rebin(event, rebinning_factor) for event in all_events_1]
events_2_rebinned = [rebin(event, rebinning_factor) for event in all_events_2]

with open(path + filename + '_rebinned' + format, 'wb') as f:
    pickle.dump(events_1_rebinned, events_2_rebinned, f)

# plotting code
# for i in range(len(all_events_1)):
#     plt.bar([4 * i for i in range(len(events_1_rebinned[i]))], events_1_rebinned[i], width=4, align="center")
#     plt.title("Simulation of a 1 MeV muon detection")
#     plt.xlabel("time (ns)")
#     plt.ylabel("photon count")
#     plt.show()