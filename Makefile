.PHONY: smoke test lint

smoke:
	PYTHONPATH=src python3 -m retail_video_intelligence smoke

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

lint:
	python3 -m compileall -q src tests
	@if command -v ruff >/dev/null 2>&1; then ruff check .; else echo "ruff is not installed; compileall passed"; fi
