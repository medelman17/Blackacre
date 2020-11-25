FROM python:3.7

ENV PYTHONPATH "${PYTHONPATH}:/blackacre"

RUN mkdir blackacre
ADD . ./blackacre

RUN python -m pip install -r ./blackacre/requirements.txt
RUN python -m spacy download en_core_web_md

EXPOSE 9999

CMD [ "python", "./blackacre/server.py", "--port", "9999" ]