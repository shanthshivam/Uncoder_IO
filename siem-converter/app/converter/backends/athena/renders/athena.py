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

from app.converter.backends.athena.const import athena_details
from app.converter.backends.athena.mapping import AthenaMappings, athena_mappings
from app.converter.core.exceptions.render import UnsupportedRenderMethod
from app.converter.core.mapping import LogSourceSignature
from app.converter.core.models.platform_details import PlatformDetails
from app.converter.core.render import BaseQueryRender, BaseQueryFieldValue


class AthenaFieldValue(BaseQueryFieldValue):
    details: PlatformDetails = athena_details

    def equal_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join([self.equal_modifier(field=field, value=v) for v in value])})"
        return f"{field} = '{value}'"

    def contains_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.contains_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '%{value}%'  ESCAPE '\\'"

    def endswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.endswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '%{value}'  ESCAPE '\\'"

    def startswith_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.startswith_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '{value}%'  ESCAPE '\\'"

    def regex_modifier(self, field, value):
        if isinstance(value, list):
            return f"({self.or_token.join(self.regex_modifier(field=field, value=v) for v in value)})"
        return f"{field} ILIKE '{value}'  ESCAPE '\\'"

    def keywords(self, field, value):
        raise UnsupportedRenderMethod(platform_name=self.details.name, method="Keywords")


class AthenaQueryRender(BaseQueryRender):
    details: PlatformDetails = athena_details
    mappings: AthenaMappings = athena_mappings

    or_token = "OR"
    and_token = "AND"
    not_token = "NOT"

    field_value_map = AthenaFieldValue(or_token=or_token)
    query_pattern = "{prefix} WHERE {query} {functions}"
    comment_symbol = "--"
    is_multi_line_comment = True

    def generate_prefix(self, log_source_signature: LogSourceSignature) -> str:
        table = str(log_source_signature) if str(log_source_signature) else "eventlog"
        return f"SELECT * FROM {table}"
