"""Causal 6E morning momentum, holding while prior hour direction persists."""
import numpy as np

PARAMS = {"lookback": 60, "start_sec": 34200, "end_sec": 50400, "risk": 250}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol == "6E":
            close = df.close.to_numpy()
            sec = df.ct_sec.to_numpy()
            for indices in df.groupby("session", sort=False).indices.values():
                for j in range(PARAMS["lookback"], len(indices)):
                    i = indices[j]
                    if PARAMS["start_sec"] <= sec[i] < PARAMS["end_sec"]:
                        out[i] = int(np.sign(close[i] - close[indices[j - PARAMS["lookback"]]]))
        result[symbol] = out
    return result


def entry_risk(panel):
    return {symbol: np.full(len(df), PARAMS["risk"], dtype=float) for symbol, df in panel.items()}
