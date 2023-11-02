"""
controller_version: 12
description: Verify functionality of NdfcSwitchUpgrade
"""
from contextlib import contextmanager
from typing import Any, Dict

import pytest
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import \
    AnsibleFailJson
from ansible_collections.cisco.dcnm.plugins.module_utils.image_mgmt.image_upgrade import \
    ImageUpgrade

from .fixture import load_fixture


@contextmanager
def does_not_raise():
    yield


patch_module_utils = "ansible_collections.cisco.dcnm.plugins.module_utils."
patch_image_mgmt = patch_module_utils + "image_mgmt."
patch_common = patch_module_utils + "common."

dcnm_send_controller_version = patch_common + "controller_version.dcnm_send"
dcnm_send_image_stage = patch_image_mgmt + "image_stage.dcnm_send"
dcnm_send_issu_details = patch_image_mgmt + "switch_issu_details.dcnm_send"


def responses_switch_details(key: str) -> Dict[str, str]:
    response_file = f"image_upgrade_responses_SwitchDetails"
    response = load_fixture(response_file).get(key)
    print(f"responses_switch_details: {key} : {response}")
    return response


class MockAnsibleModule:
    params = {}

    def fail_json(msg) -> AnsibleFailJson:
        raise AnsibleFailJson(msg)


@pytest.fixture
def module():
    return ImageUpgrade(MockAnsibleModule)


def test_init(module) -> None:
    module.__init__(MockAnsibleModule)
    assert isinstance(module, ImageUpgrade)
    assert module.class_name == "ImageUpgrade"
    assert module.max_module_number == 9


def test_init_defaults(module) -> None:
    """
    Defaults are initialized to expected values
    """
    module._init_defaults()
    assert isinstance(module.defaults, dict)
    assert module.defaults["reboot"] == False
    assert module.defaults["stage"] == True
    assert module.defaults["validate"] == True
    assert module.defaults["upgrade"]["nxos"] == True
    assert module.defaults["upgrade"]["epld"] == False
    assert module.defaults["options"]["nxos"]["mode"] == "disruptive"
    assert module.defaults["options"]["nxos"]["bios_force"] == False
    assert module.defaults["options"]["epld"]["module"] == "ALL"
    assert module.defaults["options"]["epld"]["golden"] == False
    assert module.defaults["options"]["reboot"]["config_reload"] == False
    assert module.defaults["options"]["reboot"]["write_erase"] == False
    assert module.defaults["options"]["package"]["install"] == False
    assert module.defaults["options"]["package"]["uninstall"] == False


def test_init_properties(module) -> None:
    """
    Properties are initialized to expected values
    """
    module._init_properties()
    assert isinstance(module.properties, dict)
    assert module.properties.get("bios_force") == False
    assert module.properties.get("check_interval") == 10
    assert module.properties.get("check_timeout") == 1800
    assert module.properties.get("config_reload") == False
    assert module.properties.get("devices") == None
    assert module.properties.get("disruptive") == True
    assert module.properties.get("epld_golden") == False
    assert module.properties.get("epld_module") == "ALL"
    assert module.properties.get("epld_upgrade") == False
    assert module.properties.get("force_non_disruptive") == False
    assert module.properties.get("response_data") == None
    assert module.properties.get("response") == None
    assert module.properties.get("result") == None
    assert module.properties.get("non_disruptive") == False
    assert module.properties.get("force_non_disruptive") == False
    assert module.properties.get("package_install") == False
    assert module.properties.get("package_uninstall") == False
    assert module.properties.get("reboot") == False
    assert module.properties.get("write_erase") == False
    assert module.valid_epld_module == {
        "ALL",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    }
    assert module.valid_nxos_mode == {
        "disruptive",
        "non_disruptive",
        "force_non_disruptive",
    }


# def test_ip_address_not_set(module) -> None:
#     """
#     Function description:

#     SwitchDetails.ip_address returns:
#         - IP Address, if the user has set ip_address
#         - None, if the user has not already set ip_address

#     Expected results:

#     1. instance.ip_address will return None
#     """
#     assert module.ip_address == None


# def test_ip_address_is_set(module) -> None:
#     """
#     Function description:

#     SwitchDetails.ip_address returns:
#         - IP Address, if the user has set ip_address
#         - None, if the user has not already set ip_address

#     Expected results:

#     1. instance.ip_address will return the value set by the user
#     """
#     module.ip_address = "1.2.3.4"
#     assert module.ip_address == "1.2.3.4"


# def test_refresh(monkeypatch, module) -> None:
#     """
#     Function description:

#     SwitchDetails.refresh sets the following properties:
#         - response_data
#         - response
#         - result

#     Expected results:

#     1. instance.response_data is a dictionary
#     2. instance.response is a dictionary
#     3. instance.response_data is a list
#     """

