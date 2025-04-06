import os
import json

# 기존 파일 경로
Past_words_file = 'example_learned_words.txt'

# 새로운 파일 경로
new_file = 'example_new_words.json'
filtered_output_file = 'Filtered_new_words.json'

# 과거 words 로드 함수
def load_past_words(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    return set()

# JSON 항목 처리 함수
def process_entry(entry):
    """
    JSON 항목에서 class 정보를 확인하여 전치사 여부를 검사한 후 Lemma를 반환
    """
    lemma = entry["Lemma"]
    pos_class = entry["class"]  # 품사 정보
    if pos_class == "전치사":
        print(f"Skipping preposition: {lemma}")
        return None
    return lemma

# newwords.json 내부 중복 제거 함수
def remove_internal_duplicates(entries):
    """
    newwords.json 내부에서 Lemma 중복 제거
    """
    seen_lemmas = set()
    unique_entries = []
    for entry in entries:
        lemma = entry["Lemma"]
        pos_class = entry["class"]
        if pos_class == "전치사":
            continue
        elif lemma not in seen_lemmas :
            unique_entries.append(entry)
            seen_lemmas.add(lemma)
        else:
            print(f"Removing duplicate Lemma in newwords.json: {lemma}")
    return unique_entries

# 기존 JSON 파일 처리
file_list = os.listdir(input_dir_path)
try:
    processed_words = set() 
    for file in file_list:
        if file.endswith('.json'):
            input_file_path = os.path.join(input_dir_path, file)
            # JSON 파일 읽기
            with open(input_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # 각 항목 처리
            for entry in json_data:
                processed_word = process_entry(entry)
                if processed_word:
                    processed_words.add(processed_word)

    # 추출한 단어를 텍스트 파일에 저장
    with open(Past_words_file, 'a', encoding='utf-8') as f:
        for word in sorted(processed_words):
            f.write(word + '\n')

    print(f"추출한 단어들이 {Past_words_file}에 저장되었습니다.")

except Exception as e:
    print(f"JSON 파일 처리 중 오류가 발생했습니다: {e}")

# 과거 단어 로드
past_words = load_past_words(Past_words_file)

# 새로운 파일에서 중복 제거
try:
    with open(new_file, 'r', encoding='utf-8') as f:
        new_json_data = json.load(f)

    # newwords.json 내부 중복 제거
    unique_new_data = remove_internal_duplicates(new_json_data)

    # 과거 단어와 전치사를 제외한 데이터 필터링
    filtered_data = [
        entry for entry in unique_new_data
        if entry["Lemma"] not in past_words and entry["class"] != "전치사"
    ]

    # 필터링된 데이터 저장
    with open(filtered_output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

    print(f"중복 제거된 데이터가 {filtered_output_file}에 저장되었습니다.")

except Exception as e:
    print(f"중복 제거 중 오류가 발생했습니다: {e}")