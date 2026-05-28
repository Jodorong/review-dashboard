import streamlit as st
import pandas as pd

from utils.kaggle_loader import search_datasets, download_dataset, find_csv_files
from utils.analyzer import prepare_review_data
from utils.charts import (
    set_korean_font,
    create_rating_chart,
    create_sentiment_chart,
    create_wordcloud
)
from utils.styles import apply_custom_css

st.set_page_config(
    page_title="Kaggle Review Insight Dashboard",
    layout="wide"
)

apply_custom_css()
set_korean_font()

st.title("📊 Kaggle Review Insight Dashboard")

st.markdown("""
<div class="info-box">
Kaggle 공개 데이터셋을 검색하고, CSV 파일을 불러와 리뷰 데이터를 분석하는 대시보드입니다.<br>
리뷰 컬럼과 평점 컬럼을 직접 매핑하여 별점 분포, 감성 비율, 부정 리뷰, 워드클라우드를 확인할 수 있습니다.
</div>
""", unsafe_allow_html=True)

def normalize(text):
    return text.lower().replace(".", "").replace("_", "").replace(" ", "")


def find_best_column(columns, keywords):

    normalized_columns = {
        col: normalize(col)
        for col in columns
    }

    for keyword in keywords:

        keyword = normalize(keyword)

        for original_col, normalized_col in normalized_columns.items():

            if keyword in normalized_col:
                return original_col

    return columns[0]


st.sidebar.header("데이터셋 검색")

keyword = st.sidebar.text_input(
    "Kaggle 검색어",
    value="product review"
)
st.sidebar.info(
    "리뷰 텍스트와 평점 컬럼이 포함된 데이터셋을 선택해주세요.\n\n"
    "추천 검색어: product reviews, amazon reviews, restaurant reviews, app reviews"
)
if st.sidebar.button("데이터셋 검색"):
    with st.spinner("Kaggle 데이터셋 검색 중..."):
        st.session_state["datasets"] = search_datasets(keyword)

if "datasets" in st.session_state:
    if len(st.session_state["datasets"]) == 0:
        st.warning("검색 결과가 없습니다. 다른 키워드로 검색해보세요.")
    else:
        dataset_options = {
            f"{d['title']} ({d['ref']})": d["ref"]
            for d in st.session_state["datasets"]
        }

        selected_dataset_label = st.sidebar.selectbox(
            "데이터셋 선택",
            list(dataset_options.keys())
        )

        if selected_dataset_label:
            selected_ref = dataset_options[selected_dataset_label]

            if st.sidebar.button("선택한 데이터셋 다운로드"):
                with st.spinner("데이터셋 다운로드 중..."):
                    path = download_dataset(selected_ref)
                    csv_files = find_csv_files(path)

                    st.session_state["dataset_path"] = path
                    st.session_state["csv_files"] = csv_files


if "csv_files" in st.session_state:
    st.subheader("CSV 파일 선택")

    csv_files = st.session_state["csv_files"]

    if not csv_files:
        st.warning("선택한 데이터셋에서 CSV 파일을 찾지 못했습니다. 다른 데이터셋을 선택해주세요.")
        st.stop()

    csv_file = st.selectbox(
        "분석할 CSV 파일",
        csv_files
    )

    if csv_file is None:
        st.info("분석할 CSV 파일을 선택해주세요.")
        st.stop()

    df = pd.read_csv(csv_file)
    def is_text_column(series):
        return series.dropna().astype(str).str.len().mean() > 20


    def is_rating_column(series):
        numeric = pd.to_numeric(series, errors="coerce").dropna()

        if numeric.empty:
            return False

        return numeric.between(0, 5).mean() > 0.7


    text_candidates = [
        col for col in df.columns
        if df[col].dtype == "object" and is_text_column(df[col])
    ]

    rating_candidates = [
        col for col in df.columns
        if is_rating_column(df[col])
    ]

    if not text_candidates or not rating_candidates:
        st.warning(
            "이 CSV는 리뷰 분석에 적합하지 않을 수 있습니다. "
            "리뷰 텍스트 컬럼과 0~5 범위의 평점 컬럼이 있는 데이터셋을 선택해주세요."
        )
    else:
        st.success("리뷰 분석에 적합한 컬럼 후보를 찾았습니다.")

    st.write("데이터 미리보기")
    st.dataframe(df.head())

    st.subheader("컬럼 매핑")

    columns = df.columns.tolist()

    review_keywords = [
        "review",                
        "reviews", 
        "rating", 
        "ratings", 
        "comment", 
        "feedback"
    ]

    rating_keywords = [
        "rating",
        "ratings",
        "score",
        "stars",
        "star",
        "rate"
    ]

    product_keywords = [
        "product",
        "productname",
        "name",
        "title",
        "brand",
        "category"
    ]

    default_review_col = text_candidates[0] if text_candidates else find_best_column(columns, review_keywords)
    default_rating_col = rating_candidates[0] if rating_candidates else find_best_column(columns, rating_keywords)

    review_col = st.selectbox(
        "리뷰 텍스트 컬럼 선택",
        columns,
        index=columns.index(default_review_col)
    )

    rating_col = st.selectbox(
        "평점 컬럼 선택",
        columns,
        index=columns.index(default_rating_col)
    )

    product_col = st.selectbox(
        "상품/카테고리 컬럼 선택",
        ["선택 안 함"] + columns
    )

    product_col = None if product_col == "선택 안 함" else product_col

    if st.button("리뷰 분석 시작"):
        review_df = prepare_review_data(
            df,
            review_col,
            rating_col,
            product_col
        )

        st.session_state["review_df"] = review_df


