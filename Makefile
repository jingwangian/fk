build:
	docker build -t fractal/server .

initdb:
	@echo "Starting to init database..."
	docker-compose run server scripts/init_db.sh
	@echo "All done"

mockdata:
	@echo "Starting to insert mock data into database..."
	docker-compose run server invoke add
	@echo "All done"

lint:
	@echo "Starting to lint checking..."
	flake8
	@echo "All done"

test:
	scripts/run_test.sh

run:
	docker-compose up -d
