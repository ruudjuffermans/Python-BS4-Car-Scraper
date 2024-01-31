ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY src/ /workspace/src
COPY run.py /workspace/run.py

