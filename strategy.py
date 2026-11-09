"""Causal one-trade 6E opening-move mean reversion."""
import numpy as np
PARAMS = {"signal_sec": 34200, "entry_sec": 34260, "exit_sec": 50400, "lookback": 30, "risk": 250}
def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if symbol == "6E":
            close=df.close.to_numpy(); sec=df.ct_sec.to_numpy()
            for ix in df.groupby("session",sort=False).indices.values():
                for j in range(PARAMS["lookback"],len(ix)):
                    i=ix[j]
                    if sec[i] == PARAMS["signal_sec"]:
                        side=-int(np.sign(close[i]-close[ix[j-PARAMS["lookback"]]]))
                        active=ix[(sec[ix]>=PARAMS["entry_sec"]) & (sec[ix]<PARAMS["exit_sec"])]
                        out[active]=side
        result[symbol]=out
    return result
def entry_risk(panel): return {s:np.full(len(d),PARAMS["risk"],dtype=float) for s,d in panel.items()}
