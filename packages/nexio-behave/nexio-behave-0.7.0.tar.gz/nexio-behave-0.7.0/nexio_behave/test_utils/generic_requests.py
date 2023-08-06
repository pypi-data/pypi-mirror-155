"""Common REST request functions that will server as the HTTP library wrapper

These functions will allow for the following REST operations:
1) POST
2) GET
3) PUT
4) PATCH
5) DELETE
6) OPTIONS

"""
import json as j
from pprint import pformat
from typing import Any, Dict, List, Union

from loguru import logger
import requests


class GenericRequests:
    """Holds all generic static methods for REST requests"""

    @staticmethod
    def generic_request(
        client: requests.Session,
        method: str,
        url: str,
        headers: Dict[str, Any] = None,
        json: Union[Dict[str, Any], List[Any]] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Common REST request that uses the HTTP requests library.

        This will read in a session object to use as a client.
        If no client is read in we will create a new request Session object.

        NOTE: This method is private and for internal class use only.

        Args:
            client: The HttpClient session object
            method: The method of the desired request. IE: POST, GET, etc...
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        # Set our request meta data
        request_meta: Dict[str, Any] = {
            "method": method,
            "url": url,
            "headers": headers,
            "json": json,
            "data": data,
            "files": file_path,
        }
        logger.debug(
            f"HTTP REQUEST: Sending a request with the following attributes: "
            f"\n{j.dumps(request_meta, sort_keys=True, indent=2)}\n"
        )
        # We have a client and a file
        if client and file_path:
            with open(file_path, "r") as file:
                response = client.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    files={"upload_file": file},  # type: ignore
                    headers=headers,
                )
        # We have a client but no file payload
        elif client and not file_path:
            response = client.request(
                method=method, url=url, json=json, data=data, headers=headers
            )
        # We have no client but a file payload
        elif not client and file_path:
            with open(file_path, "r") as file:
                response = requests.Session().request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    files={"upload_file": file},  # type: ignore
                    headers=headers,
                )
        # All else fails send a generic request with a new Session and no file support
        else:
            response = requests.Session().request(
                method=method, url=url, json=json, data=data, headers=headers
            )
        try:
            logger.debug(
                f"HTTP RESPONSE: \n{j.dumps(response.json(), sort_keys=True, indent=2)}\n"
            )
        except j.JSONDecodeError:
            logger.debug(f"HTTP RESPONSE: {pformat(response.text)}")
        logger.debug("")
        return response

    @staticmethod
    def post_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Union[Dict[str, Any], List[Any]] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a POST REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="post",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )

    @staticmethod
    def get_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a GET REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="get",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )

    @staticmethod
    def put_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Union[Dict[str, Any], List[Any]] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a PUT REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="put",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )

    @staticmethod
    def patch_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Union[Dict[str, Any], List[Any]] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a PATCH REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="patch",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )

    @staticmethod
    def delete_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a DELETE REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="delete",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )

    @staticmethod
    def options_request(
        client: requests.Session,
        url: str,
        headers: Dict[str, Any] = None,
        json: Dict[str, Any] = None,
        data: Any = None,
        file_path: str = None,
    ) -> requests.Response:
        """Sends a OPTIONS REST request with necessary attributes and parameters

        Args:
            client: The HttpClient session object
            url: The URL to send the request to
            headers: (OPTIONAL) The header dict to send with the request
            json: (OPTIONAL) The JSON data to send with the request
            data: (OPTIONAL) The data to send with the request. Can be any MIME type
            file_path: (OPTIONAL) The location of the file to upload plus the actual file name

        Return:
            requests.Response object

        """
        return GenericRequests.generic_request(
            client,
            method="options",
            url=url,
            headers=headers,
            json=json,
            data=data,
            file_path=file_path,
        )
