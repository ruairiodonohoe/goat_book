FROM python:3.14-slim

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install "django<6" python-dotenv

COPY src /src
COPY manage.py .

ENV PYTHONPATH="/src"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]