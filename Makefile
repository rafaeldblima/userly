.PHONY: run
run:
	@FLASK_APP=api.py FLASK_ENV=development flask run --host 0.0.0.0

.PHONY:	migrate
migrate:
	@FLASK_APP=api.py flask db upgrade

.PHONY:	test
test:
	@FLASK_APP=api.py flask test

.PHONY:	coverage
coverage:
	@FLASK_APP=api.py flask test --coverage
