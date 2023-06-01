all: README.md

.PHONY: all docs

README.md: \
		GITHUB_README.rst \
		$(wildcard docs/*.rst)
	pandoc README.rst -o README.md

docs:
	$(MAKE) -C docs html