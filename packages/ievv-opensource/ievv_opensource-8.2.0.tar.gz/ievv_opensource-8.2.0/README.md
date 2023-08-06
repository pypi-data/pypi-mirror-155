# ievv_opensource

## Documentation
http://ievv-opensource.readthedocs.org/

## Using the docker development setup
This is nice if you do not want to install postgres, redis, correct python version etc. on your local machine.
Just use docker instead - see [not_for_deploy/guides/docker-develop.md](not_for_deploy/guides/docker-develop.md).


## How to release ievv_opensource
1. Update ``ievv_opensource/version.json``.
2. Add releasenote to releasenotes folder on root with name `releasenotes-<major-version>.md`.
3. Commit with ``Release <version>``.
4. Tag the commit with ``<version>``.
5. Push (``git push && git push --tags``).
6. Release to pypi (``python setup.py sdist && twine upload dist/ievv_opensource-<version>.tar.gz``).
