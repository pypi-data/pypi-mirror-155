import pytest
from ..modules.base_control import ControlConfigurationReq, ControlConfiguration


@pytest.mark.parametrize(
    "iface_conf_dict,prefix,requirements_list,requirements_success",
    [
        (
            {
                "fail_test_dummy_name": "attr value"
            },
            "fail_test",
            ["dummy_name"],
            True
        ),
        (
            {
                "fail_test_distinct_requirement": "attr value"
            },
            "fail_test",
            ["dummy_name"],
            False
        ),
        ({}, "fail_test", ["dummy_name"], False)
    ]
    )
def test_check_requirements(iface_conf_dict, prefix, requirements_list, requirements_success):
    control_conf = ControlConfiguration(
        iface_conf_dict, prefix
    )

    conf_requirements = ControlConfigurationReq(
        requirements_list
    )

    assert conf_requirements.check_requirements(control_conf) is requirements_success
