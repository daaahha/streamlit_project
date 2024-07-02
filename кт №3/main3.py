import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Загрузка данных из загруженного файла
df = st.file_uploader("Выберите файл CSV", type=['csv'])
if df is not None:
    data = pd.read_csv(df)

    # Создание заголовка
    st.title("Круговая диаграмма")

    # Нормализация столбца 'month' для получения года
    data['year'] = pd.to_datetime(data['month']).dt.year

    # Выбор уникальных значений года
    years = data['year'].unique()
    selected_year = st.selectbox('Выберите год', years)

    # Группировка данных по году
    yearly_data = data[data['year'] == selected_year].groupby('state')['permit'].sum().reset_index()

    # Выбор топ-10 штатов по данным разрешений
    top_states = yearly_data.nlargest(10, 'permit')

    # Визуализация данных (круговая диаграмма)
    st.write(f"### Круговая диаграмма количество разрешений на штат за определённый год")
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(top_states['permit'], startangle=90, labels=top_states['state'],
                                    autopct='%1.1f%%', pctdistance=0.90, textprops=dict(color="white", fontsize=12))
    ax.axis('equal')
    ax.legend(wedges, top_states['state'], title="States", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    st.pyplot(fig)

    # Выгрузка данных по штату
    state_to_export = st.selectbox('Выберите штат для выгрузки данных', yearly_data['state'])
    selected_state_data = yearly_data[yearly_data['state'] == state_to_export]
    st.write(selected_state_data)

    # Добавление возможности сохранения данные по количеству разрешений на штат
    if st.button('Сохранить данные по количеству разрешений на штат'):
        csv = selected_state_data.to_csv()
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="state_data.csv">Скачать данные по количеству разрешений на штат</a>'
        st.markdown(href, unsafe_allow_html=True)