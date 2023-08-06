import numpy as np
import plotly.express as px
import pandas as pd,sys
from scipy import signal
from matplotlib import pyplot as plt

def s_bode_vs_freqs_vs_mano():
    b, a = signal.cheby2(4, 40, 100, 'low', analog=True)
    ##### b,a bode diagramm
    w, h = signal.freqs(b, a)
    plt.semilogx(w, 20 * np.log10(abs(h)))
    plt.title('Chebyshev Type II frequency response (rs=40)')
    plt.xlabel('Frequency [radians / second]')
    plt.ylabel('Amplitude [dB]')
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.axvline(100, color='green') # cutoff frequency
    plt.axhline(-40, color='green') # rs
    # plt.show()
    # NOTE:
    bode=pd.DataFrame([w/(2*np.pi),20 * np.log10(abs(h)),np.angle(h)*180/np.pi],index=['frequency(Hz)','gain(Db)','dephasage(degrees)']).T.set_index('frequency(Hz)')
    ##### b,a bode diagramm
    system = signal.TransferFunction(b,a, dt=0.05)
    s_bode=signal.dbode(system)
    s_bode=pd.DataFrame(s_bode,index=['frequency(Hz)','gain(Db)_db','dephasage(degrees)_db']).T.set_index('frequency(Hz)')
    s_bode.index=s_bode.index/(2*np.pi)
    fig1=px.scatter(s_bode.melt(ignore_index=False),facet_row='variable',log_x=True);fig1.update_traces(mode='lines+markers');fig1.update_yaxes(matches='x').show()
    fig2=px.scatter(bode.melt(ignore_index=False),facet_row='variable',log_x=True);fig2.update_traces(mode='lines+markers');fig2.update_yaxes(matches='x').show()

def sos_vs_ba_filter():
    b, a = signal.cheby2(4, 40, 100, 'low', analog=True)
    sos = signal.cheby2(4, 40, 100, 'low', analog=True,output='sos')

    b,a=signal.cheby2(12, 20, 17, 'hp', fs=1000, output='ba')
    sos=signal.cheby2(12, 20, 17, 'hp', fs=1000, output='sos')
    signal.dbode(b,a,10)
    b, a = signal.cheby2(4, 40, 100, 'hp', analog=True)
    w, h = signal.freqs(b, a)

# def analog_vs_digital():


# def pid_transfer_function():
kd,kp,ki=[1,1,1]
ss=signal.TransferFunction([kd,kp,ki],[1,0],dt=0.5)
w,h,phi=signal.dbode(ss)
sys.exit()

#####
