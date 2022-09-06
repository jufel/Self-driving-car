import numpy as np
import tensorflow as tf
import os
import cv2
class Model:

    speed_model = 'speed_model.tflite'
    angle_model = 'angle_model.tflite'
    signal_model = 'signal_model.tflite'

    def __init__(self):
        self.speed_interpreter = tf.lite.Interpreter(model_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                             self.speed_model))
        self.angle_interpreter = tf.lite.Interpreter(model_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                             self.angle_model))
        self.signal_interpreter = tf.lite.Interpreter(model_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                             self.signal_model))
        self.speed_interpreter.allocate_tensors()
        self.angle_interpreter.allocate_tensors()
        self.signal_interpreter.allocate_tensors()
        
        self.speed_input_details = self.speed_interpreter.get_input_details()
        self.speed_output_details = self.speed_interpreter.get_output_details()
        
        self.angle_input_details = self.angle_interpreter.get_input_details()
        self.angle_output_details = self.angle_interpreter.get_output_details()

        self.signal_input_details = self.signal_interpreter.get_input_details()
        self.signal_output_details = self.signal_interpreter.get_output_details()
        
        self.floating_model = self.speed_input_details[0]['dtype'] == np.float32         # check the type of the input tensor

    def preprocess(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = tf.image.resize(img,(224, 224))
        img = tf.reshape(img,(1,224,224,3))
        img = tf.cast(img, tf.float32)
        return img

    def predict(self, image):
        image = self.preprocess(image)

        self.speed_interpreter.set_tensor(self.speed_input_details[0]['index'], image)
        self.angle_interpreter.set_tensor(self.angle_input_details[0]['index'], image)
        self.signal_interpreter.set_tensor(self.signal_input_details[0]['index'], image)

        self.speed_interpreter.invoke()
        self.angle_interpreter.invoke()
        self.signal_interpreter.invoke()

        speed_value = self.speed_interpreter.get_tensor(self.speed_output_details[0]['index'])[0][0]
        angle_value = self.angle_interpreter.get_tensor(self.angle_output_details[0]['index'])[0][0]
        signal_value = self.signal_interpreter.get_tensor(self.signal_output_details[0]['index'])[0]
        
        if max(signal_value) != signal_value[0]:
            if abs(signal_value[1]-signal_value[2]) > 0.1:
                if signal_value[1] > signal_value[2]:
                    speed = 1
                else:
                    speed = 0
            else:
                speed = speed_value
        else:
            speed = speed_value
        if abs((1 - speed)) < abs((0-speed)):
            speed = 30
        else:
            speed = 0
        angle = angle_value * 80 + 50
        angle = 5 * round(angle/5)
        if angle < 50:
            angle = 50
        if angle > 130:
            angle = 130
            
        print("angle :", angle , "speed" , speed)
        
        return angle, speed