import os
from dotenv import load_dotenv
import kagglehub

# .env 로드
load_dotenv()

# 환경변수 가져오기
token = os.getenv("KAGGLE_API_TOKEN")

# 환경변수 등록
os.environ["KAGGLE_API_TOKEN"] = token

# 데이터셋 다운로드
path = kagglehub.dataset_download(
    "ninetyninenewton/kr3-korean-restaurant-reviews-with-ratings"
)

print("다운로드 위치:")
print(path)