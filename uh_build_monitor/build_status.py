import logging
import json
from datetime import datetime

import xmltodict

from six import iteritems

from gocd_parser.retriever import url

class Status(object):
    '''A handler for cctray xml files.'''

    def __init__(self, go_server):
        '''Convert a string of cctray xml into python. From this, gather
        various metrics.
        An example cctray url:
            http://gocd.your.org:8080/go/cctray.xml'''
        self.go_server = go_server

        self.logger = logging.getLogger(__name__+'.Status')
        self.logger.debug("handling cctray.xml")

        retrieved = url.URL( self.go_server, '/cctray.xml')

        self.metrics = {}

        doc = xmltodict.parse("\n".join(retrieved.contents))
        projects = doc['Projects']['Project']

        self.logger.debug(json.dumps(projects, sort_keys=True,
                                     indent=2))

        self.projects = {}

        for project in projects:

            project_name = project['@name']
            project_data = {}
            project_data['lastBuildStatus'] = project['@lastBuildStatus']
            project_data['activity'] = project['@activity']


            build_date = datetime.strptime(
                project['@lastBuildTime']+'UTC',
                '%Y-%m-%dT%X%Z')
            age = datetime.now() - build_date

            project_data['lastBuildTime'] = build_date
            project_data['age'] = age

            self.projects[project_name] = project_data