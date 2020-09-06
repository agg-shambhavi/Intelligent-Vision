# importing the libraries
import cv2
import matplotlib.pyplot as plt
import face_recognition
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import os
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

''' The ResizeUtils provides resizing function to keep the aspect ratio intact'''


class ResizeUtils:
    # Given a target height, adjust the image
    # by calculating the width and resize
    def rescale_by_height(self, image, target_height, method=cv2.INTER_LANCZOS4):
        # Rescale `image` to `target_height`
        # (preserving aspect ratio)
        w = int(round(target_height * image.shape[1] / image.shape[0]))
        return (cv2.resize(image, (w, target_height), interpolation=method))

        # Given a target width, adjust the image

    # by calculating the height and resize
    def rescale_by_width(self, image, target_width, method=cv2.INTER_LANCZOS4):
        # Rescale `image` to `target_width`
        # (preserving aspect ratio)
        h = int(round(target_width * image.shape[0] / image.shape[1]))
        return (cv2.resize(image, (target_width, h), interpolation=method))


'''To resize the frame images obtained from the video'''


class FramesResizing:
    # Resize the given input to fit in a specified
    def AutoResize(self, frame):
        resizeUtils = ResizeUtils()
        height, width, _ = frame.shape
        if height > 500:
            frame = resizeUtils.rescale_by_height(frame, 500)
            self.AutoResize(frame)
        if width > 700:
            frame = resizeUtils.rescale_by_width(frame, 700)
            self.AutoResize(frame)

        return frame


''' generate frames from a video'''


class FrameGenerator:
    # Function that will genearte frames from video file source
    # vid_fp is the parameter to passed which is the path to file sorce
    def GenerateFrames(self, vid_fp):
        cap = cv2.VideoCapture(vid_fp)
        _, frame = cap.read()

        fps = cap.get(cv2.CAP_PROP_FPS)
        TotalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        print("[INFO] Total Frames ", TotalFrames, " @ ", fps, " fps")
        print("[INFO] Calculating number of frames per second")

        autosize = FramesResizing()

        output_list = []

        CurrentFrame = 1
        fpsCounter = 0
        FrameWrittenCount = 1
        while CurrentFrame < TotalFrames:
            _, frame = cap.read()
            if (frame is None):
                continue

            if fpsCounter > fps:
                fpsCounter = 0
                autosize = FramesResizing()
                frame = autosize.AutoResize(frame)

                filename = "frame_" + str(FrameWrittenCount) + ".jpg"
                filepath = os.path.join(
                    'intelligent_vision V1.0\Frames_dir', filename)
                cv2.imwrite(filepath, frame)
                timestamp = cap.get(propId=0)
                output_dict = {
                    'filepath': filepath, 'frame_number': FrameWrittenCount, 'timestamp': timestamp}
                output_list.append(output_dict)
                FrameWrittenCount += 1

            fpsCounter += 1
            CurrentFrame += 1

        print('[INFO] Frames extracted')
        return output_list


''' detect face from frame list and returns a list of detected faces'''


