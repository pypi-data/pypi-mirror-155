# Copyright 2022 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""
Pulse library nodes.
"""

from typing import (
    Optional,
    Union,
)

import numpy as np
from qctrlcommons.graph import Graph
from qctrlcommons.node.node_data import (
    Pwc,
    Tensor,
)
from qctrlcommons.preconditions import check_argument

from qctrltoolkit.namespace import Namespace
from qctrltoolkit.toolkit_utils import expose


def _validate_optimizable_parameter(
    graph: Graph, parameter: Union[float, Tensor], name: str
) -> Tensor:
    """
    Converts parameter into a Tensor, checks that it contains a single element
    and returns a Tensor containing that element.
    """

    parameter = graph.tensor(parameter)
    check_argument(
        np.prod(parameter.shape) == 1,
        f"If passed as a Tensor, the {name} must either "
        "be a scalar or contain a single element.",
        {name: parameter},
        extras={f"{name}.shape": parameter.shape},
    )

    return graph.reshape(parameter, [1])[0]


@expose(Namespace.PULSES)
def square_pulse_pwc(
    graph: Graph,
    duration: float,
    amplitude: Union[float, Tensor],
    initial_time: float = 0,
    final_time: Optional[float] = None,
    name: Optional[str] = None,
) -> Pwc:
    # pylint:disable=line-too-long
    r"""
    Creates a square pulse.

    The entire signal lasts from time 0 to the given duration with the
    square pulse being applied from the initial time to the final time.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal.
    amplitude : float or Tensor
        The amplitude of the square pulse, :math:`A`.
        It must either be a scalar or contain a single element.
    initial_time : float, optional
        The start time of the square pulse, :math:`t_0`.
        Defaults to 0.
    final_time : float, optional
        The end time of the square pulse, :math:`t_1`.
        Must be greater than the initial time.
        Defaults to the value of the given duration.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The square pulse. The returned Pwc can have a maximum of three segments and a minimum
        of one, depending on the initial and final times of the pulse and the duration of the
        signal.

    Notes
    -----
        The square pulse is defined as

        .. math:: \mathop{\mathrm{Square}}(t) = A \theta(t-t_0) \theta(t-t_1) \; ,

        where :math:`A` is the amplitude, :math:`t_0` is the initial time of the pulse,
        :math:`t_1` is the final time of the pulse and :math:`\theta(t)` is the Heaviside step
        function.

    Examples
    --------

    Define a square PWC pulse.

    >>> graph.pulses.square_pulse_pwc(
    ...     duration=4.0,
    ...     amplitude=2.5,
    ...     initial_time=1.0,
    ...     final_time=3.0,
    ...     name="square_pulse",
    ... )
    <Pwc: name="square_pulse", operation_name="time_concatenate_pwc", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["square_pulse"])
    >>> result.output["square_pulse"]
    [
        {'duration': 1.0, 'value': 0.0},
        {'duration': 2.0, 'value': 2.5},
        {'duration': 1.0, 'value': 0.0}
    ]

    Define a square pulse with an optimizable amplitude.

    >>> amplitude = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=2.*np.pi, name="amplitude"
    ... )
    >>> graph.pulses.square_pulse_pwc(
    ...     duration=4.0, amplitude=amplitude, name="square_pulse"
    ... )
    <Pwc: name="square_pulse", operation_name="time_concatenate_pwc", value_shape=(), batch_shape=()>
    """

    # pylint:enable=line-too-long
    if final_time is None:
        final_time = duration

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )
    check_argument(
        final_time > initial_time,
        "The final time must be greater than the initial time.",
        {"final_time": final_time, "initial_time": initial_time},
    )

    amplitude = _validate_optimizable_parameter(graph, amplitude, "amplitude")

    if initial_time >= duration or final_time <= 0:
        # In both of these cases the signal is always zero.
        return graph.pwc_signal(duration=duration, values=np.array([0.0]), name=name)

    pwcs = []

    if initial_time > 0:
        # Add preceding step function.
        pwcs.append(graph.pwc_signal(duration=initial_time, values=np.array([0.0])))

    pwcs.append(
        graph.pwc_signal(
            duration=min(final_time, duration) - max(initial_time, 0),
            values=amplitude * np.array([1.0]),
        )
    )

    if final_time < duration:
        # Add trailing step function.
        pwcs.append(
            graph.pwc_signal(duration=duration - final_time, values=np.array([0.0]))
        )

    return graph.time_concatenate_pwc(pwcs, name=name)


@expose(Namespace.PULSES)
def sech_pulse_pwc(
    graph: Graph,
    duration: float,
    segment_count: int,
    amplitude: Union[float, Tensor],
    pulse_width: Optional[Union[float, Tensor]] = None,
    peak_time: Optional[Union[float, Tensor]] = None,
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a pulse defined by a hyperbolic secant.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal, :math:`T`.
    segment_count : int
        The number of segments in the PWC.
    amplitude : float or Tensor
        The amplitude of the pulse, :math:`A`.
        It must either be a scalar or contain a single element.
    pulse_width : float or Tensor, optional
        The characteristic time for the hyperbolic secant pulse, :math:`t_\mathrm{pulse}`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to :math:`T/12`,
        giving the pulse a full width at half maximum (FWHM) of :math:`0.22 T`.
    peak_time : float or Tensor, optional
        The time at which the pulse peaks, :math:`t_\mathrm{peak}`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to :math:`T/2`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The hyperbolic secant pulse.

    Notes
    -----
    The hyperbolic secant pulse is defined as

        .. math:: \mathop{\mathrm{Sech}}(t)
            = \frac{A}{\cosh\left((t - t_0) / t_\mathrm{pulse} \right)} \; ,

    where :math:`A` the pulse amplitude,
    :math:`t_0` is the time at which the pulse peaks,
    and :math:`t_\mathrm{pulse}` characterizes the pulse width
    (its FWHM is :math:`2.634 t_\mathrm{pulse}`).

    Examples
    --------

    Define a simple sech PWC pulse.

    >>> graph.pulses.sech_pulse_pwc(
    ...     duration=5, segment_count=50, amplitude=1, name="sech_pulse"
    ... )
    <Pwc: name="sech_pulse", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["sech_pulse"])
    >>> result.output["sech_pulse"]
    [
        {'value': -0.0056, 'duration': 0.1},
        {'value': -0.0071, 'duration': 0.1},
        ...
        {'value': 0.0071, 'duration': 0.1},
        {'value': 0.0056, 'duration': 0.1},
    ]

    Define a displaced sech PWC pulse.

    >>> graph.pulses.sech_pulse_pwc(
    ...     duration=3e-6,
    ...     segment_count=60,
    ...     amplitude=20e6,
    ...     pulse_width=0.15e-6,
    ...     peak_time=1e-6,
    ...     name="sech_pulse",
    ... )
    <Pwc: name="sech_pulse", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["sech_pulse"])
    >>> result.output["sech_pulse"]
    [
        {'value': 60137.43, 'duration': 5.e-08},
        {'value': 83928.37, 'duration': 5.e-08},
        ...
        {'value': 106.8105, 'duration': 5.e-08},
        {'value': 76.53310, 'duration': 5.e-08},
    ]

    Define a sech pulse with optimizable parameters.

    >>> graph = qctrl.create_graph()
    >>> amplitude = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=10e6, name="amplitude"
    ... )
    >>> pulse_width = graph.optimization_variable(
    ...     count=1, lower_bound=0.1e-6, upper_bound=0.5e-6, name="pulse_width"
    ... )
    >>> peak_time = graph.optimization_variable(
    ...     count=1, lower_bound=1e-6, upper_bound=2e-6, name="peak_time"
    ... )
    >>> graph.pulses.sech_pulse_pwc(
    ...     duration=3e-6,
    ...     segment_count=32,
    ...     amplitude=amplitude,
    ...     pulse_width=pulse_width,
    ...     peak_time=peak_time,
    ...     name="sech_pulse",
    ... )
    <Pwc: name="sech_pulse", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    """

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )

    if pulse_width is None:
        pulse_width = duration / 12

    if peak_time is None:
        peak_time = duration / 2

    amplitude = _validate_optimizable_parameter(graph, amplitude, "amplitude")
    pulse_width = _validate_optimizable_parameter(graph, pulse_width, "pulse width")
    peak_time = _validate_optimizable_parameter(graph, peak_time, "peak time")

    stf = amplitude / graph.cosh((graph.identity_stf() - peak_time) / pulse_width)
    return graph.discretize_stf(stf, duration, segment_count, name=name)


