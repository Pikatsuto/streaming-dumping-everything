# Nix builder
FROM debian:trixie

RUN apt update \
    && apt install -y \
        python3-full \
        python3-setuptools \
        python3-selenium \
        python3-wheel \
        chromium-driver \
        chromium \
        chromium-l10n \
        make \
        bash \
    && apt clean -y

SHELL ["/bin/bash", "-c"]

COPY . /app
WORKDIR /app

RUN python3 -m venv venv \
    && venv/bin/pip install -e .

ENV ARGS=""

CMD ["make"]