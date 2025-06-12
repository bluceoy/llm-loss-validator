import requests
import time
from loguru import logger

class FedLedger:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://fed-ledger-prod.flock.io/api"
        self.api_version = "v1"
        self.url = f"{self.base_url}/{self.api_version}"
        self.headers = {
            "flock-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        self.proxies = {
            #"https": "http://127.0.0.1:7897",
            #"https": "http://127.0.0.1:1081",
            "https": "socks5://127.0.0.1:1080",
        }

    def request_validation_assignment(self, task_id: str):
        for i in range(5):
            try:
                url = f"{self.url}/tasks/request-validation-assignment/{task_id}"
                response = requests.post(url, headers=self.headers, proxies=self.proxies)
                logger.info(f"request_validation_assignment, code = {response.status_code}")
                logger.info(f"request_validation_assignment, text = {response.text}")
                return response
            except Exception as e:
                logger.info(f"request_validation_assignment, catch {e}")
                time.sleep(3*(i+1))

    def submit_validation_result(self, assignment_id: str, loss: float, gpu_type: str):
        for i in range(5):
            try:
                url = f"{self.url}/tasks/update-validation-assignment/{assignment_id}"
                response = requests.post(
                    url,
                    headers=self.headers,
                    json={
                        "status": "completed",
                        "data": {
                            "loss": loss,
                            "gpu_type": gpu_type,
                        },
                    },
                    proxies=self.proxies,
                )
                logger.info(f"submit_validation_result, code = {response.status_code}")
                logger.info(f"submit_validation_result, text = {response.text}")
                return response
            except Exception as e:
                logger.info(f"submit_validation_result, catch {e}")
                time.sleep(3*(i+1))


    def mark_assignment_as_failed(self, assignment_id: str):
        for i in range(5):
            try:
                url = f"{self.url}/tasks/update-validation-assignment/{assignment_id}"
                response = requests.post(
                    url,
                    headers=self.headers,
                    json={
                        "status": "failed",
                    },
                    proxies=self.proxies,
                )
                logger.info(f"mark_assignment_as_failed, code = {response.status_code}")
                logger.info(f"mark_assignment_as_failed, text = {response.text}")
                return response
            except Exception as e:
                logger.info(f"mark_assignment_as_failed, catch {e}")
                time.sleep(3*(i+1))
