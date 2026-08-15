FROM python:3.14-slim

# Install Poetry
RUN pip install poetry

# Poetry: don't create a separate venv, install directly into the container's Python
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy only dependency files first (enables layer caching)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

# Now copy the actual source code
COPY . .

CMD ["python", "-m", "main"]