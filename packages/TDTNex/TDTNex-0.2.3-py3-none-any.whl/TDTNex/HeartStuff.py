import tdt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 100000
import pandas as pd

#%matplotlib qt
import matplotlib.pyplot as plt
from scipy.signal import decimate, butter, sosfiltfilt, find_peaks
from scipy.stats import zscore, f_oneway
import scipy.stats as stats
import numpy as np
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
from math import floor, ceil
import pickle
import os
import glob, subprocess
import TDTNex

# mask to sem to change default NaN behavior
def sem(a):
    return stats.sem(a,nan_policy='omit')

plt.rcParams.update({'axes.labelsize':10,
                     'xtick.labelsize':8,
                     'ytick.labelsize':8})

def PlotHeartBeatRaster(QRS_event_idxs,QRS_EMG_idxs,QRStimes,lpad,rpad,EKGsig,WvSnipDps,EKGsigfs,
                        hist=True,bin_width=0.1,hist_yscale=None, 
                        lwds=1,lineoff=0.8,linelen=0.8,
                        inset_yscale=None,raster_color='black',max_segs = 300):
                                    
    evnts, evntsArray,raster_segs = QRSRaster(QRS_event_idxs,QRS_EMG_idxs,QRStimes,
                                              lpad,rpad,EKGsig,WvSnipDps,EKGsigfs)
    nsnips = len(evntsArray)
    if nsnips<1:
        print("fewer than 1 snips")
        return(None, (None, None, None,))
    f= plt.figure()
    raster_ax = plt.axes([0.15,0.15,0.6,0.6])
    hist_ax = plt.axes([0.15,0.75,0.6,0.25])
    wf_ax = plt.axes([0.75,0.75,0.25,0.25])
    raster_ax.eventplot(evnts,linewidths = lwds, linelengths = linelen, 
                        lineoffsets = lineoff, color = 'black')
    # have to do the inset axes, histogram
    wf_ax.patch.set_alpha(0.02)
    # want to limit the number of segs for sanity
    if raster_segs.shape[0]>max_segs:
        rand_seg_idxs = np.random.randint(0,raster_segs.shape[0]-1,size=max_segs)
        raster_segs=raster_segs[rand_seg_idxs,:,:]
    raster_snips = LineCollection(raster_segs, linewidths=0.25,
                            colors=raster_color, 
                            linestyle='solid')
    wf_ax.add_collection(raster_snips)
    wf_ax.set_xlim(0,raster_segs.shape[1])
    if inset_yscale is None:
        wf_ax.set_ylim(min(raster_segs[:,:,1].flatten()),max(raster_segs[:,:,1].flatten()))
    else:
        wf_ax.set_ylim(*inset_yscale)
    wf_ax.xaxis.set_visible(False)
    wf_ax.yaxis.set_visible(False)
    bh,bx = np.histogram(evntsArray,bins = np.r_[-lpad:0:bin_width,0:rpad+(bin_width*0.01):bin_width])
    hist_ax.bar(bx[0:-1],bh/len(QRS_event_idxs)/bin_width,width = bin_width, align='edge')
    hist_ax.set_ylabel("inst. freq Hz, %.2f" % bin_width)
    hist_ax.xaxis.set_visible(False)
    hist_ax.set_xlim(-lpad,rpad)
    if hist_yscale is not None:
        hist_ax.set_ylim(*hist_yscale)
    raster_ax.set_xlim(-lpad,rpad)
    raster_ax.set_xlabel("time (s)")
    raster_ax.set_ylabel("trail num.")
    f.set_size_inches(4,4)
    return f, (hist_ax, raster_ax, wf_ax)


def QRSRaster(QRS_event_idxs,QRS_EMG_idxs,QRStimes,lpad,rpad,EKGsig,EKGsnipdps,EKGfs):
    """Return a list of events, an array of all events, and set of waveform segments
    """
    # need there to be a zero shift snip alignment, has to have odd length
    if (EKGsnipdps%2)==0:
        EKGsnipdps+=1
    lpaddp = int(lpad*EKGfs)
    rpaddp = int(rpad*EKGfs)
    nsnips = int(np.array([QRS_EMG_idxs[(QRS_EMG_idxs>(idx-lpaddp))&(QRS_EMG_idxs<(idx+rpaddp))].
                             sum() for idx in QRS_event_idxs]).sum())
    if nsnips > len(QRStimes):
        nsnips = len(QRStimes)
    # set up the index shim for snip alignment, 
    # got cute with it, flip, self subtract and int divide to get zero centered vector
    shft = np.r_[0:EKGsnipdps] # hopefully this stays and int
    shft = (shft-shft[::-1])//2
    EKG_segs = np.zeros((len(QRS_EMG_idxs),EKGsnipdps,2))
    EKG_segs[:,:,0]=np.r_[range(len(shft))]
    # just get all the QRS snips, and then mask their indexes in the loop
    # try this with xs
    xs = np.linspace(0,dur,len(EKGsig))
    # now I need to broadcast the EKGidxs into an index matrix
    QRSEMGidx_mtrx = np.repeat(QRS_EMG_idxs[:,np.newaxis],len(shft),axis=1)+shft
    # note have to deal with edge cases where the heart beat occurs near the beginning or end of the signal
    # to do this, just zero pad the beginning and end of the signal by the snip length
    zpad = np.zeros(EKGsnipdps*2,dtype = EKGsig.dtype)
    EKG_segs[:,:,1]=np.r_[zpad,EKGsig,zpad][QRSEMGidx_mtrx+len(zpad)-1]
    EKGidxs_mask = np.zeros(len(QRS_EMG_idxs),dtype = bool)


    evntsArray = np.zeros((nsnips,))
    evnts = []
    _seg_idx = 0
    for Eidx in QRS_event_idxs:
        Etime = QRStimes[Eidx]
        peri_E_mask = (QRStimes>Etime-lpad)&(QRStimes<Etime+rpad)
        _QRSidxs = QRS_idxs[peri_E_mask]
        nQRS = len(_QRSidxs)
        EKGidxs_mask|=np.in1d(QRS_idxs,(_QRSidxs).astype(np.int))
        # I am plottin all the QRS times
        evnts.append(QRStimes[peri_E_mask]-QRStimes[Eidx]) # subtract t shift to zero
        evntsArray[_seg_idx:_seg_idx+nQRS]=evnts[-1]
        _seg_idx+=nQRS
    EKGidxs_mask = EKGidxs_mask.astype(bool)    
    raster_snips = LineCollection(EKG_segs[EKGidxs_mask,:,:], linewidths=0.25,
                                colors='black', 
                                linestyle='solid')
    return(evnts,evntsArray,EKG_segs[EKGidxs_mask])


