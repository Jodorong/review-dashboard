# 📊 Kaggle Review Insight Dashboard

Kaggle 공개 데이터셋을 검색하고 다운로드하여
리뷰 데이터를 분석할 수 있는 Streamlit 기반 대시보드 프로젝트입니다.

사용자는 Kaggle에서 리뷰 데이터셋을 검색한 뒤,
CSV 파일을 선택하고 리뷰 컬럼과 평점 컬럼을 직접 매핑하여
별점 분포, 감성 비율, 부정 리뷰, 워드클라우드를 확인할 수 있습니다.

---

# 🔍 주요 기능

## Kaggle 데이터셋 검색
* Kaggle API 기반 데이터셋 검색
* 리뷰 관련 데이터셋 필터링

## 리뷰 데이터 분석
* 리뷰 텍스트 / 평점 컬럼 자동 추천
* 리뷰 데이터 유효성 검증
* 상품/카테고리별 필터링

## 시각화
* 별점 분포 그래프
* 긍/부정 감성 비율 그래프
* 긍정 리뷰 워드클라우드
* 부정 리뷰 워드클라우드
---

# 🛠 기술 스택
* Python
* Streamlit
* Pandas
* Matplotlib
* WordCloud
* Kaggle API
---

# 📂 프로젝트 구조

```txt
review-dashboard/
├─ app.py
├─ requirements.txt
├─ .gitignore
├─ .env
└─ utils/
   ├─ analyzer.py
   ├─ charts.py
   ├─ kaggle_loader.py
   └─ styles.py
```

---

# ⚙️ 실행 방법

## 1. 패키지 설치

```bash
pip install -r requirements.txt
```

## 2. Kaggle API 설정

Kaggle에서 `kaggle.json` 발급 후 아래 경로에 저장합니다.
C:\Users\사용자명\.kaggle\kaggle.json
---

## 3. Streamlit 실행
streamlit run app.py
---

# 📌 구현 포인트
* Kaggle 공개 데이터셋 검색 및 자동 다운로드 기능 구현
* 리뷰 데이터셋 여부를 자동 검증하는 로직 구현
* 컬럼명 기반 리뷰/평점 컬럼 자동 추천 기능 구현
* 긍정/부정 리뷰를 분리한 워드클라우드 시각화 구현
* CSS 커스터마이징을 통한 대시보드 UI 개선
---
# 🚀 향후 개선 예정
* 형태소 분석 기반 키워드 추출
* 실시간 감성분석 모델 연동
* 리뷰 요약 기능 추가
* 차트 인터랙션 기능 추가
* 다국어 리뷰 지원
---
