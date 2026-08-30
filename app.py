"""
📱 Flashcard Generator - Мобильное веб-приложение
Запустите: streamlit run app.py
Откройте на телефоне: http://[IP]:8501
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path

# Конфиг
st.set_page_config(
    page_title="📚 Flashcard Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Кастомный стиль
st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border-radius: 10px;
        }
        .card {
            border: 1px solid #e0e0e0;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .metric {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Инициализация session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

# Заголовок
st.markdown("# 📚 Flashcard Generator")
st.markdown("Создавайте карточки прямо с телефона")

# Метрика
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📝 Карточек", len(st.session_state.flashcards))
with col2:
    st.metric("📱 Устройства", "Поддерживаются все")
with col3:
    st.metric("💾 Сохранено", "Локально")

st.markdown("---")

# Основной контент
col1, col2 = st.columns([1, 1])

# ЛЕВАЯ КОЛОНКА - Добавление карточек
with col1:
    st.subheader("➕ Добавить новую карточку")
    
    with st.form("add_flashcard_form"):
        question = st.text_input(
            "❓ Вопрос",
            placeholder="Например: What is photosynthesis?",
            max_chars=150
        )
        
        answer = st.text_area(
            "✅ Ответ",
            placeholder="Введите ответ на вопрос",
            max_chars=500,
            height=100
        )
        
        topic = st.selectbox(
            "📋 Выберите тему",
            [
                "General",
                "🧬 Biology / Биология",
                "📜 History / История", 
                "🗺️ Geography / География",
                "📐 Mathematics / Математика",
                "🗣️ Language / Языки",
                "⚗️ Chemistry / Химия",
                "⚛️ Physics / Физика",
                "🎨 Art / Искусство"
            ]
        )
        
        submit = st.form_submit_button("➕ Добавить карточку", use_container_width=True)
        
        if submit and question and answer:
            new_card = {
                "id": int(datetime.now().timestamp() * 1000),
                "question": question,
                "answer": answer,
                "topic": topic,
                "created": datetime.now().isoformat()
            }
            st.session_state.flashcards.append(new_card)
            st.success("✅ Карточка добавлена!")
            st.rerun()
        elif submit:
            st.error("❌ Заполните вопрос и ответ!")

# ПРАВАЯ КОЛОНКА - Список карточек
with col2:
    st.subheader(f"📝 Ваши карточки ({len(st.session_state.flashcards)})")
    
    if st.session_state.flashcards:
        # Поиск
        search = st.text_input("🔍 Поиск по вопросам", "")
        
        # Фильтрация
        filtered = st.session_state.flashcards
        if search:
            filtered = [c for c in filtered if search.lower() in c['question'].lower()]
        
        if not filtered:
            st.info("😕 Карточки не найдены")
        else:
            for idx, card in enumerate(filtered):
                with st.container():
                    col_text, col_delete = st.columns([4, 1])
                    
                    with col_text:
                        st.write(f"**{idx + 1}. {card['question'][:60]}...**")
                        st.caption(f"{card['topic']} • {len(card['answer'])} символов")
                    
                    with col_delete:
                        if st.button("🗑️", key=f"del_{card['id']}", help="Удалить"):
                            st.session_state.flashcards.remove(card)
                            st.rerun()
    else:
        st.info("👆 Добавьте первую карточку в форму слева")

st.markdown("---")

# ЭКСПОРТ И ДЕЙСТВИЯ
st.subheader("💾 Действия")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Скачать JSON", use_container_width=True):
        json_data = json.dumps(st.session_state.flashcards, 
                              ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Скачать flashcards.json",
            data=json_data,
            file_name=f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

with col2:
    if st.button("📊 Скачать CSV", use_container_width=True):
        import csv
        from io import StringIO
        
        if st.session_state.flashcards:
            csv_buffer = StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=['question', 'answer', 'topic'])
            writer.writeheader()
            for card in st.session_state.flashcards:
                writer.writerow({
                    'question': card['question'],
                    'answer': card['answer'],
                    'topic': card['topic']
                })
            
            st.download_button(
                label="📊 Скачать flashcards.csv",
                data=csv_buffer.getvalue(),
                file_name=f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )

with col3:
    if st.button("🗑️ Очистить всё", use_container_width=True):
        if st.checkbox("⚠️ Подтвердите удаление"):
            st.session_state.flashcards = []
            st.success("✅ Все карточки удалены")
            st.rerun()

st.markdown("---")

# ИНФОРМАЦИЯ
with st.expander("ℹ️ Как использовать"):
    st.markdown("""
    ### 📱 Доступ с телефона:
    
    1. **На компьютере:**
       ```bash
       streamlit run app.py
       ```
    
    2. **Узнайте IP адрес:**
       ```bash
       ipconfig  # Windows
       # или
       ifconfig  # Mac/Linux
       ```
    
    3. **На телефоне в браузере:**
       ```
       http://[IP_КОМПЬЮТЕРА]:8501
       ```
    
    Где [IP_КОМПЬЮТЕРА] что-то типа: 192.168.1.100
    
    ### 💾 Сохранение:
    - Карточки сохраняются временно в памяти браузера
    - Скачивайте JSON файлы регулярно
    - Загружайте их обратно (создаём upload позже)
    
    ### ⌨️ Горячие клавиши:
    - `Ctrl+Enter` в форме вопроса = добавить карточку
    - Поиск работает в реальном времени
    
    ### 🎯 Следующие шаги:
    - Используйте скачанный JSON в Google Colab
    - Генерируйте красивые картинки там
    - Смотрите результаты в браузере телефона
    """)

with st.expander("🔧 Статистика"):
    if st.session_state.flashcards:
        topics = {}
        total_chars = 0
        
        for card in st.session_state.flashcards:
            topic = card['topic']
            topics[topic] = topics.get(topic, 0) + 1
            total_chars += len(card['question']) + len(card['answer'])
        
        st.write(f"📊 **Всего карточек:** {len(st.session_state.flashcards)}")
        st.write(f"📝 **Всего символов:** {total_chars}")
        st.write(f"📋 **Темы:**")
        for topic, count in topics.items():
            st.write(f"  - {topic}: {count}")
    else:
        st.info("Нет данных для отображения")

# Футер
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px 0;">
    💡 Совет: Регулярно скачивайте JSON файлы чтобы не потерять данные<br>
    🚀 Готовы к генерации картинок? Загрузите JSON в Google Colab!
</div>
""", unsafe_allow_html=True)
