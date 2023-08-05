"""
define client
"""

# Copyright 2018-2022 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import logging
from uuid import uuid4

try:
    from kg_core.oauth import SimpleToken, ClientCredentials
    from kg_core.kg import KGv3
    from kg_core.models import Stage, Pagination, ResponseConfiguration
    have_v3 = True
except ImportError:
    have_v3 = False

from .errors import AuthenticationError

try:
    import clb_nb_utils.oauth as clb_oauth
except ImportError:
    clb_oauth = None


logger = logging.getLogger("fairgraph")


STAGE_MAP = {
    "released": Stage.RELEASED,
    "latest": Stage.IN_PROGRESS,
    "in progress": Stage.IN_PROGRESS
}

AVAILABLE_PERMISSIONS = [
    "CREATE",
    "READ",
    "DELETE",
    "RELEASE",
    "INVITE_FOR_REVIEW",
    "INVITE_FOR_SUGGESTION",
    "SUGGEST",
    "UNRELEASE",
    "READ_RELEASED",
    "RELEASE_STATUS",
    "WRITE"
]

default_response_configuration = ResponseConfiguration(return_embedded=True)


class KGv3Client(object):

    def __init__(
        self,
        token: str = None,
        host: str = "core.kg-ppd.ebrains.eu",
        client_id: str = None,
        client_secret: str = None
    ):
        if client_id and client_secret:
            token_handler = ClientCredentials(client_id, client_secret)
        elif token:
            token_handler = SimpleToken(token)
        elif clb_oauth:
            token_handler = SimpleToken(clb_oauth.get_token())  # running in EBRAINS Jupyter Lab
        else:
            try:
                token_handler = SimpleToken(os.environ["KG_AUTH_TOKEN"])
            except KeyError:
                raise AuthenticationError("Need to provide either token or client id/secret.")
        self.host = host
        self._kg_client = KGv3(host=host, token_handler=token_handler)
        self._user_info = None
        self.cache = {}
        self._query_cache = {}
        self.accepted_terms_of_use = False

    def _check_response(self, response, ignore_not_found=False):
        if response.is_successful():
            if response.status_code < 300:
                return response
            elif response.status_code in (401, 403):
                raise AuthenticationError("Authentication/authorization problem. Your token may have expired. "
                                          f"Status code {response.status_code}. {response.message()}"
                                          f"\n{response.request_args}\n{response.request_payload}")
            else:
                raise Exception(f"Error. Status code {response.status_code} {response.message()}\n{response.request_args}\n{response.request_payload}")
        else:
            if response.error() == "Not Found" and ignore_not_found:
                return response
            raise Exception(f"Error: {response.error()}\n{response.request_args}")

    def query(self, filter, query_id, from_index=0, size=100, scope="released"):
        uuid = self.uuid_from_uri(query_id)
        params = {
            "from": from_index,
            "size": size,
            "stage": STAGE_MAP[scope],
            "returnEmbedded": True
        }
        if filter:
            params.update(filter)
        response = self._kg_client.get(
            path=f"/queries/{uuid}/instances",
            params=params
        )
        return self._check_response(response)

    def list(self, target_type, space, from_index=0, size=100, scope="released"):
        """docstring"""
        response = self._kg_client.get_instances(
            stage=STAGE_MAP[scope],
            target_type=target_type,
            space=space,
            response_configuration=default_response_configuration,
            pagination=Pagination(start_from=from_index, size=size)
        )
        return self._check_response(response)

    def instance_from_full_uri(self, uri, use_cache=True, scope="released", resolved=False):
        logger.debug("Retrieving instance from {}, api='core' use_cache={}".format(uri, use_cache))
        if resolved:
            raise NotImplementedError
        if use_cache and uri in self.cache:
            logger.debug("Retrieving instance {} from cache".format(uri))
            data = self.cache[uri]
        else:
            try:
                response = self._kg_client.get_instance(
                    stage=STAGE_MAP[scope],
                    instance_id=self._kg_client.uuid_from_absolute_id(uri),
                    response_configuration=default_response_configuration
                )
            except Exception as err:
                if "404" in str(err):
                    data = None
                else:
                    raise
            else:
                data = response.data()
        return data

    def create_new_instance(self, data=None, space=None, instance_id=None):
        response = self._kg_client.create_instance(
            space=space,
            payload=data,
            normalize_payload=True,
            instance_id=instance_id,  # if already have id
            response_configuration=default_response_configuration
        )
        return self._check_response(response).data()

    def update_instance(self, instance_id, data):
        response = self._kg_client.partially_update_contribution_to_instance(
            instance_id=instance_id,
            payload=data,
            normalize_payload=True,
            response_configuration=default_response_configuration
        )
        return self._check_response(response).data()

    def replace_instance(self, instance_id, data):
        response = self._kg_client.replace_contribution_to_instance(
            instance_id=instance_id,
            payload=data,
            normalize_payload=True,
            response_configuration=default_response_configuration
        )
        return self._check_response(response).data()

    def delete_instance(self, instance_id, ignore_not_found=True):
        response = self._kg_client.deprecate_instance(instance_id)
        return self._check_response(response, ignore_not_found=ignore_not_found).data()

    def uri_from_uuid(self, uuid):
        return self._kg_client.absolute_id(uuid)

    def uuid_from_uri(self, uri):
        return self._kg_client.uuid_from_absolute_id(uri)

    def store_query(self, query_label, query_definition, space):
        existing_query = self.retrieve_query(query_label)
        if existing_query:
            uuid = self.uuid_from_uri(existing_query["@id"])
        else:
            uuid = uuid4()

        try:
            response = self._check_response(
                self._kg_client.put(
                    path=f"/queries/{uuid}",
                    payload=query_definition,
                    params={
                        "space": space
                    })
            )
        except AuthenticationError:
            response = self._check_response(
                self._kg_client.put(
                    path=f"/queries/{uuid}",
                    payload=query_definition,
                    params={
                        "space": "myspace"
                    })
            )
        
        query_definition["@id"] = self.uri_from_uuid(uuid)

    def retrieve_query(self, query_label):
        if query_label not in self._query_cache:
            response = self._kg_client.get(
                path=f"/queries/",
                params={
                    "search": query_label
                }
            )
            if response.status_code == 401:
                raise AuthenticationError("Could not retrieve query. Has your token expired?")
            if response.total() == 0:
                return None
            elif response.total() > 1:
                # check for exact match to query_label
                found_match = False
                kgvq = "https://core.kg.ebrains.eu/vocab/query"
                for result in response.data():
                    if result[f"{kgvq}/meta"][f"{kgvq}/name"] == query_label:
                        query_definition = result
                        found_match = True
                        break
                if not found_match:
                    return None
            else:
                query_definition = response.data()[0]
            self._query_cache[query_label] = query_definition
        return self._query_cache[query_label]

    def user_info(self):
        if self._user_info is None:
            try:
                self._user_info = self._kg_client.get(
                    path="/users/me",
                    params={}
                ).data()
            except KeyError:
                self._user_info is None
        return self._user_info

    def spaces(self, permissions=None, names_only=False):
        response = self._kg_client.spaces(
            with_permissions=True,
            pagination=Pagination(start_from=0, size=100)
        )
        if permissions:
            for permission in permissions:
                if permission.upper() not in AVAILABLE_PERMISSIONS:
                    raise ValueError(f"Invalid permission '{permission}'")
        accessible_spaces = self._check_response(response).data()
        if permissions:
            filtered_spaces = []
            for space in accessible_spaces:
                for permission in permissions:
                    if permission.upper() in space["https://core.kg.ebrains.eu/vocab/meta/permissions"]:
                        if names_only:
                            filtered_spaces.append(space["http://schema.org/name"])
                        else:
                            filtered_spaces.append(space)
            return filtered_spaces
        else:
            if names_only:
                return [space["http://schema.org/name"] for space in accessible_spaces]
            else:
                return accessible_spaces

    @property
    def _private_space(self):
        # temporary workaround
        return f"private-{self.user_info()['https://schema.hbp.eu/users/nativeId']}"
