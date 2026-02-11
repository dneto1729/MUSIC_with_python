// Get the strip values and theoretical range from MUSIC simulation. Outputs
// to csv file with Left and Right channels seperated (not summed)
// CSV Format as (s0, s1L, s1R,...,s17, Range(mm), KE_heavy)
// usage in root
// root[#] .x simROOT_to_Values.C("InputFile.root")

#include <iostream>
#include <fstream>
// #include <iomanip>
// #include <sstream>
#include <vector>
#include <math.h>

#include "TFile.h"
#include "TString.h"
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"

using namespace std;

int Values_LR(string RFile){
    // Get branch from simulation data
    TFile *f1 = new TFile(RFile.c_str());
    TTree *simt = (TTree *)f1->Get("simt");
    // Setup reader to get momentum values
    TTreeReader myReader("simt");
    TTreeReaderArray<float> arr_left(myReader, "de_l"); // ΔE in Left Strips MeV
    TTreeReaderArray<float> arr_right(myReader, "de_r"); // ΔE in Right Strips MeV
    TTreeReaderValue<float> arr_s0(myReader, "stp0"); // ΔE in Strip0 MeV
    TTreeReaderValue<float> arr_s17(myReader, "stp17"); // ΔE in Strip17  MeV
    TTreeReaderArray<float> arr_Kh(myReader, "Kh"); // Energy of Heavy in MeV
    TTreeReaderValue<float> arr_xi(myReader, "xr"); // Reaction Vertex x in cm
    TTreeReaderValue<float> arr_yi(myReader, "yr"); // Reaction Vertex y in cm
    TTreeReaderValue<float> arr_zi(myReader, "zr"); // Reaction Vertex z in cm
    TTreeReaderValue<float> arr_xf(myReader, "xfe"); // Heavy Final x in cm
    TTreeReaderValue<float> arr_yf(myReader, "yfe"); // Heavy Final x in cm
    TTreeReaderValue<float> arr_zf(myReader, "zfe"); // Heavy Final x in cm
    // Initialize for storage
    // vector<float> stp_left;
    // vector<float> stp_right;
    // vector<float> Kh_eng;
    float th_range = 0.0;

    // Output CSV format file
    string outfile_name;
    outfile_name = RFile.substr (0, RFile.length() - 5);
    outfile_name += "_LR_output.dat";

    ofstream outfile;
    outfile.open(outfile_name);

    while (myReader.Next()){
        th_range = 0.0;
        vector<float> stp_left;
        vector<float> stp_right;
        vector<float> Kh_eng;

        for (auto left : arr_left){
            stp_left.push_back(left);
        }
        for (auto right : arr_right){
            stp_right.push_back(right);
        }
        for (auto heavy_eng : arr_Kh){
            Kh_eng.push_back(heavy_eng);
        }

        // Want range in mm
        th_range = 10 * sqrt((*arr_xf - *arr_xi) * (*arr_xf - *arr_xi) 
            + (*arr_yf - *arr_yi) * (*arr_yf - *arr_yi)
            + (*arr_zf - *arr_zi) * (*arr_zf - *arr_zi));

        outfile << *arr_s0 << ", " <<
        stp_left[0] << ", " << stp_right[0] << ", " <<
        stp_left[1] << ", " << stp_right[1] << ", " <<
        stp_left[2] << ", " << stp_right[2] << ", " <<
        stp_left[3] << ", " << stp_right[3] << ", " <<
        stp_left[4] << ", " << stp_right[4] << ", " <<
        stp_left[5] << ", " << stp_right[5] << ", " <<
        stp_left[6] << ", " << stp_right[6] << ", " <<
        stp_left[7] << ", " << stp_right[7] << ", " <<
        stp_left[8] << ", " << stp_right[8] << ", " <<
        stp_left[9] << ", " << stp_right[9] << ", " <<
        stp_left[10] << ", " << stp_right[10] << ", " <<
        stp_left[11] << ", " << stp_right[11] << ", " <<
        stp_left[12] << ", " << stp_right[12] << ", " <<
        stp_left[13] << ", " << stp_right[13] << ", " <<
        stp_left[14] << ", " << stp_right[14] << ", " <<
        stp_left[15] << ", " << stp_right[15] << ", " <<
        *arr_s17 << ", " << th_range << ", " << Kh_eng[0] << endl;                                 

        stp_left = {};
        stp_right = {};
        Kh_eng = {};

        // stp_left.close();
        // stp_right.close();
        // Kh_eng.close();

        }

    outfile.close();

    return 0;
}
