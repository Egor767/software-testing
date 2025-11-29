import streamlit as st
import requests

st.title("URL Shortener")
st.markdown("---")

long_url = st.text_input(
    "Введите длинный URL:",
    placeholder="https://www.example.com/very/long/path...",
    help="Вставьте URL для сокращения",
)


if st.button("Сократить", type="primary", use_container_width=True):
    if long_url:
        try:
            response = requests.post(
                "http://localhost:8080/api/link",
                json={"long_url": long_url},
                timeout=10,
            )

            if response.status_code == 200:
                short_url = response.json()["slug"]

                st.success("Ссылка успешно сокращена!")
                st.code(short_url, language="text")

                st.link_button("Перейти", short_url)

            else:
                st.error(f"Ошибка: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Не удалось подключиться к серверу: {e}")
    else:
        st.warning("Введите URL!")
