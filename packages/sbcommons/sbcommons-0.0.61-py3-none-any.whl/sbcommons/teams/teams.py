from sbcommons.logging import lambda_logger
import requests

logger = lambda_logger.get_logger(__name__)


class Teams:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, title: str, msg: str) -> bool:
        data = {
            "Text": msg,
            "TextFormat": "markdown",
            "Title": title
        }

        try:
            response = requests.post(self.webhook_url, json=data)
            if not response.status_code == 200:
                logger.info(
                    f'Tried to post {msg} on teams webhook failed, status code: {response.status_code}'
                )
                return False
        except BaseException as e:
            logger.error(f'Exception when posting to teams, exception args: {e.args}')
            return False

        return True
    
