import json
from copy import deepcopy
from datetime import timedelta
from math import isclose
from os import PathLike
from typing import Any, Dict, Iterable, List, MutableMapping, Optional, Union

import altair as alt
import pandas as pd
import yaml
from IPython import get_ipython
from IPython.display import Code

from flowchem.components.properties import (
    ActiveComponent,
    Component,
    MultiportComponentMixin,
    TempControl,
)
from flowchem.core.experiment import Experiment
from flowchem.core.graph.devicegraph import DeviceGraph
from flowchem.units import flowchem_ureg


class Protocol:
    """
    A set of procedures for a DeviceGraph.

    A protocol is defined as a list of procedures, atomic steps for the individual active components of a DeviceGraph.

    Arguments:
    - `graph`: The DeviceGraph object for which the protocol is being defined.
    - `name`: The name of the protocol. Defaults to "Protocol_X" where *X* is protocol count.
    - `description`: A longer description of the protocol.

    Attributes:
    - `graph`: The apparatus for which the protocol is being defined.
    - `description`: A longer description of the protocol.
    - `is_executing`: Whether the protocol is executing.
    - `name`: The name of the protocol. Defaults to "Protocol_X" where *X* is protocol count.
    - `procedures`: A list of the procedures for the protocol in which each procedure is a dict.
    - `was_executed`: Whether the protocol was executed.
    """

    _id_counter = 0

    def __init__(
        self,
        graph: DeviceGraph,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """See main docstring."""
        # type checking
        if not isinstance(graph, DeviceGraph):
            raise TypeError(
                f"Must pass an Apparatus object. Got {type(graph)}, "
                "which is not an instance of flowchem.DeviceGraph."
            )

        # store the passed args
        self.graph = graph
        self.description = description

        # generate the name
        if name is not None:
            self.name = name
        else:
            self.name = "Protocol_" + str(Protocol._id_counter)
            Protocol._id_counter += 1

        # ensure apparatus is valid
        if not graph.validate():
            raise ValueError("DeviceGraph is not valid.")

        # default values
        self.procedures: List[
            Dict[str, Union[float, None, ActiveComponent, Dict[str, Any]]]
        ] = []

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"Protocol {self.name} defined over {repr(self.graph)}"

    def _check_component_kwargs(self, component: ActiveComponent, **kwargs) -> None:
        """Checks that the given keyword arguments are valid for a component."""
        for kwarg, value in kwargs.items():
            # check that the component even has the attribute
            if not hasattr(component, kwarg):
                # id nor determine valid attrs for the error message
                valid_attrs = [x for x in vars(component).keys()]
                # we don't care about the name attr
                valid_attrs = [x for x in valid_attrs if x != "name"]
                # or internal ones
                valid_attrs = [x for x in valid_attrs if not x.startswith("_")]

                msg = f"Invalid attribute {kwarg} for {component}. "
                msg += f"Valid attributes are {valid_attrs}"
                raise ValueError(msg)

            # for kwargs that will be converted later, just check that the units match
            if isinstance(component.__dict__[kwarg], flowchem_ureg.Quantity):
                try:
                    value_dim = flowchem_ureg.parse_expression(value).dimensionality
                except AttributeError:
                    value_dim = type(value)
                kwarg_dim = component.__dict__[kwarg].dimensionality

                # perform the check
                if value_dim != kwarg_dim:
                    msg = f"Bad dimensionality of {kwarg} for {component}. "
                    msg += f"Expected {kwarg_dim} but got {value_dim}."
                    raise ValueError(msg)

            # if it's not a quantity, check the types
            elif not isinstance(value, type(component.__dict__[kwarg])):
                expected_type = type(component.__dict__[kwarg])
                msg = "Bad type matching. "
                msg += f"Expected '{kwarg}' to an instance of {expected_type} but got"
                msg += f"{repr(value)}, which is of type {type(value)}."
                raise ValueError(msg)

    def _add_single(
        self,
        component: ActiveComponent,
        start: Union[str, timedelta],
        stop=None,
        duration=None,
        **kwargs,
    ) -> None:
        """Adds a single procedure to the protocol.

        See add() for full documentation.
        """

        # make sure that the component being added is part of the apparatus
        assert component in self.graph, f"{component} must be part of the apparatus."

        # don't let users give empty procedures
        if not kwargs:
            raise RuntimeError(
                "No kwargs supplied. "
                "This will not manipulate the state of your synthesizer. "
                "Ensure your call to add() is valid."
            )

        # FIXME procedures are XDLexe like, the actual valve position should be passed directly, resolve before!
        # If a MultiportComponentMixin component is passed together with a new port position, check validity
        if isinstance(component, MultiportComponentMixin) and "setting" in kwargs:
            if isinstance(kwargs["setting"], Component):
                assert self.graph.graph.has_edge(component, kwargs["setting"])
                assert (
                    self.graph.graph[component][kwargs["setting"]][0]["from_port"]
                    in component.port
                )
            if isinstance(kwargs["setting"], str):
                to_component = self.graph[kwargs["setting"]]
                assert self.graph.graph.has_edge(component, to_component)
                assert (
                    self.graph.graph[component][to_component]["from_port"]
                    in component.port
                )
            if isinstance(kwargs["setting"], int):
                assert kwargs["setting"] in component.port

        # make sure the component and keywords are valid
        self._check_component_kwargs(component, **kwargs)

        # parse the start time
        if start is None:
            start = "0 secs"
        if isinstance(start, timedelta):
            start = str(start.total_seconds()) + " seconds"
        start_time = flowchem_ureg.parse_expression(start)

        # Stop or duration
        if stop is not None and duration is not None:
            raise RuntimeError("Must provide one of stop and duration, not both.")

        # Parse duration
        if duration is not None:
            if isinstance(duration, timedelta):
                duration = str(duration.total_seconds()) + " seconds"
            stop_time = start_time + flowchem_ureg.parse_expression(duration)
        # Parse stop
        else:
            assert stop is not None
            if isinstance(stop, timedelta):
                stop = str(stop.total_seconds()) + " seconds"
            stop_time = flowchem_ureg.parse_expression(stop)

        if start_time > stop_time:
            raise ValueError("Procedure beginning is after procedure end.")

        # a little magic for temperature controllers
        if isinstance(component, TempControl):
            if kwargs.get("temp") is not None and kwargs.get("active") is None:
                kwargs["active"] = True
            elif not kwargs.get("active") and kwargs.get("temp") is None:
                kwargs["temp"] = "0 degC"
            elif kwargs["active"] and kwargs.get("temp") is None:
                raise RuntimeError(
                    f"TempControl {component} is activated but temperature "
                    "setting is not given. Specify 'temp' in your call to add()."
                )

        # add the procedure to the procedure list
        self.procedures.append(
            dict(
                start=start_time.m_as("second"),
                stop=stop_time.m_as("second"),
                component=component,
                params=kwargs,
            )
        )

    def add(
        self,
        component: Union[ActiveComponent, Iterable[ActiveComponent]],
        start=None,
        stop=None,
        duration=None,
        **kwargs,
    ):
        """
        Adds a procedure to the protocol.

        ::: warning
        If stop and duration are both `None`, the procedure's stop time will be inferred as the end of the protocol.
        :::

        Arguments:
        - `component_added`: The component(s) for which the procedure being added. If an interable, all components will have the same parameters.
        - `start`: The start time of the procedure relative to the start of the protocol, such as `"5 seconds"`. May also be a `datetime.timedelta`. Defaults to `"0 seconds"`, *i.e.* the beginning of the protocol.
        - `stop`: The stop time of the procedure relative to the start of the protocol, such as `"30 seconds"`. May also be a `datetime.timedelta`. May not be given if `duration` is used.
        duration: The duration of the procedure, such as "1 hour". May not be used if `stop` is used.
        - `**kwargs`: The state of the component for the procedure.

        Raises:
        - `TypeError`: A component is not of the correct type (*i.e.* a Component object)
        - `ValueError`: An error occurred when attempting to parse the kwargs.
        - `RuntimeError`: Stop time of procedure is unable to be determined or invalid component.
        """

        if isinstance(component, Iterable):
            for _component in component:
                self._add_single(
                    _component, start=start, stop=stop, duration=duration, **kwargs
                )
        else:
            self._add_single(
                component, start=start, stop=stop, duration=duration, **kwargs
            )

    @property
    def _inferred_duration(self):
        # infer the duration of the protocol
        computed_durations = sorted(
            [x["stop"] for x in self.procedures],
            key=lambda z: z if z is not None else 0,
        )
        if all([x is None for x in computed_durations]):
            raise RuntimeError(
                "Unable to automatically infer duration of protocol. "
                "Must define stop or duration for at least one procedure"
            )
        return computed_durations[-1]

    def _compile(
        self, dry_run: bool = True, _visualization: bool = False
    ) -> Dict[ActiveComponent, List[Dict[str, Union[float, str, Dict[str, Any]]]]]:
        """
        Compile the protocol into a dict of devices and their procedures.

        Returns:
        - A dict with components as keys and lists of their procedures as the value.
        The elements of the list of procedures are dicts with two keys:
            "time" in seconds
            "params", whose value is a dict of parameters for the procedure.

        Raises:
        - `RuntimeError`: When compilation fails.
        """
        output = {}

        # Only compile active components
        for component in self.graph[ActiveComponent]:
            # determine the procedures for each component
            component_procedures: List[MutableMapping] = sorted(
                [x for x in self.procedures if x["component"] == component],
                key=lambda x: x["start"],
            )

            # validate component
            try:
                component._validate(dry_run=dry_run)
            except Exception as e:
                raise RuntimeError(
                    f"{component} isn't valid. Got error: '{str(e)}'."
                ) from e

            # Validates procedures for component
            component.validate_procedures(component_procedures)

            # give the component instructions at all times
            compiled = []
            for i, procedure in enumerate(component_procedures):
                if _visualization:
                    compiled.append(
                        dict(
                            start=procedure["start"],
                            stop=procedure["stop"],
                            params=procedure["params"],
                        )
                    )
                else:
                    compiled.append(
                        dict(time=procedure["start"], params=procedure["params"])
                    )

                    # if the procedure is over at the same time as the next
                    # procedure begins, don't go back to the base state
                    try:
                        if isclose(
                            component_procedures[i + 1]["start"], procedure["stop"]
                        ):
                            continue
                    except IndexError:
                        pass

                    # otherwise, go back to base state
                    new_state = {
                        "time": procedure["stop"],
                        "params": component._base_state,
                    }
                    compiled.append(new_state)

            output[component] = compiled

            # raise warning if duration is explicitly given but not used?
        return output

    def to_dict(self):
        compiled = deepcopy(self._compile(dry_run=True))
        compiled = {k.name: v for (k, v) in compiled.items()}
        return compiled

    def to_list(self):
        output = []
        for procedure in deepcopy(self.procedures):
            procedure["component"] = procedure["component"].name
            output.append(procedure)
        return output

    def yaml(self) -> Union[str, Code]:
        """
        Outputs the uncompiled procedures to YAML.

        Internally, this is a conversion of the output of `Protocol.json` for the purpose of enhanced human readability.

        Returns:
        - YAML of the procedure list.
        When in Jupyter, this string is wrapped in an `IPython.display.Code` object for nice syntax highlighting.

        """
        compiled_yaml = yaml.safe_dump(self.to_list(), default_flow_style=False)

        if get_ipython():
            return Code(compiled_yaml, language="yaml")
        return compiled_yaml

    def json(self) -> Union[str, Code]:
        """
        Outputs the uncompiled procedures to JSON.

        Returns:
        - JSON of the protocol.
          When in Jupyter, this string is wrapped in a `IPython.display.Code` object for nice syntax highlighting.
        """
        compiled_json = json.dumps(self.to_list(), sort_keys=True, indent=4)

        if get_ipython():
            return Code(compiled_json, language="json")
        return compiled_json

    def visualize(self, legend: bool = False, width=500, renderer: str = "notebook"):
        """
        Generates a Gantt plot visualization of the protocol.

        Arguments:
        - `legend`: Whether to show a legend.
        - `renderer`: Which renderer to use. Defaults to "notebook" but can also be "jupyterlab", or "nteract", depending on the development environment. If not in a Jupyter Notebook, this argument is ignored.
        - `width`: The width of the Gantt chart.

        Returns:
        - An interactive visualization of the protocol.
        """

        # don't try to render a visualization to the notebook if we're not in one
        if get_ipython():
            alt.renderers.enable(renderer)

        for component, procedures in self._compile(_visualization=True).items():
            # generate a dict that will be a row in the dataframe
            for procedure in procedures:
                procedure["component"] = str(component)
                procedure["start"] = pd.Timestamp(procedure["start"], unit="s")
                procedure["stop"] = pd.Timestamp(procedure["stop"], unit="s")

                # hoist the params to the main dict
                assert isinstance(procedure["params"], dict)  # needed for typing
                for k, v in procedure["params"].items():
                    procedure[k] = v

                # show what the valve is actually connecting to
                if (
                    isinstance(component, MultiportComponentMixin)
                    and "setting" in procedure.keys()
                ):
                    mapped_component = self.graph.component_from_origin_and_port(component, procedure["setting"])  # type: ignore
                    procedure["mapped component"] = mapped_component.name
                # TODO: make this deterministic for color coordination
                procedure["params"] = json.dumps(procedure["params"])

            # prettify the tooltips
            tooltips = [
                alt.Tooltip("utchoursminutesseconds(start):T", title="start (h:m:s)"),
                alt.Tooltip("utchoursminutesseconds(stop):T", title="stop (h:m:s)"),
                "component",
            ]

            # just add the params to the tooltip
            tooltips.extend(
                [
                    x
                    for x in procedures[0].keys()
                    if x not in ["component", "start", "stop", "params"]
                ]
            )

            # generate the component's graph
            source = pd.DataFrame(procedures)
            component_chart = (
                alt.Chart(source, width=width)
                .mark_bar()
                .encode(
                    x="utchoursminutesseconds(start):T",
                    x2="utchoursminutesseconds(stop):T",
                    y="component",
                    color=alt.Color("params:N", legend=None)
                    if not legend
                    else "params",
                    tooltip=tooltips,
                )
            )

            # label the axes
            component_chart.encoding.x.title = "Experiment Elapsed Time (h:m:s)"
            component_chart.encoding.y.title = "Component"

            # combine with the other charts
            try:
                chart += component_chart  # type: ignore
            except NameError:
                chart = component_chart

        return chart.interactive()

    def execute(
        self,
        dry_run: Union[bool, int] = False,
        verbosity: str = "info",
        confirm: bool = False,
        strict: bool = True,
        log_file: Union[str, bool, PathLike, None] = True,
        log_file_verbosity: Optional[str] = "trace",
        log_file_compression: Optional[str] = None,
        data_file: Union[str, bool, PathLike, None] = True,
    ) -> Experiment:
        """
        Executes the procedure.

        Arguments:
        - `confirm`: Whether to bypass the manual confirmation message before execution.
        - `dry_run`: Whether to simulate the experiment or actually perform it. Defaults to `False`,
        which means executing the protocol on real hardware. If an integer greater than zero,
        the dry run will execute at that many times speed.
        - `strict`: Whether to stop execution upon encountering any errors.
        If False, errors will be noted but ignored.
        - `verbosity`: The level of logging verbosity. One of "critical", "error", "warning", "success", "info", "debug", or "trace" in descending order of severity. "debug" and (especially) "trace" are not meant to be used regularly, as they generate significant amounts of usually useless information. However, these verbosity levels are useful for tracing where exactly a bug was generated, especially if no error message was thrown.
        - `log_file`: The file to write the logs to during execution. If `True`, the data will be written to a file in `~/.mechwolf` with the filename `{experiment_id}.log.jsonl`. If falsey, no logs will be written to the file.
        - `log_file_verbosity`: How verbose the logs in file should be. By default, it is "trace", which is the most verbose logging available. If `None`, it will use the same level as `verbosity`.
        - `log_file_compression`: Whether to compress the log file after the experiment.
        - `data_file`: The file to write the experimental data to during execution. If `True`, the data will be written to a file in `~/.mechwolf` with the filename `{experiment_id}.data.jsonl`. If falsey, no data will be written to the file.

        Returns:
        - An `Experiment` object. In a Jupyter notebook, the object yields an interactive visualization. If protocol execution fails for any reason that does not raise an error, the return type is None.

        Raises:
        - `RuntimeError`: When attempting to execute a protocol on invalid components.
        """

        # the Experiment object is going to hold all the info
        E = Experiment(self)
        E._execute(
            dry_run=dry_run,
            verbosity=verbosity,
            confirm=confirm,
            strict=strict,
            log_file=log_file,
            log_file_verbosity=log_file_verbosity,
            log_file_compression=log_file_compression,
            data_file=data_file,
        )

        return E
