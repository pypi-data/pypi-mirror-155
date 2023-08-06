from typing import Dict

from cloudspec import CloudSpecParam


def sphinx_docs(hub, parameters: CloudSpecParam) -> str:
    """
    Get the sphinx docs for the parameters
    """
    if not parameters:
        return ""

    ret = "\n    Args:\n"
    for param in parameters.values():
        ret += f"        {param.snaked}"
        if param.param_type:
            ret += f"({param.param_type}{', optional' if not param.required else ''})"

        ret += f": {param.doc}"
        if not ret.endswith("."):
            ret += "."
        if not param.required:
            ret += f" Defaults to {param.default}."

        if param.get("member", None):
            for nested_param_name, nested_param_data in (
                param.get("member").get("params").items()
            ):
                ret += "\n            * "
                ret += f"({nested_param_name}{', optional' if not nested_param_data.required else ''}): {nested_param_data.doc}"
        ret += "\n"

    return ret.rstrip()


def headers(hub, parameters: CloudSpecParam) -> str:
    """
    The arguments that will be put in the function definition
    """
    ret = ""

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_name, param_data in required_params.items():
        if param_data.get("param_type"):
            ret += f",\n    {param_data.snaked}: {param_data['param_type']}"
            if param_data.get("member", None):
                ret += nested_param(param_data.get("member"))
        else:
            ret += f",\n    {param_data.snaked}"

    unrequired_params = {
        name: data for name, data in parameters.items() if not data["required"]
    }

    for param_name, param_data in unrequired_params.items():
        param_type = param_data.get("param_type")
        if param_type:
            ret += f",\n    {param_data.snaked}: {param_type}"
            if param_data.get("member", None):
                ret += nested_param(param_data.get("member"))
        else:
            ret += f",\n    {param_data.snaked}"

        # TODO handle this case properly
        if param_data.default == "{}" or param_data.default == "[]":
            ret += f" = None"
        else:
            ret += f" = {param_data.default}"

    return ret


def nested_param(member: Dict) -> str:
    """
    Create a dataclass for a complex nested argument
    """
    ret = f'[\n        make_dataclass(\n            "{member.name}",\n            ['
    for param_name, param_data in member.get("params").items():
        ret += f"\n                "
        # TODO: Nested param name should be snaked
        ret += f'("{param_name}", {param_data.param_type}, field(default={param_data.default})), '

    # Remove last ', '
    ret = ret[0:-2]
    ret += "\n            ]\n        )\n    ]"

    return ret


def callers(hub, parameters: CloudSpecParam) -> str:
    """
    Get a mapping of the function args to the values that will be used in the final caller
    """
    ret = []

    required_params = {
        name: data for name, data in parameters.items() if data["required"]
    }
    for param_data in required_params.values():
        ret.append(f"{param_data.snaked}={param_data.default or 'value'}")

    return ", ".join(ret)


def mappings(hub, parameters: CloudSpecParam) -> Dict[str, str]:
    ret = {}
    map_params = {
        name: data
        for name, data in parameters.items()
        if data["target_type"] == "mapping"
    }
    for name, data in map_params.items():
        target = data["target"]
        if target not in ret:
            ret[target] = {}
        ret[target][name] = data.snaked

    fmt = lambda item: ", ".join(f'"{k}": {v}' for k, v in item.items())
    return {k: f"{{{fmt(v)}}}" for k, v in ret.items()}


def simple_map(hub, parameters: Dict[str, CloudSpecParam]):
    result = {}
    for k, param_data in parameters.items():
        if k == "name" and param_data.target_type == "arg":
            continue
        result[param_data.snaked] = k
    return result
