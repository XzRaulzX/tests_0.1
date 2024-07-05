import streamlit as st
import json
import random

# Función para cargar las preguntas desde un archivo JSON
def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['questions']

# Cargar preguntas
questions = load_questions('./questions.json')
# Título y logo
st.set_page_config(page_title="ExamTests", page_icon=":microscope:")

# Estado inicial
if 'answers' not in st.session_state:
    st.session_state['answers'] = [None] * len(questions)
if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'random_mode' not in st.session_state:
    st.session_state['random_mode'] = False
if 'random_question_idxs' not in st.session_state:
    st.session_state['random_question_idxs'] = list(range(len(questions)))
    random.shuffle(st.session_state['random_question_idxs'])
if 'current_random_idx' not in st.session_state:
    st.session_state['current_random_idx'] = 0

# Título
st.title("Formulario de Preguntas")

# Número de preguntas por página
num_questions_per_page = 10
num_pages = (len(questions) + num_questions_per_page - 1) // num_questions_per_page

# Función para mostrar una pregunta
def show_question(question, question_idx):
    st.subheader(f"Pregunta {question_idx + 1}")
    st.write(question['question'])

    # Mostrar imagen si existe la URL
    if 'url' in question and question['url']:
        st.image(question['url'], use_column_width=True)

    selected_options = st.session_state['answers'][question_idx]
    correct_options = question['answer']
    option_mapping = {opt[0]: opt for opt in question['options']}  # Map the letter to the option

    # Crear botones para las opciones
    if isinstance(correct_options, list):  # Pregunta de opción múltiple
        columns = st.columns(len(question['options']))
        for col_idx, option in enumerate(question['options']):
            button_label = option
            if selected_options and option[0] in selected_options:
                button_label = f"✅ {option}"
            if columns[col_idx].button(button_label, key=f"q{question_idx}_opt{col_idx}"):
                if selected_options is None:
                    selected_options = []
                if option[0] in selected_options:
                    selected_options.remove(option[0])
                else:
                    selected_options.append(option[0])
                st.session_state['answers'][question_idx] = selected_options

        # Mostrar respuestas correctas después de que se presione un botón
        if selected_options:
            correct_answers = ''.join([opt[0] for opt in correct_options])
            st.markdown(f"<h3 style='color:blue;'>Respuesta(s) correcta(s): {correct_answers}</h3>", unsafe_allow_html=True)

    else:  # Pregunta de opción única
        columns = st.columns(len(question['options']))
        for col_idx, option in enumerate(question['options']):
            button_label = option
            if selected_options is not None:
                if option == option_mapping[correct_options]:
                    if option == selected_options:
                        button_label = f"✅ {option}"
                    elif selected_options != correct_options:
                        button_label = f"❌ {option}"

            if columns[col_idx].button(button_label, key=f"q{question_idx}_opt{col_idx}"):
                st.session_state['answers'][question_idx] = option

        # Mostrar respuesta correcta después de que se presione un botón
        if selected_options is not None:
            correct_answer = option_mapping[correct_options]
            st.markdown(f"<h3 style='color:blue;'>Respuesta correcta: {correct_answer}</h3>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# Botón para modo aleatorio
random_mode = st.checkbox("Modo Aleatorio")
if random_mode:
    st.session_state['random_mode'] = True
else:
    st.session_state['random_mode'] = False

# Mostrar preguntas
if st.session_state['random_mode']:
    if st.session_state['current_random_idx'] < len(st.session_state['random_question_idxs']):
        random_question_idx = st.session_state['random_question_idxs'][st.session_state['current_random_idx']]
        show_question(questions[random_question_idx], random_question_idx)

        # Botón para siguiente pregunta aleatoria
        if st.button("Siguiente Pregunta"):
            st.session_state['current_random_idx'] += 1
            st.session_state['answers'] = [None] * len(questions)

else:
    # Mostrar preguntas para la página actual
    page = st.session_state['page']
    start_idx = (page - 1) * num_questions_per_page
    end_idx = min(start_idx + num_questions_per_page, len(questions))
    for idx in range(start_idx, end_idx):
        show_question(questions[idx], idx)

    # Navegación de páginas en el pie de la página
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Página Anterior"):
            if st.session_state['page'] > 1:
                st.session_state['page'] -= 1
    with col3:
        if st.button("Página Siguiente"):
            if st.session_state['page'] < num_pages:
                st.session_state['page'] += 1
    with col2:
        page_input = st.number_input("Ir a la página", min_value=1, max_value=num_pages, value=page, step=1)
        if st.button("Ir"):
            st.session_state['page'] = page_input
