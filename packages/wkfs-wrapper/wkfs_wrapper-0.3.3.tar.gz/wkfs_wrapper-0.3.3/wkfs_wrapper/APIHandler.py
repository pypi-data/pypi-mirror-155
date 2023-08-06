import logging.config

import requests

from requests.exceptions import (
    ConnectionError,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    Timeout,
    TooManyRedirects,
)

from .constants import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger("root")


class APIHandler:

    # TODO: Define own variables as per requirement
    def __init__(
        self,
        host: str,
        headers: dict,
        timeout: int,
        logging: bool = True,
    ):
        self._host = host
        self._headers = headers
        self.__logging = logging
        self._timeout = timeout
        
        self.connection_exceptions = (
            ConnectionError,
            ProxyError,
            ReadTimeout,
            SSLError,
            Timeout,
            TooManyRedirects,
        )

    @property
    def host(self):
        return self._host

    def send_request(
        self, method, url, payload=None, log_config: dict = None, headers: dict = None
    ):
        if not headers:
            headers = self._headers

        if self.__logging:
            LOGGER.info("Sending [%s] API call to [%s]", method, f"{self.host}{url}")

        log_entry = None

        if log_config:
            if (
                "model" not in log_config
                or "user" not in log_config
                or "loan" not in log_config
                or "timezone" not in log_config
            ):
                raise Exception("Invalid log dict")

        try:
            if log_config:
                log_entry = log_config["model"](
                    loan=log_config["loan"],
                    requested_by=log_config["user"],
                    request_url=f"{method}: {url}",
                    request_headers=headers,
                    request_body=payload,
                    request_time=log_config["timezone"].now(),
                    package_name=log_config.get("package_name")
                )

            response = requests.request(
                method,
                f"{self.host}{url}",
                headers=headers,
                timeout=self._timeout,
                data=payload,
            )

            if self.__logging:
                LOGGER.info(
                    "Received [%s] response for [%s: %s]",
                    response.status_code,
                    method,
                    f"{self.host}{url}",
                )

            response.raise_for_status()

            if log_entry:
                log_entry.response_code = response.status_code
                log_entry.response_body = response.text
                log_entry.response_time = log_entry.request_time + response.elapsed
                log_entry.save()

            response = response.text

            if self.__logging:
                LOGGER.info(
                    "WKFS Response for [%s: %s] -- [%s]",
                    method,
                    f"{self.host}{url}",
                    response,
                )

            # In case if the token expires, the response status code will be 401, the header will contain the error information.
            # The header property for 401 error is WWW-Authenticate.
            # Value for header property for 401 error is Bearer error="invalid_token", error_description="The token expired at '11/09/2021 14:58:41'"
            return response
        except self.connection_exceptions as excp:
            if self.__logging:
                LOGGER.error(
                    "[WKFS] - Exception while connecting to WKFS. URL: [%s: %s]. Error: [%s]",
                    method,
                    self.url,
                    excp,
                )

            if log_entry:
                from datetime import datetime
                log_entry.response_code = 408
                log_entry.response_body = str(excp)
                log_entry.response_time = datetime.now()
                log_entry.save()

            exception_message = f"Exception while connecting to WKFS. Error: {excp}"
            
        except HTTPError as excp:
            if self.__logging:
                LOGGER.error(
                    "[WKFS] API Failed. Received [%s] response for [%s: %s]",
                    excp.response.status_code,
                    method,
                    f"{self.host}{url}",
                )
            package_name=None    
            if log_config:
                package_name = log_config.get("package_name", None)
            wkfs_error_details = self.generate_wkfs_error_details(payload, log_entry, response, excp, package_name)
            exception_message = f"Failed to get success response from WKFS. Received [{response.status_code}] for [{method}] Response: [{wkfs_error_details}]"
        except Exception as excp:
            if self.__logging:
                LOGGER.error(
                    "[WKFS] API Failed. Received [%s] response for [%s: %s]",
                    excp.response.status_code,
                    method,
                    f"{self.host}{url}",
                )
            package_name=None    
            if log_config:
                package_name = log_config.get("package_name", None)
            #wkfs_error_details = self.generate_wkfs_error_details(payload, log_entry, response, excp, package_name)
            exception_message = f"Failed to get success response from WKFS. Received [{excp}] for [{method}]"

        raise Exception(f"Exception while connecting to WKFS. Error: {exception_message}")

    def generate_wkfs_error_details(self, payload, log_entry, response, excp, wkfs_package_name):
        response_data = content_uri = transactionIdentifier = None
        if excp.response.text:
            response_data = excp.response.json()
            transactionIdentifier = response_data.get("generateResultsResponse", {}).get("getGenerateResultsResult", {}).get("transactionIdentifier", None)
        try:
            import json    
            p = json.loads(payload)
            content_uri = p["generate"]["request"]["contentIdentifier"]
        except Exception as e:
            content_uri = None
            pass
            
        additional_details = response_data if response_data else excp
        wkfs_error_details = self.generate_wkfs_exception(
               form_name=wkfs_package_name,
               expere_transaction_id=transactionIdentifier if transactionIdentifier else None,
                content_uri=content_uri if content_uri else None,
                additional_details=additional_details
            )
        if log_entry:
            log_entry.response_code = excp.response.status_code
            log_entry.response_body = response_data
            log_entry.response_time = log_entry.request_time + response.elapsed
            log_entry.save()
        return wkfs_error_details
        
    def generate_wkfs_exception(self, customer_name=None, expere_transaction_id=None, form_name=None, content_uri=None, transaction_xml_file_name=None, description=None, additional_details=None):
        wkfs_error_details = {}
        wkfs_error_details["customer_name"]=customer_name
        wkfs_error_details["expere_transaction_id"]=expere_transaction_id
        wkfs_error_details["form_name"]=form_name
        wkfs_error_details["content_uri"]=content_uri
        wkfs_error_details["transaction_xml_file_name"]=transaction_xml_file_name
        wkfs_error_details["issue_description"]=description
        wkfs_error_details["additional_details"]=additional_details
        return wkfs_error_details