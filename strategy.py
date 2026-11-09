"""Causal ES prior-day close to overnight directional continuation, one daily trade."""
import numpy as np
PARAMS={"signal_sec":30600,"entry_sec":30660,"exit_sec":43200,"risk":250}
def signals(panel):
    result={}
    for symbol,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if symbol=="ES":
            sec=df.ct_sec.to_numpy(); close=df.close.to_numpy()
            previous=None
            for ix in df.groupby("session",sort=False).indices.values():
                j=np.searchsorted(sec[ix],PARAMS["signal_sec"])
                if previous is not None and j<len(ix) and sec[ix[j]]==PARAMS["signal_sec"]:
                    side=int(np.sign(close[ix[j]]-previous))
                    out[ix[(sec[ix]>=PARAMS["entry_sec"])&(sec[ix]<PARAMS["exit_sec"])]]=side
                previous=close[ix[-1]]
        result[symbol]=out
    return result
def entry_risk(panel): return {s:np.full(len(d),PARAMS["risk"],float) for s,d in panel.items()}
