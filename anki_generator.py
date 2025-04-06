import json
import os
import genanki
import html
import re
import random

# --------------------------------------------------
# 입력 JSON 파일 경로
input_file_path = './filtered_new_words.json'

# --------------------------------------------------
"""
문제 카드의 뒷면에 들어갈 HTML을 생성
"""
def create_html(korean, sentence, answer, word_class, definition, notes, examples):
    escaped_examples = html.escape(examples).replace(' / ', '<br>')
    html_content = f"""
    <div>
        <p><b>Answer:</b> {html.escape(word_class)}) {html.escape(answer)}</p>
        <p><b>Definition:</b> {html.escape(definition)}</p>
        <p><b>Notes:</b> {html.escape(notes)}</p>
        <p><b>Examples:</b><br> {escaped_examples}</p>
    </div>
    """
    return html_content

# --------------------------------------------------
"""
문제 카드의 앞면 HTML을 생성 (사용자 입력 인터페이스 포함)
"""
def create_front_html(korean, sentence, answer, hint):
    escaped_answer = html.escape(answer)
    words = re.split(r'(\s+|___)', sentence)

    # 공백과 빈칸을 처리하여 input 태그 생성
    text_input_html = ""
    input_index = 0
    for word in words:
        if word == "___":
            for i in range(len(answer)):
                text_input_html += (
                    f" <input type='text' maxlength='1' id='char-{input_index}' class='char-box' "
                    f"oninput='handleInput({input_index}, \"{escaped_answer}\")' "
                    f"onclick='setActiveBox({input_index})' "
                    f"onkeydown='handleKey(event, {input_index}, \"{escaped_answer}\")' "
                    f"style='width: 20px; text-align: center; color: black;'> "
                )
                input_index += 1
        elif word.strip():
            text_input_html += f"<span>{html.escape(word)}</span> "

    # 힌트 버튼 및 첫 글자 버튼
    hint_button = (
        f"<button onclick=\"toggleVisibility('hint')\">Show Hint</button><br>"
        f"<span id='hint' style='display: none; color: blue;'> {html.escape(hint)}</span><br>"
    )
    first_letter_button = (
        f"<button onclick=\"toggleVisibility('first-letter')\">Show First Letter</button><br>"
        f"<span id='first-letter' style='display: none;'> <b>{html.escape(answer[0])}</b></span><br>"
    )

    # 최종 HTML 조합
    html_content = f"""
    <div class='question-container' data-answer='{escaped_answer}'>
        <b style="font-size: 24px;">{html.escape(korean)}</b><br>
        <p style="font-size: 22px;" id='sentence-text'>{text_input_html}</p>
        <button class='submit-button' onclick='checkAnswer(this)'>Submit</button>
        <div id='feedback'></div>
        <p><b>Hint:</b> {hint_button}</p>
        <p><b>First Letter:</b> {first_letter_button}</p>
    </div>
    <script>
        // 사용자 입력 처리용 JS 함수들
        let activeBox = 0;
        function setActiveBox(index) {{
            activeBox = index;
        }}
        function toggleVisibility(elementId) {{
            const element = document.getElementById(elementId);
            element.style.display = (element.style.display === 'none' || element.style.display === '') ? 'inline' : 'none';
        }}
        function handleInput(index, correctAnswer) {{
            const currentBox = document.getElementById('char-' + index);
            const nextBox = document.getElementById('char-' + (index + 1));
            currentBox.style.color = 'black';
            currentBox.style.fontWeight = 'bold';
            if (currentBox.value.length === 1 && nextBox) {{
                nextBox.focus();
                activeBox = index + 1;
            }}
        }}
        function handleKey(event, index, correctAnswer) {{
            const currentBox = document.getElementById('char-' + index);
            const prevBox = document.getElementById('char-' + (index - 1));
            const nextBox = document.getElementById('char-' + (index + 1));
            if (event.key === 'ArrowLeft' && prevBox) {{
                prevBox.focus(); event.preventDefault();
            }} else if (event.key === 'ArrowRight' && nextBox) {{
                nextBox.focus(); event.preventDefault();
            }} else if (event.key === 'Backspace') {{
                if (currentBox.value === '' && prevBox) {{
                    prevBox.focus(); prevBox.value = '';
                }} else {{
                    currentBox.value = '';
                }}
                event.preventDefault();
            }} else if (!event.ctrlKey && !event.altKey && event.key.length === 1) {{
                currentBox.value = event.key;
                if (nextBox) nextBox.focus();
                event.preventDefault();
            }} else if (event.key === 'Enter') {{
                const questionContainer = currentBox.closest('.question-container');
                const charBoxes = questionContainer.querySelectorAll('.char-box');
                if (index === charBoxes.length - 1) {{
                    const submitButton = questionContainer.querySelector('.submit-button');
                    submitButton.click(); event.preventDefault();
                }}
            }}
        }}
        function checkAnswer(buttonElement) {{
            const container = buttonElement.closest('.question-container');
            const correctAnswer = container.getAttribute('data-answer');
            let userAnswer = '', correctCount = 0;
            for (let i = 0; i < correctAnswer.length; i++) {{
                const box = document.getElementById('char-' + i);
                const val = box.value || '_';
                userAnswer += val;
                if (val === correctAnswer[i]) {{
                    box.style.color = 'darkgreen'; box.style.fontWeight = '900'; correctCount++;
                }} else {{
                    box.style.color = 'red'; box.style.fontWeight = 'bold';
                }}
            }}
            const feedback = container.querySelector('#feedback');
            const hint = container.querySelector('#hint');
            feedback.innerHTML = (correctCount === correctAnswer.length)
                ? '<span style="color: green;">Correct!</span>'
                : '<span style="color: red;">Incorrect!</span>';
            hint.style.display = (correctCount === correctAnswer.length) ? 'none' : 'inline';
        }}
    </script>
    <style>
        .char-box {{ width: 20px; height: 30px; font-size: 16px; text-align: center; border: 1px solid #ccc; }}
        .char-box:focus {{ border-color: #007bff; outline: none; }}
        #sentence-text span {{ font-size: 22px; }}
    </style>
    """
    return html_content

