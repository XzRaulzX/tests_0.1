import streamlit as st
import json
import random

# Función para cargar las preguntas desde un archivo JSON
def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['questions']

# Configuración inicial de la página
st.set_page_config(page_title="ExamTests", page_icon="🚀")

# Estado inicial de la sesión
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}
if 'questions' not in st.session_state:
    st.session_state['questions'] = {'Data Engineer Google Cloud': None, 'PowerBI': None}
if 'random_mode' not in st.session_state:
    st.session_state['random_mode'] = {'Data Engineer Google Cloud': False, 'PowerBI': False}
if 'current_question_idx' not in st.session_state:
    st.session_state['current_question_idx'] = {'Data Engineer Google Cloud': 0, 'PowerBI': 0}
if 'puntuacion_check' not in st.session_state:
    st.session_state['puntuacion_check'] = 0
if 'puntuacion_x' not in st.session_state:
    st.session_state['puntuacion_x'] = 0
if 'total_questions' not in st.session_state:
    st.session_state['total_questions'] = 0
if 'test_completed' not in st.session_state:
    st.session_state['test_completed'] = False

# Estilo personalizado para el diseño y puntuación
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
        display: flex;
        justify-content: space-between;
    }
    .footer-content div {
        flex: 1;
        text-align: center;
    }
    .footer-content .score {
        font-size: 18px;
        font-weight: bold;
        color: #333;
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

    # Verificar si existe una respuesta para esta pregunta
    selected_options = st.session_state['answers'].get(question_idx, [])
    correct_options = question['answer']
    option_mapping = {opt[0]: opt for opt in question['options']}  # Mapear la letra con la opción

    # Crear botones para las opciones
    for col_idx, option in enumerate(question['options']):
        button_label = option
        if option[0] in selected_options:
            if option[0] in correct_options:
                button_label = f"✅ {option}"
            else:
                button_label = f"❌ {option}"

        if st.button(button_label, key=f"q{question_idx}_opt{col_idx}"):
            if option[0] in selected_options:
                selected_options.remove(option[0])
            else:
                selected_options.append(option[0])
            st.session_state['answers'][question_idx] = selected_options

    # Mostrar respuestas correctas después de seleccionar una opción
    if selected_options:
        if set(selected_options) == set(correct_options):
            st.markdown(f"<h3 style='color:green;'>✅ ¡Respuesta(s) correcta(s)!</h3>", unsafe_allow_html=True)
            st.session_state['puntuacion_check'] += 1
        else:
            st.markdown(f"<h3 style='color:red;'>❌ Respuesta(s) incorrecta(s). La(s) correcta(s) es(son): {', '.join(correct_options)}</h3>", unsafe_allow_html=True)
            st.session_state['puntuacion_x'] += 1

    st.markdown('</div>', unsafe_allow_html=True)

# Botón para activar el modo aleatorio
random_mode = st.sidebar.checkbox("Modo Aleatorio")

# Botones para cargar diferentes archivos JSON con preguntas
st.sidebar.markdown("### Cargar Preguntas")
file_option = st.sidebar.radio("Seleccionar Categoría:", ('Data Engineer Google Cloud', 'PowerBI'))

if file_option == 'Data Engineer Google Cloud':
    if st.session_state['questions']['Data Engineer Google Cloud'] is None:
        st.session_state['questions']['Data Engineer Google Cloud'] = load_questions('./questionscloud.json')
    st.session_state['random_mode']['Data Engineer Google Cloud'] = random_mode
    questions = st.session_state['questions']['Data Engineer Google Cloud']
elif file_option == 'PowerBI':
    if st.session_state['questions']['PowerBI'] is None:
        st.session_state['questions']['PowerBI'] = load_questions('./questionspower.json')
    st.session_state['random_mode']['PowerBI'] = random_mode
    questions = st.session_state['questions']['PowerBI']

# Mostrar preguntas
if questions:
    if st.session_state['random_mode'][file_option]:
        if 'random_questions_order' not in st.session_state:
            st.session_state['random_questions_order'] = list(range(len(questions)))
            random.shuffle(st.session_state['random_questions_order'])
        
        random_order = st.session_state['random_questions_order']
        current_question_idx = st.session_state['current_question_idx'][file_option]

        if current_question_idx < len(random_order):
            show_question(questions[random_order[current_question_idx]], random_order[current_question_idx])

            # Avanzar a la siguiente pregunta si se selecciona una respuesta
            if st.session_state['answers'].get(random_order[current_question_idx]):
                st.session_state['current_question_idx'][file_option] += 1
        else:
            st.session_state['test_completed'] = True

    else:
        current_question_idx = st.session_state['current_question_idx'][file_option]
        if current_question_idx < len(questions):
            show_question(questions[current_question_idx], current_question_idx)

            # Avanzar a la siguiente pregunta si se selecciona una respuesta
            if st.session_state['answers'].get(current_question_idx):
                st.session_state['current_question_idx'][file_option] += 1
        else:
            st.session_state['test_completed'] = True

# Mostrar puntuación actualizada en el pie de página
st.markdown(
    """
    <div class="footer-content">
        <div>
            <h3 class="score">Puntuación check:</h3>
            <p>{}</p>
        </div>
        <div>
            <h3 class="score">Puntuación X:</h3>
            <p>{}</p>
        </div>
    </div>
    """.format(st.session_state['puntuacion_check'], st.session_state['puntuacion_x']),
    unsafe_allow_html=True
)

# Mostrar resultado del test al finalizar
if st.session_state['test_completed']:
    total_questions = len(questions)
    puntuacion_check = st.session_state['puntuacion_check']
    puntuacion_x = st.session_state['puntuacion_x']
    percentaje_aprobado = (puntuacion_check / total_questions) * 100

    if percentaje_aprobado > 75:
        st.markdown(
            f"<h2 style='color:green;'>Felicidades, has aprobado con un {percentaje_aprobado}% de respuestas correctas!</h2>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<h2 style='color:red;'>Has suspendido con un {percentaje_aprobado}% de respuestas correctas.</h2>",
            unsafe_allow_html=True
        )

# Botón para sumar 1 a la puntuación al hacer clic
if st.button("Elección Multiple"):
    st.session_state['puntuacion_check'] += 1
