import pandas as pd

def classify_sentiment(rating):
    if rating >= 4:
        return "긍정"
    elif rating == 3:
        return "중립"
    else:
        return "부정"


def prepare_review_data(df, review_col, rating_col, product_col=None):
    selected = df[[review_col, rating_col]].copy()

    selected.columns = ["review", "rating"]

    if product_col:
        selected["product"] = df[product_col]
    else:
        selected["product"] = "전체"

    selected = selected.dropna(subset=["review", "rating"])
    selected["rating"] = pd.to_numeric(selected["rating"], errors="coerce")
    selected = selected.dropna(subset=["rating"])

    selected["sentiment"] = selected["rating"].apply(classify_sentiment)

    return selected