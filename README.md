# PhaseDetection
A simple program to detect the phase of a spin echo signal.

This was created during my Masters' project. It allows for detection of the phase of a spin-echo signal (a wave pulse) from a spectrometer, which is an important parameter to determine, as it confirms the sample is responding in the intended way, and can provide information about its resonance characteristics.

Phase is detected via a (real) fast Fourier transform (provided by NumPy), with a large padding to the signal to allow the high resolution of frequency detection necessary.

This program also uncovered a systematic experimental error in our spectrometer. The detected signal has both quadrature and in-phase components, which ought to have a phase difference of -0.5 pi (the same as 1.5 pi), however this is closer to -0.45 pi (the same as 1.55 pi), as can be seen from running the program with the demo data. This could be, for instance, due to a difference in cable lengths.

The program takes input data from a MATLAB .mat data file containing in_phase_echo and quadrature_echo columns. One such file (200MHz Sine - BDPA.mat), from measurements of a BDPA sample, is provided. This file format is used because it can easily be saved and loaded using the SciPy.io library, but still allows quick plotting and analysis using MATLAB.

Sample output data from the program, using the demo data, can be found in "Sample output.png".


Dependencies:
NumPy,
Matplotlib.PyPlot,
loadmat from SciPy.io
