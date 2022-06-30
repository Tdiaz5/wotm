import ROOT
import pickle

filename = ""
f = ROOT.TFile.Open(filename, "READ")
tree = f.Get("DepositionGeant4")
hist1 = tree.Get("detection_time_scintillator_box1")
hist2 = tree.Get("detection_time_scintillator_box2")

# format to python lists
nbins = 1000
all_events_1 = [[hist1.GetBinContent(x, y) for x in range(nbins)] for y in range(nbins)]
all_events_2 = [[hist2.GetBinContent(x, y) for x in range(nbins)] for y in range(nbins)]

with open('scintillator_simulations.pkl', 'w') as f:
    pickle.dump([all_events_1, all_events_2], f)