FROM python:3.9

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry --version

RUN poetry install --no-dev

COPY . /app

CMD ["poetry", "run", "python", "main.py"]

