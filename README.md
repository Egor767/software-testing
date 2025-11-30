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

    frontend:
    ```bash
      uv run pytest frontend/tests/ --cache-clear
    ```
   backend:
    ```bash
      uv run pytest backend/tests/ --cov=backend --cov-report=term-missing --cov-fail-under=75 --cache-clear
    ```

