from collections import namedtuple
import logging
import traceback
from typing import List
import attr
from .node import PipelineNode, PipelineConnection
from .. import repositories, entities, services

logger = logging.getLogger(name='dtlpy')


class PipelineAverages:
    def __init__(
            self,
            avg_time_per_execution: float,
            avg_execution_per_day: float
    ):
        self.avg_time_per_execution = avg_time_per_execution
        self.avg_execution_per_day = avg_execution_per_day

    @classmethod
    def from_json(cls, _json: dict = None):
        if _json is None:
            _json = dict()
        return cls(
            avg_time_per_execution=_json.get('avgTimePerExecution', 'NA'),
            avg_execution_per_day=_json.get('avgExecutionsPerDay', 'NA')
        )


class NodeAverages:
    def __init__(
            self,
            node_id: str,
            averages: PipelineAverages
    ):
        self.node_id = node_id
        self.averages = averages

    @classmethod
    def from_json(cls, _json: dict):
        return cls(
            node_id=_json.get('nodeId', None),
            averages=PipelineAverages.from_json(_json.get('executionStatistics'))
        )


class PipelineCounter:
    def __init__(
            self,
            status: str,
            count: int
    ):
        self.status = status
        self.count = count


class NodeCounters:
    def __init__(
            self,
            node_id: str,
            counters: List[PipelineCounter]
    ):
        self.node_id = node_id
        self.counters = counters

    @classmethod
    def from_json(cls, _json: dict):
        return cls(
            node_id=_json.get('nodeId', None),
            counters=[PipelineCounter(**c) for c in _json.get('statusCount', list())],
        )


class PipelineStats:
    def __init__(
            self,
            pipeline_counters: List[PipelineCounter],
            node_counters: List[NodeCounters],
            pipeline_averages: PipelineAverages,
            node_averages: List[NodeAverages]
    ):
        self.pipeline_counters = pipeline_counters
        self.node_counters = node_counters
        self.pipeline_averages = pipeline_averages
        self.node_averages = node_averages

    @classmethod
    def from_json(cls, _json: dict):
        return cls(
            pipeline_counters=[PipelineCounter(**c) for c in _json.get('pipelineExecutionCounters', list())],
            node_counters=[NodeCounters.from_json(_json=c) for c in _json.get('nodeExecutionsCounters', list())],
            pipeline_averages=PipelineAverages.from_json(_json.get('pipelineExecutionStatistics', None)),
            node_averages=[NodeAverages.from_json(_json=c) for c in _json.get('nodeExecutionStatistics', list())]
        )


