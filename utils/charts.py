import matplotlib.pyplot as plt
from wordcloud import WordCloud
import platform


def set_korean_font():

    if platform.system() == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"

    elif platform.system() == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"

    else:
        plt.rcParams["font.family"] = "NanumGothic"

    plt.rcParams["axes.unicode_minus"] = False


def create_rating_chart(df):

    rating_counts = df["rating"].value_counts().sort_index()

    fig, ax = plt.subplots()

    colors = [
        "#EF4444",  # 1점
        "#F97316",  # 2점
        "#FACC15",  # 3점
        "#84CC16",  # 4점
        "#22C55E"   # 5점
    ]

    ax.bar(
        rating_counts.index.astype(str),
        rating_counts.values,
        color=colors[:len(rating_counts)]
    )

    ax.set_xlabel("평점")
    ax.set_ylabel("리뷰 수")
    ax.set_title("별점 분포")

    return fig


def create_sentiment_chart(df):

    sentiment_counts = df["sentiment"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("감성 비율")

    return fig


def create_wordcloud(text):

    stopwords = {
        "좋아요", "좋네요", "좋습니다", "좋은", "좋고", "좋음", "좋다",
        "싫어요", "싫네요", "별로", "그냥", "너무", "정말", "진짜",
        "많이", "매우", "좀", "더", "잘", "안", "못", "것", "수",
        "있어요", "있습니다", "없는", "없어요", "합니다", "해요",
        "그리고", "하지만", "그래도", "이", "그", "저", "거", "듯",
        "은", "는", "이", "가", "을", "를", "에", "의", "로", "으로",
        "알라딘"
    }

    words = text.split()

    filtered_words = [
        word.strip(".,!?~…ㅋㅋㅎㅎㅠㅠ\"'()[]{}")
        for word in words
        if len(word.strip(".,!?~…ㅋㅋㅎㅎㅠㅠ\"'()[]{}")) >= 2
        and word.strip(".,!?~…ㅋㅋㅎㅎㅠㅠ\"'()[]{}") not in stopwords
    ]

    cleaned_text = " ".join(filtered_words)

    wordcloud = WordCloud(
        width=900,
        height=450,
        background_color="white",
        font_path="C:/Windows/Fonts/malgun.ttf",
        stopwords=stopwords,
        max_words=80,
        collocations=False
    ).generate(cleaned_text)

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.imshow(wordcloud)
    ax.axis("off")

    return fig