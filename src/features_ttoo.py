import pandas as pd


def pivot_ttoo_volumes_all(df_ttoo: pd.DataFrame) -> pd.DataFrame:
    """
    Volumen diario por TTOO (rn_*).
    """

    df = df_ttoo.copy()

    agg = (
        df.groupby(["fecha", "hotel", "ttoo"])["roomnights"]
        .sum()
        .reset_index()
    )

    wide = agg.pivot_table(
        index=["fecha", "hotel"],
        columns="ttoo",
        values="roomnights",
        fill_value=0,
    )

    wide.columns = [f"rn_{c}" for c in wide.columns]

    return wide.reset_index()