# --------------------------------------------------
"""
JSON 데이터를 기반으로 Anki 덱을 생성하고 .apkg 파일로 저장
"""
def create_anki_deck(input_file_path, output_file):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = shuffle_json_data(data)

    deck_name = os.path.splitext(os.path.basename(input_file_path))[0]
    deck = genanki.Deck(
        hash(deck_name),
        deck_name
    )

    model = genanki.Model(
        hash("Simple Model with Front Feedback"),
        "Simple Model with Front Feedback",
        fields=[
            {"name": "FrontHTML"},
            {"name": "BackHTML"},
        ],
        templates=[{
            "name": "Card Template",
            "qfmt": "{{FrontHTML}}",
            "afmt": "<div>{{FrontSide}}<hr>{{BackHTML}}</div>",
        }],
        css="""
        .card {
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
        }
        """
    )

    for entry in data:
        front_html = create_front_html(entry["korean"], entry["sentence"], entry["answer"], entry.get("hint", ""))
        back_html = create_html(entry["korean"], entry["sentence"], entry["answer"],
                                entry["class"], entry["definition"], entry["notes"], entry["examples"])

        note = genanki.Note(model=model, fields=[front_html, back_html])
        deck.add_note(note)

    genanki.Package(deck).write_to_file(output_file)

# --------------------------------------------------
"""
JSON 데이터를 받아서 무작위 순서로 섞은 후 반환
"""
def shuffle_json_data(json_data):
    if isinstance(json_data, list):
        random.shuffle(json_data)
    else:
        raise ValueError("JSON 데이터는 리스트 형태여야 합니다.")
    return json_data

# --------------------------------------------------
"""
단일 JSON 파일을 받아서 Anki 덱 생성 프로세스를 실행
"""
def process_json_files(input_file_path):
    if input_file_path.endswith('.json'):
        output_file = input_file_path.replace('.json', '.apkg')
        create_anki_deck(input_file_path, output_file)

# --------------------------------------------------
# 메인 실행
if __name__ == "__main__":
    process_json_files(input_file_path)