# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

__version__ = "2.0.0"

import threading
from elasticsearch import Elasticsearch
from minty import Base

__all__ = ["ElasticsearchInfrastructure"]


class ElasticsearchInfrastructure(Base):
    """Elasticsearch infrastructure class"""

    def __init__(self, config_name: str = "default"):
        """Initialize the Elasticsearch infrastructure.

        :param config_name: Name of the Elastic infrastructure configuration to
            load, defaults to "default"
        :type namconfig_namee: str
        """
        self._cache_lock = threading.Lock()
        self._config_name = config_name
        self._es_instance = None

    def __call__(self, config: dict):
        """Create a new connection to Elasticsearch using the specified
        configuration"""

        # We lock here, to ensure only one ES instance is created even if two
        # threads request the infrastructure in parallel.
        # The Elasticsearch instance itself is thread safe.
        with self._cache_lock:
            if self._es_instance is None:
                self._es_instance = self._connect_to_es(config)

        return self._es_instance

    def _connect_to_es(self, config: dict):
        """Create a new connection to Elasticsearch.

        This will look in `config["elasticsearch"][config_name]`

        :param config: configuration dictionary, for the current running
            instance.
        :type config: dict
        :raises KeyError: if the Elasticsearch config block with name
            `self.name` does not exits.
        """

        es_config = config["elasticsearch"][self._config_name]
        return Elasticsearch(**es_config)
