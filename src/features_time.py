import pandas as pd


def add_calendar_features(df: pd.DataFrame, date_col: str = "fecha") -> pd.DataFrame:
    out = df.copy()
    dt = out[date_col]

    out["is_weekend"] = (dt.dt.dayofweek >= 5).astype(int)
    return out


def add_season_feature(df: pd.DataFrame, date_col: str = "fecha") -> pd.DataFrame:
    out = df.copy()

    def get_season(m):
        if m in [12, 1, 2]:
            return "winter"
        elif m in [3, 4, 5]:
            return "spring"
        elif m in [6, 7, 8]:
            return "summer"
        else:
            return "autumn"

    out["season"] = out[date_col].dt.month.map(get_season)
    return out