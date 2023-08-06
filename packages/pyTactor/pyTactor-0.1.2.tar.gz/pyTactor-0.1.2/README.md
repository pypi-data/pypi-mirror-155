# pyTactor

### Parties Involved
Institution: Munroe Meyer Institute in the University of Nebraska Medical Center<br>
Laboratory: Virtual Reality Laboratory<br>
Advisor: Dr. James Gehringer<br>
Developer: Walker Arce<br>

### Motivation
This Python library was written to facilitate closed-loop experimental protocol for biomechanics and motor-control related research.

### Installation
Clone this repository, cd into the directory using either your virtual environment or your local environment, and run:
`python setup.py install`

### Usage
```
import time
from pytactor import VibrotactorArray

ble = VibrotactorArray.get_ble_instance()
vta_1 = VibrotactorArray(ble)
vta_2 = VibrotactorArray(ble)

vta_1.set_all_motors(200)
vta_1.trigger_vib()
vta_1.start_imu()

vta_2.set_all_motors(200)
vta_2.trigger_vib()
vta_2.start_imu()

time.sleep(10)
```

### Citation
```
@misc{Arce_pyTactor_2022,
      author = {Arce, Walker and Gehringer, James},
      month = {6},
      title = {{pyTactor}},
      url = {https://github.com/Munroe-Meyer-Institute-VR-Laboratory/pyTactor},
      year = {2022}
}
```
