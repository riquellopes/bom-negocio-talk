.SILENT:

help:
	@echo "Como usar make <option>"
	@echo ""
	@echo "Opções:"
	@echo " run"
	@echo " tests"

run:
	python talk.py

tests:
	nosetests --with-coverage test/
