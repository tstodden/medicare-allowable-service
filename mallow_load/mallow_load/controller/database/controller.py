import os

from elastic_transport import HeadApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from mallow_load.mallow_load.controller.database.mapping import get_mapping_by_index


class ElasticsearchController:
    def __init__(self) -> None:
        self.client = Elasticsearch(
            os.environ["ELASTICSEARCH_HOST"],
            basic_auth=(
                os.environ["ELASTICSEARCH_USERNAME"],
                os.environ["ELASTICSEARCH_PASSWORD"],
            ),
        )

    def create_index_if_not_exists(self, index: str) -> None:
        if self._does_index_exist(index):
            return

        self.client.indices.create(index=index, mappings=get_mapping_by_index(index))

    def _does_index_exist(self, index: str) -> HeadApiResponse:
        return self.client.indices.exists(index=index)
