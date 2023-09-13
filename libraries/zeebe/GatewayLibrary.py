import logging

import requests
from robot.api.deco import keyword

logger = logging.getLogger(__name__)


class GatewayLibrary:
    """Library for interacting with the Zeebe gateway."""

    def __init__(self, host: str = "localhost", port: int = 9600) -> None:
        """Initialize the library.

        Args:
            host (str, optional): The host of the Zeebe gateway. Defaults to "localhost".
            port (int, optional): The port of the Zeebe gateway. Defaults to 9600.
        """
        self.host = host
        self.port = port

    @keyword
    def get_gateway_health(self) -> requests.Response:
        """Get the health of the Zeebe gateway.
        https://docs.camunda.io/docs/self-managed/zeebe-deployment/configuration/gateway-health-probes/

        Returns:
            requests.Response: The response from the gateway.
        """
        response = requests.get(f"http://{self.host}:{self.port}/actuator/health")
        logger.info(f"Zeebe gateway health: {response.json()}")

        return response
