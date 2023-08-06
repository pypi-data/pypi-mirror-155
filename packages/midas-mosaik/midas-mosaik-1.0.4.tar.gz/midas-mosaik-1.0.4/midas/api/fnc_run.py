import os
from typing import Any, Optional, Union, List, Dict

import click
from midas.scenario.configurator import Configurator
from midas.scenario.scenario import Scenario

from . import fnc_configure, fnc_download


def run(
    scenario_name: str = "demo",
    params: Optional[Dict[str, Any]] = None,
    config: Optional[Union[str, List[str]]] = None,
    no_run: bool = False,
    no_script: bool = False,
    no_yaml: bool = False,
    skip_configure: bool = False,
    skip_download: bool = False,
) -> Scenario:
    """The main run method to start a MIDAS scenario.

    Parameters
    ----------
    scenario_name: str
        The name of the scenario to start. The name is the toplevel
        key in the scenario yaml file.
    params: Union[Dict, None]
        Optional dictionary with scenario parameters that will be
        passed to the configurator.
    config: Union[Tuple, str, None]
        One or more custom configs to load the scenario from.

    """

    # Just to be save: Configure runtime config and download datasets.
    if not skip_configure:
        fnc_configure.configure(autocfg=True)
    if not skip_download:
        fnc_download.download()

    if scenario_name == "demo":
        scenario_name = "midasmv"

    if params is None:
        params = dict()

    params.setdefault("silent", False)

    if config is not None:
        if isinstance(config, str):
            config = (config,)
        config = [os.path.abspath(c) for c in config]

    configurator = Configurator()
    scenario = configurator.configure(
        scenario_name, params, config, no_script, no_yaml
    )
    if scenario.success:
        if no_run:
            return scenario
        else:
            configurator.run()
    else:
        click.echo(
            "Scenario configuration failed. See log files for more infos"
        )

    return scenario
