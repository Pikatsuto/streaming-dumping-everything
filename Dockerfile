# Nix builder
FROM debian:unstable-20241111

# Copy our source and setup our working dir.
COPY . /app
WORKDIR /app

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

RUN python3 -m venv venv \
    && venv/bin/pip install -e .

SHELL ["/bin/bash", "-c"]

CMD ["make"]