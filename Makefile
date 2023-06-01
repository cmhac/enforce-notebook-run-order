all: README.md

.PHONY: all docs test

README.md: \
		GITHUB_README.rst \
		$(wildcard docs/*.rst)
	pandoc $< -o $@

test:
	pytest --cov
	coverage html

docs:
	$(MAKE) -C docs html