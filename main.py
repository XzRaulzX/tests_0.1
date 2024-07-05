import streamlit as st
import json
import random

# Función para cargar las preguntas desde un archivo JSON
def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['questions']

# Configuración inicial de la página
st.set_page_config(page_title="ExamTests", page_icon="📚✒️")

# Estado inicial de la sesión
if 'answers' not in st.session_state:
    st.session_state['answers'] = None
if 'questions' not in st.session_state:
    st.session_state['questions'] = None
if 'current_random_idx' not in st.session_state:
    st.session_state['current_random_idx'] = 0
if 'random_mode' not in st.session_state:
    st.session_state['random_mode'] = False

# Estilo personalizado para el diseño
st.markdown(
    """
    <style>
    .main-content {
        background-color: #ffffff; /* Fondo blanco para el contenido principal */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .sidebar-content {
        background-color: #f0f0f0; /* Fondo grisáceo para laterales */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .footer-content {
        background-color: #f0f0f0; /* Fondo grisáceo para el pie de página */
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Función para mostrar una pregunta
def show_question(question, question_idx):
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.subheader(f"Pregunta {question_idx + 1}")
    st.write(question['question'])

    # Mostrar imagen si existe la URL
    if 'url' in question and question['url']:
        st.image(question['url'], use_column_width=True)

    selected_option = st.session_state['answers']
    correct_option = question['answer']
    option_mapping = {opt[0]: opt for opt in question['options']}  # Mapear la letra con la opción

    # Crear botones para las opciones
    columns = st.columns(len(question['options']))
    for col_idx, option in enumerate(question['options']):
        button_label = option
        if selected_option is not None:
            if option == option_mapping[correct_option]:
                if option == selected_option:
                    button_label = f"✅ {option}"
                elif selected_option != correct_option:
                    button_label = f"❌ {option}"

        if st.button(button_label, key=f"q{question_idx}_opt{col_idx}"):
            st.session_state['answers'] = option

    # Mostrar respuesta correcta después de seleccionar una opción
    if selected_option is not None:
        correct_answer = option_mapping[correct_option]
        st.markdown(f"<h3 style='color:blue;'>Respuesta correcta: {correct_answer}</h3>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Botón para activar el modo aleatorio
random_mode = st.sidebar.checkbox("Modo Aleatorio")
if random_mode:
    st.session_state['random_mode'] = True
else:
    st.session_state['random_mode'] = False

# Botones para cargar diferentes archivos JSON con preguntas
st.sidebar.markdown("### Cargar Preguntas")
file_option = st.sidebar.radio("Seleccionar Categoria:", ('Data Engineer Google Cloud', 'PowerBI'))

if file_option == 'Data Engineer Google Cloud':
    st.session_state['questions'] = load_questions('./questionscloud.json')
elif file_option == 'PowerBI':
    st.session_state['questions'] = load_questions('./questionspower.json')

# Mostrar preguntas
if st.session_state['questions']:
    if st.session_state['random_mode']:
        if st.session_state['current_random_idx'] < len(st.session_state['questions']):
            random_question_idx = st.session_state['current_random_idx']
            show_question(st.session_state['questions'][random_question_idx], random_question_idx)

            # Botón para siguiente pregunta aleatoria
            if st.button("Siguiente Pregunta"):
                st.session_state['current_random_idx'] += 1
                st.session_state['answers'] = None
    else:
        for idx in range(len(st.session_state['questions'])):
            show_question(st.session_state['questions'][idx], idx)

# Limpiar sesión si se cambia de archivo
if st.session_state['questions'] is None:
    st.session_state['answers'] = None
    st.session_state['current_random_idx'] = 0
