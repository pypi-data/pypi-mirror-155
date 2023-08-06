import pluggy

import logging

from flask import abort, jsonify, make_response, Response, request

from typing import List, Dict, Union, Any

from JuMonC.handlers.base import RESTAPI
from JuMonC.authentication import scopes
from JuMonC.authentication.check import check_auth

logger = logging.getLogger(__name__)

hookimpl = pluggy.HookimplMarker("JuMonC")


links:        List[Dict[str, Union[bool, str, List[Dict[str, str]]]]] = []

@hookimpl
def plugin_arguments(aruments: str) -> None:
    """
    Get a string of user supplied arguments for this plugin.
    
    JuMonC will pass on arguments for plugins, to let them evealute their own arguments.
    """

    
@hookimpl
def needed_REST_paths() -> List[str]:
    """
    Return a list of paths that this plugin wants to add to the REST-API.
    
    :return: a list of REST API paths
    """
    return ["logParser"]


@hookimpl
def register_REST_path(requested_path: str, approved_path:str) -> Dict[str, Union[bool, str, List[Dict[str, str]]]]:
    """
    Register the requested path with the REST-API.

    :param requested_path: the path that was requested
    :param approved_path: the path that that was approved
    :return: if the approved path was added, return a dictonary, explaining the path,
    as a dictonary with entries for the link, a description and parameters. 
    
    Note:
    A dictonary for the link description could look like this:
    {
        "link": "/v" + str(version) + gpu_path + "/config",
        "isOptional": True,
        "description": "Gather information concerning the memory config",
        "parameters": [
            {"name": "token",
             "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
    }
    
    """
    @RESTAPI.route("/logParser", methods=["GET"])
    @check_auth(scopes["see_links"])
    def returnLogParserLinks() -> Response:
        logging.debug("Accessed /logParser/")
        return make_response(jsonify(sorted(links, key=lambda dic: dic['link'])), 200)
    
    return {
            "link": "/logParser",
            "isOptional": True,
            "description": "See avaiable information through the log parser plugin",
            "parameters": [
                {"name": "token",
                 "description": "Supply a token that shows you are allowed to access this link (or login once using /login)"}]
        }


@hookimpl
def register_startup_parameter() -> List[Dict[str, Union[bool, int, float, str, type]]]:
    """
    Register the wanted startup parameter for this plugin.

    :return: a list of dictonaries, one dictonary for each parameter.
    """


@hookimpl
def startup_parameter(parameter_name: str, value:Any) -> None:
    """
    Use the user supplied value for start parameter.

    :param parameter_name: the name of the parameter
    :param value: the value set for this parameter
    """


@hookimpl
def register_MPI(MPI_ID_min:int, MPI_ID_max:int) -> None:
    """
    Let the plugin handle all necessary steps for it's MPI communication.
    
    Let the plugin register callback options for MPI_IDs used in JuMonC's communication.
    This plugin can use all MPI_IDs between min and max for all it's internal needs.
    """

