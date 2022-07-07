import ROOT
import pickle

filename = "modules.root"

f = ROOT.TFile.Open(filename, "READ")
tree = f.Get("DepositionGeant4")
hist1 = tree.Get("detection_time_scintillator_box1")
hist2 = tree.Get("detection_time_scintillator_box2")

# format to python lists
nbins = 1000
n_events = 10

all_events_1 = [[hist1.GetBinContent(x, y) for x in range(nbins)] for y in range(n_events)]
all_events_2 = [[hist2.GetBinContent(x, y) for x in range(nbins)] for y in range(n_events)]

with open('output.pkl', 'wb') as f:
    pickle.dump([all_events_1, all_events_2], f)