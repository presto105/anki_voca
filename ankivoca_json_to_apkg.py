import json
import os
import genanki
import html
import re
import random

# Example usage
input_folder = './'
output_folder = './'

# Function to create HTML for back side
def create_html(korean, sentence, answer, word_class, definition, notes, examples):
    # 직접 HTML 태그 삽입
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

# Function to create HTML for front side
def create_front_html(korean, sentence, answer, hint):
    escaped_answer = html.escape(answer)

    # 문장 처리 및 텍스트 박스 삽입
    words = re.split(r'(\s+|___)', sentence)
    text_input_html = ""
    input_index = 0
    for word in words:
        if word == "___":
            for i in range(len(answer)):
                text_input_html += f" <input type='text' maxlength='1' id='char-{input_index}' class='char-box' " \
                                    f"oninput='handleInput({input_index}, \"{escaped_answer}\")' onclick='setActiveBox({input_index})' onkeydown='handleKey(event, {input_index}, \"{escaped_answer}\")' style='width: 20px; text-align: center; color: black;'> "
                input_index += 1
        elif word.strip(): # 공백이 아닌 경우에만 span으로 감싸기
            text_input_html += f"<span>{html.escape(word)}</span> "

    # Hint button 및 span
    hint_button = (
        f"<button onclick=\"toggleVisibility('hint')\" style='margin: 5px; padding: 5px 10px;'>Show Hint</button><br>"
        f"<span id='hint' style='display: none; color: blue;'> {html.escape(hint)}</span><br>"
    )

    # First letter button 및 span
    first_letter_button = (
        f"<button onclick=\"toggleVisibility('first-letter')\" style='margin: 5px; padding: 5px 10px;'>Show First Letter</button><br>"
        f"<span id='first-letter' style='display: none;'> <b>{html.escape(answer[0])}</b></span><br>"
    )

    
    # HTML 콘텐츠
    html_content = f"""
    <div class='question-container' data-answer='{escaped_answer}'>
        <b style="font-size: 24px;">{html.escape(korean)}</b><br>
        <p style="font-size: 22px;" id='sentence-text'>{text_input_html}</p>
        <button class='submit-button' onclick='checkAnswer(this)' style='margin-top: 10px; padding: 5px 10px;'>Submit</button>
        <div id='feedback' style='margin-top: 10px; font-weight: bold;'></div>
        <p><b>Hint:</b> {hint_button}</p>
        <p><b>First Letter:</b> {first_letter_button}</p>
    </div>
    <script>
        let activeBox = 0;
        function setActiveBox(index) {{
            activeBox = index;
        }}
        function toggleVisibility(elementId) {{
            const element = document.getElementById(elementId);
            if (element.style.display === 'none' || element.style.display === '') {{
                element.style.display = 'inline';
            }} else {{
                element.style.display = 'none';
            }}
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
            const prevBox = document.getElementById('char-' + (index - 1));
            const nextBox = document.getElementById('char-' + (index + 1));
            const currentBox = document.getElementById('char-' + index);
            if (event.key === 'ArrowLeft' && prevBox) {{
                prevBox.focus();
                activeBox = index - 1;
                event.preventDefault();
            }} else if (event.key === 'ArrowRight' && nextBox) {{
                nextBox.focus();
                activeBox = index + 1;
                event.preventDefault();
            }} else if (event.key === 'Backspace') {{
                if (currentBox.value === '' && prevBox) {{
                    prevBox.focus();
                    prevBox.value = '';
                }} else {{
                    currentBox.value = '';
                }}
                event.preventDefault();
            }} else if (!event.ctrlKey && !event.altKey && event.key.length === 1) {{
                 currentBox.value = event.key;
                 const nextBox = document.getElementById('char-' + (index + 1));
                if (nextBox) {{
                    nextBox.focus();
                }}
                 event.preventDefault();
            }} else if (event.key === 'Enter') {{
                const questionContainer = currentBox.closest('.question-container');
                const charBoxes = questionContainer.querySelectorAll('.char-box');
                if (index === charBoxes.length - 1) {{
                    const submitButton = questionContainer.querySelector('.submit-button');
                   submitButton.click();
                    event.preventDefault();
                }}
           }}
        }}
        function checkAnswer(buttonElement) {{
            const questionContainer = buttonElement.closest('.question-container');
            const correctAnswer = questionContainer.getAttribute('data-answer');
            
            let userAnswer = '';
            let correctCount = 0;
            const hintElement = questionContainer.querySelector('#hint'); // 변경됨: id로 직접 찾기
            const sentenceText = questionContainer.querySelector('#sentence-text');
             for (let i = 0; i < correctAnswer.length; i++) {{
                const charBox = document.getElementById('char-' + i);
                if (charBox) {{
                    const charValue = charBox.value || '_';
                    userAnswer += charValue;
                    if (charValue === correctAnswer[i]) {{
                        charBox.style.color = 'darkgreen';
                        charBox.style.fontWeight = '900';
                        correctCount++;
                    }} else {{
                        charBox.style.color = 'red';
                        charBox.style.fontWeight = 'bold';
                    }}
                }}
            }}
            const feedback = questionContainer.querySelector('#feedback');
            if (correctCount === correctAnswer.length) {{
                feedback.innerHTML = '<span style="color: green;">Correct!</span>';
                hintElement.style.display = 'none';
            }} else {{
                feedback.innerHTML = '<span style="color: red;">Incorrect!</span>';
                hintElement.style.display = 'inline'; // 오답일 경우 힌트 표시
            }}
        }}
    </script>
    <style>
        .char-box {{
            width: 20px;
            height: 30px;
            font-size: 16px;
            text-align: center;
            border: 1px solid #ccc;
            font-weight: normal;
        }}
         .char-box:focus {{
             border-color: #007bff;
             outline: none;
         }}
        #sentence-container span {{
            font-size: 22px;
        }}
        #sentence-text span {{
          font-size: 22px;
        }}
    </style>
    """
    return html_content

