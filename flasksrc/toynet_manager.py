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

'''
This module provides utilities for building the Toynet container and managing
its lifecycle as well as providing a way to ensure that the system does not
overcommit resources.
'''

import sys
import docker
import psutil

DEV_IMAGE = 'toynet-dev'
PROD_IMAGE = 'toynet'


class ToynetManager():
    '''
    This class enables management of Toynet containers running within a local
    Docker environment as well as facilitating resource checks and managing
    Toynet Docker images.

    Public methods:
        run_mininet_container
        build_mininet_container
        import_image
    Public static methods:
        check_cpu_availability
        check_memory_availability
        check_network_exists
    Instance variables:
        client: a DockerClient to communicate with the Docker daemon
        dev_image: an Image object of the development Toynet image
        prod_image: an Image object of the production Toynet image
        running_containers: Dict(String: Container) containing all the started
        containers, referenced by their names
    '''

    def __init__(self, net):
        '''
        Creates the DockerClient needed to communicate with the Docker daemon.
        Development and production Docker images are initially None until built
        within this instance.
        '''

        self.client = docker.from_env()
        self.dev_image = None
        self.prod_image = None
        self.running_containers = dict()
        if not self.check_network_exists(self.client, net):
            raise docker.errors.APIError('Docker network does not exist,'
                                         f'make sure to create it: {net}')

    def run_mininet_container(self, dev=True, net='bridge'):
        '''
        Runs the specified Docker image as a container and binds the provided
        file for Toynet to parse its initial topology from.

        dev: bool - True if we want to run the developer image, False for
                    production
        net: String - the Docker network we want this container to attach to

        returns: String - the name of the container running, empty string if no
                          image is available
        '''

        vol = dict()
        vol['/lib/modules'] = {'bind': '/lib/modules', 'mode': 'ro'}
        image_name = ''

        if dev and self.dev_image is not None:
            image_name = self.dev_image
        elif not dev and self.prod_image is not None:
            image_name = self.prod_image
        else:
            return image_name

        # Ensure the network exists already
        if not self.check_network_exists(self.client, net):
            return ''

        new_container = self.client.containers.run(image_name, privileged=True,
                                                   remove=True, detach=True,
                                                   network=net, volumes=vol)
        self.running_containers[new_container.name] = new_container

        return new_container.name

    def build_mininet_container(self, dev=True, docker_file='dev.Dockerfile'):
        '''
        Builds the Toynet container from the local Dockerfile or dev.Dockerfile.

        dev: bool - True indicates to build the development image, False
                    indicates to build the production image
        dockerfile: String - indicates the relative path to the Dockerfile to
                             use for the image build

        returns: True if successful build, False otherwise
        '''

        if dev:
            try:
                self.dev_image = self.client.images.build(path='.',
                                                          dockerfile=docker_file,
                                                          rm=True, tag=DEV_IMAGE)[0]
            except docker.errors.APIError:
                self.dev_image = None
                return False
        else:
            try:
                self.prod_image = self.client.images.build(path='.', dockerfile=docker_file,
                                                           rm=True, tag=PROD_IMAGE)[0]
            except docker.errors.APIError:
                self.prod_image = None
                return False

        return True

    def import_image(self, dev=True, image_name=DEV_IMAGE):
        '''
        Imports the specified Toynet image from the existing Docker environment

        dev: bool - True indicates to import the development image, False
                    indicates to import the production image
        image_name: String - indicates the image tag to import
        '''

        if dev:
            try:
                self.dev_image = self.client.images.get(image_name)

            except (docker.errors.ImageNotFound, docker.errors.APIError):
                self.dev_image = None
                return False
        else:
            try:
                self.prod_image = self.client.images.get(image_name)

            except (docker.errors.ImageNotFound, docker.errors.APIError):
                self.prod_image = None
                return False

        return True

    def kill_container(self, container_name):
        '''
        Kills the specified Docker container if running.

        container_name: String - the name of the container to kill

        returns: True if the container was killed, False otherwise
        '''

        res = None

        try:
            self.running_containers[container_name].kill()
            del self.running_containers[container_name]
            res = True
        except (KeyError, docker.errors.APIError):
            res = False

        return res

    @staticmethod
    def check_network_exists(client, network_name):
        '''
        Checks if the specified network exists and creates it if not.

        client: DockerClient - the client used to interact with the Docker engine
        network_name: String - the name of the network to check for

        returns: bool - True if the network exists created, False otherwise
        '''

        try:
            networks = client.networks.list()
        except docker.errors.APIError:
            return False

        for network in networks:
            if network.name == network_name:
                return True

        return False

    @staticmethod
    def check_cpu_availability(short_thresh=80.0, med_thresh=75.0, long_thresh=70.0):
        '''
        Polls the CPU load and determines if the system can safely start
        another Toynet container.

        short_thresh: float - the threshold for above which we consider the one
                              minute average CPU load to be too high
        med_thresh: float - the threshold for above which we consider the five
                              minute average CPU load to be too high
        long_thresh: float - the threshold for above which we consider the
                             fifteen minute average CPU load to be too high

        returns: bool - True if CPU load is below thresholds, False otherwise
        '''

        # CPU percent usage representation for the past 1, 5, and 15 minutes
        try:
            loads = [load / psutil.cpu_count() * 100 for load in psutil.getloadavg()]
        except OSError:
            return False

        # We say the CPU usage is available if we are keeping a good
        # utilization buffer in long and short timescales
        for load, threshold in zip(loads, [short_thresh, med_thresh, long_thresh]):
            if load > threshold:
                return False
        return True

    @staticmethod
    def check_memory_availability(threshold=75.0, min_mem=2):
        '''
        Polls system memory to determine if the system can safely start another
        Toynet container.

        threshold: float - the maximum RAM usage above which we consider the
                           system unable to support another Toynet container.
        min_mem: int - the minimum number of GiB of available memory we
                       require to consider the system able to support another
                       Toynet container. Defaults to 2 GiB because most of our
                       containers build from Ubuntu images with 2 GiB
                       minimum recommended RAM.

        returns: bool - True if memory availability meets minimum requirements,
                        False otherwise
        '''

        ONE_GB = 1024 ** 3
        memory = psutil.virtual_memory()

        return memory.percent < threshold and memory.available > min_mem * ONE_GB


def main():
    '''
    Hello world example code to use this module to test resources, build the
    Toynet image, and run the Toynet container.
    '''
    test_toynet = ToynetManager()

    # Resource checks
    if test_toynet.check_cpu_availability(85.0, 75.0, 60.0):
        print('Sufficient CPU')
    else:
        print('Insufficient CPU')
        sys.exit(1)
    if test_toynet.check_memory_availability():
        print('Sufficient RAM')
    else:
        print('Insufficient RAM')
        sys.exit(1)

    # Build containers
    test_toynet.build_mininet_container()
    test_toynet.build_mininet_container(dev=False, docker_file='Dockerfile')
    print('Finished building images')

    # Run containers
    print('Running containers')
    dev_container = test_toynet.run_mininet_container()
    prod_container = test_toynet.run_mininet_container(dev=False)

    # Kill the containers
    if test_toynet.kill_container(dev_container):
        print('Killed development container successfully')
    else:
        print('Error killing dev container')
    if test_toynet.kill_container(prod_container):
        print('Killed production container successfully')
    else:
        print('Error killing production container')


if __name__ == '__main__':
    main()
