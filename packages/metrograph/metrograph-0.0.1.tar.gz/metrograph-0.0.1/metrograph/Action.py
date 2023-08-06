"""

    Metrograph Core - Action
    
    Author:             Hamza EL GARRAB
    License:            MIT
    Last Update:        May 29th 2022

"""

import os
import docker
from metrograph.errors import ImageNotFound, ContainerError, APIError
from metrograph.errors.BuildError import BuildError

class Action:

    METROGRAPH_CONTAINER_HOME = '/home/metrograph/action'
    client = docker.from_env()

    def __init__(self, uuid, runtime, runtime_version):
        self.uuid = uuid
        self.runtime = runtime
        self.runtime_version = runtime_version
        self.project_path = f'{os.environ["METROGRAPH_HOME"]}/actions/{self.uuid}'
        self.action_path = f'{os.environ["METROGRAPH_HOME"]}/actions/{self.uuid}/action'

    def get_images():
        try:
            result = Action.client.images.list()
        except docker.errors.APIError as e:
            raise APIError(e)

    def get_image(name):
        try:
            result = Action.client.images.get(name)
        except docker.errors.ImageNotFound as e:
            raise ImageNotFound(e, name)
        except docker.errors.APIError as e:
            raise APIError(e)

    def build_image(self):
        try:
            Action.client.images.build(path=self.project_path, tag=f"metrograph/action_{self.uuid}", rm=True, pull=True)
        except docker.errors.BuildError as e:
            raise BuildError(e)
        except docker.errors.APIError as e:
            raise APIError(e)

    def run(self):
        try:
            volumes = {
                self.action_path : {'bind': Action.METROGRAPH_CONTAINER_HOME, 'mode': 'rw'}
            }
            c = Action.client.containers.run(f"metrograph/action_{self.uuid}", detach = False, volumes = volumes)
        except docker.errors.ImageNotFound as e:
            raise ImageNotFound(e, image_name=f"metrograph/action_{self.uuid}")
        except docker.errors.APIError as e:
            raise APIError(e)
        except ContainerError as e:
            raise ContainerError(e)


