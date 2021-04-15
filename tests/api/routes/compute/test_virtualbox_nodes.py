# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from fastapi import FastAPI, status
from httpx import AsyncClient
from tests.utils import asyncio_patch
from unittest.mock import patch

from gns3server.compute.project import Project

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def vm(app: FastAPI, client: AsyncClient, compute_project: Project) -> None:

    vboxmanage_path = "/fake/VboxManage"
    params = {
        "name": "VMTEST",
        "vmname": "VMTEST",
        "linked_clone": False
    }

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.create", return_value=True) as mock:
        response = await client.post(app.url_path_for("create_virtualbox_node", project_id=compute_project.id),
                                     json=params)
    assert mock.called
    assert response.status_code == status.HTTP_201_CREATED

    with patch("gns3server.compute.virtualbox.VirtualBox.find_vboxmanage", return_value=vboxmanage_path):
        return response.json()


async def test_vbox_create(app: FastAPI, client: AsyncClient, compute_project: Project) -> None:

    params = {
        "name": "VM1",
        "vmname": "VM1",
        "linked_clone": False
    }

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.create", return_value=True):
        response = await client.post(app.url_path_for("create_virtualbox_node", project_id=compute_project.id),
                                     json=params)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "VM1"
        assert response.json()["project_id"] == compute_project.id


async def test_vbox_get(app: FastAPI, client: AsyncClient, compute_project: Project, vm: dict) -> None:

    response = await client.get(app.url_path_for("get_virtualbox_node",
                                                 project_id=vm["project_id"],
                                                 node_id=vm["node_id"]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "VMTEST"
    assert response.json()["project_id"] == compute_project.id


async def test_vbox_start(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.start", return_value=True) as mock:

        response = await client.post(app.url_path_for("start_virtualbox_node",
                                     project_id=vm["project_id"],
                                    node_id=vm["node_id"]))
        assert mock.called
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_vbox_stop(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.stop", return_value=True) as mock:
        response = await client.post(app.url_path_for("stop_virtualbox_node",
                                                      project_id=vm["project_id"],
                                                      node_id=vm["node_id"]))
        assert mock.called
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_vbox_suspend(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.suspend", return_value=True) as mock:
        response = await client.post(app.url_path_for("suspend_virtualbox_node",
                                                      project_id=vm["project_id"],
                                                      node_id=vm["node_id"]))
        assert mock.called
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_vbox_resume(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.resume", return_value=True) as mock:
        response = await client.post(app.url_path_for("resume_virtualbox_node",
                                                      project_id=vm["project_id"],
                                                      node_id=vm["node_id"]))
        assert mock.called
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_vbox_reload(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.reload", return_value=True) as mock:
        response = await client.post(app.url_path_for("reload_virtualbox_node",
                                                      project_id=vm["project_id"],
                                                      node_id=vm["node_id"]))
        assert mock.called
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_vbox_nio_create_udp(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    params = {
        "type": "nio_udp",
        "lport": 4242,
        "rport": 4343,
        "rhost": "127.0.0.1"
    }

    url = app.url_path_for("create_virtualbox_node_nio",
                           project_id=vm["project_id"],
                           node_id=vm["node_id"],
                           adapter_number="0",
                           port_number="0")

    with asyncio_patch('gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.adapter_add_nio_binding') as mock:
        response = await client.post(url, json=params)
        assert mock.called
        args, kwgars = mock.call_args
        assert args[0] == 0

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["type"] == "nio_udp"


# @pytest.mark.asyncio
# async def test_vbox_nio_update_udp(app: FastAPI, client: AsyncClient, vm):
#
#     params = {
#         "type": "nio_udp",
#         "lport": 4242,
#         "rport": 4343,
#         "rhost": "127.0.0.1",
#         "filters": {}
#     }
#
#     with asyncio_patch('gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.ethernet_adapters'):
#         with asyncio_patch('gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.adapter_remove_nio_binding'):
#             response = await client.put("/projects/{project_id}/virtualbox/nodes/{node_id}/adapters/0/ports/0/nio".format(project_id=vm["project_id"], node_id=vm["node_id"]), params)
#
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json()["type"] == "nio_udp"


async def test_vbox_delete_nio(app: FastAPI, client: AsyncClient, vm: dict) -> None:

    url = app.url_path_for("delete_virtualbox_node_nio",
                           project_id=vm["project_id"],
                           node_id=vm["node_id"],
                           adapter_number="0",
                           port_number="0")

    with asyncio_patch('gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.adapter_remove_nio_binding') as mock:
        response = await client.delete(url)
        assert mock.called
        args, kwgars = mock.call_args
        assert args[0] == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_vbox_update(app: FastAPI, client: AsyncClient, vm, free_console_port):

    params = {
        "name": "test",
        "console": free_console_port
    }

    response = await client.put(app.url_path_for("update_virtualbox_node",
                                                 project_id=vm["project_id"],
                                                 node_id=vm["node_id"]), json=params)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "test"
    assert response.json()["console"] == free_console_port


@pytest.mark.asyncio
async def test_virtualbox_start_capture(app: FastAPI, client: AsyncClient, vm):

    params = {
        "capture_file_name": "test.pcap",
        "data_link_type": "DLT_EN10MB"
    }

    url = app.url_path_for("start_virtualbox_node_capture",
                           project_id=vm["project_id"],
                           node_id=vm["node_id"],
                           adapter_number="0",
                           port_number="0")

    with patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.is_running", return_value=True):
        with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.start_capture") as mock:
            response = await client.post(url, json=params)
            assert response.status_code == status.HTTP_200_OK
            assert mock.called
            assert "test.pcap" in response.json()["pcap_file_path"]


@pytest.mark.asyncio
async def test_virtualbox_stop_capture(app: FastAPI, client: AsyncClient, vm):

    url = app.url_path_for("stop_virtualbox_node_capture",
                           project_id=vm["project_id"],
                           node_id=vm["node_id"],
                           adapter_number="0",
                           port_number="0")

    with patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.is_running", return_value=True):
        with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.stop_capture") as mock:
            response = await client.post(url)
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert mock.called


# @pytest.mark.asyncio
# async def test_virtualbox_pcap(app: FastAPI, client: AsyncClient, vm, compute_project):
#
#     with asyncio_patch("gns3server.compute.virtualbox.virtualbox_vm.VirtualBoxVM.get_nio"):
#         with asyncio_patch("gns3server.compute.virtualbox.VirtualBox.stream_pcap_file"):
#             response = await client.get("/projects/{project_id}/virtualbox/nodes/{node_id}/adapters/0/ports/0/pcap".format(project_id=compute_project.id, node_id=vm["node_id"]), raw=True)
#             assert response.status_code == status.HTTP_200_OK
