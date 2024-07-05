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
if 'random_shown_questions' not in st.session_state:
    st.session_state['random_shown_questions'] = []

# Título
st.title("Formulario de Preguntas")

# Número de preguntas por página
num_questions_per_page = 10
num_pages = (len(questions) + num_questions_per_page - 1) // num_questions_per_page

# Función para mostrar una pregunta
def show_question(question, question_idx):
    st.subheader(f"Pregunta {question_idx + 1}")
    st.write(question['question'])

    selected_option = st.session_state['answers'][question_idx]
    correct_option = question['answer']
    option_mapping = {opt[0]: opt for opt in question['options']}  # Map the letter to the option

    # Crear botones para las opciones
    if isinstance(correct_option, list):  # Pregunta de opción múltiple
        if selected_option is None:
            selected_option = []
        columns = st.columns(len(question['options']))
        for col_idx, option in enumerate(question['options']):
            button_label = option
            if option in selected_option:
                if option in correct_option:
                    button_label = f"✅ {option}"
                else:
                    button_label = f"❌ {option}"
            if columns[col_idx].button(button_label, key=f"q{question_idx}_opt{col_idx}"):
                if option in selected_option:
                    selected_option.remove(option)
                else:
                    selected_option.append(option)
                st.session_state['answers'][question_idx] = selected_option

        # Mostrar la respuesta correcta si se ha seleccionado una opción
        if selected_option:
            correct_answers = [option_mapping[opt] for opt in correct_option]
            st.markdown(f"<h3 style='color:green;'>Respuestas correctas: {', '.join(correct_answers)}</h3>", unsafe_allow_html=True)

    else:  # Pregunta de opción única
        columns = st.columns(len(question['options']))
        for col_idx, option in enumerate(question['options']):
            button_label = option
            if selected_option is not None:
                if option == option_mapping[correct_option]:
                    button_label = f"✅ {option}"
                elif option == selected_option:
                    button_label = f"❌ {option}"

            if columns[col_idx].button(button_label, key=f"q{question_idx}_opt{col_idx}"):
                st.session_state['answers'][question_idx] = option

        # Mostrar la respuesta correcta si se ha seleccionado una opción
        if selected_option is not None:
            correct_answer = option_mapping[correct_option]
            if selected_option == correct_option:
                st.markdown(f"<h3 style='color:green;'>Correcto: {correct_answer}</h3>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h3 style='color:red;'>Incorrecto. Respuesta correcta: {correct_answer}</h3>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# Botón para modo aleatorio
if st.checkbox("Modo Aleatorio"):
    st.session_state['random_mode'] = True
else:
    st.session_state['random_mode'] = False

# Mostrar preguntas
if st.session_state['random_mode']:
    if st.session_state['current_random_idx'] < len(st.session_state['random_question_idxs']):
        random_question_idx = st.session_state['random_question_idxs'][st.session_state['current_random_idx']]
        
        # Verificar si la pregunta aleatoria ya se ha mostrado
        while random_question_idx in st.session_state['random_shown_questions']:
            st.session_state['current_random_idx'] += 1
            if st.session_state['current_random_idx'] >= len(st.session_state['random_question_idxs']):
                break
            random_question_idx = st.session_state['random_question_idxs'][st.session_state['current_random_idx']]
        
        if st.session_state['current_random_idx'] < len(st.session_state['random_question_idxs']):
            show_question(questions[random_question_idx], random_question_idx)
    else:
        st.write("No hay más preguntas en modo aleatorio.")

    # Botón para siguiente pregunta aleatoria
    if st.button("Siguiente Pregunta Aleatoria"):
        st.session_state['current_random_idx'] += 1
        st.session_state['answers'] = [None] * len(questions)
        st.session_state['random_shown_questions'] = []
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
