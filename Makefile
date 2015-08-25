help:
	@echo "Como usar make <option>"
	@echo ""
	@echo "Opções:"
	@echo " run"
	@echo " test_app"

run:
	@python talk.py

test_app:
	@nosetests --with-coverage test/
