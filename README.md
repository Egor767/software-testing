from root dir:
1. backend:
    ```bash
    uv run python backend/main.py
    ```

2. frontend:
    ```bash
     uv run streamlit run frontend/main.py
    ```

3. tests:
    ```bash
      uv run pytest --cov=backend --cov-report=term-missing --cov-fail-under=75 --cache-clear
    ```
