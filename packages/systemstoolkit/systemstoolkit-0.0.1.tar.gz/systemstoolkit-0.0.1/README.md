# systemstoolkit

## Create an Attitude File

```python
In [1]: import systemstoolkit as stk
In [2]: import numpy as np
In [3]: time = np.datetime64("2020-01-02 03:04:05") + np.arange(10).astype("timedelta64[s]")
In [4]: time
Out[4]:
array(['2020-01-02T03:04:05', '2020-01-02T03:04:06',
       '2020-01-02T03:04:07', '2020-01-02T03:04:08',
       '2020-01-02T03:04:09', '2020-01-02T03:04:10',
       '2020-01-02T03:04:11', '2020-01-02T03:04:12',
       '2020-01-02T03:04:13', '2020-01-02T03:04:14'],
      dtype='datetime64[s]')
In [5]: data = np.array([[0,10,20]]*10, dtype='float32')
In [6]: data
Out[6]:
array([[ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.],
       [ 0., 10., 20.]], dtype=float32)
In [7]: afile = stk.attitude_file(time[0:10], data[0:10], "YPRAngles")
In [8]: print(afile)
stk.v.11.0
BEGIN Attitude
ScenarioEpoch                  02 Jan 2020 03:04:05.000
MessageLevel                   Warnings

TimeFormat                     EpSec

AttitudeTimeYPRAngles
            0.0        0.000000       10.000000       20.000000
            1.0        0.000000       10.000000       20.000000
            2.0        0.000000       10.000000       20.000000
            3.0        0.000000       10.000000       20.000000
            4.0        0.000000       10.000000       20.000000
            5.0        0.000000       10.000000       20.000000
            6.0        0.000000       10.000000       20.000000
            7.0        0.000000       10.000000       20.000000
            8.0        0.000000       10.000000       20.000000
            9.0        0.000000       10.000000       20.000000

END Attitude
```
