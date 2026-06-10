import pandas as pd
from .features_time import add_calendar_features, add_season_feature


def build_hotel_features(df_hotel: pd.DataFrame) -> pd.DataFrame:
    """
    Features causales y simples a nivel hotel.
    NO incluye variables derivadas del target.
    """

    df = df_hotel.copy()

    df = add_calendar_features(df, date_col="fecha")

    df = add_season_feature(df, date_col="fecha")

    return df