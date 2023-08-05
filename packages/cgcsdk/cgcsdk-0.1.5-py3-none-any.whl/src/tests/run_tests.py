import time

# pylint: disable=import-error
from src.tests import volume_tests as vol, compute_tests as comp

VOLUME = "test-volume"

vol.test_volume_create(VOLUME)
time.sleep(3)

vol.test_volume_list(VOLUME)
comp.test_compute_create(VOLUME)
time.sleep(3)

comp.test_compute_list(VOLUME)
comp.test_compute_delete()
vol.test_volume_delete(VOLUME)
time.sleep(3)

comp.test_compute_list()
vol.test_volume_list()
