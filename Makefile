setup:
	pip install -r requirements.txt

test:
	py.test

build:
	rm -f dist/*
	python -m build

clean:
	pip uninstall django-aetos -y
	rm -f dist/*

install:
	pip install dist/*.whl

uninstall:
	pip uninstall django-aetos -y

install-dev:
	pip install -e .

upload-test:
	python3 -m twine upload --repository testpypi dist/*.tar.gz dist/*.whl

upload:
	python3 -m twine upload dist/*.tar.gz dist/*.whl

PART ?= "minor"

bump-version:
	bump-my-version bump ${PART}
	@echo now at version $$(bump-my-version show current_version)