# random main stuff:
if __name__=='__main__':
    # try this with a band pass filter.
    # from /home/matthew/Documents/LrN/StomachEMG_LrN/2020_06_05/ ...
    # this is a MWE as of 2020_06_12
    root_d = os.path.join(os.environ.get("HOME"),'Documents','LrN','StomachEMG_LrN','2020_06_05')
    tdtfn = os.path.join(root_d,'./2020_06_05_Intact05_Session02/AP(B)2755ML1444DV6426Exp-1/')
    nexfn = os.path.join(root_d,'./2020_06_05_Intact05_Session02_AP(B)2755ML1444DV6426Exp-1_sorted-better.nex')
    coordrecfn = os.path.join(root_d,"CoordRec_%s.pckl" % os.path.basename(os.path.splitext(nexfn)[0]))
    print(coordrecfn)
    try:
        with open(coordrecfn, 'rb') as pf:
            rec = pickle.load(pf)
    except FileNotFoundError:
        print('rec object not constructed yet:')
        rec = TDTNex.TDTNex(tdtfn,nexfn)
        with open(coordrecfn, 'wb') as pf:
            pickle.dump(rec,pf)

    fs = rec.tdt.streams.EMGx.fs
    sos = butter(4,[10,200],'bp',fs = fs,output = 'sos')
    #tstart = 1050
    #tend = 1100
    tstart = 0
    tend = rec.tdt.info.duration.total_seconds()
    subset = slice(int(tstart*fs),int(tend*fs))
    bp_abdom = zscore(sosfiltfilt(sos,rec.tdt.streams.EMGx.data[2,subset]))
    bp_abdom_ds = decimate(bp_abdom,int(fs/800)) # should drop to abound 800 Hz

    # find the peak of the QRS, in the un-downsampled signal
    idxs,peak_props = find_peaks(bp_abdom_ds,4)

    # lets decimate the signal for sanity
    bp_abdom_ds = decimate(bp_abdom,int(fs/800)) # should drop to abound 800 Hz
    xs = np.linspace(tstart,tend,len(bp_abdom_ds))
    f,ax = plt.subplots(1,1)

    # find the peak of the QRS
    idxs,peak_props = find_peaks(bp_abdom_ds,4)
    rt = xs[idxs]

    trans = transforms.blended_transform_factory(
        ax.transData, ax.transAxes)

    #ax.plot(xs,lp_stmach,lw=0.6)
    ax.plot(xs, bp_abdom_ds,lw = 0.6)
    ax.plot(rt,peak_props['peak_heights'],'or',ms = 3, lw = 0)

    # let's plot the instantaneous heart rate.
    HR = 1/np.diff(xs[idxs])

    # make a kernel, roll the kernel over the actual heart beat times (is this kosher?)
    # sobel like
    k = np.r_[np.ones(10)*-1,
              0,
              np.ones(10)]
    hr_conv = np.convolve(k,HR,mode ='same')
    # now lets find peaks for the rate changes
    # nows lets plot both
    plt.plot(rt[0:-1],hr_conv*0.5, color = 'magenta')

    # I think I need to use an edge finding kernel
    #plt.plot(xs[idxs][0:-1],zscore(HR))
    f.set_size_inches(15,5)
    for s,e in zip(rec.tdt.epocs.Blln.onset,
                   rec.tdt.epocs.Blln.offset):
        rect = mpatches.Rectangle((s, 0), width=e-s, height=1,
                                 transform=trans, color='black',
                                 alpha=0.3)

        ax.add_patch(rect)

    # with a left-handed sobel, these peaks are the beginning of bradycardias
    brady_ixs,bpp = find_peaks(hr_conv,height=10, distance = 7)
    tachy_ixs,tpp = find_peaks(hr_conv*-1,height=10, distance = 7)
    brady_times = rt[0:-1][brady_ixs]
    tachy_times = rt[0:-1][tachy_ixs]
    plt.plot(rt[0:-1][brady_ixs],bpp['peak_heights']*0.5,'ok',label = 'brady calls')
    plt.plot(rt[0:-1][tachy_ixs],tpp['peak_heights']*-0.5,'ob',label = 'tachy calls')
    ax.legend()
    ax.set_ylim(-12,12)
    ax.set_xlim(tstart,tend)
    #f.savefig("2020_06_05_session01_TachyCardia_Balloon_Li.png", dpi = 300)
    #ax.set_xlim(d.epocs.Blln.onset[1],d.epocs.Blln.onset[1]+20)
    plt.show()
