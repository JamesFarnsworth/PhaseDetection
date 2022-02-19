# PhaseDetection
A simple program to detect and compensate for the phase of a spin echo.

This was created during my Masters' project. It allows for detection of the phase of a spin-echo signal (a wave pulse) from a spectrometer, which is an important parameter to determine, as it confirms the sample is responding in the intended way, and can provide information about its resonance characteristics.

This program also uncovered a systematic experimental error in our spectrometer. The detected signal has both quadrature and in-phase components, which ought to have a phase difference of -0.5 pi (the same as 1.5 pi), however this is closer to -0.45 pi (the same as 1.55 pi), as can be seen from the demo data. This could be, for instance, due to a difference in cable lengths.

The program takes input data from a MATLAB .mat data file containing in_phase_echo and quadrature_echo columns. One such file (200MHz Sine - BDPA.mat), from measurements of a BDPA sample, is provided.


Dependencies:

NumPy,
Matplotlib.PyPlot,
loadmat from SciPy.io,
