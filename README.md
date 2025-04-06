# 📘 Interactive Vocabulary Anki Deck Generator

이 프로젝트는 새로운 단어 리스트(JSON)를 기반으로 **전치사와 중복 단어를 필터링**한 뒤, **인터랙티브 Anki 덱을 자동 생성**하는 Python 스크립트입니다.

---

## 📂 프로젝트 구성

```
.
├── filter_duplicated_words.py       # 전치사 및 중복 제거 스크립트
├── anki_generator.py                # Anki 덱 생성기
├── example_learned_words.json              # Anki 덱 생성기
├── example_new_words.json                # Anki 덱 생성기
├── filtered_new_words.json          # 필터링된 단어 리스트 (중복 제거)
├── filtered_new_words.apkg          # 생성된 Anki 덱 파일
└── README.md
```
---

## 🧠 주요 기능

### ✅ 단어 필터링 (`filter_duplicated_words.py`)
- `전치사` 단어 제외
- 기존 학습한 단어와 중복되는 항목 제외 (`example_learned_words.txt` 기준)
- 내부 JSON 중복 제거
- 결과를 `filtered_new_words.json`에 저장

> 💡 **참고:** 이미 외운 단어는 `example_learned_words.txt` 파일에 저장되며, 이후 새로운 단어장을 만들 때 해당 단어들은 자동으로 제외됩니다.

### ✅ Anki 덱 생성 (`anki_generator.py`)
- 사용자가 타이핑하여 단어를 완성하는 인터랙티브 카드 생성
- `힌트`, `첫 글자 보기`, `자동 피드백` 포함
- 카드 뒷면에 정의, 예문, 품사, 비고 정보 표시
- 최종 결과를 `.apkg` 파일로 저장 (Anki import 가능)

---

## 🛠 사용 방법

### 1. 이미 외운 단어 필터링 실행
```bash
python filter_duplicated_words.py
```
- 이미 외운 단어들을 제외하기 위해서는 `example_new_words.json`와 같은 파일이 존재해야 함
- 실행 후 `filtered_new_words.json` 생성됨

### 2. Anki 덱 생성
```bash
python anki_generator.py
```
- `filtered_new_words.json`을 기반으로 `filtered_new_words.apkg` 생성됨

---

## 🧾 JSON 포맷 예시 (`example_new_words.json`)

Anki 덱 생성을 위해 입력 JSON 파일은 다음과 같은 구조로 구성되어야 합니다:

```json
[
  {
    "korean": "정부는 빈곤율을 줄이기 위해 새로운 정책을 시행했습니다.",
    "sentence": "The government implemented a new policy to reduce the ___ rate.",
    "answer": "poverty",
    "Lemma": "poverty",
    "class": "명사",
    "hint": "Refers to the state of being extremely poor.",
    "definition": "빈곤, 가난",
    "notes": "'Poverty rate'는 사회적 경제 상황을 나타낼 때 자주 사용됩니다.",
    "examples": "Efforts to tackle the poverty rate are ongoing. / Poverty is a major challenge in developing nations."
  }
]
```

각 항목 필드는 다음과 같은 역할을 합니다:
- `korean`: 한글 뜻 또는 문장
- `sentence`: 문제 문장 (빈칸은 `___`로 표시)
- `answer`: 정답 단어 (빈칸에 들어갈 것)
- `Lemma`: 기본형 단어 (중복 및 기록 비교에 사용)
- `class`: 품사 (예: 명사, 동사 등)
- `hint`: 힌트 텍스트
- `definition`: 영어 단어의 뜻
- `notes`: 추가 설명 또는 사용 맥락
- `examples`: 예문들 (슬래시 `/`로 구분)

---

## 💡 Anki 카드 미리보기

### 앞면 (사용자 입력)
```
The government implemented a new policy to reduce the _____ rate.

Submit
Hint: Show Hint
First Letter: Show First Letter
```

### 뒷면 (정답과 설명)
```
Answer: 명사) poverty

Definition: 빈곤, 가난

Notes: 'Poverty rate'는 사회적 경제 상황을 나타낼 때 자주 사용됩니다.

Examples:
Efforts to tackle the poverty rate are ongoing.
Poverty is a major challenge in developing nations.
```

---

## 🔧 필요 라이브러리

- `genanki`  
설치:
```bash
pip install genanki
```

---

## 📬 문의
궁금한 점이나 제안 사항이 있다면 언제든지 이슈를 남겨주세요!