#     def mock_dcnm_send(*args, **kwargs) -> Dict[str, Any]:
#         key = "SwitchDetails_get_return_code_200"
#         return responses_switch_details(key)

#     monkeypatch.setattr(dcnm_send_patch, mock_dcnm_send)

#     module.refresh()
#     assert isinstance(module.response_data, dict)
#     assert isinstance(module.result, dict)
#     assert isinstance(module.response, dict)


# def test_refresh_response_data(monkeypatch, module) -> None:
#     """
#     Function description:

#     See test_refresh

#     Expected results:

#     1. instance.response_data is a dictionary
#     2. When instance.ip_address is set, getter properties will return values specific to ip_address
#     """

#     def mock_dcnm_send(*args, **kwargs) -> Dict[str, Any]:
#         key = "SwitchDetails_get_return_code_200"
#         return responses_switch_details(key)

#     monkeypatch.setattr(dcnm_send_patch, mock_dcnm_send)

#     module.refresh()
#     assert isinstance(module.response_data, dict)
#     module.ip_address = "172.22.150.110"
#     assert module.hostname == "cvd-1111-bgw"
#     module.ip_address = "172.22.150.111"
#     # We use the above IP address to test the remaining properties
#     assert module.fabric_name == "easy"
#     assert module.hostname == "cvd-1112-bgw"
#     assert module.logical_name == "cvd-1112-bgw"
#     assert module.model == "N9K-C9504"
#     # This is derived from "model" and is not in the NDFC response
#     assert module.platform == "N9K"
#     assert module.role == "border gateway"
#     assert module.serial_number == "FOX2109PGD1"


# match = "Unable to retrieve switch information from the controller. "


# @pytest.mark.parametrize(
#     "key,expected",
#     [
#         ("SwitchDetails_get_return_code_200", does_not_raise()),
#         (
#             "SwitchDetails_get_return_code_404",
#             pytest.raises(AnsibleFailJson, match=match),
#         ),
#         (
#             "SwitchDetails_get_return_code_500",
#             pytest.raises(AnsibleFailJson, match=match),
#         ),
#     ],
# )
# def test_result(monkeypatch, module, key, expected) -> None:
#     """
#     Function description:

#     SwitchDetails.result returns the result of its superclass
#     method ImageUpgradeCommon._handle_response()

#     Expectations:

#     1.  200 RETURN_CODE, MESSAGE == "OK",
#         SwitchDetails.result == {'found': True, 'success': True}

#     2.  404 RETURN_CODE, MESSAGE == "Not Found",
#         SwitchDetails.result == {'found': False, 'success': True}

#     3.  500 RETURN_CODE, MESSAGE ~= "Internal Server Error",
#         SwitchDetails.result == {'found': False, 'success': False}

#     Expected results:

#     1. SwitchDetails_result_200 == {'found': True, 'success': True}
#     2. SwitchDetails_result_404 == {'found': False, 'success': True}
#     3. SwitchDetails_result_500 == {'found': False, 'success': False}
#     """

#     def mock_dcnm_send(*args, **kwargs) -> Dict[str, Any]:
#         return responses_switch_details(key)

#     monkeypatch.setattr(dcnm_send_patch, mock_dcnm_send)

#     with expected:
#         module.refresh()


# @pytest.mark.parametrize(
#     "item, expected",
#     [
#         ("fabricName", "easy"),
#         ("hostName", "cvd-1111-bgw"),
#         ("licenseViolation", False),
#         ("location", None),
#         ("logicalName", "cvd-1111-bgw"),
#         ("managable", True),
#         ("model", "N9K-C9504"),
#         ("present", True),
#         ("serialNumber", "FOX2109PGCT"),
#         ("switchRole", "border gateway"),
#     ],
# )
# def test_get_with_ip_address_set(monkeypatch, module, item, expected) -> None:
#     """
#     Function description:

#     SwitchDetails._get is called by all getter properties.
#     It raises AnsibleFailJson if the user has not set ip_address.
#     It returns the value of the requested property if the user has set ip_address.
#     The property value is passed to both make_boolean() and make_none(), which
#     either:
#         - converts it to a boolean
#         - converts it to NoneType
#         - returns the value unchanged

#     Expectations:

#     1.  ControllerVersion._get returns above values
#         given corresponding responses

#     Expected results:

#     1. ControllerVersion_mode_LAN == "LAN"
#     2. ControllerVersion_mode_none == None
#     """

#     def mock_dcnm_send(*args, **kwargs) -> Dict[str, Any]:
#         key = "SwitchDetails_get_return_code_200"
#         return responses_switch_details(key)

#     monkeypatch.setattr(dcnm_send_patch, mock_dcnm_send)

#     module.refresh()
#     module.ip_address = "172.22.150.110"
#     assert module._get(item) == expected