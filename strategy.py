"""Causal ES intraday directional drift, entered at midnight CT and flat by EOD."""
import numpy as np

PARAMS = {"entry_sec": 0, "exit_sec": 54000, "risk": 250}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol == "ES":
            sec = df.ct_sec.to_numpy()
            out[(sec >= PARAMS["entry_sec"]) & (sec < PARAMS["exit_sec"])] = 1
        result[symbol] = out
    return result


def entry_risk(panel):
    return {symbol: np.full(len(df), PARAMS["risk"], dtype=float) for symbol, df in panel.items()}
