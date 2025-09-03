import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from commpy.modulation import QAMModem
from commpy.channels import awgn
from commpy.filters import rrcosfilter

#%% 1. Parámetros
rolloff = 0.25  # Factor roll-off del filtro RRC
span = 16  # Expansión del filtro RRC
sps = 16  # Número de muestras por símbolo
num_sym = 10000  # Número de símbolos a transmitir
Rsym = 1e6  # Symbol Rate
Fs = Rsym * sps  # Sampling Frequency
M = 16 # Número de símbolos

constel = 1; #Si 1, muestra el diagrama de constelación
sweep_snr = 1  # Si 1, realiza el ciclo for con diferentes valores de SNR


#%% 2. Generación de Símbolos y Bits
sym_data = np.random.randint(0, M, num_sym)
# Convertir datos a bits
bit_data = np.array([np.binary_repr(x, width=int(np.log2(M))) for x in sym_data])  # Representación binaria
bit_data = np.array([[int(b) for b in bits] for bits in bit_data]).flatten()  # Convertir a array de bits

#%% 3. Modulación M-QAM

modem = QAMModem(M)

modData = modem.modulate(bit_data)

#%% 4. Formación de Pulsos

_, filtCoeff = rrcosfilter(span * sps, rolloff, 1 / Rsym, Fs) #el de la librería Commpy

plt.plot(filtCoeff, label=f'Roll-off = {rolloff}')
plt.title('Respuesta al Impulso RRC')
plt.grid()
plt.legend()
plt.show()

# Pulse shaping (Tx)
txSig = upfirdn(filtCoeff, modData, sps)

#%% 5. Diagrama de Ojo
def eyediagram(Sig, sps, span, rolloff, color, title):
    plt.figure()
    for i in range(sps*span, 3000, 2*sps):
        plt.plot(np.real(Sig[i:i+2*sps]), color)
    plt.title(title)
    plt.grid()
    plt.show()

eyediagram(txSig, sps, span, rolloff, color='b', title= f'Roll-Off {rolloff}, Señal Tx - In-Phase')


#%% 6. Curva de Errores vs SNR
snr = np.array([10, 12, 14, 16, 18, 20]) if sweep_snr else np.array([20])
error = np.zeros(len(snr))

for i, snr_val in enumerate(snr):
    rxSig = awgn(modData, snr_val)
    if constel == 1:
        plt.figure()
        plt.scatter(np.real(rxSig), np.imag(rxSig), label=f'SNR {snr_val}')
        plt.scatter(np.real(modData), np.imag(modData), marker='*', color='r', label='Constelación')
        plt.title(f'Diagrama de Constelación - SNR {snr_val}')
        plt.legend()
        plt.grid()
        plt.show()
    
    demodData = modem.demodulate(rxSig, 'hard')
    error[i] = np.sum(bit_data != demodData)

plt.figure()
plt.plot(snr, error, 'o-')
plt.title('Errores vs. SNR')
plt.xlabel('SNR [dB]')
plt.ylabel('Número de Errores')
plt.grid()
plt.legend(['16QAM rectangular'])
plt.show()

