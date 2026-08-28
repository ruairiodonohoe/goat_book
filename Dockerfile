FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install "django<6" python-dotenv gunicorn whitenoise

COPY src /src
COPY manage.py .

ENV PYTHONPATH="/src"

CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]