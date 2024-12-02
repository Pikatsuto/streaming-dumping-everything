all: start

VENV = venv
VBIN = $(VENV)/bin

$(VENV):
	python3 -m venv venv
	$(VBIN)/pip install -e .

build:
	docker build -t pikatsuto/streaming-dumping-everything .
	docker compose up -d

start: $(VENV)
	bash streamde

clean:
	rm -rf venv
	rm -rf *.-egg-info

.PHONY: all build start clean