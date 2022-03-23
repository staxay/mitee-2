# Attitude Determination Code for MiTEE-2

### Written by: Sam Taxay
### Adapted from [MiTEE-1 OADCS Code](https://gitlab.eecs.umich.edu/mitee-oadcs/attitude-determination-for-mitee-1/-/tree/main/) and Brian Leung's [QUEST Algorithm](https://github.com/bleung329/py_QUEST)
### [Visit MiTEE's website for more details!](https://clasp-research.engin.umich.edu/groups/s3fl/mitee/home/)
## What is this?

Before being implemented into the OADCS microcontroller onboard the MiTEE-2 satellite, the OADCS sub-team uses code like this to determine the attitude of MiTEE-2 while in space.

| File                   | Description                                                                                                |
|------------------------|------------------------------------------------------------------------------------------------------------|
| `quest.py`             | Implements QUEST algorithm and driver for code                                                             |
| `gps_snr.py`           | Reads GPS data and transforms values into antenna boresight vector                                         |
| `mag_field.py`         | Reads magnetometer data and transforms values into inertial vector (Note: **Not completed**)               |
| `eig_helper.py`        | Makes characteristic equation calculations more organized                                                  |
| `sun_vector_approx.py` | Reads photodiode voltage data and transforms values into inertial vector (Note: **Used only for testing**) |
| `test.py`              | Unit tests for `quest.py`                                                                                  |
| `test_data.txt`        | GPS reciever test data                                                                                     |

## Why does MiTEE-2 have different code than MiTEE-1?

While MiTEE-1 had well written code, MiTEE-2 uses a new method of attitude determination called QUEST rather than TRIAD, which was what MiTEE-1 used. 

## What is QUEST?

QUEST is an algorithm used to determine the attitude of a spacecraft. It is fairly simple, which is why we chose to implement it on MiTEE-2.

## Why is this being written?

To be updated

