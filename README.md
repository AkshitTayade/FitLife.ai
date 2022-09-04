# FitLife.ai - Smart Fitness Assistant

## Problem Statement
Physical activity, particularly structured exercises, not only improves physical function but has also been 
linked to improved social and mental wellbeing. However, for some people, regular training, particularly 
at a gym or outside, may be inconvenient or impossible. Currently, the only way to achieve this is through 
interaction with a trainer or other gym-goers. Personal trainers are expensive, and many people who wish 
to exercise cannot afford one. 

44% of gym users are too embarrassed to seek help from a gym employee” (pure gym, 2019). During the 
COVID-19 epidemic, the majority of people have looked into some type of at-home exercise. "40% OF 
CONSUMERS ANTICIPATING TO EXERCISE MORE AS A RESULT OF THE ONGOING 
PANDEMIC" (LSN GLOBAL, 2020). Additionally, fast-food consumption is frighteningly increasing, 
which has resulted in the consumption of unhealthy foods. As a result, it has become critical for people to 
have a well-balanced nutritionally sound diet in addition to engaging in physical activity. However, in this 
fast-paced world, not everyone has the time or money to spend on a personal dietitian and nutritionist who 
will monitor and care for their health by counseling them on a balanced food plan
. 
In this study, we looked at how technology can help with home training, how it can persuade people to start 
and maintain an active lifestyle, and how it may be helpful in attaining better strength and balance. We 
reviewed individual personal information in this study and attempted to propose a diet type and meal plans 
for a healthy lifestyle

## Description
<p align="justify">
We present a system that analyzes the user's body posture during a workout and provides posture corrections to help fix this problem and offer visual feedback while conducting an exercise. Fitness AI, the smart fitness assistant, is what we call it. 

Our fitness application counts reps, corrects technique, and tracks practically any workout using your device's camera and a 3D capture technology. Captions are provided as real-time feedback tailored to your performance. It's like if you had a personal trainer at your side, encouraging you to work harder and reach higher goals. It transforms your device's camera into a relentless motivator, assisting you in getting the greatest results and avoiding damage by counting squats, timing planks, and evaluating your pace. It would also gather detailed information for each workout and track your progress over time, allowing you to see real results. 

We suggest a two-step method for analyzing exercise posture, which includes a count of repetitions and a recommendation for inappropriate posture. The real-time body tracking model, which extracts a total of 32 body coordinates, is the initial stage in Fitness AI. Furthermore, these body coordinates are fed into a statistical system that offers a person with exercise count and posture correction recommendations. The device will not only track the number of exercises completed, but will also monitor body posture, assisting in staying fit and healthy. The application also checks the accuracy of a user's projected stance for a particular exercise. We use machine learning models to accomplish this, with the poses and teaching of certified professionals serving as the ground truth for perfect form. The suggested system employs the K Nearest Neighbor (KNN) model, Random Forest, Deep Neural Networks (DNN), and Linear Regression for classification. 

The second portion of our application allows users to calculate BMI (Body Mass Index) and BMR (Basal Metabolic Rate) from their input data using the Mifflin-St Jeor Equation. In addition, the project intends to develop a personalized diet advice system based on the user's input. Machine learning model was created using a random-forest classifier based on input values for clustering and classification of six types of diet according to their particular preferences and building a healthy lifestyle behavior. 
</p>

## Challenges of AI in fitness
<p align='justify'>
(a) **Specifics of Physiology:** 
Humans do not have ideal body proportions. There are disproportions in everyone, whether it be the length of their arms, the legs, or the back. We need to understand that only those images of people used for training will be used to analyse the user's body for pose estimation. This means, the model’s perception of the body of the user depends on people’s bodies from the training images. It is not assured that the training dataset consists of images of the same body structure. 

(b) **Detection of start of the exercises:** 
In order to estimate the exercise duration period, the system is expected to detect the exercise start and end. For example, while squatting with a barrel, the system can analyse the user's hand and shoulder positions through arbitrary hard-coded thresholds. Errors might occur if the arm angles briefly exceed this threshold. 

(c) **Quick Movements of the Lower Body Part:** 
Another example where these AI-based apps may cause errors is in Martial arts while using legs for kicking. In the case of a quick kick, the deep learning model might be unable to record this action. This is because the fast leg-transition could lead to the blurring of key points of the leg. Additionally, the 2D key point dataset may not include images of such limb actions. The 2D detections which act as an input for 3D pose prediction were detected wrongly. As a result, 3D predictions for the lower-body will not reflect real actions. 

(d) **Horizontal position:** 
A human pose estimation model may also have difficulty estimating push-ups. A large number of errors are returned by the model when detecting 2D key points of arms and legs of this athlete doing push-ups in the video. However, rotating the video vertically to examine the athlete's movements worked wonderfully. This problem proved that visual data in such open datasets was not sufficient. 
</p>

## Model Architecture
### 1. Exercise Correction
- **Pre-processing of Images to get Multi-Pose Landmarks**<br>
- **Angle Calculation using Landmarks**<br>
- **Posture Correction**<br>
- **Calories Burned Estimation**<br>

### 2. Diet Recommendation
- **Dataset Collection**<br>
- **EDA**<br>
- **Machine Learning Algorithms**<br>

> For detailed explaination refer [here](https://github.com/Vidhi-Sejpal/FitLife.ai/blob/master/LY%20Project%20Report.pdf) Page 16

## Tech Stack
1. Figma (UI Designing)
2. Bootstrap (Frontend)
3. Django (Backend)
4. SQLite (Database)
5. OpenCV (Posture Correction)
6. Pandas,Numpy,Scikit Learn (ML Models)
7. JSON
8. Github (Version Control)
9. Visual Studio Code (Code Editor)

**Video Link** - https://youtu.be/4w8zIXG8bek
