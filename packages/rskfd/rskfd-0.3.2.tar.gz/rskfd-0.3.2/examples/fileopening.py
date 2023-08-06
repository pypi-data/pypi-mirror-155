# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 2021

(C) 2021, Rohde&Schwarz, ramian
"""

def ConvertIiQq2Wv():
    '''
    Test
    '''
    import rskfd

    fs = 320e6
    data = rskfd.ReadIqw( r'\\Rsint.net\data\MU\SATURN\GROUP\GR_1E\TRANSFER\Reichert\signal\higher_qams.iiqq', iqiq=False)
    rskfd.WriteWv( data, fs, r'\\Rsint.net\data\MU\SATURN\GROUP\GR_1E\TRANSFER\Reichert\signal\higher_qams_DEC.wv')
    # rskfd.WriteBin( data, fs, r'C:\Users\ramian\Documents\waveforms\Keysight PXI Waveforms\WLAN_11be_320MHz_MCS13_dec.bin')
    rskfd.WriteIqTar( data, fs, r'\\Rsint.net\data\MU\SATURN\GROUP\GR_1E\TRANSFER\Reichert\signal\higher_qams_DEC.iq.tar')



def ReadFile( filename):
    '''
    Test
    '''
    import rskfd

    data,fs = rskfd.ReadWv( filename)
    print( f'RMS power in file: {rskfd.MeanPower( data)} dBm, peak power: {rskfd.MeanPower( data)} dBm.\n')
    rskfd.WriteWv( data, fs, 'myfilename.wv')

if __name__ == "__main__":
	# ReadFile( r'awgn_20kHz.wv')
    ConvertIiQq2Wv()