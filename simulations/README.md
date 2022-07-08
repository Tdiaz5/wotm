Steps to make and analyze simulation data:
1. Make the data by running a setup with scintillators in our custom allpix squared
2. run `convert_root_to_python.py` to convert the data into python lists (don't forget to change the parameters at the top)
3. run `rebinning_code.py` to rebin to the desired number of bins
4. Look for decays. We were not able to complete this step: no second peaks were found. See `peak_testing_code.py`.