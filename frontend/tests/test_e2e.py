import re
from playwright.sync_api import expect


class TestUrlShortener:
    def test_successful_url_shortening(
        self,
        setup_page,
        random_long_url,
        streamlit_url,
        api_url,
    ):
        page = setup_page

        page.goto(streamlit_url)

        url_input = page.get_by_placeholder("https://www.example.com/very/long/path...")
        url_input.fill(random_long_url)

        submit_button = page.get_by_role("button", name="Сократить")
        submit_button.click()

        page.wait_for_timeout(3000)

        short_url_element = page.locator("code").first
        expect(short_url_element).to_be_visible(timeout=10000)

        short_url = short_url_element.text_content()

        assert short_url is not None
        assert short_url.startswith(f"{api_url}/api/s/")

        url_pattern = re.compile(rf"^{re.escape(api_url)}/api/s/[a-zA-Z0-9]+$")
        assert url_pattern.match(short_url)

        link_element = page.locator("a").filter(has_text="Перейти")
        expect(link_element).to_be_visible()

    def test_invalid_url_shows_error(self, setup_page, streamlit_url):
        page = setup_page

        page.goto(streamlit_url)

        invalid_urls = [
            "invalid_url",
            "http://",
            "https://",
            "www.example.com",
        ]

        for invalid_url in invalid_urls:
            url_input = page.get_by_placeholder(
                "https://www.example.com/very/long/path..."
            )
            url_input.clear()
            url_input.fill(invalid_url)

            submit_button = page.get_by_role("button", name="Сократить")
            submit_button.click()

            try:
                error_422 = page.get_by_text("Ошибка: 422")
                error_connection = page.get_by_text("Не удалось подключиться к серверу")
                warning_message = page.get_by_text("Введите URL!")

                expect(
                    error_422.or_(error_connection).or_(warning_message)
                ).to_be_visible(timeout=5000)

            except Exception:
                error_elements = page.locator(
                    "[data-testid='stAlert'], .stAlert, [role='alert']"
                )
                expect(error_elements).to_be_visible()

            page.wait_for_timeout(1000)

    def test_empty_url_shows_warning(self, setup_page, streamlit_url):
        page = setup_page

        page.goto(streamlit_url)

        url_input = page.get_by_placeholder("https://www.example.com/very/long/path...")
        url_input.clear()

        submit_button = page.get_by_role("button", name="Сократить")
        submit_button.click()

        warning_message = page.get_by_text("Введите URL!")
        expect(warning_message).to_be_visible()
