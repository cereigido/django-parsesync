clean:
	@find . -name "*.pyc" -print0 | xargs -0 rm -rf
	@rm -rf dist build

install:
	@pip install -e .
	@pip install -r requirements-dev.txt

pypi:
	@python setup.py sdist upload -r pypi

pypiregister:
	@python setup.py register -r pypi

pypitest:
	@python setup.py sdist upload -r pypitest

pypitestregister:
	@python setup.py register -r pypitest

sdist:
	@python setup.py sdist

test: clean
	@python runtests.py --verbosity 2 --with-coverage --cover-html --cover-package=parsesync --with-yanc
