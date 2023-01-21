FROM python:3.10-slim

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
EXPOSE 4000

CMD ["python", "src/tools/scrape_new_deadlines.py"]