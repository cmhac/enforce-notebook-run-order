all: README.md

.PHONY: all docs

README.md: \
		GITHUB_README.rst \
		$(wildcard docs/*.rst)
	pandoc $< -o $@

docs:
	$(MAKE) -C docs html