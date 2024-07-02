import streamlit as st
import pandas as pd
import base64

# Загрузка данных из загруженного файла
df = st.file_uploader("Выберите файл CSV", type=['csv'])
if df is not None:
    data = pd.read_csv(df)

    # Создание заголовка и описания дашборда
    st.title("Интерактивный дэшборд для данных из датафрейма по оружию")

    # Виджет для выбора параметра
    selected_param = st.selectbox("Выберите параметр", data.columns)

    # Отображение данных на основе выбранного параметра
    st.write(f"### Датафрейм по оружию")
    st.write(data)

    # Функция для отображения статистических показателей в реальном времени
    def show_stats():
        return data[selected_param].describe()

    # Получение статистических показателей
    stats_df = show_stats()

    # Отображение статистических показателей
    st.write(f"### Статистические показатели для {selected_param}")
    st.write(stats_df)

    # Добавление возможности сохранения результатов статистического анализа в CSV
    if st.button('Сохранить результаты статистических показателей в CSV'):
        csv = stats_df.to_csv()
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="stats_results.csv">Скачать результаты статистических показателей</a>'
        st.markdown(href, unsafe_allow_html=True)

