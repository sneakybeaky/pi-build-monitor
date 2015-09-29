import logging
import time
from build_status import Status
from swirly import Swirly

import unicornhat as UH
import time


class Monitor(object):
    '''Polls a GO build server and changes display depending on what happens
    '''

    def __init__(self, go_server, buildname):
        self.go_server = go_server
        self.buildname = buildname
        self.logger = logging.getLogger(__name__ + '.Monitor')

        self.logger.debug("Monitoring {0}".format(buildname))
        self.swirly = Swirly()

    def monitor(self):
        self.logger.debug("Starting to monitor")

        while 1:
            build_status = self.get_status()

            if build_status['activity'] != 'Building':
                self.logger.debug('Not building')

                self.set_build_result(build_status)
                time.sleep(5)

            else:
                self.do_building()

    def get_status(self):
        status = Status(self.go_server)
        self.logger.debug("Status is {0}".format(status))

        build_status = status.projects[self.buildname]
        return build_status

    def set_build_result(self, build_status):
        if build_status['lastBuildStatus'] == 'Success':
            self.set_build_success()
        else:
            self.set_build_failure()

    def set_build_success(self):
        self.logger.debug("Last build worked !")
        for y in range(8):
            for x in range(8):
                UH.set_pixel(x, y, 0, 255, 0)
                UH.show()
                time.sleep(0.05)

    def set_build_failure(self):
        self.logger.debug("Last build failed !")

        for y in range(8):
            for x in range(8):
                UH.set_pixel(x, y, 255, 0, 0)
                UH.show()
                time.sleep(0.05)

    def do_building(self):
        self.logger.debug("Building...")
        self.swirly.show(5)
