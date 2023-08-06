import base64
import csv
import os
import json
import requests

from .utils import handle_data_store_response, handle_http_request


class CraftAiSdk:
    """Main class to instantiate

    Attributes:
        base_environment_url (str): Base URL to CraftAI environment API.
    """

    def __init__(
        self,
        access_token=None,
        environment_url=None,
    ):
        """Inits CraftAiSdk.

        Args:
            access_token (:obj:`str`, optional): CraftAI access token.
                Defaults to ``CRAFT_AI_ACCESS_TOKEN`` environment variable.
            environment_url (:obj:`str`, optional): URL to CraftAI environment.
                Defaults to ``CRAFT_AI_ENVIRONMENT_URL`` environment variable.

        Raises:
            ValueError: if the ``environment_url`` is not defined
                or when the corresponding environment variable is not set.
        """
        self._session = requests.Session()

        # Set authorization token
        if access_token is None:
            access_token = os.environ.get("CRAFT_AI_ACCESS_TOKEN")
        if access_token is None:
            raise ValueError(
                'Parameter "access_token" should be set, since '
                '"CRAFT_AI_ACCESS_TOKEN" environment variable is not defined.'
            )
        self._session.headers["Authorization"] = f"Bearer {access_token}"

        # Set base environment url
        if environment_url is None:
            environment_url = os.environ.get("CRAFT_AI_ENVIRONMENT_URL")
        if environment_url is None:
            raise ValueError(
                'Parameter "environment_url" should be set, since '
                '"CRAFT_AI_ENVIRONMENT_URL" environment variable is not defined.'
            )
        self.base_environment_url = f"{environment_url}/api/v1"

    # _____ REQUESTS METHODS _____

    @handle_http_request
    def _get(self, url, params=None, **kwargs):
        return self._session.get(url, params=params, **kwargs)

    @handle_http_request
    def _post(self, url, data=None, params=None, files=None, **kwargs):
        return self._session.post(url, data=data, params=params, files=files, **kwargs)

    @handle_http_request
    def _delete(self, url, **kwargs):
        return self._session.delete(url, **kwargs)

    # _____ STEPS _____

    def create_steps(self, repo, private_key, branch_name=None):
        """Create pipeline steps from a source code located on a remote repository.

        Args:
            repo (str): Remote repository url.
            private_key (str): Private SSH key related to the repository.
            branch_name (:obj:`str`, optional): Branch name. Defaults to None.

        Returns:
            :obj:`list` of :obj:`dict[str, str]`: List of steps represented as
            :obj:`dict` (with keys ``"id"`` and ``"name"``).
        """
        url = f"{self.base_environment_url}/steps"

        data = {
            "private_key": private_key,
            "repo": repo,
            "branch_name": branch_name,
        }

        return self._post(url, data=data)

    def list_steps(self):
        """Get the list of all steps.

        Returns:
            :obj:`list` of :obj:`dict`: List of steps represented as :obj:`dict`
            (with keys ``"id"``, ``"name"``).
        """
        url = f"{self.base_environment_url}/steps"

        return self._get(url)

    def delete_one_step(self, step_name):
        """Delete one step.

        Args:
            step_name (str): Name of the step to delete
                as defined in the ``config.yaml`` configuration file.

        Returns:
            :obj:`dict[str, str]`: Deleted step represented as :obj:`dict`
            (with keys ``"id"`` and ``"name"``).
        """
        url = os.path.join(f"{self.base_environment_url}/steps", step_name)
        return self._delete(url)

    # _____ PIPELINES _____

    def create_pipeline(self, pipeline_name, template_path):
        """Create and execute a pipeline as defined by a YAML template.

        Args:
            pipeline_name (str): Name of the pipeline.
            template_path (str): Path to a YAML template file that defines the structure
                of the pipeline as a DAG.

        Returns:
            :obj:`dict[str, str]`: Created pipeline represented as :obj:`dict`
            (with key ``id``).
        """
        url = f"{self.base_environment_url}/pipelines"
        files = {
            "template": open(template_path, "rb"),
        }
        params = {
            "pipeline_name": pipeline_name,
        }

        resp = self._post(url, files=files, params=params)
        return resp

    def delete_pipeline(self, pipeline_name, force_endpoints_deletion=False):
        """Delete a pipeline identified by its name and id.

        Args:
            pipeline_name (str): Name of the pipeline.
            force_endpoints_deletion (:obj:`bool`, optional): if True the associated
                endpoints will be deleted too. Defaults to False.

        Returns:
            :obj:`dict`: The deleted pipeline and assiocated deleted endpoints.
            The returned ``dict`` contains two keys:

                * ``"pipeline"`` (:obj:`dict`): Deleted pipeline represented as
                  :obj:`dict` (with keys ``"id"`` and ``"pipeline_name"``).
                * ``"endpoints"`` (:obj:`list`): List of deleted endpoints represented
                  as :obj:`dict` (with keys ``"id"``, ``"name"``, ``"body_params"``
                  and ``allow_unknown_params``).
        """
        url = f"{self.base_environment_url}/pipelines"
        params = {
            "pipeline_name": pipeline_name,
            "force_endpoints_deletion": force_endpoints_deletion,
        }
        return self._delete(url, params=params)

    def get_pipeline_status(self, pipeline_name):
        """Get the status of a pipeline identified by its name.

        Args:
            pipeline_name (str): Name of the pipeline.

        Returns:
            :obj:`str`: The status of the pipeline (i.e. either ``"Pending"``,
            ``"Running"``, ``"Succeeded"`` or ``"Failed"``).
        """
        url = f"{self.base_environment_url}/pipelines/status"
        params = {
            "pipeline_name": pipeline_name,
        }
        response = self._get(url, params=params)

        return response["pipeline_status"]

    def get_pipeline_logs(
        self, pipeline_name, from_timestamp=None, to_timestamp=None, limit=None
    ):
        """Get the logs of an executed pipeline identified by its name.

        Args:
            pipeline_name (str): Name of the pipeline.
            from_timestamp (:obj:`int`, optional): Timestamp (in ms) from which the logs
                are collected.
            to_timestamp (:obj:`int`, optional): Timestamp (in ms) until which the logs
                are collected.
            limit (:obj:`int`, optional): Maximum number of logs that are collected.

        Returns:
            :obj:`list`: List of collected logs.
        """
        url = f"{self.base_environment_url}/pipelines/{pipeline_name}/logs"
        data = {
            "from": from_timestamp,
            "to": to_timestamp,
            "limit": limit,
        }
        # filter optional parameters
        data = {k: v for k, v in data.items() if v is not None}

        response = self._post(url, json=data)
        lines = response[0].splitlines()
        reader = csv.reader(lines)
        return list(reader)

    # _____ ENDPOINTS _____

    def create_endpoint(
        self,
        pipeline_name,
        endpoint_name,
        endpoint_params=None,
        allow_unknown_params=None,
    ):
        """Create a custom endpoint associated to a given pipeline.

        Args:
            pipeline_name (str): Name of the pipeline.
            endpoint_name (str): Name of the endpoint.
            endpoint_params (:obj:`dict[str, dict]`, optional): structure of the
                endpoint parameters. Each item defines a parameter which name is given
                by the key and which constraints (type and requirement) are given by
                the value. An item has the form::

                    [str: parameter name] : {
                        "required": [bool],
                        "type": [str in ["string", "number", "object", "array"]],
                    }

                Defaults to None.
            allow_unknown_params (:obj:`bool`, optional): if True the custom endpoint
                allows other parameters not specified in ``endpoint_params``.
                Defaults to None.
        """
        url = f"{self.base_environment_url}/endpoints"

        endpoint_params = {} if endpoint_params is None else endpoint_params
        data = {
            "pipeline_name": pipeline_name,
            "name": endpoint_name,
            "allow_unknown_params": allow_unknown_params,
            "body_params": endpoint_params,
        }
        # filter optional parameters
        data = {k: v for k, v in data.items() if v is not None}

        return self._post(url, json=data)

    def delete_endpoint(self, endpoint_name):
        """Delete an endpoint identified by its name.

        Args:
            endpoint_name (str): Name of the endpoint.

        Returns:
            :obj:`dict`: Deleted endpoint represented as dict (with keys ``"id"``,
            ``"name"``, ``"body_params"``, ``"allow_unknown_params"``).
        """
        url = os.path.join(f"{self.base_environment_url}/endpoints", endpoint_name)
        return self._delete(url)

    def list_endpoints(self):
        """Get the list of all endpoints.

        Returns:
            :obj:`list` of :obj:`dict`: List of endpoints represented as :obj:`dict`
            (with keys ``"id"``, ``"name"``, ``"body_params"``,
            ``"allow_unknown_params"`` and ``"pipeline_name"``).
        """
        url = f"{self.base_environment_url}/endpoints"
        return self._get(url)

    def get_endpoint(self, endpoint_name):
        """Get information of an endpoint.

        Args:
            endpoint_name (str): Name of the endpoint.

        Returns:
            :obj:`dict`: Endpoint information represented as :obj:`dict` (with keys
            ``"id"``, ``"name"``, ``"body_params"``, ``"allow_unknown_params"`` and
            ``"pipeline_name"``).
        """
        url = os.path.join(f"{self.base_environment_url}/endpoints", endpoint_name)
        return self._get(url)

    def trigger_endpoint(self, endpoint_name, params=None):
        """Trigger an endpoint.

        Args:
            endpoint_name (str): Name of the endpoint.
            params (:obj:`dict`, optional): Parameters to be provided to the endpoint.
                Defaults to None.
        """
        url = os.path.join(
            f"{self.base_environment_url}/endpoints", endpoint_name, "trigger"
        )
        return self._post(url, json=params)

    # _____ DATA STORE _____

    def data_store_list_objects(self):
        """Get the list of the objects stored in the data store.

        Returns:
            :obj:`list` of :obj:`dict`: List of objects in the data store represented
            as :obj:`dict` (with keys ``"path"``, ``"last_modified"``, and ``"size"``).
        """
        url = f"{self.base_environment_url}/data-store/list"
        response = self._get(url)

        return response["listed_elem"]["contents"]

    def _get_upload_presigned_url(self):
        url = f"{self.base_environment_url}/data-store/upload"
        resp = self._get(url)["urlObject"]
        presigned_url, data = resp["url"], resp["fields"]

        # Extract prefix condition from the presigned url
        policy = data["Policy"]
        policy_decode = json.loads(base64.b64decode(policy))
        prefix_condition = policy_decode["conditions"][0]
        prefix = prefix_condition[-1]
        return presigned_url, data, prefix

    def data_store_upload_object(self, filepath_or_buffer, object_path_in_datastore):
        """Upload a file as an object into the data store.

        Args:
            filepath_or_buffer (:obj:`str`, or file-like object): String, path to the
                file to be uploaded ;
                or file-like object implenting a ``read()`` method (e.g. via buildin
                ``open`` function). The file object must be opened in binary mode,
                not text mode.
            object_path_in_datastore (str): Destination of the uploaded file.
        """
        if isinstance(filepath_or_buffer, str):
            # this is a filepath: call the method again with a buffer
            with open(filepath_or_buffer, "rb") as file_buffer:
                return self.data_store_upload_object(
                    file_buffer, object_path_in_datastore
                )

        if not hasattr(filepath_or_buffer, "read"):  # not a readable buffer
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a read() method (file-like object)."
            )

        file_buffer = filepath_or_buffer
        files = {"file": file_buffer}
        presigned_url, data, prefix = self._get_upload_presigned_url()
        data["key"] = os.path.join(prefix, object_path_in_datastore)

        resp = requests.post(url=presigned_url, data=data, files=files)
        handle_data_store_response(resp)

    def _get_download_presigned_url(self, object_path_in_datastore):
        url = f"{self.base_environment_url}/data-store/download"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        presigned_url = self._post(url, data=data)["signedUrl"]
        return presigned_url

    def data_store_download_object(self, object_path_in_datastore, filepath_or_buffer):
        """Download an object in the data store and save it into a file.

        Args:
            object_path_in_datastore (str): Location of the object to download from the
                data store.
            filepath_or_buffer (:obj:`str` or file-like object):
                String, filepath to save the file to ; or a file-like object
                implementing a ``write()`` method, (e.g. via builtin ``open`` function).

        Returns:
            str: content of the file
        """
        presigned_url = self._get_download_presigned_url(object_path_in_datastore)
        resp = requests.get(presigned_url)
        object_content = handle_data_store_response(resp)

        if isinstance(filepath_or_buffer, str):  # filepath
            with open(filepath_or_buffer, "w") as f:
                f.write(object_content)
        elif hasattr(filepath_or_buffer, "write"):  # writable buffer
            filepath_or_buffer.write(object_content)
        else:
            raise ValueError(
                "'filepath_or_buffer' must be either a string (filepath) or an object "
                "with a write() method (file-like object)."
            )

    def data_store_delete_object(self, object_path_in_datastore):
        """Delete an object on the datastore.

        Args:
            object_path_in_datastore (str): Location of the object to be deleted in the
                data store.
        """
        url = f"{self.base_environment_url}/data-store/delete"
        data = {
            "path_to_object": object_path_in_datastore,
        }
        self._delete(url, data=data)
