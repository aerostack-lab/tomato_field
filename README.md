# Application: tower_inspection_gazebo

This application illustrates how a drone inspects a each floor of a tower. During the mission execution, it is possible to pause and continue the mission execution. While the mission is executing, the drones explores and saves the map of every floor that has been explored.

In order to execute the mission, perform the following steps:

- Execute the script that launches Gazebo for this project:

        $ ./launcher_gazebo.sh

- Wait until the following window is presented:

<img src="https://github.com/aerostack/tower_inspection_gazebo/blob/master/doc/towerlaunch.png" width=600>

- Execute the script that launches the Aerostack components for this project:

        $ ./main_launcher.sh

As a result of this command, a set of windows are presented to monitor the execution of the mission. These windows include:
- Belief viewer
- Lidar mapping

In order to start the execution of the mission, execute the following commands:

	$ rosservice call /drone111/python_based_mission_interpreter_process/start

The following video illustrates how to launch the project:

[ ![Launch](https://i.ibb.co/W6VYpD7/towerlaunch2.png)](https://youtu.be/aySFEPMCUPA)

The following video shows the complete execution:

[ ![Execution](https://i.ibb.co/RhKBQZV/towerexe.png)](https://youtu.be/pHfRGtLMTms)


