# Self-driving-car
Self-driving car using MobileNetV3-Large

## Introduction
Current self-driving cars rely on sensors, complex decision-making algorithms, deep neural networks(DNN) and powerful processors to achieve their intent. Cars make use of various sensors like lidar, radar, camera, ultrasonic sensor, etc to map their surroundings. The software onboard then does motion planning, obstacle avoidance, lane keeping, and traffic signal recognition and takes over the wheel to steer, accelerate and brake accordingly. In this project, we take the first step towards solving the problem of self-driving by developing a DNN. To keep this simple, here we train a DNN to determine the steering angle and speed.

## Dataset description
The MLiS-II dataset consisted of 13.8k images, collected by driving this car manually around 3 different tracks, were provided to us. The images were of dimensions 320x240 pixels. The labels of the images included the steering angle and the speed. For simplicity, speed takes only binary values- ’go’: 1, ’stop’: 0. Both steering angle and speed were normalized to values between 0 and 1 according to the equations as follows: 

    anglenorm = (angle−50) / 80 
    speednorm = (speed−0) / 35 
                                                                    
On top of this, we collected 1.3k more images to collect more data on left turns, traffic signal response and on the 8-shaped track.

## Implementation
Usually, a common start to a problem like this would be to look for the right model small enough to run within the constraint time and big enough to learn the underlying pattern and not just overfit. We ended up choosing Google’s MobileNetV3-Large for this reason. We decided to go with 2 models: one for speed and one for angle. SpeedNet: for speed classification and AngleNet: for angle prediction. As speed is binary, a binary classification model would work. On the other hand, angle takes values between 0 and 1. This makes it a regression problem. To increase the training data and to increase the robustness of the model, the training data was augmented. The four types of augmentation performed included: randomizing contrast, saturation and brightness and addition of random noise. This augmented image has to be clipped into the range of 0 to 255 because MobileNetV3-Large has been trained on RGB images with pixels values ranging from 0 to 255. We removed the last 10 layers of MobileNetV3-Large and a dropout layer, a convolution layer, and 2 dense layers followed by the output layer with the appropriate number of output nodes depending on the network. For training each of the three models, we froze every layer from first to last but the 44th layer and trained the rest. 

## Results
The SpeedNet had a training 7 accuracy of 99.97% and a validation accuracy of 98.83%. The AngleNet had a training loss of 0.0011 and a validation loss of 0.011. As our normal TensorFlow model had a latency of 2s, we converted it to a Tensorflow Lite model. This conversion reduced the inference time to 300ms. Our model was able to complete the oval and 8-shaped tracks. It was able to stop when a pedestrian is on the left lane of the road, pass by pedestrians if it's not on the left lane of the road, stop at the red signal, and continue to drive at the green signal. Due to the low inference time, our car was able to complete the oval track with a speed of 50. The car was able to do a partial right turn at the right arrow junction. Although, it failed a couple of tasks: Stopping for an obstacle on the road and taking a left turn at the left arrow junction.

## Future improvements
As the model failed in detecting a left arrow traffic symbol, we could increase the number of left arrow traffic symbol photos in the dataset. Instead of having 2 networks, one could also go for a 4 network model where the 2 extra networks take care of signals(red or green) and arrow traffic symbols. This would enable the model to overcome both the problems encountered during the testing phase. As our model has 2 networks trained through transfer learning, the first 44 layers have the same weights. Hence, these can be shared by both the networks, thereby reducing the number of weights, computations and latency. 
