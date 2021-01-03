# Intelligent-Vision
We are aiming to make a tool that will assist crime investigation authorities to rapidly analyze CCTV recordings/videos. 

# Problem
Let's say we have an images of a suspects, and we have the CCTV recordings of the crime scene. Now, the video recording could be of hours and there can be a long list of suspects. Finding the suspects manually in the video can be a time-consuming and labour intensive task. Given the seriousness of any crime investigation where prompt actions are required, a lot of time is wasted in analyzing videos. 

# Solution
Let's automate this task and save some time!<br> Enter the suspect's picture and the video recording in our tool, and our tool will find the suspect's face in the video recording. You will be able to see the frames in which the suspect appeared in the video. 

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
 
 # Tech-Stack
 <ul>
  <li> Front-end : HTML, CSS, Bootstrap, JavaScript </li>
<li>Back-end: Flask </li>
<li>Machine Learning Libraries:  Numpy, Pandas, Sci-Kit Learn, Face-recognition, OpenCV </li>

 # Team Members
This project was built by [Shambhavi Aggarwal](https://github.com/agg-shambhavi), [Bhargav Akhani](https://github.com/bhargav2427) and [Dharven Doshi](https://github.com/dharven)