if "review_df" in st.session_state:
    review_df = st.session_state["review_df"]

    st.divider()
    st.header("리뷰 분석 결과")

    product_list = review_df["product"].dropna().unique().tolist()

    selected_product = st.sidebar.selectbox(
        "상품/카테고리 필터",
        ["전체"] + product_list
    )

    if selected_product != "전체":
        filtered_df = review_df[review_df["product"] == selected_product]
    else:
        filtered_df = review_df

    total_reviews = len(filtered_df)
    avg_rating = filtered_df["rating"].mean()
    negative_count = len(filtered_df[filtered_df["sentiment"] == "부정"])
    negative_ratio = round((negative_count / total_reviews) * 100, 2) if total_reviews else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("전체 리뷰 수", total_reviews)
    col2.metric("평균 평점", round(avg_rating, 2))
    col3.metric("부정 리뷰 수", negative_count)
    col4.metric("부정 비율", f"{negative_ratio}%")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("별점 분포")
        st.pyplot(create_rating_chart(filtered_df))

    with col_right:
        st.subheader("감성 비율")
        st.pyplot(create_sentiment_chart(filtered_df))

    st.divider()

    st.subheader("리뷰 검색")

    search_keyword = st.text_input("리뷰 내 검색어 입력")

    if search_keyword:
        searched_df = filtered_df[
            filtered_df["review"].astype(str).str.contains(search_keyword, na=False)
        ]

        st.write(f"검색 결과: {len(searched_df)}건")
        st.dataframe(searched_df)
    else:
        st.dataframe(filtered_df.head(100))

    st.divider()

    st.subheader("부정 리뷰 확인")

    negative_reviews = filtered_df[filtered_df["sentiment"] == "부정"]
    st.dataframe(negative_reviews.head(100))


    st.subheader("워드클라우드")

    positive_text = " ".join(
        filtered_df[filtered_df["sentiment"] == "긍정"]["review"].astype(str).tolist()
    )

    negative_text = " ".join(
        filtered_df[filtered_df["sentiment"] == "부정"]["review"].astype(str).tolist()
    )

    col_pos, col_neg = st.columns(2)

    with col_pos:
        st.markdown("### 긍정 리뷰 워드클라우드")

        if positive_text.strip():
            try:
                st.pyplot(create_wordcloud(positive_text))
            except Exception:
                st.warning("긍정 리뷰 워드클라우드 생성 중 오류가 발생했습니다.")
        else:
            st.info("긍정 리뷰 데이터가 없습니다.")

    with col_neg:
        st.markdown("### 부정 리뷰 워드클라우드")

        if negative_text.strip():
            try:
                st.pyplot(create_wordcloud(negative_text))
            except Exception:
                st.warning("부정 리뷰 워드클라우드 생성 중 오류가 발생했습니다.")
        else:
            st.info("부정 리뷰 데이터가 없습니다.")