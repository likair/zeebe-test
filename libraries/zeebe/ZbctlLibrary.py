import subprocess
import logging
import json
from typing import Union

from robot.api.deco import keyword


logger = logging.getLogger(__name__)


class ZbctlLibrary:
    """Library to use the zbctl command line tool."""

    def __init__(self, address: str = None, insecure: bool = True) -> None:
        """Initialize the library.

        Args:
            address (str, optional): The address of the Zeebe gateway. Defaults to None.
            insecure (bool, optional): Whether to use an insecure connection. Defaults to True.
        """
        self.address = address
        self.insecure = insecure
        self.worker_processes = []

    @keyword
    def execute_zbctl(self, command: str, arguments: list = None) -> Union[str, dict]:
        """
        Execute a zbctl command with the provided arguments.

        Args:
        - command (str): The zbctl command to execute.
        - arguments (list): List of arguments to pass to the command.

        Returns:
        - str | dict: The output of the executed command. If the output is JSON, it will be parsed into a dict. Otherwise, it will be returned as a string.
        """

        if arguments is None:
            arguments = []

        cmd = ["zbctl", command]

        if self.insecure:
            cmd.append("--insecure")

        if self.address is not None:
            cmd.append(f"--address={self.address}")

        cmd.extend(arguments)

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.info(f"{' '.join(cmd)}: {result.stderr}")
            return result.stderr

        json_result = json.loads(result.stdout)
        logger.info(f"{' '.join(cmd)}: {json.dumps(json_result, indent=2)}")

        return json_result

    @keyword
    def deploy_resource(
        self, resource: str, variables: dict = None
    ) -> Union[str, dict]:
        """Deploy a resource.

        Args:
        - resource (str): The resource to deploy.
        - variables (dict): The variables to use.

        Returns:
        - str | dict: The output of the executed command. If the output is JSON, it will be parsed into a dict. Otherwise, it will be returned as a string.
        """

        if variables is None:
            return self.execute_zbctl("deploy", ["resource", resource])

        return self.execute_zbctl(
            "deploy",
            ["resource", resource, "--variables", json.dumps(variables)],
        )

    @keyword
    def create_process_instance(
        self, process_id: str, variables: dict = None
    ) -> Union[str, dict]:
        """Create a process instance.

        Args:
        - process_id (str): The process ID.
        - variables (dict): The variables to use.

        Returns:
        - str | dict: The output of the executed command. If the output is JSON, it will be parsed into a dict. Otherwise, it will be returned as a string.
        """

        if variables is None:
            return self.execute_zbctl(
                "create", ["instance", process_id, "--withResult"]
            )

        return self.execute_zbctl(
            "create",
            [
                "instance",
                process_id,
                "--variables",
                json.dumps(variables),
                "--withResult",
            ],
        )

    @keyword
    def create_worker(self, job_type: str, handler: str) -> None:
        """Create a worker.

        Args:
        - job_type (str): The job type.
        - handler (str): The handler.
        """

        cmd = "zbctl create"

        if self.insecure:
            cmd += " --insecure"

        if self.address is not None:
            cmd += f" --address={self.address}"

        cmd += f" worker {job_type} --handler {handler}"

        worker_process = subprocess.Popen(cmd, shell=True)
        self.worker_processes.append(worker_process)

    @keyword
    def terminate_workers(self) -> None:
        """Terminate workers."""

        for worker_process in self.worker_processes:
            worker_process.terminate()

        self.worker_processes = []

        logger.info("Terminated workers.")
