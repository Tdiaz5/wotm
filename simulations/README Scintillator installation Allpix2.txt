#Simulations need to be run in stoomboot via SSH
#to get acces to stoomboot use a terminal in your private computer

#login to Nikhef
$ ssh -Y <nikhef_username>@login.nikhef.nl
$ <password>

#login to stoomboot
$ ssh -Y <nikhef_username>@stbc-i1.nikhef.nl
$ ssh -Y jdehaan@stbc-i1.nikhef.nl
$ <password>

#use the correct shell
$ /bin/zsh

#move to a folder with enough space (more than 1 GB)
#clone kvandenb repo
git clone https://gitlab.cern.ch/kvandenb/allpix-squared.git -b Scintillator_detector allpix-squared-scintillator

#make corrections in specific files before running cmake.

#Corrections to make the scintillator work with Geant4 version of 10.7 or higher

#open
$ ~/allpix-squared-scintillator/src/modules/DepositionGeant4/SensitiveScintillatorActionG4.cpp

#Correction 1
#Change 
G4bool SensitiveScintillatorActionG4::ProcessHits(G4Step* step, G4TouchableHistory*) {
    // Get the step parameters
    auto edep = step->GetTotalEnergyDeposit();
    G4StepPoint* preStepPoint = step->GetPreStepPoint();
    G4StepPoint* postStepPoint = step->GetPostStepPoint(); 

#Into
G4bool SensitiveScintillatorActionG4::ProcessHits(G4Step* step, G4TouchableHistory*) {
    // Get the step parameters
    G4StepPoint* preStepPoint = step->GetPreStepPoint();
    if(step->GetTrack()->GetDynamicParticle()->GetPDGcode() == -22){
        step->SetTotalEnergyDeposit(preStepPoint->GetTotalEnergy());
        step->GetTrack()->SetTrackStatus(fStopAndKill);
    }
   auto edep = step->GetTotalEnergyDeposit();
    G4StepPoint* postStepPoint = step->GetPostStepPoint();

#Correction 2
#Change:
// Add new hit if the number of hits is more than zero and the particle is an optical photon
    if(edep == 0 || step->GetTrack()->GetDynamicParticle()->GetPDGcode() != 0) {
        return false;
    }

#Into:
// Add new hit if the number of hits is more than zero and the particle is an optical photon
  if(edep == 0 || step->GetTrack()->GetDynamicParticle()->GetPDGcode() != -22) {
        return false;
    }

#Correction 3
#Change: 
// LOG(DEBUG) << "Geant4 transformation to local: " << Units::display(deposit_position_g4loc, {"mm", "um"});
    if((deposit_position_g4loc - deposit_position).mag2() > 0.001) {
        LOG(ERROR) << "Difference G4 to internal: "
                   << Units::display((deposit_position_g4loc - deposit_position), {"mm", "um"});
    }

#Into:
// LOG(DEBUG) << "Geant4 transformation to local: " << Units::display(deposit_position_g4loc, {"mm", "um"});
   if((deposit_position_g4loc - deposit_position).mag2() > 0.001) {
        LOG(DEBUG) << "Difference G4 to internal: "
                   << Units::display((deposit_position_g4loc - deposit_position), {"mm", "um"});
    }

#Corrections to make the simulation to discriminate per event.

#open ~/allpix-squared-scintillator/src/modules/DepositionGeant4/DepositionGeant4Module.cpp 

#Correction 4
#Change: 
for(auto& deposits : sensor->getDeposits()) {
                energies_[sensor->getName()]->Fill(1e6 * deposits.getEnergy());
                wavelengths_[sensor->getName()]->Fill(deposits.getWavelength());
                emission_time_[sensor->getName()]->Fill(deposits.getEmissionTime());
                detection_time_[sensor->getName()]->Fill(deposits.getDetectionTime());
                travel_time_[sensor->getName()]->Fill(deposits.getDetectionTime() - deposits.getEmissionTime());

#Into:
for(auto& deposits : sensor->getDeposits()) {
                energies_[sensor->getName()]->Fill(1e6 * deposits.getEnergy());
                wavelengths_[sensor->getName()]->Fill(deposits.getWavelength());
                emission_time_[sensor->getName()]->Fill(deposits.getEmissionTime());
                detection_time_[sensor->getName()]->Fill(deposits.getDetectionTime(), event->number);
                travel_time_[sensor->getName()]->Fill(deposits.getDetectionTime() - deposits.getEmissionTime());

#Correction 5
#Change:
// Plot axis are in kilo electrons - convert from framework units!
        auto maximum_charge = static_cast<int>(Units::convert(config_.get<int>("output_scale_charge", 100), "ke"));
        auto maximum_hits = config_.get<int>("output_scale_hits", 10000);
        auto maximum_wavelength =
            static_cast<int>(Units::convert(config_.get<double>("output_scale_wavelength", 1e-3), "nm"));
        auto maximum_energy = static_cast<int>(Units::convert(config_.get<double>("output_scale_energy", 1e-5), "eV"));
        auto maximum_time = config_.get<int>("output_scale_time", 200);

        auto nbins_charge = 5 * maximum_charge;
        auto nbins_hits = maximum_hits / 10;
        auto nbins_wavelength = maximum_wavelength;
        auto nbins_time = 5 * maximum_time;

#Into:
// Plot axis are in kilo electrons - convert from framework units!
        auto maximum_charge = static_cast<int>(Units::convert(config_.get<int>("output_scale_charge", 100), "ke"));
        auto maximum_hits = config_.get<int>("output_scale_hits", 10000);
        auto maximum_wavelength =
            static_cast<int>(Units::convert(config_.get<double>("output_scale_wavelength", 1e-3), "nm"));
        auto maximum_energy = static_cast<int>(Units::convert(config_.get<double>("output_scale_energy", 1e-5), "eV"));
        auto maximum_time = config_.get<int>("output_scale_time", 200);
        auto number_of_events = config_.get<int>("number_of_events", 1);

        auto nbins_charge = 5 * maximum_charge;
        auto nbins_hits = maximum_hits / 10;
        auto nbins_wavelength = maximum_wavelength;
        auto nbins_time = config.get<int>("nbins_time",1000);

#Correction 6
#Change:
            emission_time_[sensor->getName()] = new TH1D(
                plot_name_emission_time.c_str(), "emission_time; emission_time[ns] ;photons", nbins_time, 0, maximum_time);
            detection_time_[sensor->getName()] = new TH1D(plot_name_detection_time.c_str(),
                                                          "detection_time; detection_time[ns] ;photons",
                                                          nbins_time,
                                                          0,
                                                          maximum_time);

#Into:
            emission_time_[sensor->getName()] = new TH1D(
                plot_name_emission_time.c_str(), "emission_time; emission_time[ns] ;photons", nbins_time, 0, maximum_time);
            detection_time_[sensor->getName()] = new TH2D(plot_name_detection_time.c_str(),
                                                          "detection_time; detection_time[ns] ;photons",
                                                          nbins_time,
                                                          0,
                                                          maximum_time,
                                                          number_of_events,
                                                          0,
                                                          number_of_events);

#open ~/allpix-squared-scintillator/src/modules/DepositionGeant4/DepositionGeant4Module.hpp 

#Correction 7
#Change:
	#include <TH1D.h>

#Into:
	#include <TH1D.h>
	#include <TH2D.h>

#Correction 8
#Change:
        // Vector of histogram pointers for debugging plots
        std::map<std::string, TH1D*> charge_per_event_;
        std::map<std::string, TH1D*> hits_per_event_;
        std::map<std::string, TH1D*> energies_;
        std::map<std::string, TH1D*> wavelengths_;
        std::map<std::string, TH1D*> emission_time_;
        std::map<std::string, TH1D*> detection_time_;
        std::map<std::string, TH1D*> travel_time_;

#Into:
        // Vector of histogram pointers for debugging plots
        std::map<std::string, TH1D*> charge_per_event_;
        std::map<std::string, TH1D*> hits_per_event_;
        std::map<std::string, TH1D*> energies_;
        std::map<std::string, TH1D*> wavelengths_;
        std::map<std::string, TH1D*> emission_time_;
        std::map<std::string, TH2D*> detection_time_;
        std::map<std::string, TH1D*> travel_time_;

#open ~/allpix-squared-scintillator/src/tools/ROOT.h
#Correction 9

#change:
#include <TH1.h>

#into:
#include <TH1.h>
#include <TH2.h>

#Corrections to make the sourcing work

#Change the location of ini file in setup
#open ~/allpix-squared-scintillator/etc/scripts/setup_lxplus.sh

#Correction 10
#change:
source $ABSOLUTE_PATH/../../.ci/init_x86_64.sh

#into:
source /<your exact location>/allpix-squared-scintillator/.ci/init_x86_64.sh

# go to directory
$ cd allpix-squared-scintillator

#source the setup
$ source etc/scripts/setup_lxplus.sh

#Now run cmake
# go to directory
$ cd allpix-squared-scintillator

$ mkdir build
$ cd build
$ cmake ..
$ make install

#Run the example to check if the installation works

# go to directory
$ cd allpix-squared-scintillator/examples/

#Run the tutorial
$ /<your folder location>/allpix-squared-scintillator/bin/allpix -c scintillator_tutorial_config.conf 

#If this doesn't work, open the file:allpix -c scintillator_tutorial_config.conf 
#And comment out visualization, as this sometimes causes issues.

#GOOD Luck!!