@expose(Namespace.PULSES)
def linear_ramp_pwc(
    graph: Graph,
    duration: float,
    segment_count: int,
    slope: Union[float, Tensor],
    zero_time: Optional[Union[float, Tensor]] = None,
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a linear ramp.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal.
    segment_count : int
        The number of segments in the PWC.
    slope : float or Tensor
        The slope of the ramp.
        It must either be a scalar or contain a single element.
    zero_time : float or Tensor, optional
        The time at which the ramp is zero.
        If passed, it must either be a scalar or contain a single element.
        Defaults to half of the given duration.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The linear ramp.

    Notes
    -----
        The linear ramp is defined as

        .. math:: \mathop{\mathrm{Linear}}(t) = \alpha (t - t_0) \; ,

        where :math:`\alpha` is the slope and :math:`t_0` is the time at which the ramp is zero.

    Examples
    --------

    Define a linear PWC ramp.

    >>> graph.pulses.linear_ramp_pwc(
    ...     duration=2.0, segment_count=4, slope=1.0, zero_time=0.25, name="linear_ramp"
    ... )
    <Pwc: name="linear_ramp", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["linear_ramp"])
    >>> result.output["linear_ramp"]
    [
        {'duration': 0.5, 'value': -0.125},
        {'duration': 0.5, 'value': 0.125},
        {'duration': 0.5, 'value': 0.375},
        {'duration': 0.5, 'value': 0.625},
    ]

    Define a linear ramp with an optimizable slope.

    >>> slope = graph.optimization_variable(
    ...     count=1, lower_bound=-30, upper_bound=30, name="slope"
    ... )
    >>> graph.pulses.linear_ramp_pwc(
    ...     duration=4.0, segment_count=64, slope=slope, name="linear_ramp"
    ... )
    <Pwc: name="linear_ramp", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    """

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )

    if zero_time is None:
        zero_time = duration / 2

    slope = _validate_optimizable_parameter(graph, slope, "slope")
    zero_time = _validate_optimizable_parameter(graph, zero_time, "zero time")

    stf = slope * (graph.identity_stf() - zero_time)
    return graph.discretize_stf(stf, duration, segment_count, name=name)


@expose(Namespace.PULSES)
def tanh_ramp_pwc(
    graph: Graph,
    duration: float,
    segment_count: int,
    final_value: Union[float, Tensor],
    initial_value: Optional[Union[float, Tensor]] = None,
    ramp_time: Optional[Union[float, Tensor]] = None,
    zero_time: Optional[Union[float, Tensor]] = None,
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a ramp defined by a hyperbolic tangent between an initial and a final value.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal, :math:`T`.
    segment_count : int
        The number of segments in the PWC.
    final_value : float or Tensor
        The asymptotic value of the ramp towards :math:`t \to +\infty`, :math:`a_+`.
        It must either be a scalar or contain a single element.
    initial_value : float or Tensor, optional
        The asymptotic value of the ramp towards :math:`t \to -\infty`, :math:`a_-`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to minus `final_value`.
    ramp_time : float or Tensor, optional
        The characteristic time for the hyperbolic tangent ramp, :math:`t_\mathrm{ramp}`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to :math:`T/6`.
    zero_time : float or Tensor, optional
        The time at which the ramp has its greatest slope, :math:`t_0`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to :math:`T/2`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The hyperbolic tangent ramp.

    Notes
    -----
    The hyperbolic tangent ramp is defined as

        .. math:: \mathop{\mathrm{Tanh}}(t)
            = \frac{a_+ + a_-}{2}
                + \frac{a_+ - a_-}{2} \tanh\left( \frac{t - t_0}{t_\mathrm{ramp}} \right) \; ,

    where :math:`a_\pm` are the final and initial values, that is, the function's asymptotic values,

        .. math:: \lim_{t\to\pm\infty} \mathop{\mathrm{Tanh}}(t) = a_\pm \; ,

    :math:`t_\mathrm{ramp}` is the characteristic time for the ramp,
    and :math:`t_0` is the time at which the ramp has its greatest slope:

        .. math::
            \left.\frac{{\rm d}\mathop{\mathrm{Tanh}}(t)}{{\rm d}t}\right|_{t=t_0}
                = \frac{ (a_+ - a_-)}{2 t_\mathrm{ramp}} \; .

    Note that if :math:`t_0` is close to the edges of the PWC,
    for example :math:`t_0 \lesssim 2 t_\mathrm{ramp}`,
    then the first and last values of the PWC will differ from the expected asymptotic values.

    With the default values of `initial_value` (:math:`a_-`),
    `ramp_time` (:math:`t_\mathrm{ramp}`), and `zero_time` (:math:`t_0`),
    the ramp expression simplifies to

        .. math:: \mathop{\mathrm{Tanh}}(t) = A \tanh\left( \frac{t - T/2}{T/6} \right)\; ,

    where :math:`A = a_+` is the final value (the initial value is then :math:`-A`)
    and :math:`T` is the PWC duration. This defines a symmetric ramp (around :math:`(T/2, 0)`)
    between :math:`-0.995 A` (at :math:`t=0`) and :math:`0.995 A` (at :math:`t=T`).

    Examples
    --------

    Define a simple tanh PWC ramp.

    >>> graph.pulses.tanh_ramp_pwc(
    ...     duration=5.0, segment_count=50, final_value=1, name="tanh_ramp"
    ... )
    <Pwc: name="tanh_ramp", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["tanh_ramp"])
    >>> result.output["tanh_ramp"]
    [
        {'value': -0.9944, 'duration': 0.1},
        {'value': -0.9929, 'duration': 0.1},
        ...
        {'value': 0.9929, 'duration': 0.1},
        {'value': 0.9944, 'duration': 0.1},
    ]

    Define a flat-top pulse from two tanh ramps.

    >>> ramp = graph.pulses.tanh_ramp_pwc(
    ...     duration=3,
    ...     segment_count=60,
    ...     final_value=1,
    ...     ramp_time=0.25,
    ...     zero_time=0.5,
    ... )
    >>> flat_top_pulse = 0.5 * (ramp + graph.time_reverse_pwc(ramp))
    >>> flat_top_pulse.name="flat_top_pulse"
    >>> print(flat_top_pulse)
    <Pwc: name="flat_top_pulse", operation_name="multiply", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["flat_top_pulse"])
    >>> result.output["flat_top_pulse"]
    [
        {'value': 0.0219, 'duration': 0.05},
        {'value': 0.0323, 'duration': 0.05},
        ...
        {'value': 0.0323, 'duration': 0.05},
        {'value': 0.0219, 'duration': 0.05},
    ]

    Define a tanh ramp with optimizable parameters.

    >>> final_value = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=3e6, name="final_value"
    ... )
    >>> ramp_time = graph.optimization_variable(
    ...     count=1, lower_bound=0.1e-6, upper_bound=0.3e-6, name="ramp_time"
    ... )
    >>> zero_time = graph.optimization_variable(
    ...     count=1, lower_bound=0.25e-6, upper_bound=0.75e-6, name="zero_time"
    ... )
    >>> graph.pulses.tanh_ramp_pwc(
    ...     duration=1e-6,
    ...     segment_count=32,
    ...     final_value=final_value,
    ...     initial_value=0.0,
    ...     ramp_time=ramp_time,
    ...     zero_time=zero_time,
    ...     name="tanh_ramp",
    ... )
    <Pwc: name="tanh_ramp", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    """

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )

    if initial_value is None:
        initial_value = -final_value

    if ramp_time is None:
        ramp_time = duration / 6

    if zero_time is None:
        zero_time = duration / 2

    final_value = _validate_optimizable_parameter(graph, final_value, "final value")
    initial_value = _validate_optimizable_parameter(
        graph, initial_value, "initial_value"
    )
    ramp_time = _validate_optimizable_parameter(graph, ramp_time, "ramp time")
    zero_time = _validate_optimizable_parameter(graph, zero_time, "zero time")

    stf = initial_value + 0.5 * (final_value - initial_value) * (
        1 + graph.tanh((graph.identity_stf() - zero_time) / ramp_time)
    )
    return graph.discretize_stf(stf, duration, segment_count, name=name)


