# Copyright (c) 2024 Cisco and/or its affiliates.
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

__metaclass__ = type
__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__author__ = "Allen Robel"

import copy
import inspect
from collections.abc import MutableMapping as Map
from typing import Any, Dict

class ParamsMergeDefaults:
    """
    Merge default parameters into parameters.

    Given a parameter specification (params_spec) and a playbook config
    (parameters) merge key/values from params_spec which have a default
    associated with them into parameters (if parameters is missing the
    corresponding key/value).
    """
    def __init__(self, ansible_module):
        self.class_name = self.__class__.__name__
        self.ansible_module = ansible_module
        self.file_handle = None

        self._build_properties()
        self._build_reserved_params()
        self.committed = False

    def _build_properties(self):
        """
        Container for the properties of this class.
        """
        method_name = inspect.stack()[0][3]
        self.properties = {}
        self.properties["params_spec"] = None
        self.properties["parameters"] = None
        self.properties["merged_parameters"] = None
        self.properties["debug"] = False
        self.properties["logfile"] = None

    def _build_reserved_params(self):
        """
        These are reserved parameter names that are skipped
        during merge.
        """
        self.reserved_params = set()
        self.reserved_params.add("choices")
        self.reserved_params.add("default")
        self.reserved_params.add("length_max")
        self.reserved_params.add("no_log")
        self.reserved_params.add("range_max")
        self.reserved_params.add("range_min")
        self.reserved_params.add("required")
        self.reserved_params.add("type")
        self.reserved_params.add("preferred_type")

    def _merge_default_params(
            self,
            spec: Dict[str, Any],
            params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge default parameters into parameters.

        Caller: 
        - commit()
        Return:
        -   A modified copy of params where missing parameters are added if:
            1. they are present in spec
            2. they have a default value defined in spec
        """
        method_name = inspect.stack()[0][3]

        for spec_key, spec_value in spec.items():

            if spec_key in self.reserved_params:
                continue

            if spec_key not in params and "default" in spec_value:
                params[spec_key] = spec_value["default"]

            if spec_key not in params and "default" not in spec_value:
                continue

            if isinstance(spec_value, Map):
                params[spec_key] = self._merge_default_params(spec_value, params[spec_key])

        return copy.deepcopy(params)

    def commit(self) -> None:
        """
        Merge default parameters into parameters.

        The merged parameters are stored in self.merged_parameters
        """
        method_name = inspect.stack()[0][3]

        if self.params_spec is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Cannot commit. params_spec is None."
            self.ansible_module.fail_json(msg)

        if self.parameters is None:
            msg = f"{self.class_name}.{method_name}: "
            msg += "Cannot commit. parameters is None."
            self.ansible_module.fail_json(msg)

        self.properties["merged_parameters"] = self._merge_default_params(self.params_spec, self.parameters)


    def log_msg(self, msg):
        """
        Used for debugging.  To enable, both debug and logfile properties
        must be set e.g.:

        instance = ParamsValidate(ansible_module)
        instance.debug = True
        instance.logfile = "/tmp/params_validate.log"
        etc...
        """
        if self.debug is False:
            return
        if self.logfile is None:
            return
        if self.file_handle is None:
            try:
                # since we need self.file_handle open throughout this class
                # we are disabling pylint R1732
                self.file_handle = open(  # pylint: disable=consider-using-with
                    f"{self.logfile}", "a+", encoding="UTF-8"
                )
            except IOError as err:
                msg = f"error opening logfile {self.logfile}. "
                msg += f"detail: {err}"
                self.ansible_module.fail_json(msg)

        self.file_handle.write(msg)
        self.file_handle.write("\n")
        self.file_handle.flush()

    @property
    def debug(self):
        """
        Enable/disable debugging to self.logfile
        """
        return self.properties["debug"]

    @debug.setter
    def debug(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, bool):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Invalid type for debug. Expected bool. "
            msg += f"Got {type(value)}."
            self.ansible_module.fail_json(msg)
        self.properties["debug"] = value

    @property
    def logfile(self):
        """
        Set file to which debug log is written
        """
        return self.properties["logfile"]

    @logfile.setter
    def logfile(self, value):
        method_name = inspect.stack()[0][3]  # pylint: disable=unused-variable
        self.properties["logfile"] = value

    @property
    def merged_parameters(self):
        """
        Getter for the merged parameters.
        """
        if self.properties["merged_parameters"] is None:
            msg = f"{self.class_name}.merged_parameters: "
            msg += "Call instance.commit() before calling merged_parameters."
            self.ansible_module.fail_json(msg)
        return self.properties["merged_parameters"]

    @property
    def parameters(self):
        """
        The parameters into which defaults are merged.
        
        The merge consists of adding any missing parameters
        (per a comparison with params_spec) and setting their
        value to the default value defined in params_spec.
        """
        return self.properties["parameters"]

    @parameters.setter
    def parameters(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, dict):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Invalid parameters. Expected type dict. "
            msg += f"Got type {type(value)}."
            self.ansible_module.fail_json(msg)
        self.properties["parameters"] = value

    @property
    def params_spec(self):
        """
        The param specification used to validate the parameters
        """
        return self.properties["params_spec"]

    @params_spec.setter
    def params_spec(self, value):
        method_name = inspect.stack()[0][3]
        if not isinstance(value, dict):
            msg = f"{self.class_name}.{method_name}: "
            msg += "Invalid params_spec. Expected type dict. "
            msg += f"Got type {type(value)}."
            self.ansible_module.fail_json(msg)
        self.properties["params_spec"] = value

