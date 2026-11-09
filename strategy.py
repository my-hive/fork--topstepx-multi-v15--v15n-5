"""Causal ES opening-range breakout continuation, one scheduled trade daily."""
import numpy as np
PARAMS={"range_start":30600,"signal_sec":34200,"entry_sec":34260,"exit_sec":43200,"risk":250}
def signals(panel):
    r={}
    for s,d in panel.items():
        out=np.zeros(len(d),dtype=np.int64)
        if s=="ES":
            sec=d.ct_sec.to_numpy(); close=d.close.to_numpy()
            for ix in d.groupby("session",sort=False).indices.values():
                j=np.searchsorted(sec[ix],PARAMS["signal_sec"])
                if j<len(ix) and sec[ix[j]]==PARAMS["signal_sec"]:
                    prior=ix[(sec[ix]>=PARAMS["range_start"])&(sec[ix]<PARAMS["signal_sec"])]
                    side=int(np.sign(close[ix[j]]-close[prior[0]])) if len(prior) else 0
                    out[ix[(sec[ix]>=PARAMS["entry_sec"])&(sec[ix]<PARAMS["exit_sec"])]]=side
        r[s]=out
    return r
def entry_risk(panel): return {s:np.full(len(d),PARAMS["risk"],float) for s,d in panel.items()}
