all: README.md

.PHONY: all setup test docs

README.md: \
		GITHUB_README.rst \
		$(wildcard docs/*.rst)
	pandoc $< -o $@

setup:
	poetry install --with dev
	pre-commit install

test:
	poetry run pytest --cov
	poetry run coverage html

docs:
	$(MAKE) -C docs html