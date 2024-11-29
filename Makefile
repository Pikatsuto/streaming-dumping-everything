all: start

VENV = venv
VBIN = $(VENV)/bin

$(VENV):
	python3 -m venv venv
	$(VBIN)/pip install -e .

build:
	nix build
	docker build -t pikatsuto/streaming-dumping-everything .

start: $(VENV)
	bash streamde

clean:
	rm -rf venv
	rm -rf *.-egg-info

.PHONY: all install start clean