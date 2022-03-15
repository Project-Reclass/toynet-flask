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
	@echo "\tlint --runs the linting"

prod: prod-image
	docker run \
		--privileged \
		-v /lib/modules:/lib/modules miniflask-prod

prod-test: prod-image
	docker run \
		-t \
		--privileged \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/sh" miniflask-prod -c "/root/toynet-flask/toynet_mininet/test-entrypoint.sh tests/$(ARGS)"

prod-interactive: prod-image
	docker run \
		--privileged \
		-it \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/sh" miniflask-prod -c /root/toynet-flask/toynet_mininet/interactive-entrypoint.sh

prod-interactive-container: prod-image
	docker run \
		--privileged \
		-it \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/bash" miniflask-prod

test: test-image
	docker run \
		-t \
		--privileged \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/sh" miniflask-dev -c "/root/toynet-flask/toynet_mininet/test-entrypoint.sh tests/$(ARGS)"

interactive: test-image
	docker run \
		--privileged \
		-it \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/sh" miniflask-dev -c /root/toynet-flask/toynet_mininet/interactive-entrypoint.sh

interactive-container: test-image
	docker run \
		--privileged \
		-it \
		-v /lib/modules:/lib/modules \
		--entrypoint "/bin/bash" miniflask-dev

prod-image: submodule-init
	docker build --no-cache -f Dockerfile -t miniflask-prod .

test-image: submodule-init
	docker build -f dev.Dockerfile -t miniflask-dev .

lint:
	flake8 flasksrc --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 flasksrc --count --max-complexity=15 --max-line-length=100 --statistics	

submodule-init:
	cd mininet-submodule && git submodule update --init --recursive
