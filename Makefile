.PHONY: start
start:
	docker-compose up --build

.PHONY: stop
stop:
	docker-compose down

.PHONY: test-api
test-api:
	docker exec -it autonomous-b2b-sales-agent_api_1 pytest
