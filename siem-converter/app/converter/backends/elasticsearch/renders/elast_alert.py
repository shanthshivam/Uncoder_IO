"""
Uncoder IO Community Edition License
-----------------------------------------------------------------
Copyright (c) 2023 SOC Prime, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----------------------------------------------------------------
"""

from app.converter.backends.elasticsearch.const import ELASTICSEARCH_ALERT, elastalert_details
from app.converter.backends.elasticsearch.mapping import ElasticSearchMappings, elasticsearch_mappings
from app.converter.backends.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender, ElasticSearchFieldValue
from app.converter.core.mapping import SourceMapping
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.operator_types.output import MetaInfoContainer
from app.converter.tools.utils import get_author_str, concatenate_str, get_mitre_attack_str, get_licence_str


SEVERITIES_MAP = {"informational": "5", "low": "4", "medium": "3", "high": "2", "critical": "1"}


class ElasticAlertRuleFieldValue(ElasticSearchFieldValue):
    details: PlatformDetails = elastalert_details


class ElastAlertRuleRender(ElasticSearchQueryRender):
    details: PlatformDetails = elastalert_details
    mappings: ElasticSearchMappings = elasticsearch_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = ElasticAlertRuleFieldValue(or_token=or_token)
    query_pattern = "{prefix} {query} {functions}"

    def finalize_query(self, prefix: str, query: str, functions: str, meta_info: MetaInfoContainer,
                       source_mapping: SourceMapping = None, not_supported_functions: list = None):
        query = super().finalize_query(prefix=prefix, query=query, functions=functions, meta_info=meta_info)
        rule = ELASTICSEARCH_ALERT.replace("<query_placeholder>", query)
        description = concatenate_str(meta_info.description, get_author_str(meta_info.author))
        description = concatenate_str(description, get_licence_str(meta_info.license))
        description = concatenate_str(description, get_mitre_attack_str(meta_info.mitre_attack))

        rule = rule.replace("<description_place_holder>", description)
        rule = rule.replace("<title_place_holder>", meta_info.title)
        rule = rule.replace("<priority_place_holder>", SEVERITIES_MAP[meta_info.severity])
        if not_supported_functions:
            rendered_not_supported = self.render_not_supported_functions(not_supported_functions)
            return rule + rendered_not_supported
        return rule
