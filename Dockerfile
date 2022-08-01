FROM python:3.10.5

WORKDIR /scrapenewstodwh

RUN pip install pipenv

COPY . .

RUN pipenv install --system --deploy

CMD [ "python", "main.py" ]

