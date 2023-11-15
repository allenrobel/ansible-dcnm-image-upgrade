# Copyright (c) 2020-2024 Cisco and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import pytest
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import \
    AnsibleFailJson

from .fixture import load_fixture
from .image_upgrade_utils import MockAnsibleModule, does_not_raise, issu_details_by_ip_address_fixture


__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__author__ = "Allen Robel"

"""
controller_version: 12
description: Verify functionality of subclass SwitchIssuDetailsByIpAddress
"""


patch_module_utils = "ansible_collections.cisco.dcnm.plugins.module_utils."
patch_image_mgmt = patch_module_utils + "image_mgmt."

dcnm_send_issu_details = patch_image_mgmt + "switch_issu_details.dcnm_send"


def responses_switch_issu_details(key: str) -> Dict[str, str]:
    response_file = f"image_upgrade_responses_SwitchIssuDetails"
    response = load_fixture(response_file).get(key)
    print(f"responses_switch_issu_details: {key} : {response}")
    return response


def test_image_mgmt_switch_issu_details_by_ip_address_00001(issu_details_by_ip_address) -> None:
    """
    Function
    - __init__

    Test
    - fail_json is not called
    - issu_details_by_ip_address.properties is a dict
    """
    with does_not_raise():
        issu_details_by_ip_address.__init__(MockAnsibleModule)
    assert isinstance(issu_details_by_ip_address.properties, dict)


def test_image_mgmt_switch_issu_details_by_ip_address_00002(issu_details_by_ip_address) -> None:
    """
    Function
    - _init_properties

    Test
    - Class properties initialized to expected values
    - issu_details_by_ip_address.properties is a dict
    - issu_details_by_ip_address.action_keys is a set
    - action_keys contains expected values
    """
    action_keys = {"imageStaged", "upgrade", "validated"}

    issu_details_by_ip_address._init_properties()
    assert isinstance(issu_details_by_ip_address.properties, dict)
    assert isinstance(issu_details_by_ip_address.properties.get("action_keys"), set)
    assert issu_details_by_ip_address.properties.get("action_keys") == action_keys
    assert issu_details_by_ip_address.properties.get("response_data") is None
    assert issu_details_by_ip_address.properties.get("response") is None
    assert issu_details_by_ip_address.properties.get("result") is None
    assert issu_details_by_ip_address.properties.get("ip_address") is None


