import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat


#can generate dummy signal for testing purposes
'''
def dummy_signal(start, stop, delta_t):
    time = np.arange(start, stop, delta_t) #time is in nanoseconds

    frequencies = [214.1234, 215, 100] #MHz
    amplitudes = [30, 0.3, 0.4]
    phases = [3.9, 0.2, 0.3] #rad
    
    wave = np.zeros(len(time))
    for i in range(0, len(frequencies)):
        #0.001 is factor 10^3 because time is in ns and frequency in MHz
        wave += amplitudes[i] * np.cos(2 * np.pi * frequencies[i] * time * 0.001 + phases[i])
    
    #gaussian envelope
    envelope_width = 10
    envelope_centre = 50
    wave = wave * np.exp(- ((time - envelope_centre)/envelope_width) ** 2)
    
    #sinusoidal envelope
    #a_envelope = 1
    #phi_envelope = 0.2
    #f_envelope = 20 #MHz
    #wave = wave * a_envelope * np.cos(2 * np.pi * f_envelope * 0.001 * time + phi_envelope)

    return wave, time
'''


def measure_phase(input_signal, lower_cutoff_index=0):
    #Fourier transform
    sample_window_length = 1000000 #if this is bigger than size of input_signal, it will pad the signal with zeros
    ft = np.fft.rfft(input_signal, n = sample_window_length)
    
    #Find highest amplitude component
    amplitudes = np.abs(ft)
    max_amplitude_index = np.argmax(amplitudes) #returns index of highest amplitude component

    #Find phase of highest amplitude component
    phase = np.angle(ft[max_amplitude_index])

    #Optional phase compensation for different position of cut-out subset of the signal
    if lower_cutoff_index != 0:
        freq = np.fft.rfftfreq(sample_window_length) #frequency returned is cycles per sample
        main_freq = freq[max_amplitude_index]
        phase -= 2 * np.pi * np.abs(main_freq) * lower_cutoff_index
        phase -= 2 * np.pi #to make sure phase is negative before applying fmod
        phase = np.fmod(phase, 2 * np.pi) + 2 * np.pi

    return phase



#user-set parameters

#specifies what time range contains the echo
cutout_centre = 508 #ns
cutout_width = 80 #ns

sample_interval = 0.1  #ns - time elapsed between values of signal
time_of_signal_beginning = 0 #ns
time_of_signal_ending = 1000 #ns

t = np.arange(time_of_signal_beginning, time_of_signal_ending, sample_interval)





#load data
#for this data, sample_interval = 0.1 ns, time_of_signal_ending = 1000 (and of course time_of_signal_beginning = 0), cutout_centre = 508 ns, cutout_width = 80 ns
data = loadmat("200 MHz Sine - BDPA.mat")

in_phase_echo = data['in_phase_echo']
quadrature_echo = data['quadrature_echo']


#find indexes delimiting echo part of signal
lower_cutoff_index = np.where(t > cutout_centre - (cutout_width / 2))
lower_cutoff_index = (lower_cutoff_index[0])[0]
upper_cutoff_index = np.where(t < cutout_centre + (cutout_width / 2))
upper_cutoff_index = (upper_cutoff_index[0])[-1]

#cut out t and signal
t = t[lower_cutoff_index:upper_cutoff_index]
in_phase_echo = in_phase_echo[:,lower_cutoff_index:upper_cutoff_index]
quadrature_echo = quadrature_echo[:,lower_cutoff_index:upper_cutoff_index]

#measure phases
phases_from_in_phase_signal = np.zeros(np.shape(in_phase_echo)[0])
for i in np.arange(0, np.shape(in_phase_echo)[0]):
    phases_from_in_phase_signal[i] = measure_phase(in_phase_echo[i,:])

phases_from_quadrature_signal = np.zeros(np.shape(quadrature_echo)[0])
for i in np.arange(0, np.shape(quadrature_echo)[0]):
    phases_from_quadrature_signal[i] = measure_phase(quadrature_echo[i,:])





#output
in_phase_phase_deviation = np.std(phases_from_in_phase_signal)
in_phase_phase_mean = np.mean(phases_from_in_phase_signal)
print('\nPhase mean from in-phase signals = %s' % str(in_phase_phase_mean))
print('Phase standard deviation from in-phase signals = %s \n' % str(in_phase_phase_deviation))

quadrature_phase_deviation = np.std(phases_from_quadrature_signal)
quadrature_phase_mean = np.mean(phases_from_quadrature_signal)
print('Phase mean from quadrature signals = %s' % str(quadrature_phase_mean))
print('Phase standard deviation from quadrature signals = %s \n' % str(quadrature_phase_deviation))



quadrature_difference = phases_from_quadrature_signal - phases_from_in_phase_signal
quadrature_difference += 2 * np.pi
quadrature_difference = np.fmod(quadrature_difference, 2 * np.pi)

avg_quadrature_difference = np.mean(quadrature_difference)

print('Average difference (quadrature - in-phase) in units of pi = %s \n' % str(avg_quadrature_difference / np.pi))


#display the jth echo signal as a check the signal looks as expected
j=13 #unlucky for some...
plt.figure()
plt.plot(t, in_phase_echo[j,:], '-b', label='In-phase')
plt.plot(t, quadrature_echo[j,:], '-g', label='Quadrature')
plt.legend()
plt.xlabel('Time / ns')
plt.ylabel('Echo amplitude')
plt.title('Echo number ' + str(j))

echo_number = np.arange(1, len(phases_from_in_phase_signal) + 1)
plt.figure()
plt.plot(echo_number, phases_from_in_phase_signal, '-b', label='In-phase')
plt.plot(echo_number, phases_from_quadrature_signal, '-g', label='Quadrature')
plt.legend()
plt.xlabel('Echo number')
plt.ylabel('Detected phase / rad')

plt.show()