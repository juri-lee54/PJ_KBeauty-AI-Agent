# 💄 Global K-Beauty Trend Agent
**Amorepacific Global Market Intelligence & Decision Support AI Agent**
다언어·다채널 데이터(Instagram, YouTube, OliveYoung)를 실시간으로 분석하여, 글로벌 시장의 트렌드를 조기 탐지하고 실행 가능한(Actionable) 전략을 매주 뉴스레터로 제안하는 AI 에이전트입니다.

## 📋 목차 (Table of Contents)
1. [프로젝트 배경 및 문제 정의](#-프로젝트-배경-및-문제-정의-background)
2. [핵심 가치 및 기대효과](#-핵심-가치-및-기대효과-core-value)
3. [AI Agent 구조 및 아키텍처](#-ai-agent-구조-및-아키텍처-architecture)
4. [프로젝트 구조](#-프로젝트-구조-project-structure)
5. [설치 및 실행 방법](#-설치-및-실행-방법-installation--usage)

---

## 📖 프로젝트 배경 및 문제 정의 (Background)

아모레퍼시픽의 글로벌 비즈니스 환경에서 발견된 3가지 핵심 문제를 해결하기 위해 기획되었습니다.

### 1. ⚠️ 높은 해외 의존도와 트렌드 조기 탐지 실패 리스크
* **구조적 위험:** 해외 매출 비중이 약 **43%**이며, 그중 중국·미국·일본 3국이 **89.8%**를 차지합니다.
* **기회 손실:** 소수 핵심 시장의 소비자 니즈 신호를 놓칠 경우, 즉각적인 매출 비효율 및 기회 손실로 이어집니다.

### 2. 🧩 다언어·다채널 데이터의 파편화 ('보이지 않는 트렌드')
* **데이터 분산:** 글로벌 트렌드는 **2개 이상의 언어**(영어, 일어)와 **3개 이상의 채널**(올리브영 글로벌, 유튜브, 인스타그램)에 흩어져 있습니다.
* **해석의 어려움:** 텍스트, 해시태그, 영상 자막 등 포맷이 다양하여 통합 파악이 어렵고 해석 오류가 발생합니다.

### 3. 🐢 '탐지'는 되지만 '실행'이 늦는 인사이트
* **느린 사이클:** 리서치부터 의사결정까지 평균 **3~8주**가 소요되어, 그 사이 트렌드가 전환되는 사례가 **20%** 이상입니다.
* **Action 부재:** 대부분의 데이터가 단순 KPI에 머물러, '구체적으로 무엇을 해야 하는가'에 대한 행동 권고가 부족합니다.

---

## 💎 핵심 가치 및 기대효과 (Core Value)

1.  **⚡ 실시간 시장 민감도 지표:** 미·중·일 소비자 신호를 정량화하여 트렌드 급변 조짐을 **1주 내 조기 탐지**.
2.  **📊 데이터 통합 및 정량화:** 4개 언어·다채널 데이터를 자동 통합/정규화하여 성분·제형별 **실행 가능한 지표** 제시.
3.  **💌 자동화된 의사결정 지원:** 주력 제품, 신규 기회, 리스크 대응책을 담은 **주간 뉴스레터 자동 발송**.

---

## 🤖 AI Agent 구조 및 아키텍처 (Architecture)

### 1. 전체 파이프라인 (Overview)
수집부터 실행 제안(이메일 발송)까지 전 과정을 수행하는 구조입니다.

```
mermaid
graph LR
    A[Data Sources<br/>(Insta, YT, OliveYoung)] -->|Collecting| B(Data Processing<br/>& AI Analysis)
    B -->|Insights| C{Insight Agent}
    C -->|Construct| D[Newsletter Builder]
    D -->|SMTP| E[User Email<br/>(Actionable Report)]
```

### 2. 상세 분석 로직

수집된 이종 데이터를 통합하고 RAG 기반으로 인사이트를 도출합니다.

```
mermaid
flowchart TD
    Raw[Raw Data] -->|NLLB Translation| Stat[1. 통계적 속성 추출]
    Stat --> Candidate[2. 키워드/토큰 분석]
    Candidate --> Sentiment[3. 부정 이슈 검출<br>(BERT Sentiment)]
    Sentiment --> RAG[4. RAG 기반 인사이트 생성<br>(LLM Fact Check)]
    RAG --> Report[5. 국가별 통합 리포트 생성]
```

* **Data Pipeline:** Selenium & BeautifulSoup (OliveYoung), Official APIs (YouTube, Instagram)
* **AI Models:** * **Translation:** Meta NLLB-200 (다국어 리뷰 통합)
* **Extraction:** Gemini-2.5-flash (성분/제형 구조화), KeyBERT (키워드 추출)
* **Analysis:** GPT-4o-mini (RAG 기반 인사이트 요약 및 검증)



---

## 📂 프로젝트 구조 (Project Structure)

```bash
PJ_KBeauty-AI-Agent/
├── config/
│   └── email_config.py      # 이메일 발송 관련 환경 설정 (SMTP, 계정 정보)
├── data/
│   ├── agent_results.json   # AI 에이전트 최종 분석 결과
│   ├── instagram_trend.json # 인스타그램 해시태그 트렌드 데이터
│   ├── youtube_trend.csv    # 유튜브 제품 언급 및 메타 데이터
│   ├── img/                 # 뉴스레터에 포함될 제품 이미지 리소스
│   └── assets/              # 로고 등 정적 자산
├── mailer/
│   └── smtp_sender.py       # SMTP 기반 이메일 전송 모듈
├── newsletter/
│   ├── builder.py           # 데이터 파싱 및 뉴스레터 HTML 생성 로직
│   └── templates.py         # HTML 이메일 템플릿 (CSS 스타일링 포함)
├── run_newsletter.py        # [Entry Point] 뉴스레터 생성 및 발송 실행 스크립트
├── requirements.txt         # 프로젝트 의존성 라이브러리 목록
├── .env                     # 환경 변수 (API Key, SMTP 설정)
└── README.md                # 프로젝트 문서

```

---

## 🛠 설치 및 실행 방법 (Installation & Usage)

### 1. 환경 설정

Python 3.9+ 환경에서 실행을 권장합니다.

```bash
# Repository Clone
git clone [https://github.com/anonymous-nyancat/PJ_KBeauty-AI-Agent.git](https://github.com/anonymous-nyancat/PJ_KBeauty-AI-Agent.git)
cd PJ_KBeauty-AI-Agent

# Install Dependencies
pip install -r requirements.txt

```

### 2. 환경 변수 설정 (.env)

프로젝트 루트 경로에 `.env` 파일을 생성하고 아래 내용을 입력하세요.

```ini
# SMTP Configuration (Gmail 예시)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
FROM_NAME=K-Beauty Insight Bot

# Report Recipients
REPORT_RECIPIENTS=team_lead@amorepacific.com, marketer@amorepacific.com

# User Role (Report Customization)
USER_ROLE=마케팅 팀

```

### 3. 데이터 준비

`data/` 폴더 내에 분석된 JSON/CSV 파일이 위치해야 합니다. (실제 운영 시 Data Pipeline에 의해 자동 생성됨)

* `agent_results.json`
* `instagram_trend.json`
* `youtube_trend.csv`

### 4. 뉴스레터 발송 실행

아래 명령어를 실행하면 데이터를 읽어 HTML 리포트를 생성하고 이메일을 발송합니다.

```bash
python run_newsletter.py

```

* 실행 결과로 `dist/` 폴더에 `newsletter_preview_YYYY_MM_DD.html` 파일이 생성되어, 발송된 내용을 미리보기 할 수 있습니다.

---

## 📊 데이터 구조 및 활용 (Data Details)

### 카테고리 분류 기준 (Category Standard)

Agent는 `oliveyoung_product` 데이터를 기준으로 **9종의 Sub Category**를 기본 분석 단위로 사용합니다.

| Major Category | **Sub Category (Agent Standard)** |
| --- | --- |
| **Skincare** | `Moisturizers`, `Cleansers` |
| **Makeup** | `Face`, `Eye`, `Lip`, `Nail` |
| **Others** | `All Masks`, `All Suncare`, `All Hair` |

### 주요 데이터 속성

* **Instagram:** `#Kbeauty` 해시태그 기반 실시간 트렌드 및 급상승 키워드
* **YouTube:** 영상 메타데이터 기반 장기적 인지도 및 인기 제품(Hot Item)
* **Olive Young:** 리뷰 및 평점 기반 소비자 니즈, 제품 성분/제형 상세 속성

