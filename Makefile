VIRTUALENV_NAME=gcloud-run.$(shell pwd | rev | cut -d '/' -f 1 | rev)

.PHONY: install uninstall clean

uninstall:
	@./bin/remove_pyenv.sh

install: uninstall
	@./bin/setup_pyenv.sh $(VIRTUALENV_NAME)

clean:
	@./bin/cleanup.sh
