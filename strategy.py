"""Causal ZN midday mean reversion after 30-minute movement, fixed 30-minute holding."""
import numpy as np
PARAMS={"start_sec":39600,"end_sec":46800,"lookback":30,"hold":30,"risk":250}
def signals(panel):
    result={}
    for symbol,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if symbol=="ZN":
            close=df.close.to_numpy(); sec=df.ct_sec.to_numpy()
            for ix in df.groupby("session",sort=False).indices.values():
                for j in range(PARAMS["lookback"],len(ix)-PARAMS["hold"]):
                    i=ix[j]
                    if PARAMS["start_sec"]<=sec[i]<PARAMS["end_sec"] and not out[ix[j-1]]:
                        side=-int(np.sign(close[i]-close[ix[j-PARAMS["lookback"]]]))
                        out[ix[j+1:j+1+PARAMS["hold"]]]=side
        result[symbol]=out
    return result
def entry_risk(panel): return {s:np.full(len(d),PARAMS["risk"],float) for s,d in panel.items()}
