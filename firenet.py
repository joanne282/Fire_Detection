from imageai.Detection.Custom import CustomObjectDetection, CustomVideoObjectDetection
import os
import cv2


detector = None
execution_path = os.getcwd()


def load():
    # construct and display model
    global detector

    detector = CustomVideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
    detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
    detector.loadModel()


def get_frame(path):
    interval = 1

    if path.isdecimal():
        gen_frame = detector.detectObjectsFromVideo(
            camera_input = cv2.VideoCapture(int(path)),
            frames_per_second=1,
            frame_detection_interval=interval,
            minimum_percentage_probability=1,)
            # log_progress=True)
    else:
        gen_frame = detector.detectObjectsFromVideo(
            input_file_path=os.path.join(execution_path, path),
            frames_per_second=1,
            frame_detection_interval=interval,
            minimum_percentage_probability=1,)
            # log_progress=True)

    for frame in gen_frame:
        yield frame
