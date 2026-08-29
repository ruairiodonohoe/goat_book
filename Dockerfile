FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && rm -rf /var/lib/apt/lists/*
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin:$PATH"

#COPY --from=uv /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT="/venv"
ENV PATH="/venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

# RUN python -m venv /venv
# ENV PATH="/venv/bin:$PATH"

# RUN pip install "django<6" python-dotenv gunicorn whitenoise


COPY src /src
COPY manage.py .

ENV PYTHONPATH="/src"

RUN uv run python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1

RUN adduser --uid 1234 nonroot
USER nonroot


CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]