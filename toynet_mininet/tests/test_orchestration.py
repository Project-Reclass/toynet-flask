'''
Unit test suite for ToyNet Docker container orchistration utilities
'''

import pytest

from toynet_manager import ToynetManager

@pytest.fixture
def manager():
    '''
    Instantiate the ToynetManager class
    '''

    yield ToynetManager()

def test_check_resources(manager):
    '''
    Test that the ToynetManager can correctly assess resource constraints
    '''

    # Confirm high/low CPU usage detection
    assert manager.check_cpu_availability(100.0, 100.0, 100.0)
    assert not manager.check_cpu_availability(-1.0, -1.0, -1.0)

    # Confirm high/low memory usage detection
    assert manager.check_memory_availability(100, 0)
    assert not manager.check_memory_availability(0, 1024)

def test_build_image(manager):
    '''
    Test that the ToynetManager can build images as directed
    '''

    # Test invalid filename
    assert not manager.build_mininet_container(dev=False, docker_file='fake_file')
    assert manager.dev_image is None

    # Test development image build
    assert manager.build_mininet_container()
    assert manager.dev_image is not None and 'toynet-dev:latest' in manager.dev_image.tags

    # Test production image build
    assert manager.build_mininet_container(False, 'Dockerfile')
    assert manager.prod_image is not None and 'toynet:latest' in manager.prod_image.tags

def test_run_container(manager):
    '''
    Test that the ToynetManager can run containers correctly
    '''

    # Test invalid filename
    no_container = manager.run_mininet_container()
    assert no_container == '' and no_container not in manager.running_containers

    # Build images
    manager.build_mininet_container()
    manager.build_mininet_container(False, 'Dockerfile')

    # Test development container
    dev_container = manager.run_mininet_container()
    assert dev_container != '' and dev_container in manager.running_containers

    # Test production container
    prod_container = manager.run_mininet_container(dev=False)
    assert prod_container != '' and prod_container in manager.running_containers

    # Test killing nonexistent container
    assert not manager.kill_container(None)

    # Test killing development and production containers
    assert manager.kill_container(dev_container)
    assert manager.kill_container(prod_container)

def test_import_image(manager):
    '''
    Test that the ToynetManager can import images as directed
    '''

    # Test invalid filename
    assert not manager.import_image(dev=False, image_name='fake_image')
    assert manager.dev_image is None

    # Test development image build
    assert manager.import_image()
    assert manager.dev_image is not None and 'toynet-dev:latest' in manager.dev_image.tags

    # Test production image build
    assert manager.import_image(dev=False, image_name='toynet')
    assert manager.prod_image is not None and 'toynet:latest' in manager.prod_image.tags
