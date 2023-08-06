# loop over the Tast epoc, calc the laser frequency during the taste, draw a stim block and write freq.


trans = btt(ax.transData,ax.transAxes)



laser_freqs = np.zeros(len(d.epocs.Tast.onset))
# pull the peaks into a dataframe, have the laser frequency as a variable.

for i,(b,e) in enumerate(zip(d.epocs.Tast.onset,d.epocs.Tast.offset)):
    pulse_m = (d.epocs.LsrP.onset>b)&(d.epocs.LsrP.onset<e)
    pulses = d.epocs.LsrP.onset[pulse_m]
    dur = (d.epocs.LsrP.offset[pulse_m] - d.epocs.LsrP.onset[pulse_m]).mean()
    freq = np.round(1/np.diff(pulses).mean(),0)
    laser_freqs[i] = freq
    pulse_coll = BBHcoll(np.c_[pulses,np.repeat(dur,len(pulses))],(0.5,0.1),transform = trans, color = 'darkcyan')
    ax.add_collection(pulse_coll)
    sR = Rect((b,0.85),width = e-b, height = 0.1, transform = trans, color = 'blue', alpha = 0.5)
    # draw each patch (as a collection?)
    ax.add_patch(sR)
    ax.text(b,0.85,"%d" % freq,size = 10, color = 'black', transform = trans)
