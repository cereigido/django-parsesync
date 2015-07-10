install:
	@pip install -e .
	@pip install -r requirements-dev.txt

clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@rm -rf dist build

test: clean
	@python runtests.py --verbosity 2 --with-coverage --cover-html --cover-package=parsesync --with-yanc

sdist:
	@python setup.py sdist
