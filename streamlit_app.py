import streamlit as st

from clients.maps import GIS_IMAGE_URL, get_coords_by_address
from ml_process import State, render_garage_data

# Инициализация состояния
if "coords" not in st.session_state:
    st.session_state.coords = None
if "search_state" not in st.session_state:
    st.session_state.search_state = State.NEW


def reset_app():
    """Полностью сбрасываем приложение"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


st.subheader("Детектор незаконных гаражей ;)")
st.write(
    "С помощью распознавания карт и запросов в Росреестр, ищем незаконные гаражи "
    "в области карты"
)

with open("README.md", "r", encoding="utf-8") as file:
    readme_content = file.read()

with st.expander("Как это работает"):
    st.markdown(readme_content)

with st.form("my_form"):
    address = st.text_input(
        label="Введите адрес области для поиска",
        value="Санкт-Петербург, улица Бутлерова",
        help="Адрес будет центральной точкой для поиска",
    )

    submit = st.form_submit_button("Задать область поиска", use_container_width=True)

    if submit:
        st.session_state.coords = get_coords_by_address(address)
        st.session_state.search_state = State.NEW

left_side, right_side = st.columns(2)

with left_side:
    if st.session_state.coords:
        st.image(image=f"{GIS_IMAGE_URL}{st.session_state.coords}")
        st.badge(
            f"Координаты: {st.session_state.coords}",
            icon=":material/location_on:",
            color="green",
            width="stretch",
        )

with right_side:
    if st.session_state.coords:
        # Поиск гаражей
        if st.session_state.search_state == State.NEW:
            if st.button("Найти объекты, похожие на гаражи", use_container_width=True):
                st.session_state.search_state = State.FOUND
                st.rerun()

        # Проверка в Росреестре
        elif st.session_state.search_state == State.FOUND:
            if st.button(
                "Проверить объекты в Росреестре",
                use_container_width=True,
                type="primary",
            ):
                st.session_state.search_state = State.CHECKED
                st.rerun()

        # Сброс поиска
        if st.session_state.search_state == State.CHECKED:
            if st.button("Начать новый поиск", use_container_width=True):
                reset_app()

        # Отображение таблицы
        table_data = render_garage_data(
            st.session_state.search_state, st.session_state.coords
        )
        if table_data:
            st.table(table_data)
