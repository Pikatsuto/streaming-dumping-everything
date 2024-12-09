all: start

VENV = venv
VBIN = $(VENV)/bin
DRIVER := $(shell whereis chromedriver | cut -d " " -f 2)
ARGS := $(shell [ -z $(ARGS) ] && echo "-sd -t 6" || echo $(ARGS))

$(VENV):
	python3 -m venv venv
	$(VBIN)/pip install -e .

build:
	docker compose kill
	docker build -t pikatsuto/streaming-dumping-everything .
	docker compose up -d

start: $(VENV)
	CHROMEDRIVER=$(DRIVER) ./venv/bin/python streaming-dumping-everything $(ARGS)

clean:
	rm -rf venv
	rm -rf *.-egg-info

.PHONY: all build start clean