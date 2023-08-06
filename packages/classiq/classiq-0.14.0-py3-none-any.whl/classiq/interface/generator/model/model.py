from typing import Any, Dict, List, Optional, Union

import pydantic

import classiq.interface.generator.validations.flow_graph as flow_graph
from classiq.interface._version import VERSION as _VERSION
from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.functions import FunctionLibraryData, FunctionType
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.user_defined_function_params import CustomFunction
from classiq.interface.status import Status

LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG = (
    "Cannot have multiple function calls with the same name"
)


class Model(pydantic.BaseModel):
    """
    All the relevand data for generating quantum circuit in one place.
    """

    version: str = _VERSION

    # Must be validated before logic_flow
    function_library: Optional[FunctionLibraryData] = pydantic.Field(
        default=None,
        description="The user-defined custom function library.",
    )

    logic_flow: List[FunctionCall] = pydantic.Field(
        default_factory=list,
        description="List of function calls to be applied in the circuit",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    class Config:
        extra = "forbid"

    @pydantic.validator("logic_flow")
    def validate_logic_flow(
        cls, logic_flow: List[FunctionCall], values: Dict[str, Any]
    ) -> List[FunctionCall]:
        if not logic_flow:
            return logic_flow

        function_call_names = set(call.name for call in logic_flow)
        if len(function_call_names) != len(logic_flow):
            raise ValueError(LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG)

        functions_to_validate = logic_flow.copy()
        library = values.get("function_library")

        while functions_to_validate:
            function_call = functions_to_validate.pop()
            params = function_call.function_params
            if not isinstance(params, CustomFunction):
                continue

            FunctionLibraryData.validate_function_in_library(
                library=library, function_params=params
            )
            assert isinstance(library, FunctionLibraryData)
            function_data = library.function_dict[params.name]
            params.generate_io_names(
                input_set=function_data.input_set,
                output_set=function_data.output_set,
            )
            function_call.validate_custom_function_io()
            if function_data.function_type == FunctionType.CompositeFunction:
                functions_to_validate.extend(function_data.logic_flow)

        flow_graph.validate_legal_wiring(logic_flow, allow_one_ended_wires=True)
        flow_graph.validate_acyclic_logic_flow(logic_flow, allow_one_ended_wires=True)

        return logic_flow

    def get_one_ended_wires(
        self,
        *,
        input_wire_names: Optional[List[str]] = None,
        output_wire_names: Optional[List[str]] = None,
    ) -> List[str]:
        return flow_graph.validate_legal_wiring(
            logic_flow=self.logic_flow,
            flow_input_names=input_wire_names,
            flow_output_names=output_wire_names,
            should_raise=False,
        )


class ModelResult(pydantic.BaseModel):
    status: Status
    details: Union[Model, str]
