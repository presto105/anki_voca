import os
import json

# 파일 경로 설정
PAST_WORDS_FILE = 'example_learned_words.txt'
NEW_WORDS_FILE = 'example_new_words.json'
FILTERED_OUTPUT_FILE = 'filtered_new_words.json'

# --------------------------------------------------
"""
기존 학습된 단어들을 텍스트 파일에서 불러와 set 형태로 반환
"""
def load_past_words(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set()

# --------------------------------------------------
"""
JSON 항목에서 class 정보를 확인하여 전치사 여부를 검사한 후 Lemma를 반환
"""
def process_entry(entry):
    lemma = entry.get("Lemma")
    pos_class = entry.get("class")
    if pos_class == "전치사":
        print(f"Skipping preposition: {lemma}")
        return None
    return lemma

# --------------------------------------------------
"""
JSON 목록 내부에서 중복된 Lemma 항목을 제거하고 전치사는 제외한 리스트 반환
"""
def remove_internal_duplicates(entries):
    seen_lemmas = set()
    unique_entries = []

    for entry in entries:
        lemma = entry.get("Lemma")
        pos_class = entry.get("class")

        if pos_class == "전치사":
            continue
        if lemma not in seen_lemmas:
            unique_entries.append(entry)
            seen_lemmas.add(lemma)
        else:
            print(f"Removing duplicate Lemma in newwords.json: {lemma}")

    return unique_entries

"""
새로운 단어 JSON 파일에서 전치사 및 과거 학습 단어를 제외한 항목을 필터링하여 저장
"""
def filter_new_words(new_words_json, past_words_txt, output_json):
    try:
        past_words = load_past_words(past_words_txt)

        with open(new_words_json, 'r', encoding='utf-8') as f:
            new_json_data = json.load(f)

        unique_new_data = remove_internal_duplicates(new_json_data)

        filtered_data = [
            entry for entry in unique_new_data
            if entry["Lemma"] not in past_words and entry["class"] != "전치사"
        ]

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)

        print(f"중복 제거된 데이터가 {output_json}에 저장되었습니다.")
    except Exception as e:
        print(f"중복 제거 중 오류가 발생했습니다: {e}")

# --------------------------------------------------
# 메인 실행 흐름
if __name__ == "__main__":
    filter_new_words(NEW_WORDS_FILE, PAST_WORDS_FILE, FILTERED_OUTPUT_FILE)