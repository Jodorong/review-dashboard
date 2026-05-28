import os
import glob
from kaggle.api.kaggle_api_extended import KaggleApi


def get_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api


def search_datasets(keyword):
    api = get_kaggle_api()

    results = api.dataset_list(
        search=keyword,
        sort_by="hottest",
        page=1
    )

    review_keywords = [
        "review",
        "reviews",
        "rating",
        "ratings",
        "comment",
        "comments",
        "feedback",
        "sentiment"
    ]

    datasets = []

    for item in results:
        title = item.title or ""
        ref = item.ref or ""
        text = f"{title} {ref}".lower()

        if any(word in text for word in review_keywords):
            datasets.append({
                "title": title,
                "ref": ref
            })

        if len(datasets) >= 10:
            break

    return datasets


def download_dataset(dataset_ref):
    api = get_kaggle_api()

    folder_name = dataset_ref.split("/")[-1]
    download_path = os.path.join("datasets", folder_name)

    os.makedirs(download_path, exist_ok=True)

    api.dataset_download_files(
        dataset_ref,
        path=download_path,
        unzip=True
    )

    return download_path


def find_csv_files(path):
    return glob.glob(
        os.path.join(path, "**", "*.csv"),
        recursive=True
    )