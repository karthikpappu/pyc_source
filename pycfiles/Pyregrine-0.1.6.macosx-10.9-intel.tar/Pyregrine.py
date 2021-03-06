# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/Pyregrine/Pyregrine.py
# Compiled at: 2014-12-11 14:53:53
import requests
from xml.etree import ElementTree

class Pyregrine(object):
    """
    A Python wrapper for Apache Falcon's RESTful API. Uses the external library 'Requests'. 
    
    @author: James Barney
    @version: 0.1
    @since: 6 DECEMBER 2014
    """

    def __init__(self, host='http://127.0.0.1', port='15000', path='api/'):
        self.host = host
        self.port = port
        self.path = path
        self.master_url = self.host + ':' + self.port + '/' + self.path
        self.credentials = {'user.name': 'admin', 'password': 'admin'}
        self.request = requests.Session()

    def _get(self, path, params):
        return self.request.get(self.master_url + path, params=params)

    def _post(self, path, params):
        return self.request.post(self.master_url + path, params=params)

    def _delete(self, path, params):
        return self.request.delete(self.master_url + path, params=params)

    def get_stack(self):
        """
        GET    api/admin/stack    Get stack of the server
        """
        params = self.credentials
        return self._get('admin/stack', params)

    def get_version(self):
        """
        GET    api/admin/version    Get version of the server
        """
        params = self.credentials
        return self._get('admin/version', params)

    def get_config(self, config_type):
        """
        GET    api/admin/config/:config-type    Get configuration information of the server
        :config-type can be build, deploy, startup or runtime.
        """
        params = self.credentials
        return self._get('admin/config/' + config_type, params)

    def validate_entity(self, entity_type):
        """
        POST    api/entities/validate/:entity-type    Validate the entity
        
        :entity-type can be cluster, feed or process.

        """
        params = self.credentials
        return self._post('entities/validate/' + entity_type, params)

    def submit_entity(self, entity_type):
        """
        POST    api/entities/submit/:entity-type    Submit the entity
        
        :entity-type can be cluster, feed or process.

        """
        params = self.credentials
        return self._post('entities/submit/' + entity_type, params)

    def update_entity(self, entity_type, entity_name, effective=None):
        """
        POST    api/entities/update/:entity-type/:entity-name    Update the entity
        :entity-type can be cluster, feed or process.
        :entity-name is name of the feed or process.
        ::effective is optional effective time

        """
        params = self.credentials
        params['effective='] = effective
        return self._post('entities/update/' + entity_type + '/' + entity_name, params)

    def submit_and_schedule_entity(self, entity_type):
        """
        POST    api/entities/submitAndSchedule/:entity-type    Submit & Schedule the entity
        :entity-type can either be a feed or a process.
        
        """
        return self._post('entities/submitAndSchedule/' + entity_type, self.credentials)

    def schedule_entity(self, entity_type, entity_name):
        """
        POST    api/entities/schedule/:entity-type/:entity-name    Schedule the entity
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._post('entities/schedule/' + entity_type + '/' + entity_name, params)

    def suspend_entity(self, entity_type, entity_name):
        """
        POST    api/entities/suspend/:entity-type/:entity-name    Suspend the entity
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._post('entities/suspend/' + entity_type + '/' + entity_name, params)

    def resume_entity(self, entity_type, entity_name):
        """
        POST    api/entities/resume/:entity-type/:entity-name    Resume the entity

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._post('entities/resume/' + entity_type + '/' + entity_name, params)

    def delete_entity(self, entity_type, entity_name):
        """
        DELETE    api/entities/delete/:entity-type/:entity-name    Delete the entity

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._delete('entities/delete/' + entity_type + '/' + entity_name, params)

    def get_entity_status(self, entity_type, entity_name):
        """
        GET    api/entities/status/:entity-type/:entity-name    Get the status of the entity

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._get('entities/status/' + entity_type + '/' + entity_name, params)

    def get_entity_definition(self, entity_type, entity_name):
        """
        GET    api/entities/definition/:entity-type/:entity-name    Get the definition of the entity

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._get('entities/definition/' + entity_type + '/' + entity_name, params)

    def get_entity_list(self, entity_type, fields=None, filterBy=None, tags=None, orderBy=None, sortOrder=None, offset=None, numResults=None):
        """
        GET    api/entities/list/:entity-type    Get the list of entities

        :entity_type Valid options are cluster, feed or process.
        :fields <optional param> Fields of entity that the user wants to view, separated by commas.
            Valid options are STATUS, TAGS, PIPELINES.
        ::filterBy <optional param> Filter results by list of field:value pairs. Example: filterBy=STATUS:RUNNING,PIPELINES:clickLogs
            Supported filter fields are NAME, STATUS, PIPELINES, CLUSTER.
            Query will do an AND among filterBy fields.
        ::tags <optional param> Return list of entities that have specified tags, separated by a comma. Query will do AND on tag values.
            Example: tags=consumer=consumer@xyz.com,owner=producer@xyz.com
        ::orderBy <optional param> Field by which results should be ordered.
            Supports ordering by "name".
        ::sortOrder <optional param> Valid options are "asc" and "desc"
        ::offset <optional param> Show results from the offset, used for pagination. Defaults to 0.
        ::numResults <optional param> Number of results to show per request, used for pagination. Only integers > 0 are valid, Default is 10.
        
        GET http://localhost:15000/api/entities/list/process?filterBy=STATUS:RUNNING,PIPELINES:dataReplication&fields=status,pipelines,tags&tags=consumer=consumer@xyz.com&orderBy=name&offset=2&numResults=2
        """
        params = self.credentials
        params['fields='] = fields
        params['filterBy='] = filterBy
        params['tags='] = tags
        params['orderBy='] = orderBy
        params['sortOrder='] = sortOrder
        params['offset='] = offset
        params['numResults='] = numResults
        return self._get('entities/list/' + entity_type, params)

    def get_entity_summary(self, entity_type, cluster, start=None, end=None, fields=None, filterBy=None, tags=None, orderBy=None, sortOrder=None, offset=None, numResults=None, numInstances=None):
        """
        GET    api/entities/summary/:entity-type/:cluster    Get instance summary of all entities

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> Show entity summaries from this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            By default, it is set to (end - 2 days).
        ::end <optional param> Show entity summary up to this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            Default is set to now.
        ::fields <optional param> Fields of entity that the user wants to view, separated by commas.
            Valid options are STATUS, TAGS, PIPELINES.
        ::filterBy <optional param> Filter results by list of field:value pairs. Example: filterBy=STATUS:RUNNING,PIPELINES:clickLogs
            Supported filter fields are NAME, STATUS, PIPELINES, CLUSTER.
            Query will do an AND among filterBy fields.
        ::tags <optional param> Return list of entities that have specified tags, separated by a comma. Query will do AND on tag values.
            Example: tags=consumer=consumer@xyz.com,owner=producer@xyz.com
        ::orderBy <optional param> Field by which results should be ordered.
            Supports ordering by "name".
        ::sortOrder <optional param> Valid options are "asc" and "desc"
        ::offset <optional param> Show results from the offset, used for pagination. Defaults to 0.
        ::numResults <optional param> Number of results to show per request, used for pagination. Only integers > 0 are valid, Default is 10.
        ::numInstances <optional param> Number of recent instances to show per entity. Only integers > 0 are valid, Default is 7.
        """
        params = self.credentials
        params['start='] = start
        params['end='] = end
        params['fields='] = fields
        params['tags='] = tags
        params['orderBy='] = orderBy
        params['sortOrder='] = sortOrder
        params['offset='] = offset
        params['numResults='] = numResults
        params['numInstances='] = numInstances
        return self._get('entities/summary/' + entity_type + '/' + cluster, params)

    def get_entity_dependencies(self, entity_type, entity_name):
        """
        GET    api/entities/dependencies/:entity-type/:entity-name    Get the dependencies of the entity

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._get('entities/dependencies/' + entity_type + '/' + entity_name, params)

    def get_running_instances(self, entity_type, entity_name):
        """
        GET    api/instance/running/:entity-type/:entity-name    List of running instances.
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._get('instance/running/' + entity_type + '/' + entity_name, params)

    def get_list_instances(self, entity_type, entity_name):
        """
        GET    api/instance/list/:entity-type/:entity-name    List of instances

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        """
        params = self.credentials
        return self._get('instance/running/' + entity_type + '/' + entity_name, params)

    def get_status_instance(self, entity_type, entity_name, start=None, end=None, colo=None, lifecycle=None, filterBy=None, orderBy=None, sortOrder=None, offset=None, numResults=None, numInstances=None):
        """
        GET    api/instance/status/:entity-type/:entity-name    Status of a given instance
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> Show instances from this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            By default, it is set to (end - (10 * entityFrequency)).
        ::end <optional param> Show instances up to this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            Default is set to now.
        ::colo <optional param> Colo on which the query should be run.
        ::lifecycle <optional param> Valid lifecycles for feed are Eviction/Replication(default) and for process is Execution(default).
        ::filterBy <optional param> Filter results by list of field:value pairs. Example: filterBy=STATUS:RUNNING,CLUSTER:primary-cluster
            Supported filter fields are STATUS, CLUSTER, SOURCECLUSTER, STARTEDAFTER.
            Query will do an AND among filterBy fields.
        ::orderBy <optional param> Field by which results should be ordered.
            Supports ordering by "status","startTime","endTime","cluster".
        ::sortOrder <optional param> Valid options are "asc" and "desc"
        ::offset <optional param> Show results from the offset, used for pagination. Defaults to 0.
        ::numResults <optional param> Number of results to show per request, used for pagination. Only integers > 0 are valid, Default is 10.

        """
        params = self.credentials
        params['start='] = start
        params['end='] = end
        params['colo='] = colo
        params['lifecycle='] = lifecycle
        params['filterBy='] = filterBy
        params['orderBy='] = orderBy
        params['sortOrder='] = sortOrder
        params['offset='] = offset
        params['numResults='] = numResults
        params['numInstances='] = numInstances
        return self._get('instance/status/' + entity_type + '/' + entity_name, params)

    def kill_instance(self, entity_type, entity_name, start=None, lifecycle=None):
        """
        POST    api/instance/kill/:entity-type/:entity-name    Kill a given instance

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> start time of the entity.
        ::lifecycle <optional param> can be Eviction/Replication(default) for feed and Execution(default) for process.
        """
        params = self.credentials
        params['start='] = start
        params['lifecycle='] = lifecycle
        return self._post('instance/kill/' + entity_type + '/' + entity_name, params)

    def suspend_instance(self, entity_type, entity_name, start=None, lifecycle=None):
        """
        POST    api/instance/suspend/:entity-type/:entity-name    Suspend a running instance

        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start is the start time of the instance that you want to refer to
        ::lifecycle <optional param> can be Eviction/Replication(default) for feed and Execution(default) for process.
        """
        params = self.credentials
        params['start='] = start
        params['lifecycle='] = lifecycle
        return self._post('instance/suspend/' + entity_type + '/' + entity_name, params)

    def resume_instance(self, entity_type, entity_name, start=None, lifecycle=None):
        """
        POST    api/instance/resume/:entity-type/:entity-name    Resume a given instance
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> the start time of the instance that you want to refer to
        ::lifecycle <optional param> can be Eviction/Replication(default) for feed and Execution(default) for process.
        """
        params = self.credentials
        params['start='] = start
        params['lifecycle='] = lifecycle
        return self._post('instance/resume/' + entity_type + '/' + entity_name, params)

    def rerun_instance(self, entity_type, entity_name, start=None, lifecycle=None):
        """
        POST    api/instance/rerun/:entity-type/:entity-name    Rerun a given instance
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> the start time of the instance that you want to refer to
        ::lifecycle <optional param> can be Eviction/Replication(default) for feed and Execution(default) for process.
        """
        params = self.credentials
        params['start='] = start
        params['lifecycle='] = lifecycle
        return self._post('instance/rerun/' + entity_type + '/' + entity_name, params)

    def get_instance_logs(self, entity_type, entity_name, start=None, end=None, colo=None, runId=None, lifecycle=None, filterBy=None, orderBy=None, sortOrder=None, offset=None, numResults=None, numInstances=None):
        """
        GET    api/instance/logs/:entity-type/:entity-name    Get logs of a given instance
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> Show instances from this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            By default, it is set to (end - (10 * entityFrequency)).
        ::end <optional param> Show instances up to this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            Default is set to now.
        ::colo <optional param> Colo on which the query should be run.
        ::lifecycle <optional param> Valid lifecycles for feed are Eviction/Replication(default) and for process is Execution(default).
        ::filterBy <optional param> Filter results by list of field:value pairs. Example: filterBy=STATUS:RUNNING,CLUSTER:primary-cluster
            Supported filter fields are STATUS, CLUSTER, SOURCECLUSTER, STARTEDAFTER.
            Query will do an AND among filterBy fields.
        ::orderBy <optional param> Field by which results should be ordered.
            Supports ordering by "status","startTime","endTime","cluster".
        ::sortOrder <optional param> Valid options are "asc" and "desc"
        ::offset <optional param> Show results from the offset, used for pagination. Defaults to 0.
        ::numResults <optional param> Number of results to show per request, used for pagination. Only integers > 0 are valid, Default is 10.

        """
        params = self.credentials
        params['start='] = start
        params['end='] = end
        params['colo='] = colo
        params['runId='] = runId
        params['lifecycle='] = lifecycle
        params['filterBy='] = filterBy
        params['orderBy='] = orderBy
        params['sortOrder='] = sortOrder
        params['offset='] = offset
        params['numResults='] = numResults
        params['numInstances='] = numInstances
        return self._get('instance/logs/' + entity_type + '/' + entity_name, params)

    def get_instance_summary(self, entity_type, entity_name, start=None, end=None, colo=None, lifecycle=None):
        """
        GET    api/instance/summary/:entity-type/:entity-name    Return summary of instances for an entity
        
        :entity-type can either be a feed or a process.
        :entity-name is name of the entity.
        ::start <optional param> Show instances from this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            By default, it is set to (end - (10 * entityFrequency)).
        ::end <optional param> Show instances up to this date. Date format is yyyy-MM-dd'T'HH:mm'Z'.
            Default is set to now.
        ::colo <optional param> Colo on which the query should be run.
        ::lifecycle <optional param> Valid lifecycles for feed are Eviction/Replication(default) and for process is Execution(default).

        """
        params = self.credentials
        params['start='] = start
        params['end='] = end
        params['colo='] = colo
        params['lifecycle='] = lifecycle
        return self._get('instance/summary/' + entity_type + '/' + entity_name, params)

    def serialize_graph(self, entity_type, entity_name):
        """
        GET    api/graphs/lineage/serialize    dump the graph

        """
        params = self.credentials
        return self._get('graphs/lineage/' + entity_type + '/' + entity_name, params)

    def get_all_vertices(self):
        """
        GET    api/graphs/lineage/vertices/all    get all vertices

        """
        params = self.credentials
        return self._get('graphs/lineage/vertices/all', params)

    def get_kv_vertex(self, key, value):
        """
        GET    api/graphs/lineage/vertices?key=:key&value=:value    get all vertices for a key index

        """
        params = self.credentials
        params['key='] = key
        params['value='] = value
        return self._get('graphs/lineage/vertices', params)

    def get_vertex(self, vertex_id):
        """
        GET    api/graphs/lineage/vertices/:id    get the vertex with the specified id

        """
        params = self.credentials
        return self._get('graphs/lineage/vertices/' + vertex_id, params)

    def get_vertex_properties(self, vertex_id, relationships=False):
        """
        GET    api/graphs/lineage/vertices/properties/:id?relationships=:true    get the properties of the vertex with the specified id

        """
        params = self.credentials
        params['relationships='] = relationships
        return self._get('graphs/lineage/vertices/properties/' + vertex_id, params)

    def get_adjacent_vertices(self, vertex_id, direction):
        """
        GET    api/graphs/lineage/vertices/:id/:direction    get the adjacent vertices or edges of the vertex with the specified direction

        """
        params = self.credentials
        return self._get('graphs/lineage/vertices/' + vertex_id + '/' + direction, params)

    def get_all_edges(self):
        """
        GET    api/graphs/lineage/edges/all    get all edges

        """
        params = self.credentials
        return self._get('graphs/lineage/vertices/edges/all', params)

    def get_edge(self, vertex_id):
        """
        GET    api/graphs/lineage/edges/:id    get the edge with the specified id
        """
        params = self.credentials
        return self._get('graphs/lineage/vertices/' + vertex_id, params)


if __name__ == '__main__':
    peregrine = Pyregrine()
    feeds = peregrine.get_entity_list('feed', orderBy='name')
    print feeds.url
    tree = ElementTree.fromstring(feeds.text)
    for elem in tree.findall('.//'):
        print elem.tag
        print elem.text

    print
    feeds = peregrine.get_entity_list('process', orderBy='name')
    tree = ElementTree.fromstring(feeds.text)
    for elem in tree.findall('.//'):
        print elem.tag
        print elem.text

    print
    clusters = peregrine.get_entity_list('cluster')
    tree = ElementTree.fromstring(clusters.text)
    for elem in tree.findall('.//'):
        print elem.tag
        print elem.text