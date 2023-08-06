from __future__ import annotations

import logging
import os
import pickle
from dataclasses import dataclass, field
from distutils.util import strtobool
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import mosaik
import numpy as np
from midas.util.runtime_config import RuntimeConfig

if TYPE_CHECKING:
    from midas.util.upgrade_module import UpgradeModule

LOG = logging.getLogger(__name__)


class Scenario:
    """Stores everything that is related to the scenario
    build process of MIDAS.

    """

    def __init__(self, name: str, params: Dict[str, Any]):
        self.name: str = name
        self.world = None
        self.base: Base = Base()
        self.script: Script = Script()
        self.sensors: list = []
        self.actuators: list = []

        self._sim_keys: Dict[str, Any] = {}
        self._mappings: Dict[str, Any] = {}
        self._ict_mappings: List[Dict[str, Any]] = []

        self._configure(params)
        self.success: bool = False

    def _configure(self, params):
        """Create the base configuration for midas scenarios.

        Parameters
        ----------
        params: dict
            A *dict* containing the cascading contents of yaml config
            files.

        """
        paths = RuntimeConfig().paths
        data = RuntimeConfig().data
        self.base.seed_max = int(
            RuntimeConfig().misc.get("seed_max", 1_000_000)
        )
        self.base.output_path = paths["output_path"]
        self.base.data_path = params.setdefault(
            "data_path", paths["data_path"]
        )

        os.makedirs(self.base.output_path, exist_ok=True)

        self.base.step_size = int(params.setdefault("step_size", 15 * 60))
        self.base.start_date = params.setdefault(
            "start_date", "2020-01-01 00:00:00+0100"
        )

        self.base.end = int(params.setdefault("end", 1 * 24 * 60 * 60))
        self.base.cos_phi = params.setdefault("cos_phi", 0.9)
        self.base.no_db = set_default_bool("no_db", params, False)
        self.base.with_timesim = set_default_bool(
            "with_timesim", params, False
        )
        self.base.with_arl = set_default_bool("with_arl", params, False)
        self.sensors = params.setdefault("sensors", [])
        self.actuators = params.setdefault("actuators", [])
        self.base.with_ict = set_default_bool("with_ict", params, False)
        self.base.no_rng = set_default_bool("no_rng", params, False)
        self.base.forecast_horizon_hours = params.setdefault(
            "forecast_horizon_hours", 0.25
        )
        self.base.flexibility_horizon_hours = params.setdefault(
            "flexibility_horizon_hours", self.base.forecast_horizon_hours
        )
        self.base.flexibility_horizon_start_hours = params.setdefault(
            "flexibility_horizon_start_hours", 0
        )
        self.base.cmd = params.setdefault("cmd", "python")
        self.base.default_weather_name = data["weather"][0]["name"]
        self.base.default_simbench_name = data["simbench"][0]["name"]
        self.base.default_commcercials_name = data["commercials"][0]["name"]

        mosaik_params = params.setdefault("mosaik_params", {})
        self.world = mosaik.World(sim_config={}, mosaik_config=mosaik_params)

        if "random_state" in params:
            # A path to a random state object was passed with the params
            with open(params["random_state"], "rb") as state_f:
                random_state = pickle.load(state_f)
            self.base.rng = np.random.RandomState()
            self.base.rng.set_state(random_state)
        elif "seed" in params and params["seed"] is not None:
            # A seed was passed with the params
            if isinstance(params["seed"], int):
                self.base.rng = np.random.RandomState(params["seed"])
            else:
                LOG.warning(
                    "Invalid seed %s of type %s. Provide an integer!",
                    params["seed"],
                    type(params["seed"]),
                )
            state_fname = os.path.join(
                self.base.output_path, f"{self.name}-random_state"
            )
            with open(state_fname, "wb") as state_f:
                pickle.dump(self.base.rng.get_state(), state_f)
            params["random_state"] = state_fname
        else:
            # We create a random state object regardless if no_rng
            # is true. If no_rng is true, random number just won't be
            # used by the simulators.
            self.base.rng = np.random.RandomState()

        if not self.base.no_rng and self.base.start_date == "random":
            self.base.start_date = (
                f"2020-{self.base.rng.randint(1, 12):02d}-"
                f"{self.base.rng.randint(1, 28):02d} "
                f"{self.base.rng.randint(0, 23):02d}:00:00+0100"
            )
            params["start_date"] = self.base.start_date

        self.script.imports.append("import_mosaik\n")
        self.script.imports.append("import numpy as np\n")
        self.script.sim_start.append("world = mosaik.World(sim_config)\n")
        self.script.world_start.append("world.run(until=end)\n")
        for key, value in self.base.__dict__.items():
            if key in ("rng"):
                continue

            if isinstance(value, str):
                self.script.definitions.append(f'{key} = "{value}"\n')
            else:
                self.script.definitions.append(f"{key} = {value}\n")

        self.script.definitions.append(
            f'rng = np.random.RandomState({params.get("seed", None)})\n'
        )

    def generate_sim_key(self, module):
        sim_key = f"{module.module_name}_{module.scope_name}_sim".lower()
        self._sim_keys[sim_key] = {}

        return sim_key

    def sim_started(self, sim_key):
        if self._sim_keys[sim_key]:
            return True
        else:
            return False

    def add_sim(self, sim_key, sim):
        self._sim_keys[sim_key]["sim"] = sim
        self._sim_keys[sim_key]["models"] = {}

    def get_sim(self, sim_key):
        try:
            return self._sim_keys[sim_key]["sim"]
        except KeyError:
            LOG.info("Simulator with key %s does not exist, yet!")
            return None

    def model_started(self, model_key, sim_key=None):
        if sim_key is not None:
            if self.sim_started(sim_key):
                if model_key in self._sim_keys[sim_key]["models"]:
                    return True
                else:
                    return False

        for sim_key, sim_cfg in self._sim_keys.items():
            if not sim_cfg:
                continue

            if model_key in sim_cfg["models"]:
                return True

        return False

    def add_model(self, model_key, sim_key, model):
        self._sim_keys[sim_key]["models"][model_key] = model

    def get_models(self, sim_key):
        return self._sim_keys[sim_key].get("models", {})

    def get_model(self, model_key, sim_key=None):
        if sim_key is not None:
            if self.sim_started(sim_key):
                if model_key in self._sim_keys[sim_key]["models"]:
                    return self._sim_keys[sim_key]["models"][model_key]

        for sim_key, sim_cfg in self._sim_keys.items():
            if not sim_cfg:
                continue
            if model_key in sim_cfg["models"]:
                return sim_cfg["models"][model_key]

        LOG.info("Model with key %s does not exist, yet!", model_key)
        return None

    def generate_model_key(
        self,
        module: UpgradeModule,
        first_key: Optional[str] = None,
        second_key: Optional[str] = None,
        third_key: Optional[str] = None,
    ):
        model_key = f"{module.module_name}_{module.scope_name}"
        if first_key is not None:
            model_key += f"_{first_key}"
        if second_key is not None:
            model_key += f"_{second_key}"
        if third_key is not None:
            model_key += f"_{third_key}"
        return model_key

    def find_models(self, sim_key, model_key=None, add_key1=None):
        results = {}
        sim_keys = []
        if sim_key not in self._sim_keys:
            for key in self._sim_keys:
                if sim_key in key:
                    sim_keys.append(key)
        else:
            sim_keys.append(sim_key)
        for sim_key in sim_keys:
            for key, model in self.get_models(sim_key).items():
                if model_key is not None:
                    if model_key not in key:
                        continue
                if add_key1 is not None:
                    if add_key1 not in key:
                        continue
                results[key] = model

        return results

    def find_first_model(
        self, sim_key, model_key=None
    ) -> Tuple[Union[str, None], Union[Any, None]]:
        models = self.find_models(sim_key, model_key)

        for key, model in models.items():
            return key, model

        return None, None

    def create_seed(self):
        return self.base.rng.randint(self.base.seed_max)

    def create_shared_mapping(
        self,
        module: UpgradeModule,
        first_key: Optional[str] = None,
        second_key: Optional[str] = None,
    ):

        key = f"{module.module_name}_{module.scope_name}"

        if first_key is not None:
            key += f"_{first_key}"
        if second_key is not None:
            key += f"_{second_key}"

        key += "_mapping"

        return self._mappings.setdefault(key, {})

    def get_shared_mappings(
        self,
        module_name: Optional[str] = None,
        scope_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        if module_name is not None or scope_name is not None:
            mappings = {}
            for key, mapping in self._mappings.items():
                if module_name is not None and scope_name is not None:
                    if f"{module_name}_{scope_name}" in key:
                        mappings[key] = mapping
                elif module_name is not None:
                    if module_name in key:
                        mappings[key] = mapping
                elif scope_name is not None:
                    if scope_name in key:
                        mappings[key] = mapping
            return mappings
        else:
            return self._mappings

    def get_ict_mappings(self) -> List[Dict[str, Any]]:
        if self._ict_mappings is None:
            self._ict_mappings = []

        return self._ict_mappings

    def find_grid_entities(self, grid_name, etype, idx=None, endswith=None):
        if idx is not None:
            etype += f"_{idx}"
        entities = self.find_models("powergrid", grid_name, etype)

        if endswith is None:
            return entities
        else:
            results = {}
            for key, entity in entities.items():
                if key.endswith(endswith):
                    results[key] = entity
            return results


@dataclass(init=False)
class Base:

    seed: int
    seed_max: int
    output_path: str
    data_path: str
    step_size: int
    start_date: str
    end: int
    cos_phi: float
    no_db: bool
    with_timesim: bool
    with_arl: bool
    with_ict: bool
    no_rng: bool
    forecast_horizon_hours: float
    flexibility_horizon_hours: float
    flexibility_horizon_start_hours: float
    rng: np.random.RandomState
    cmd: str

    default_weather_name: str
    default_simbench_name: str
    default_commcercials_name: str


@dataclass(init=False)
class Script:
    imports: List[str] = field(default_factory=list)
    definitions: List[str] = field(default_factory=list)
    simconfig: List[str] = field(default_factory=list)
    model_start: List[str] = field(default_factory=list)
    connects: List[str] = field(default_factory=list)
    sim_start: List[str] = field(default_factory=list)
    world_start: List[str] = field(default_factory=list)

    def __init__(self):
        self.imports = []
        self.definitions = []
        self.simconfig = []
        self.sim_start = []
        self.model_start = []
        self.connects = []
        self.world_start = []


def set_default_bool(key, params, default=False):
    val = params.get(key, default)
    if not isinstance(val, bool):
        val = strtobool(val)
    params[key] = val
    return val