# Function to create Anki deck from JSON data
def create_anki_deck(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = shuffle_json_data(data)

    deck_name = os.path.splitext(os.path.basename(json_file))[0]
    deck = genanki.Deck(
        hash(deck_name),  # Unique ID based on file name
        deck_name
    )
    
    model = genanki.Model(
        hash("Simple Model with Front Feedback"), # 모델명 변경
        "Simple Model with Front Feedback",
        fields=[
            {"name": "FrontHTML"},
            {"name": "BackHTML"},
        ],
        templates=[
            {
                "name": "Card Template",
                "qfmt": "{{FrontHTML}}",
                "afmt": "<div>{{FrontSide}}<hr>{{BackHTML}}</div>",
            }
        ],
        css="""
        .card {
            font-family: Arial, sans-serif;
            font-size: 14px;
            line-height: 1.5;
        }
        input[type=checkbox] {
            transform: scale(1.2);
            margin-right: 10px;
        }
        input[type=text] {
            width: 100%;
            padding: 5px;
            margin-top: 5px;
            font-size: 14px;
        }
        button {
            margin-top: 10px;
            padding: 5px 10px;
            font-size: 14px;
            cursor: pointer;
        }
        """
    )

    for entry in data:
        korean = entry["korean"]
        sentence = entry["sentence"]
        answer = entry["answer"]
        word_class = entry["class"]
        hint = entry.get("hint", "")
        definition = entry["definition"]
        notes = entry["notes"]
        examples = entry["examples"]

        front_html = create_front_html(korean, sentence, answer, hint)
        back_html = create_html(korean, sentence, answer, word_class, definition, notes, examples)

        note = genanki.Note(
            model=model,
            fields=[front_html, back_html]
        )

        deck.add_note(note)

    genanki.Package(deck).write_to_file(output_file)

# Function to process multiple JSON files
def process_json_files(input_folder, output_folder):
    
    for json_file in os.listdir(input_folder):
        if json_file.endswith('.json'):
            input_path = os.path.join(input_folder, json_file)
            output_file = os.path.join(output_folder, json_file.replace('.json', '.apkg'))
            
            create_anki_deck(input_path, output_file)

def shuffle_json_data(json_data):
    """
    JSON 데이터의 순서를 무작위로 섞는 함수.
    :param json_data: 리스트 형태의 JSON 데이터
    :return: 무작위로 순서가 섞인 JSON 데이터
    """
    if isinstance(json_data, list):
        random.shuffle(json_data)  # 리스트를 무작위로 섞음
    else:
        raise ValueError("JSON 데이터는 리스트 형태여야 합니다.")
    return json_data


os.makedirs(output_folder, exist_ok=True)
process_json_files(input_folder, output_folder)