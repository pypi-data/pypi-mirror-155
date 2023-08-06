import inspect
from typing import Callable, get_args, Union, get_origin

from ._models import FunctionInformation, FunctionArgInfo


def parse_function_information(
    function: Callable,
) -> FunctionInformation:
    return FunctionInformation(
        function_object=function,
        args=parse_function_parameters(function),
    )


def parse_function_parameters(
    function: Callable,
) -> dict[str, FunctionArgInfo]:
    def _parse_types_by_parameter(parameter):
        # todo rewrite for recursive parsing
        annotation = parameter.annotation
        # if no annotation provided
        if annotation is inspect.Parameter.empty:
            return None

        # if Union type annotation convert to Union args
        # else convert to list of 1 element
        if get_origin(annotation) is Union:
            annotation = get_args(annotation)
        else:
            annotation = [annotation]

        return annotation

    return {
        parameter.name: FunctionArgInfo(
            name=parameter.name,
            types=_parse_types_by_parameter(parameter),
            default_value=parameter.default if parameter.default is not inspect.Parameter.empty else ...,
        )
        for _, parameter in inspect.signature(function).parameters.items()
    }
