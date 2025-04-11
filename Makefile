.PHONY: fmt lint test check

# フォーマット（black + isort）
fmt:
	poetry run isort .
	poetry run black .

# 静的解析（flake8 + mypy）
lint:
	poetry run flake8 .
	poetry run mypy .

# テスト（pytest）
test:
	poetry run pytest

# fmtとlintだけまとめてチェック
check: fmt lint