@expose(Namespace.PULSES)
def gaussian_pulse_pwc(
    graph: Graph,
    duration: float,
    segment_count: int,
    amplitude: Union[float, Tensor],
    width: Optional[Union[float, Tensor]] = None,
    center: Optional[float] = None,
    drag: Optional[Union[float, Tensor]] = None,
    flat_time: Optional[float] = None,
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a Gaussian pulse.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal, :math:`T`.
    segment_count : int
        The number of segments in the PWC.
    amplitude : float or Tensor
        The amplitude of the Gaussian pulse, :math:`A`.
        It must either be a scalar or contain a single element.
    width : float or Tensor, optional
        The standard deviation of the Gaussian pulse, :math:`\sigma`.
        It must either be a scalar or contain a single element.
        Defaults to :math:`T/10` or :math:`(T-t_\mathrm{flat})/10` if `flat_time` is passed.
    center : float, optional
        The center of the Gaussian pulse, :math:`t_0`.
        Defaults to half of the given value of the duration, :math:`T/2`.
    drag : float or Tensor, optional
        The DRAG parameter, :math:`\beta`.
        If passed, it must either be a scalar or contain a single element.
        Defaults to no DRAG correction.
    flat_time : float, optional
        The amount of time to remain constant after the peak of the Gaussian,
        :math:`t_\mathrm{flat}`.
        If passed, it must be positive and less than the duration.
        Defaults to None, in which case no constant part is added to the Gaussian pulse.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The sampled Gaussian pulse.
        If no flat time is passed then the pulse is evenly sampled between :math:`0` and :math:`T`.
        If one is passed, the flat part of the pulse is described by one or two segments (depending
        on the values of `center` and `segment_count`),
        and the rest of the pulse is evenly sampled with the remaining segments.

    Notes
    -----
        The Gaussian pulse is defined as

        .. math:: \mathop{\mathrm{Gaussian}}(t) =
           \begin{cases}
                A \left(1-\frac{i\beta (t-t_1)}{\sigma^2}\right)
                \exp \left(- \frac{(t-t_1)^2}{2\sigma^2} \right)
                    &\mathrm{if} \quad t < t_1=t_0- t_\mathrm{flat}/2\\
                A
                    &\mathrm{if} \quad t_0-t_\mathrm{flat}/2 \le t < t_0+t_\mathrm{flat}/2 \\
                A \left(1-\frac{i\beta (t-t_2)}{\sigma^2}\right)
                \exp \left(- \frac{(t-t_2)^2}{2\sigma^2} \right)
                    &\mathrm{if} \quad t > t_2=t_0+t_\mathrm{flat}/2
            \end{cases}\; ,

        where :math:`A` is the amplitude, :math:`\beta` is the DRAG parameter,
        :math:`t_0` is the center of the pulse, :math:`\sigma` is the width of the pulse and
        :math:`t_\mathrm{flat}` is the flat time.

        If the flat time is zero (the default setting), this reduces to

        .. math:: \mathop{\mathrm{Gaussian}}(t) =
            A \left(1-\frac{i\beta (t-t_0)}{\sigma^2}\right)
            \exp \left(- \frac{(t-t_0)^2}{2\sigma^2} \right) \; .

    Examples
    --------

    Define a Gaussian PWC pulse.

    >>> graph.pulses.gaussian_pulse_pwc(
    ...     duration=3.0,
    ...     segment_count=100,
    ...     amplitude=1.0,
    ...     name="gaussian",
    ... )
    <Pwc: name="gaussian", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["gaussian"])
    >>> result.output["gaussian"]
    [
        {'duration': 0.03, 'value': 4.7791e-06},
        {'duration': 0.03, 'value': 7.8010e-06},
        ...
        {'duration': 0.03, 'value': 7.8010e-06},
        {'duration': 0.03, 'value': 4.7791e-06}
    ]

    Define a flat-top Gaussian PWC pulse with a DRAG correction.

    >>> graph.pulses.gaussian_pulse_pwc(
    ...     duration=3.0,
    ...     segment_count=100,
    ...     amplitude=1.0,
    ...     width=0.2,
    ...     center=1.5,
    ...     drag=0.1,
    ...     flat_time=0.2,
    ...     name="gaussian",
    ... )
    <Pwc: name="gaussian", operation_name="time_concatenate_pwc", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(graph=graph, output_node_names=["gaussian"])
    >>> result.output["gaussian"]
    [
        {'duration': 0.0285, 'value': (3.7655e-11+1.3044e-10j)},
        {'duration': 0.0285, 'value': (1.0028e-10+3.4026e-10j)},
        ...
        {'duration': 0.0285, 'value': (1.0028e-10-3.4026e-10j)},
        {'duration': 0.0285, 'value': (3.7655e-11-1.3044e-10j)}
    ]

    Define a Gaussian pulse with optimizable parameters.

    >>> amplitude = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=2.*np.pi, name="amplitude"
    ... )
    >>> width = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=2., name="width"
    ... )
    >>> drag = graph.optimization_variable(
    ...     count=1, lower_bound=0, upper_bound=1., name="drag"
    ... )
    >>> graph.pulses.gaussian_pulse_pwc(
    ...     duration=3.0,
    ...     segment_count=100,
    ...     amplitude=amplitude,
    ...     width=width,
    ...     drag=drag,
    ...     name="gaussian",
    ... )
    <Pwc: name="gaussian", operation_name="discretize_stf", value_shape=(), batch_shape=()>
    """

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )

    if center is None:
        center = 0.5 * duration

    if width is None:
        if flat_time is None:
            width = duration / 10
        else:
            width = (duration - flat_time) / 10

    amplitude = _validate_optimizable_parameter(graph, amplitude, "amplitude")
    width = _validate_optimizable_parameter(graph, width, "width")

    def create_gaussian(center_parameter):
        return graph.exp(
            -((graph.identity_stf() - center_parameter) ** 2) / (2 * width**2)
        )

    def create_amplitude(center_parameter):
        if drag is None:
            return amplitude
        return amplitude * (
            1.0 - 1j * drag * (graph.identity_stf() - center_parameter) / (width**2)
        )

    if drag is not None:
        drag = _validate_optimizable_parameter(graph, drag, "drag")

    if flat_time is None:
        return graph.discretize_stf(
            create_amplitude(center) * create_gaussian(center),
            duration,
            segment_count,
            name=name,
        )

    check_argument(
        0.0 < flat_time < duration,
        "The flat time must be positive and less than the duration.",
        {"flat_time": flat_time},
        extras={"duration": duration},
    )

    flat_time_begin = center - 0.5 * flat_time  # Time at which first Gaussian ends.
    flat_time_end = center + 0.5 * flat_time  # Time at which second Gaussian begins.

    if flat_time_begin >= duration:
        # In this case since the flat segment starts after the duration, it is not part of
        # the signal.
        return graph.discretize_stf(
            create_amplitude(flat_time_begin) * create_gaussian(flat_time_begin),
            duration,
            segment_count,
            name=name,
        )

    if flat_time_end <= 0:
        # In this case since the flat segment finishes before time zero, it is not part of
        # the signal.
        return graph.discretize_stf(
            create_amplitude(flat_time_end) * create_gaussian(flat_time_end),
            duration,
            segment_count,
            name=name,
        )

    if flat_time_end >= duration:
        # In this case since the flat segment finishes after the duration, the second Gaussian
        # is not part of the signal.
        durations = [flat_time_begin, duration - flat_time_begin]
        segment_counts = [segment_count - 1, 1]
        stfs = [
            create_amplitude(flat_time_begin) * create_gaussian(flat_time_begin),
            graph.constant_stf(amplitude),
        ]

    elif flat_time_begin <= 0:
        # In this case since the flat segment begins before time zero, the first Gaussian
        # is not part of the signal.
        durations = [flat_time_end, duration - flat_time_end]
        segment_counts = [1, segment_count - 1]
        stfs = [
            graph.constant_stf(amplitude),
            create_amplitude(0.0) * create_gaussian(0.0),
        ]

    else:
        # In this case, the number of segments each Gaussian part has is in proportion to their
        # duration of time.
        durations = [flat_time_begin, flat_time, duration - flat_time_end]
        gaussian_time = duration - flat_time
        segment_counts = [
            int((segment_count - 1) * durations[0] / gaussian_time),
            0,
            int((segment_count - 1) * durations[2] / gaussian_time),
        ]
        # The constant part of the signal will either have one or two segments.
        segment_counts[1] = segment_count - segment_counts[0] - segment_counts[2]

        stfs = [
            create_amplitude(flat_time_begin) * create_gaussian(flat_time_begin),
            graph.constant_stf(amplitude),
            create_amplitude(0.0) * create_gaussian(0.0),
        ]

    pwcs = [
        graph.discretize_stf(*args) for args in zip(stfs, durations, segment_counts)
    ]
    return graph.time_concatenate_pwc(pwcs, name=name)


@expose(Namespace.PULSES)
def hann_series_pwc(
    graph: Graph,
    duration: float,
    segment_count: int,
    coefficients: Union[np.ndarray, Tensor],
    name: Optional[str] = None,
) -> Pwc:
    r"""
    Creates a sum of Hann window functions.

    The piecewise-constant function is sampled from Hann functions that start and end at zero.

    Parameters
    ----------
    graph : Graph
        The graph object where the node will belong.
    duration : float
        The duration of the signal, :math:`T`.
    segment_count : int
        The number of segments in the PWC.
    coefficients : np.ndarray or Tensor
        The coefficients for the different Hann window functions, :math:`c_n`.
        It must be a 1D array or Tensor and it can't contain more than `segment_count` elements.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc
        The sampled Hann window functions series.

    Notes
    -----

    The series is defined as

        .. math::`\mathop{\mathrm{Hann}}(t)
            = \sum_{n=1}^N c_n \sin^2 \left( \frac{\pi n t}{T} \right) \; ,`

    where :math:`c_n` are the coefficients for the different terms,
    :math:`N` is the number of coefficients,
    and :math:`T` is the PWC duration.

    Examples
    --------

    Define a simple Hann series.

    >>> graph.pulses.hann_series_pwc(
    ...     duration=5.0,
    ...     segment_count=50,
    ...     coefficients=np.array([0.5, 1, 0.25]),
    ...     name="hann_series",
    ... )
    <Pwc: name="hann_series", operation_name="pwc_signal", value_shape=(), batch_shape=()>
    >>> result = qctrl.functions.calculate_graph(
    ...     graph=graph, output_node_names=["hann_series"]
    ... )
    >>> result.output["hann_series"]
    [
        {'value': 0.0067, 'duration': 0.1},
        {'value': 0.0590, 'duration': 0.1},
        ...
        {'value': 0.0590, 'duration': 0.1},
        {'value': 0.0067, 'duration': 0.1},
    ]

    Define a Hann series with optimizable coefficients.

    >>> coefficients = graph.optimization_variable(
    ...     count=8, lower_bound=-3.5e6, upper_bound=3.5e6, name="coefficients"
    ... )
    >>> graph.pulses.hann_series_pwc(
    ...     duration=2.0e-6,
    ...     segment_count=128,
    ...     coefficients=coefficients,
    ...     name="hann_series",
    ... )
    <Pwc: name="hann_series", operation_name="pwc_signal", value_shape=(), batch_shape=()>
    """

    check_argument(
        duration > 0.0, "The duration must be positive.", {"duration": duration}
    )

    check_argument(
        len(coefficients.shape) == 1,
        "The coefficients must be in a 1D array or Tensor.",
        {"coefficients": coefficients},
        extras={"coefficients.shape": coefficients.shape},
    )

    check_argument(
        coefficients.shape[0] <= segment_count,
        "There can't be more coefficients than segments.",
        {"coefficients": coefficients, "segment_count": segment_count},
        extras={"coefficients.shape": coefficients.shape},
    )

    # Define scaled times π t / T to sample the function.
    times, time_step = np.linspace(
        0, duration, segment_count, endpoint=False, retstep=True
    )
    scaled_times = (times + time_step / 2) * np.pi / duration

    # Calculate function values.
    nss = np.arange(1, coefficients.shape[0] + 1)
    values = graph.sum(coefficients * np.sin(nss * scaled_times[:, None]) ** 2, axis=1)

    return graph.pwc_signal(duration=duration, values=values, name=name)
