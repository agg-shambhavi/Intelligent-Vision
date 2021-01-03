# Intelligent-Vision
We are aiming to make a tool that will assist crime investigation authorities to rapidly analyze CCTV recordings/videos. 

# Problem
Let's say we have an images of a suspects, and we have the CCTV recordings of the crime scene. Now, the video recording could be of hours and there can be a long list of suspects. Finding the suspects manually in the video can be a time-consuming and labour intensive task. Given the seriousness of any crime investigation where prompt actions are required, a lot of time is wasted in analyzing videos. 

# Solution
Let's automate this task and save some time!<br> Enter the suspect's picture and the video recording in our tool, and our tool will find the suspect's face in the video recording. You will be able to see the frames in which the suspect appeared in the video. 

# Demo
![iv3](https://user-images.githubusercontent.com/48705124/103475900-4e2fe080-4dd7-11eb-9a71-0b3e0e2361bc.gif)

# Machine Learning Pipeline 
<ol>
  <li> Divide the video into frames. </li>
  <li> Detect faces in the frames and put those frames into a list. </li>
  <li> Encode detected faces using FaceNet(used face-recognition library).</li>
  <li> Group the faces of one person in a cluster using DBSCAN Algorithm. </li>
  <li> Detect the face in the query image and encode it. </li>
  <li> Predict in which cluster will the query image belong to using SVM.</li>
  <li> Retrieve all the frames in the predicted cluster </li>
 </ol>
 
 We have deployed the ML-Pipeline on a Web application using Flask.
 
 # Screenshots
 
 | ![image](https://user-images.githubusercontent.com/48705124/103476039-53415f80-4dd8-11eb-8fb9-51463abe491a.png) | ![image](https://user-images.githubusercontent.com/48705124/103476082-aadfcb00-4dd8-11eb-92fc-99022a785968.png)  |
|---|---|
| Landing Page | Home Page |
| ![image](https://user-images.githubusercontent.com/48705124/103476093-c8149980-4dd8-11eb-8557-941f6a5ac795.png) | ![shambhavii](https://user-images.githubusercontent.com/48705124/103476179-7d475180-4dd9-11eb-8a14-e0322d21e337.jpg) |
| Enter Query image & Video | Query Image |
| ![input frames](https://user-images.githubusercontent.com/48705124/103476239-f5157c00-4dd9-11eb-9954-4c01bde6c521.jpg) | ![image](https://user-images.githubusercontent.com/48705124/103476289-62291180-4dda-11eb-9780-655864e2c3bc.png) |
| Frames of the video | Results |
 
 # Tech-Stack
 <ul>
  <li> Front-end : HTML, CSS, Bootstrap, JavaScript </li>
<li>Back-end: Flask </li>
<li>Machine Learning Libraries:  Numpy, Pandas, Sci-Kit Learn, Face-recognition, OpenCV </li>
  

 # Team Members
 This project was built by [Shambhavi Aggarwal](https://github.com/agg-shambhavi), [Bhargav Akhani](https://github.com/bhargav2427) and [Dharven Doshi](https://github.com/dharven)