def test_image_mgmt_switch_issu_details_by_ip_address_00020(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - issu_details_by_ip_address.response is a dict
    - issu_details_by_ip_address.response_data is a list
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00020a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        print(f"mock_dcnm_send_issu_details: {responses_switch_issu_details(key)}")
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    issu_details_by_ip_address.refresh()
    assert isinstance(issu_details_by_ip_address.response, dict)
    assert isinstance(issu_details_by_ip_address.response_data, list)


def test_image_mgmt_switch_issu_details_by_ip_address_00021(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - Properties are set based on device_name
    - Expected property values are returned
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00021a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        print(f"mock_dcnm_send_issu_details: {responses_switch_issu_details(key)}")
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    issu_details_by_ip_address.refresh()
    issu_details_by_ip_address.ip_address = "172.22.150.102"
    assert issu_details_by_ip_address.device_name == "leaf1"
    assert issu_details_by_ip_address.serial_number == "FDO21120U5D"
    # change ip_address to a different switch, expect different information
    issu_details_by_ip_address.ip_address = "172.22.150.108"
    assert issu_details_by_ip_address.device_name == "cvd-2313-leaf"
    assert issu_details_by_ip_address.serial_number == "FDO2112189M"
    # verify remaining properties using current ip_address
    assert issu_details_by_ip_address.eth_switch_id == 39890
    assert issu_details_by_ip_address.fabric == "hard"
    assert issu_details_by_ip_address.fcoe_enabled is False
    assert issu_details_by_ip_address.group == "hard"
    # NOTE: For "id" see switch_id below
    assert issu_details_by_ip_address.image_staged == "Success"
    assert issu_details_by_ip_address.image_staged_percent == 100
    assert issu_details_by_ip_address.ip_address == "172.22.150.108"
    assert issu_details_by_ip_address.issu_allowed is None
    assert issu_details_by_ip_address.last_upg_action == "2023-Oct-06 03:43"
    assert issu_details_by_ip_address.mds is False
    assert issu_details_by_ip_address.mode == "Normal"
    assert issu_details_by_ip_address.model == "N9K-C93180YC-EX"
    assert issu_details_by_ip_address.model_type == 0
    assert issu_details_by_ip_address.peer is None
    assert issu_details_by_ip_address.platform == "N9K"
    assert issu_details_by_ip_address.policy == "KR5M"
    assert issu_details_by_ip_address.reason == "Upgrade"
    assert issu_details_by_ip_address.role == "leaf"
    assert issu_details_by_ip_address.status == "In-Sync"
    assert issu_details_by_ip_address.status_percent == 100
    # NOTE: switch_id appears in the response data as "id"
    # NOTE: "id" is a python reserved keyword, so we changed the property name
    assert issu_details_by_ip_address.switch_id == 2
    assert issu_details_by_ip_address.sys_name == "cvd-2313-leaf"
    assert issu_details_by_ip_address.system_mode == "Normal"
    assert issu_details_by_ip_address.upg_groups is None
    assert issu_details_by_ip_address.upgrade == "Success"
    assert issu_details_by_ip_address.upgrade_percent == 100
    assert issu_details_by_ip_address.validated == "Success"
    assert issu_details_by_ip_address.validated_percent == 100
    assert issu_details_by_ip_address.version == "10.2(5)"
    # NOTE: Two vdc_id values exist in the response data for each switch.
    # NOTE: Namely, "vdcId" and "vdc_id"
    # NOTE: Properties are provided for both, as follows.
    # NOTE: vdc_id == vdcId
    # NOTE: vdc_id2 == vdc_id
    assert issu_details_by_ip_address.vdc_id == 0
    assert issu_details_by_ip_address.vdc_id2 == -1
    assert issu_details_by_ip_address.vpc_peer is None
    # NOTE: Two vpc role keys exist in the response data for each switch.
    # NOTE: Namely, "vpcRole" and "vpc_role"
    # NOTE: Properties are provided for both, as follows.
    # NOTE: vpc_role == vpcRole
    # NOTE: vpc_role2 == vpc_role
    # NOTE: Values are synthesized in the response for this test
    assert issu_details_by_ip_address.vpc_role == "FOO"
    assert issu_details_by_ip_address.vpc_role2 == "BAR"


def test_image_mgmt_switch_issu_details_by_ip_address_00022(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - issu_details_by_ip_address.result is a dict
    - issu_details_by_ip_address.result contains expected key/values for 200 RESULT_CODE
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00022a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        print(f"mock_dcnm_send_issu_details: {responses_switch_issu_details(key)}")
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    issu_details_by_ip_address.refresh()
    assert isinstance(issu_details_by_ip_address.result, dict)
    assert issu_details_by_ip_address.result.get("found") is True
    assert issu_details_by_ip_address.result.get("success") is True


def test_image_mgmt_switch_issu_details_by_ip_address_00023(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - refresh calls handle_response, which calls json_fail on 404 response
    - Error message matches expectation
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00023a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        print(f"mock_dcnm_send_issu_details: {responses_switch_issu_details(key)}")
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    match = "Bad result when retriving switch information from the controller"
    with pytest.raises(AnsibleFailJson, match=match):
        issu_details_by_ip_address.refresh()


def test_image_mgmt_switch_issu_details_by_ip_address_00024(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - fail_json is called on 200 response with empty DATA key
    - Error message matches expectation
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00024a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    match = "SwitchIssuDetailsByIpAddress.refresh: "
    match += "The controller has no switch ISSU information."
    with pytest.raises(AnsibleFailJson, match=match):
        issu_details_by_ip_address.refresh()


def test_image_mgmt_switch_issu_details_by_ip_address_00025(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function
    - refresh

    Test
    - fail_json is called on 200 response with DATA.lastOperDataObject length 0
    - Error message matches expectation
    """
    key = "test_image_mgmt_switch_issu_details_by_ip_address_00025a"

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        print(f"mock_dcnm_send_issu_details: {responses_switch_issu_details(key)}")
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    match = "SwitchIssuDetailsByIpAddress.refresh: "
    match += "The controller has no switch ISSU information."
    with pytest.raises(AnsibleFailJson, match=match):
        issu_details_by_ip_address.refresh()


def test_image_mgmt_switch_issu_details_by_ip_address_00040(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function description:

    SwitchIssuDetailsByIpAddress._get is called by all getter properties.
    It raises AnsibleFailJson if the user has not set ip_address or if
    the ip_address is unknown, or if an unknown property name is queried.
    It returns the value of the requested property if the user has set a known
    ip_address.

    Expected results:

    1.  fail_json is called with appropriate error message since an unknown
        ip_address is set.
    """

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        key = "test_image_mgmt_switch_issu_details_by_ip_address_00040a"
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    issu_details_by_ip_address.refresh()
    issu_details_by_ip_address.ip_address = "1.1.1.1"
    match = "SwitchIssuDetailsByIpAddress._get: 1.1.1.1 does not exist "
    match += "on the controller."
    with pytest.raises(AnsibleFailJson, match=match):
        issu_details_by_ip_address._get("serialNumber")


def test_image_mgmt_switch_issu_details_by_ip_address_00041(
    monkeypatch, issu_details_by_ip_address
) -> None:
    """
    Function description:

    SwitchIssuDetailsByIpAddress._get is called by all getter properties.
    It raises AnsibleFailJson if the user has not set ip_address or if
    the ip_address is unknown, or if an unknown property name is queried.
    It returns the value of the requested property if the user has set a
    known ip_address and the property name is valid.

    Expected results:

    1.  fail_json is called with appropriate error message since an unknown
        property is queried.
    """

    def mock_dcnm_send_issu_details(*args, **kwargs) -> Dict[str, Any]:
        key = "test_image_mgmt_switch_issu_details_by_ip_address_00041a"
        return responses_switch_issu_details(key)

    monkeypatch.setattr(dcnm_send_issu_details, mock_dcnm_send_issu_details)

    issu_details_by_ip_address.refresh()
    issu_details_by_ip_address.ip_address = "172.22.150.102"
    match = "SwitchIssuDetailsByIpAddress._get: 172.22.150.102 unknown "
    match += f"property name: FOO"
    with pytest.raises(AnsibleFailJson, match=match):
        issu_details_by_ip_address._get("FOO")
