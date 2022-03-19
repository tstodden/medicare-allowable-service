import os
from typing import Iterable

from elastic_transport import HeadApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

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

    def bulk_load_into_index(self, index: str, generator: Iterable[dict]) -> None:
        self.create_index_if_not_exists(index)
        bulk(self.client, generator)

    def create_index_if_not_exists(self, index: str) -> None:
        if self._does_index_exist(index):
            return

        self.client.indices.create(index=index, mappings=get_mapping_by_index(index))

    def _does_index_exist(self, index: str) -> HeadApiResponse:
        return self.client.indices.exists(index=index)
