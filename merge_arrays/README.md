# Wisconsin Autonomous ROS Coding Challenge

This coding challenge is designed for us to evaluate what you can bring to the table and an opportunity for you to get some hands on experience with the tools we use in the team. We use ROS2 Humble as our middleware for our modular system to communicate with each other. A good understanding of ROS is vital for our success. While we understand that this might be your first time using ROS, this challenge also aims for us to see how you can learn on the fly, which is an important aspect of being part of this team.  

## Challenge Descrpiption

Please design a node `merge_arrays_node` in a package `merge_arrays`. The specification on the node is as following:  
You will be given two ROS topics to subscribe to:  

- `/input/array1`
    - Type: `std_msgs/Int32MultiArray`
    - Content: an array of sorted `Int32`

- `/input/array2`
    - Type: `std_msgs/Int32MultiArray`
    - Content: an array of sorted `Int32`

Your node will take in these two arrays and create a merged sorted array. This merged sorted array will be published to ROS topic `/output/array`. The type will also be `std_msgs/Int32MultiArray`.  

Example: given `[1 4 8 12 26]` and `[3 9 18 20 30]`, you node should publish `[1 3 4 8 9 12 18 20 26 30]`. If nothing is making sense dont worry, there are helpful links below to help you understand the lingo.

## Submission Specificaion
- You node should be written in either Matlab, Python, or C++.
- The package name should be `merge_arrays` and node should be called `merge_arrays_node`.
- Your node will be evaluated by an automated system with `ros2 run merge_arrays merge_arrays_node`.
- You are not allowed to use non-ROS dependencies for this challenge.
- Please upload the full package in the correct folder structure to a public github repository for us to review.  



## Tips

1. You are allowed to use any resources available to you. Google is your friend!
2. [ROS2 Humble documentation](https://docs.ros.org/en/foxy/Releases/Release-Humble-Hawksbill.html) is a great place to start if you are new to ROS. This [page](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html) walks you throug how to create a publisher and subscriber node in c++, this [page](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html) for python
3. Ubuntu 22.04 is required for ROS2 Humble. You will need to set up dual boot, or use Docker, or WSL. We use Ubuntu 22.04 for all our code so might be a good idea to start getting familiar with it.
4. The learning curve can be steep here! We don't want you to get stuck! Feel free to ask questions in slack.

