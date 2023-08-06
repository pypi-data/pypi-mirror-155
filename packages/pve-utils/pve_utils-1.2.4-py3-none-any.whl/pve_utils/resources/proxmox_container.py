import os
import sys
import time
from typing import List

from paramiko import AutoAddPolicy, SSHClient, SSHException

from pve_utils.config import settings
from pve_utils.utils import SSHconnectable, pprint
from pve_utils.utils.decorators import with_ssh


class ProxmoxContainer(SSHconnectable):
    name: str
    vmid: int

    def __init__(self, node, name: str, vmid: int, *args, **kwargs):
        self.node = node
        self.name = name
        self.vmid = vmid
        self.host = settings.CT_IP
        self.port = settings.CT_SSH_PORT
        self.user = settings.CT_USER
        self.password = settings.CT_PASSWORD
        self.ct = self.__get_ct()

    def __get_ct(self):
        return self.node.lxc(self.vmid)

    @with_ssh
    def exec(self, client: SSHClient, commands: List[str]) -> None:
        pprint.info(
            f"Run commands on CT: {self.vmid} "
            f"{self.host}:{self.port} as: {self.user}"
        )
        for command in commands:
            self.run_command(client, command)

    @with_ssh
    def upload(
        self,
        client: SSHClient,
        host_path: str,
        container_path: str,
    ) -> None:
        pprint.info(
            f"Upload {host_path} on CT: {self.vmid} to "
            f"{self.host}:{self.port}{container_path} as: {self.user}"
        )
        sftp = client.open_sftp()
        try:
            host_path = os.path.abspath(host_path)
            file_name = os.path.basename(host_path)
            if os.path.isdir(host_path):
                self.upload_dir(sftp, host_path, container_path)
            else:
                container_path = (
                    container_path
                    if container_path.endswith(file_name)
                    else f"{container_path}{file_name}"
                    if container_path.endswith("/")
                    else f"{container_path}/{file_name}"
                )
                sftp.put(host_path, container_path)
        except Exception as e:
            pprint.error(
                f"Failed to upload {host_path} on CT: {self.vmid} "
                f"{self.host}:{self.port}{container_path} as: {self.user}"
            )
            pprint.info("Traceback:")
            pprint.normal(e)
            sys.exit(1)

    def ssh_wait(self, wait_limit=600):
        wait_limit = wait_limit + time.time()
        while time.time() < wait_limit:
            response = os.system(f"ping -c 1 {self.host}")
            if response == 0:
                pprint.success("CT is started")
                return
            else:
                time.sleep(0.1)
        pprint.error("CT is not aviable")
        sys.exit(1)

    def upload_dir(self, sftp, source, target):
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                sftp.put(
                    os.path.join(source, item),
                    "%s/%s" % (target, item),
                )
            else:
                self.mkdir(
                    sftp, "%s/%s" % (target, item), ignore_existing=True
                )
                self.put_dir(
                    sftp,
                    os.path.join(source, item),
                    "%s/%s" % (target, item),
                )

    def mkdir(self, sftp, path, mode=511, ignore_existing=False):
        try:
            sftp.mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

    def run_command(self, client: SSHClient, command: str) -> None:
        stdin, stdout, stderr = client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            pprint.error(
                f"Failed to execute command: {command}. Exit code: {exit_code}"
            )
            output = stdout.readlines()
            if output:
                pprint.info("Info:")
                for line in output:
                    pprint.normal(line.strip())
            traceback = stderr.readlines()
            if traceback:
                pprint.info("Traceback:")
                for line in traceback:
                    pprint.normal(line.strip())
            sys.exit(1)
        else:
            pprint.success(f"Success execute command: {command}")
            output = stdout.readlines()
            if output:
                pprint.info("Output:")
                for line in output:
                    pprint.normal(line.strip())

    def __str__(self):
        return f"CT {self.vmid}: {self.name}"
