FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0
ARG requirements=requirement_files/development_requirement.txt
RUN apt-get update && apt-get install -y gcc libpq-dev gettext
ENV PIP_DEFAULT_TIMEOUT=100
ADD /${requirements} /code/${requirements}
RUN pip install -r /code/${requirements}
WORKDIR /code
ADD . /code/
ENTRYPOINT [ "/code/docker-entrypoint.sh" ]
EXPOSE $PORT