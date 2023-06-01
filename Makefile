all: README.md

.PHONY: all docs test

README.md: \
		GITHUB_README.rst \
		$(wildcard docs/*.rst)
	pandoc $< -o $@

setup:
	poetry install
	pre-commit install

test:
	poetry run pytest --cov
	poetry run coverage html

docs:
	$(MAKE) -C docs html