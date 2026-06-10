import pandas as pd

from .loaders import read_parquet_hotel, read_parquet_ttoo
from .features_hotel import build_hotel_features
from .features_ttoo import pivot_ttoo_volumes_all


def make_hotel_ttoo_datasets(
    hotel_parquet: str,
    ttoo_parquet: str,
    out_dir: str,
) -> None:

    dfh = read_parquet_hotel(hotel_parquet)
    dfh_feat = build_hotel_features(dfh)

    dft = read_parquet_ttoo(ttoo_parquet)

    wide = pivot_ttoo_volumes_all(dft)

    full = pd.merge(dfh_feat, wide, on=["fecha", "hotel"], how="left")

    rn_cols = [c for c in full.columns if c.startswith("rn_")]
    full[rn_cols] = full[rn_cols].fillna(0.0)

    keep_cols = [
        "fecha", "hotel",
        "ocup_total",
        "is_weekend", "season", 
    ] + rn_cols

    for h in full["hotel"].astype("category").cat.categories:
        sub = full[full["hotel"] == h].copy()
        sub = sub[keep_cols]
        sub = sub.dropna(subset=["ocup_total"])
        sub.to_parquet(f"{out_dir}/{h}.parquet", index=False)