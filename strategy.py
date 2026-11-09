"""Causal ES afternoon reversal of morning directional move, one trade daily."""
import numpy as np
PARAMS={"reference_sec":34200,"signal_sec":43200,"entry_sec":43260,"exit_sec":50400,"risk":250}
def signals(panel):
    result={}
    for symbol,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if symbol=="ES":
            sec=df.ct_sec.to_numpy(); close=df.close.to_numpy()
            for ix in df.groupby("session",sort=False).indices.values():
                j=np.searchsorted(sec[ix],PARAMS["signal_sec"])
                k=np.searchsorted(sec[ix],PARAMS["reference_sec"])
                if j<len(ix) and k<len(ix) and sec[ix[j]]==PARAMS["signal_sec"] and sec[ix[k]]==PARAMS["reference_sec"]:
                    side=-int(np.sign(close[ix[j]]-close[ix[k]]))
                    out[ix[(sec[ix]>=PARAMS["entry_sec"])&(sec[ix]<PARAMS["exit_sec"])]]=side
        result[symbol]=out
    return result
def entry_risk(panel): return {s:np.full(len(d),PARAMS["risk"],float) for s,d in panel.items()}
