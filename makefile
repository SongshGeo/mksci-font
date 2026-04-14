setup:
	make install-tests
	make install-jupyter
	make setup-pre-commit

# 安装必要的代码检查工具
# black: https://github.com/psf/black
# flake8: https://github.com/pycqa/flake8
# isort: https://github.com/PyCQA/isort
# nbstripout: https://github.com/kynan/nbstripout
# pydocstyle: https://github.com/PyCQA/pydocstyle
# pre-commit-hooks: https://github.com/pre-commit/pre-commit-hooks
setup-pre-commit:
	uv add --optional dev flake8 isort nbstripout pydocstyle pre-commit-hooks
	uv run pre-commit install

install-jupyter:
	uv add --optional dev ipykernel

install-tests:
	uv add --optional dev pytest allure-pytest

# https://timvink.github.io/mkdocs-git-authors-plugin/index.html
install-docs:
	uv add --optional docs mkdocs mkdocs-material mkdocs-git-revision-date-localized-plugin mkdocs-minify-plugin mkdocs-redirects mkdocs-awesome-pages-plugin mkdocs-git-authors-plugin "mkdocstrings[python]" mkdocs-bibtex mkdocs-macros-plugin mkdocs-callouts mkdocs-glightbox
