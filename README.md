from root dir:
1. backend:
    ```bash
    uv run python -m backend.main
    ```

2. frontend:
    ```bash
     uv run streamlit run frontend/main.py
    ```

3. tests:
    ```bash
     uv run pytest --cov=backend
    ```