class DetectFaces:
    # Function detects faces from the list of frames
    # parameter - frame_list, which is list of frames
    def face_detector(self, frame_list):
        output_list = []
        for frame_dict in frame_list:
            imagepath = frame_dict['filepath']
            image = cv2.cvtColor(cv2.imread(imagepath), cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(image, model='cnn')
            if len(boxes) != 0:
                encodings = face_recognition.face_encodings(
                    image, boxes, model='large')
                for box in boxes:
                    output_subdict = {'timestamp': frame_dict['timestamp'],
                                      'filepath': frame_dict['filepath'],
                                      'frame_number': frame_dict['frame_number'],
                                      'box_loc': box,
                                      'encodings': encodings[0]}
                    output_list.append(output_subdict)
        return output_list


class DataFrameUtils:
    # Function to create pandas dataframe of a list which has dictionaries
    def createDataFrame(self, input_list):
        df = pd.DataFrame(input_list)
        print("[INFO] The shape of df is {}".format(df.shape))
        return df


class ImageReaderEncoder:
    def __init__(self, image_fp):
        self.image_fp = image_fp

    def image_read_encode(self):
        read_img = plt.imread(self.image_fp)
        img_encoding = pd.DataFrame(
            face_recognition.face_encodings(read_img, model='large'))
        return img_encoding


class dbscan_clustering:
    def db_cluster(self, derived_df):
        dbscan_model = DBSCAN(eps=0.4, metric="euclidean").fit(derived_df)
        print("[INFO] Number of unique clusters {}".format(
            len(np.where((np.unique(dbscan_model.labels_)) > -1)[0])))
        return dbscan_model.labels_


class TrainSVM:
    def __init__(self, derived_df, labels_of_dbscan, image_enc):
        self.derived_df = derived_df
        self.labels_of_dbscan = labels_of_dbscan
        self.image_enc = image_enc

    def prepare_dataset(self):
        x_train = self.derived_df
        y_train = np.array(self.labels_of_dbscan)
        out_encoder = LabelEncoder()
        out_encoder.fit(y_train)
        y_train = out_encoder.transform(y_train)
        return x_train, y_train

    def fit_model(self):
        svm_dbscan = SVC(kernel='linear', probability=True)
        x_train, y_train = self.prepare_dataset()
        svm_dbscan.fit(x_train, y_train)
        yhat_train = svm_dbscan.predict(x_train)
        score_train = accuracy_score(y_train, yhat_train)
        print("[INFO] Accuracy of SVM Classifier is {}".format(score_train))
        return svm_dbscan

    def predict_img_cluster(self):
        svm_dbscan = self.fit_model()
        return svm_dbscan.predict(self.image_enc)[0]


class Retrieve_instances:
    def __init__(self, y_train_lbl, detected_faces_list, predicted_cluster_number):
        self.y_train_lbl = y_train_lbl
        self.detected_faces_list = detected_faces_list
        self.predicted_cluster_number = predicted_cluster_number

    def back_mapping(self):
        back_mapping = []
        for y_lbl, frame_dict in zip(self.y_train_lbl, self.detected_faces_list):
            time_min = int(frame_dict['frame_number']) // 60
            time_sec = int(frame_dict['frame_number']) % 60
            final_dict = {'timestamp': frame_dict['timestamp'],
                          'filepath': frame_dict['filepath'],
                          'frame_number': frame_dict['frame_number'],
                          'box_loc': frame_dict['box_loc'],
                          'encodings': frame_dict['encodings'],
                          'labels': y_lbl,
                          'time_in_min': str(time_min) + ":" + str(time_sec)}
            back_mapping.append(final_dict)
        Mapping_df = pd.DataFrame(back_mapping)
        return Mapping_df

    def df_to_retrieve(self):
        Mapping_df = self.back_mapping()
        cluster_df = Mapping_df[Mapping_df['labels'] == self.predicted_cluster_number].loc[:,
                                                                                           ['time_in_min', 'filepath']]
        return cluster_df


class img_to_vid_match:
    def __init__(self, image_fp, video_fp):
        self.image_fp = image_fp
        self.video_fp = video_fp

    def Final_Match(self):
        generate_frames_list = FrameGenerator().GenerateFrames(self.video_fp)
        detected_faces_list = DetectFaces().face_detector(generate_frames_list)
        full_dataset = DataFrameUtils().createDataFrame(detected_faces_list)
        encodings_datframe = pd.DataFrame(full_dataset.encodings.to_list())
        image_encoding = ImageReaderEncoder(self.image_fp).image_read_encode()
        dbscan_labels = dbscan_clustering().db_cluster(encodings_datframe)
        svm = TrainSVM(encodings_datframe, dbscan_labels, image_encoding)
        _, y_train = svm.prepare_dataset()
        pred_cluster = svm.predict_img_cluster()
        final_df = Retrieve_instances(
            y_train, detected_faces_list, pred_cluster).df_to_retrieve()
        return final_df
