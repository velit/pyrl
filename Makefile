test:
	py.test

profile-test:
	python -m profile/profile
	less profiling_results

debug:
	python -m pdb pyrl.py

clean:
	find . -name '*.pyc' -delete
	rm -f errors.err profiling_results

release:
	python setup.py sdist
