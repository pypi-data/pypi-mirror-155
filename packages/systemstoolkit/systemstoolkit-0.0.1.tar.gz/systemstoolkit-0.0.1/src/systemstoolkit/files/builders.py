import datetime
import numpy as np

from .files import AttitudeFile
from .formats import AttitudeFileFormat
from .keywords import (
    MessageLevel,
    Coordinate,
    CoordinateAxes,
    CoordinateAxesEpoch,
    ScenarioEpoch,
    CentralBody,
    Interpolation,
    InterpolationMethod,
    InterpolationOrder,
    AttitudeDeviations,
    BlockingFactor,
)


def attitude_file(
    time: np.ndarray,
    data: np.ndarray,
    format: str = None,
    epoch: datetime.datetime = None,
    axes: str = None,
    axes_epoch: datetime.datetime = None,
    message: str = 'Warnings',
    body: str = None,
    int_method: str = None,
    int_order: int = None,
    deviations: str = None,
    blocking: int = None,
) -> str:
    '''Create an STK Attitude (.a) file.
    
    Params
    ------
    time: np.ndarray[np.datetime64]

    data: np.ndarray[][]

    format: str
        The file formats used to specify data points in the attitude file.
        (i.e. "AttitudeTimeQuaternions" keyword for Quaternions)

        Quaternion-based formats
            Quaternions
            QuatScalarFirst
            QuatAngVels
            AngVels
        Euler-based Formats
            EulerAngles
            EulerAngleRates
            EulerAnglesAndRates
        YPR-based formats
            YPRAngles
            YPRAngleRates
            YPRAnglesAndRates
        DCM-based formats
            DCM
            DCMAngVels
        Vector-based formats
            ECFVector
            ECIVector
    
    epoch: datetime.datetime
        ScenarioEpoch. This is the reference epoch time for the time values of the attitude data in the file. 
        
        There is no relationship between ScenarioEpoch and the scenario epoch in your STK scenario.
        
        The default is the time in time[0].
    
    axes: str
        CoordinateAxes. AGI recommends that you supply these, but they are not required.

        These are the reference axes from which the rotation to the body axes is performed. Normally, the coordinate axes is the name of a valid coordinate system for the central body specified above (see Central Body Coordinate Systems). Typically, each central body supports Fixed, J2000, ICRF, Inertial, TrueOfDate, and MeanOfDate, but some bodies support additional systems.

        The default Coordinate Axes is Inertial, which is ICRF for Earth and Sun.

    axes_epoch: datetime.datetime
        CoordinateAxesEpoch. This is the epoch time for the coordinate axes.

        This parameter is required with coordinate axes that reference an epoch:
            MeanOfEpoch
            TrueOfEpoch
            TEMEOfEpoch
            AlignmentAtEpoch
    
    message: str
        MessageLevel. You can set this value to determine the level of message(s) you receive from STK as it attempts to read the file. The value options are:

            Errors - You only receive the reported error messages.
            Warnings - You receive error messages plus reporting on other information (e.g., unrecognized keywords).
            Verbose - You receive all that is in Warnings plus a success message if STK reads and accepts the complete file.

    body: str
        CentralBody. This is the central body that the attitude points are relative to. The keyword value that completes the phrase can be the name of any registered central body. You can find registered central bodies in the STKData\CentralBodies directory.

        The default is the central body for the vehicle, and that default is Earth.

    int_method: str
        InterpolationMethod. This is the method by which STK interpolates between attitude points. Valid values are:

            Lagrange (Default)
            Hermite - This option enables you to take advantage of angular velocity information to achieve smoother attitude interpolation. One application is if you are using files containing very irregularly spaced data points. Another is if you have data representing a spinning attitude that is susceptible to ringing and aliasing effects if derivative information is not considered during interpolation. Hermitian interpolation assumes that the velocity component of the attitude is the derivative of the position. Hermitian interpolation should not be used when velocity data is not available as part of the attitude file.

    int_order: int
        InterpolationOrder. This is the order of interpolation that STK will use. You can override the default by specifying a different interpolation order. This parameter is often used with the AttitudeLLATimePos attitude format.

        The default is 1.

    Returns
    -------
    a_file: str
        The Attitude File text as a string.
    '''


    format = AttitudeFileFormat(format)
    if message:
        message = MessageLevel(message)

    if axes:
        coord = CoordinateAxes(axes)
        if axes_epoch:
            axes_epoch = CoordinateAxesEpoch(axes_epoch)
        axes = Coordinate(axes=coord, epoch=axes_epoch)

    if epoch:
        epoch = ScenarioEpoch(epoch)

    if body:
        body = CentralBody(body)

    if int_method:
        int_method = InterpolationMethod(int_method)

    if int_order:
        int_order = InterpolationOrder(int_order)

    interpolation = Interpolation(method=int_method, order=int_order)

    if deviations:
        deviations = AttitudeDeviations(deviations)
    
    if blocking:
        blocking = BlockingFactor(blocking)

    a_file = AttitudeFile(
        time,
        data,
        format=format,
        axes=axes,
        epoch=epoch,
        message=message,
        body=body,
        interp=interpolation,
        deviations=deviations,
        blocking=blocking,
    )

    return a_file.to_string()
