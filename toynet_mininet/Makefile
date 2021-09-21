help:
	@echo "Production targets:"
	@echo "\tprod-image --builds the production image"
	@echo "\tprod --runs the production container"
	@echo "\tprod-test --runs the tests on the production container; default: all tests; specific tests: 'ARGS=<filename>' "
	@echo "\t\texample: make prod-test ARGS=test_command.py"
	@echo "\tprod-interactive --interacts with mininet on the production container"
	@echo "\tprod-interactive-container --interacts with the production container"
	@echo ""
	@echo "Test targets:"
	@echo "\ttest-image --builds the test image"
	@echo "\ttest --runs the tests on the test container; default: all tests; specific tests: 'ARGS=<filename>' "
	@echo "\t\texample: make test ARGS=test_command.py"
	@echo "\tinteractive --interacts with mininet on the test container"
	@echo "\tinteractive-container --interacts with the test container"

prod: prod-image
	docker run --privileged -v /lib/modules:/lib/modules miniflask-prod

prod-test: prod-image
	docker run --privileged -v /lib/modules:/lib/modules --entrypoint "/bin/sh" miniflask-prod -c "/root/toynet-mininet/test-entrypoint.sh tests/$(ARGS)"

prod-interactive: prod-image
	docker run --privileged -it -v /lib/modules:/lib/modules --entrypoint "/bin/sh" miniflask-prod -c /root/toynet-mininet/interactive-entrypoint.sh

prod-interactive-container: prod-image
	docker run --privileged -it -v /lib/modules:/lib/modules --entrypoint "/bin/bash" miniflask-prod

test: test-image
	docker run --privileged -v /lib/modules:/lib/modules --entrypoint "/bin/sh" miniflask-dev -c "/root/toynet-mininet/test-entrypoint.sh tests/$(ARGS)"

interactive: test-image
	docker run --privileged -it -v /lib/modules:/lib/modules --entrypoint "/bin/sh" miniflask-dev -c /root/toynet-mininet/interactive-entrypoint.sh

interactive-container: test-image
	docker run --privileged -it -v /lib/modules:/lib/modules --entrypoint "/bin/bash" miniflask-dev

prod-image:
	docker build -f Dockerfile -t miniflask-prod .

test-image:
	docker build -f dev.Dockerfile -t miniflask-dev .