@attr.s
class Pipeline(entities.BaseEntity):
    """
    Package object
    """
    # platform
    id = attr.ib()
    name = attr.ib()
    creator = attr.ib()
    org_id = attr.ib()
    connections = attr.ib()

    # name change
    created_at = attr.ib()
    updated_at = attr.ib(repr=False)
    start_nodes = attr.ib()
    project_id = attr.ib()
    composition_id = attr.ib()
    url = attr.ib()
    preview = attr.ib()
    description = attr.ib()
    revisions = attr.ib()

    # sdk
    _project = attr.ib(repr=False)
    _client_api = attr.ib(type=services.ApiClient, repr=False)
    _repositories = attr.ib(repr=False)

    @staticmethod
    def _protected_from_json(_json, client_api, project, is_fetched=True):
        """
        Same as from_json but with try-except to catch if error
        :param _json: platform json
        :param client_api: ApiClient entity
        :param is_fetched: is Entity fetched from Platform
        :return:
        """
        try:
            pipeline = Pipeline.from_json(
                _json=_json,
                client_api=client_api,
                project=project,
                is_fetched=is_fetched
            )
            status = True
        except Exception:
            pipeline = traceback.format_exc()
            status = False
        return status, pipeline

    @classmethod
    def from_json(cls, _json, client_api, project, is_fetched=True):
        """
        Turn platform representation of pipeline into a pipeline entity

        :param dict _json: platform representation of package
        :param dl.ApiClient client_api: ApiClient entity
        :param dtlpy.entities.project.Project project: project entity
        :param bool is_fetched: is Entity fetched from Platform
        :return: Pipeline entity
        :rtype: dtlpy.entities.pipeline.Pipeline
        """
        if project is not None:
            if project.id != _json.get('projectId', None):
                logger.warning('Pipeline has been fetched from a project that is not belong to it')
                project = None

        connections = [PipelineConnection.from_json(_json=con) for con in _json.get('connections', list())]
        inst = cls(
            created_at=_json.get('createdAt', None),
            updated_at=_json.get('updatedAt', None),
            project_id=_json.get('projectId', None),
            org_id=_json.get('orgId', None),
            composition_id=_json.get('compositionId', None),
            creator=_json.get('creator', None),
            client_api=client_api,
            name=_json.get('name', None),
            project=project,
            id=_json.get('id', None),
            connections=connections,
            start_nodes=_json.get('startNodes', None),
            url=_json.get('url', None),
            preview=_json.get('preview', None),
            description=_json.get('description', None),
            revisions=_json.get('revisions', None),
        )
        for node in _json.get('nodes', list()):
            inst.nodes.add(node=PipelineNode.from_json(node))
        inst.is_fetched = is_fetched
        return inst

    def to_json(self):
        """
        Turn Package entity into a platform representation of Package

        :return: platform json of package
        :rtype: dict
        """
        _json = attr.asdict(self,
                            filter=attr.filters.exclude(attr.fields(Pipeline)._project,
                                                        attr.fields(Pipeline)._repositories,
                                                        attr.fields(Pipeline)._client_api,
                                                        attr.fields(Pipeline).project_id,
                                                        attr.fields(Pipeline).org_id,
                                                        attr.fields(Pipeline).connections,
                                                        attr.fields(Pipeline).created_at,
                                                        attr.fields(Pipeline).updated_at,
                                                        attr.fields(Pipeline).start_nodes,
                                                        attr.fields(Pipeline).project_id,
                                                        attr.fields(Pipeline).composition_id,
                                                        attr.fields(Pipeline).url,
                                                        attr.fields(Pipeline).preview,
                                                        attr.fields(Pipeline).description,
                                                        attr.fields(Pipeline).revisions,
                                                        ))

        _json['projectId'] = self.project_id
        _json['createdAt'] = self.created_at
        _json['updatedAt'] = self.updated_at
        _json['compositionId'] = self.composition_id
        _json['startNodes'] = self.start_nodes
        _json['orgId'] = self.org_id
        _json['nodes'] = [node.to_json() for node in self.nodes]
        _json['connections'] = [con.to_json() for con in self.connections]
        _json['url'] = self.url
        if self.preview is not None:
            _json['preview'] = self.preview
        if self.description is not None:
            _json['description'] = self.description
        if self.revisions is not None:
            _json['revisions'] = self.revisions

        return _json

    #########
    # Props #
    #########

    @property
    def platform_url(self):
        return self._client_api._get_resource_url("projects/{}/pipelines/{}".format(self.project_id, self.id))

    @property
    def project(self):
        if self._project is None:
            self._project = self.projects.get(project_id=self.project_id, fetch=None)
        assert isinstance(self._project, entities.Project)
        return self._project

    ################
    # repositories #
    ################
    @_repositories.default
    def set_repositories(self):
        reps = namedtuple('repositories',
                          field_names=['projects', 'pipelines', 'pipeline_executions', 'triggers', 'nodes'])

        r = reps(
            projects=repositories.Projects(client_api=self._client_api),
            pipelines=repositories.Pipelines(client_api=self._client_api),
            pipeline_executions=repositories.PipelineExecutions(
                client_api=self._client_api, project=self._project, pipeline=self
            ),
            triggers=repositories.Triggers(client_api=self._client_api, pipeline=self),
            nodes=repositories.Nodes(client_api=self._client_api, pipeline=self)
        )
        return r

    @property
    def projects(self):
        assert isinstance(self._repositories.projects, repositories.Projects)
        return self._repositories.projects

    @property
    def triggers(self):
        assert isinstance(self._repositories.triggers, repositories.Triggers)
        return self._repositories.triggers

    @property
    def nodes(self):
        assert isinstance(self._repositories.nodes, repositories.Nodes)
        return self._repositories.nodes

    @property
    def pipelines(self):
        assert isinstance(self._repositories.pipelines, repositories.Pipelines)
        return self._repositories.pipelines

    @property
    def pipeline_executions(self):
        assert isinstance(self._repositories.pipeline_executions, repositories.PipelineExecutions)
        return self._repositories.pipeline_executions

    ###########
    # methods #
    ###########
    def update(self):
        """
        Update pipeline changes to platform

        :return: pipeline entity
        """
        return self.pipelines.update(pipeline=self)

    def delete(self):
        """
        Delete pipeline object

        :return: True
        """
        return self.pipelines.delete(pipeline=self)

    def open_in_web(self):
        """
        Open the pipeline in web platform

        :return:
        """
        self._client_api._open_in_web(url=self.platform_url)

    def install(self):
        """
        install pipeline

        :return: Composition entity
        """
        return self.pipelines.install(pipeline=self)

    def pause(self):
        """
        pause pipeline

        :return: Composition entity
        """
        return self.pipelines.pause(pipeline=self)

    def execute(self, execution_input=None):
        """
        execute a pipeline and return the execute

        :param execution_input: list of the dl.FunctionIO or dict of pipeline input - example {'item': 'item_id'}
        :return: entities.PipelineExecution object
        """
        execution = self.pipeline_executions.create(pipeline_id=self.id, execution_input=execution_input)
        return execution

    def reset(self, stop_if_running: bool = False):
        """
        Resets pipeline counters

        :param bool stop_if_running: If the pipeline is installed it will stop the pipeline and reset the counters.
        :return: bool
        """
        return self.pipelines.reset(pipeline_id=self.id, stop_if_running=stop_if_running)

    def stats(self):
        """
        Get pipeline counters

        :return: PipelineStats
        :rtype: dtlpy.entities.pipeline.PipelineStats
        """
        return self.pipelines.stats(pipeline_id=self.id)

    def set_start_node(self, node: PipelineNode):
        """
        Set the start node of the pipeline

        :param PipelineNode node: node to be the start node
        """
        if self.start_nodes:
            for pipe_node in self.start_nodes:
                if pipe_node['type'] == 'root':
                    pipe_node['nodeId'] = node.node_id
        else:
            self.start_nodes = [{"nodeId": node.node_id,
                                 "type": "root", }]
