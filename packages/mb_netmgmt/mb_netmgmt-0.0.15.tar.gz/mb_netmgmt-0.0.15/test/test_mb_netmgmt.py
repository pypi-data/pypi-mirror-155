import os
from threading import Thread

import paramiko
import pytest
from mb_netmgmt import mb, ssh
from mb_netmgmt.__main__ import create_server

port = 8080
prompt = b"prompt"


@pytest.mark.parametrize("protocol", ["http", "snmp", "telnet", "netconf"])
def test_create_imposter(protocol):
    with mb([{"protocol": protocol, "port": port}]):
        pass


def test_ssh():
    with mb(
        [
            {
                "protocol": "ssh",
                "port": port,
                "stubs": [prompt_stub()],
            }
        ]
    ):
        client = connect_ssh()
        chan = client.invoke_shell()
        out = chan.recv(1024)
        assert out == prompt


def test_ssh_proxy():
    with mb(
        [
            {
                "protocol": "ssh",
                "port": port,
                "stubs": [
                    prompt_stub(),
                    {
                        "responses": [
                            {
                                "proxy": {
                                    "to": f"ssh://{os.environ['NETCONF_USERNAME']}:{os.environ['NETCONF_PASSWORD']}@localhost"
                                }
                            },
                        ]
                    },
                ],
            }
        ]
    ):
        client = connect_ssh()
        chan = client.invoke_shell()
        out = chan.recv(1024)
        assert out == prompt


def prompt_stub():
    return {"responses": [{"is": {"response": prompt}}]}


def test_create_ssh_server():
    server = create_server(ssh, port, None)
    Thread(target=server.serve_forever).start()
    connect_ssh().close()
    server.shutdown()


def connect_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect("localhost", port)
    return client
