# This file is part of Toynet-Flask.
#
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

prod-tag = macroflask-prod
dev-tag = macroflask-dev

help:
	@echo "Production targets:"
	@echo "\tprod-image --builds the production image"
	@echo "\tprod --runs the production container"
	@echo "\tprod-test --runs the tests on the production container; default: all tests; specific tests: 'ARGS=<filename>' "
	@echo "\t\texample: make prod-test ARGS=test_command.py"
	@echo ""
	@echo "Test targets:"
	@echo "\ttest-image --builds the test image"
	@echo "\ttest --runs the tests on the test container; default: all tests; specific tests: 'ARGS=<filename>' "
	@echo "\t\texample: make test ARGS=test_command.py"
	@echo "\tlint --runs the flake8 lint tests that are part of the CI pipeline"
	@echo ""
	@echo "Toynet Mininet targets:"
	@echo "\tmininet-prod --runs the mininet container"
	@echo "\tmininet-prod-image --builds the mininet production image"
	@echo "\tmininet-prod-test --runs the tests on the mininet production container"
	@echo "\tmininet-test --runs the tests on the mininet container"
	@echo "\tmininet-test-image --builds the mininet test image"
	@echo "\tmininet-lint lints the mininet submodule"
	@echo "\tmininet-submodule-init --initializes the mininet submodule"
	@echo ""
	@echo "Pull Request Validation targets:"
	@echo "pr-validate --runs the linting and testing targets"
	

prod: prod-image mininet-prod-image
	docker run --privileged -v /lib/modules:/lib/modules -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock $(prod-tag)

prod-test: prod-image mininet-prod-image
	. environment/env-prod; docker run \
		-t \
		--network=$${COMPOSE_NETWORK} \
		--privileged \
		-v /lib/modules:/lib/modules \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--entrypoint "/bin/bash" $(prod-tag) -c "/app/test-entrypoint.sh tests/$(ARGS)"

test: test-image
	. environment/env-dev; docker run \
		-t \
		--network=$${COMPOSE_NETWORK} \
		--privileged \
		-v /lib/modules:/lib/modules \
		-v /var/run/docker.sock:/var/run/docker.sock \
		--entrypoint "/bin/bash" $(dev-tag) -c "/app/test-entrypoint.sh tests/$(ARGS)"

prod-image: mininet-prod-image
	. environment/env-prod; docker build \
		--build-arg FLASK_APP=$${FLASK_APP} \
		--build-arg FLASK_ENV=$${FLASK_ENV} \
		--build-arg TOYNET_IMAGE_TAG=$${TOYNET_IMAGE_TAG} \
		--build-arg MINI_FLASK_PORT=$${MINI_FLASK_PORT} \
		--build-arg COMPOSE_NETWORK=$${COMPOSE_NETWORK} \
		-f Dockerfile -t $(prod-tag) .

test-image: 
	. environment/env-dev; docker build \
		--build-arg FLASK_APP=$${FLASK_APP} \
		--build-arg FLASK_ENV=$${FLASK_ENV} \
		--build-arg TOYNET_IMAGE_TAG=$${TOYNET_IMAGE_TAG} \
		--build-arg MINI_FLASK_PORT=$${MINI_FLASK_PORT} \
		--build-arg COMPOSE_NETWORK=$${COMPOSE_NETWORK} \
		-f dev.Dockerfile -t $(dev-tag) .

mininet-prod: 
	$(MAKE) -C toynet_mininet prod

mininet-prod-test:
	$(MAKE) -C toynet_mininet-prod-test

mininet-prod-image:
	$(MAKE) -C toynet_mininet prod-image

mininet-test-image:
	$(MAKE) -C toynet_mininet test-image

mininet-test:
	$(MAKE) -C toynet_mininet test

mininet-lint:
	$(MAKE) -C toynet_mininet lint

mininet-submodule-init:
	$(MAKE) -C toynet_mininet submodule-init

#run linting that will be run from CI pipeline
lint:
	flake8 flasksrc --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 flasksrc --count --max-complexity=15 --max-line-length=100 --statistics

pr-validate: test lint mininet-lint mininet-test


