import pandas as pd


def _parse_date_column(df: pd.DataFrame) -> pd.Series:
    if pd.api.types.is_integer_dtype(df["date"]):
        return pd.to_datetime(df["date"], unit="ms", utc=True).dt.tz_localize(None)
    return pd.to_datetime(df["date"])


def read_parquet_hotel(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.columns = df.columns.str.strip().str.lower()

    df["fecha"] = _parse_date_column(df)
    df = df.rename(columns={"codigo_hotel": "hotel"})
    df = df.sort_values(["hotel", "fecha"]).reset_index(drop=True)

    df["hotel"] = df["hotel"].astype("category")

    return df[["fecha", "hotel", "ocup_total"]]


def read_parquet_ttoo(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.columns = df.columns.str.strip().str.lower()

    df["fecha"] = _parse_date_column(df)
    df = df.rename(columns={"codigo_hotel": "hotel", "codigo_ttoo": "ttoo"})
    df = df.sort_values(["hotel", "ttoo", "fecha"]).reset_index(drop=True)

    df["hotel"] = df["hotel"].astype("category")
    df["ttoo"] = df["ttoo"].astype("category")

    return df[["fecha", "hotel", "ttoo", "roomnights"]]