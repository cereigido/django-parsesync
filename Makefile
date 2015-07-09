install:
	@pip install -e .
	@pip install -r requirements-dev.txt

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@rm -rf dist build

test: clean
	@python runtests.py

sdist:
	@python setup.py sdist
