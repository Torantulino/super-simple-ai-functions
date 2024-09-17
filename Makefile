.PHONY: format-code check-code

format-code:
	black -l 100 ai_functions.py test_ai_functions.py
	isort ai_functions.py test_ai_functions.py

check-code:
	flake8 --max-line-length=100 ai_functions.py test_ai_functions.py

