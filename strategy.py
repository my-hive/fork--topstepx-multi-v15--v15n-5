"""Causal intraday opening-range extension fade on ZN."""
import numpy as np

PARAMS = {"range_minutes": 30, "entry_start": 37800, "entry_end": 45000, "z_multiple": 1.5, "risk": 250}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        target = np.zeros(len(df), dtype=np.int64)
        if symbol != "ZN":
            result[symbol] = target
            continue
        close = df.close.to_numpy()
        high = df.high.to_numpy()
        low = df.low.to_numpy()
        sec = df.ct_sec.to_numpy()
        for indices in df.groupby("session", sort=False).indices.values():
            n = len(indices)
            for j in range(PARAMS["range_minutes"], n):
                i = indices[j]
                if not PARAMS["entry_start"] <= sec[i] < PARAMS["entry_end"]:
                    continue
                prior = indices[:j]
                opening = prior[sec[prior] < 36000]
                if len(opening) < PARAMS["range_minutes"]:
                    continue
                upper = high[opening].max()
                lower = low[opening].min()
                width = upper - lower
                if width and close[i] > upper + PARAMS["z_multiple"] * width:
                    target[i] = -1
                elif width and close[i] < lower - PARAMS["z_multiple"] * width:
                    target[i] = 1
        result[symbol] = target
    return result


def entry_risk(panel):
    return {symbol: np.full(len(df), PARAMS["risk"], dtype=float) for symbol, df in panel.items()}
