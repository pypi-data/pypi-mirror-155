*****
Kobukidriver
*****
|version| 

Kobukidriver is a python driver for Kobuki quanser qbot2 which helps in control and utilization of the mobile robot.You can build numerous application with the help of the driver.

Links
=====

- Project: https://github.com/jaxram/kobuki
- PyPi: https://pypi.org/project/kobukidriver/

Quickstart
==========

Install using pip:


::

    pip install kobukidriver

  

kobukidriver works in both windows and linux

Features
--------

- Develop any mobile robot applications 
- Gyro sensor data
- Docking IR data
- Inertial sensor data
- Cliff sensor data
- current data
- general purpose input data
- Basic sensor data
- Set/Clear LED
- Set digital output pin
- Control mobile robot speed
- Play inbuilt/custom sounds 

Examples
--------

Get started by importing the ``Kobuki`` class:

.. code-block:: python

    #import the kobuki class
    from kobukidriver import Kobuki
    #create the instance for the kobuki
    kobuki_instance=Kobuki()#raise error if kobuki is not connected

Example code for reading basic sensor data from Kobuki robot

.. code-block:: python

    from kobukidriver import Kobuki
    import time as t
    kobuki_instance=Kobuki()
   
    while(1):
        t.sleep(0.2)#delay for fetching data
        basic_sensor_data=kobuki_instance.basic_sensor_data()
        print(basic_sensor_data)#prints the basic sensor data from the robot
    
Steps for building the mobile robot application using the driver

.. code-block:: python

    from kobukidriver import Kobuki
    kobuki_instance=Kobuki()
    #Don't change the start function name
    def start():
        while(1):
            #your logic
    kobuki_instance.kobukistart(start)
