# Author: Tobias den Hollander
# Data: 7-7-2022
#
# Converts our root file into python lists
# This is mostly useful so that further programs can be run without root

import ROOT
import pickle

# ------------- PARAMETERS TO EDIT -----------------
filename = "modules.root"
nbins = 1000
n_events = 10
# --------------------------------------------------


f = ROOT.TFile.Open(filename, "READ")
tree = f.Get("DepositionGeant4")
hist1 = tree.Get("detection_time_scintillator_box1")
hist2 = tree.Get("detection_time_scintillator_box2")

# format to python lists
all_events_1 = [[hist1.GetBinContent(x, y) for x in range(nbins)] for y in range(n_events)]
all_events_2 = [[hist2.GetBinContent(x, y) for x in range(nbins)] for y in range(n_events)]

with open('output.pkl', 'wb') as f:
    pickle.dump([all_events_1, all_events_2], f)