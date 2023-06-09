#  ****ENVy : A Application for Classification Environtment Quality with TensorFlow****
![1](https://github.com/ykbintang/Groco_Corn-plant-disease-detection-system/assets/126853793/53de9f07-a252-45f8-824f-42ce8212bae3)
![PPT ENVy](https://github.com/ykbintang/Groco_Corn-plant-disease-detection-system/assets/126853793/6ca03539-f3df-466e-b20f-bc35d74a89ae)

Hi everyone, we are from C23-PS057  proudly present, ENVy!
our innovation to raise public awareness regarding environments quality !

## Table of contents

- [Table of contents](#table-of-contents)
- [Team Developer](#developer)
- [About](#about)
     - [Background](#background)
     - [Project Goals](#project-goals)
     - [Building Model and Deploy Model](#building-model-and-deploy-model)
        - [Dataset](#dataset)
        - [Build Model](#build-model)
        - [Project Installation](#project-installation)
     - [Features](#features)
     - [Screenshots](#screenshots)
- [Workflow ENVy](#workflow-envy)
- [Bussines Plan](#bussines-plan)
- [Presentation Video](#presentation-video)
- [Demo Video](#demo-video)
- [Support By](#support-by)
- [API Reference](#api-reference)

## Developer
Team ID : C23-PS057 

Team Member :
1. (ML) M295DSX1443 – Riza Fazhriansyah Hermawan 
2. (ML) M295DSY0164 - Humaira Zahra Ihwati 
3. (ML)  M295DKY4071 – Arum Putri Juniarsih 
4. (CC) C069DSX2613 – Akmal Muhammad Ridho 
5. (CC) C100DSY4892 – Ariel Almutatohirin 
6. (MD) A259DKX4947 – Yayes Kasnanda Bintang
   
## About
ENVy (Environments Quality) is a mobile application designed to detect and measure the quality of water, air, and soil based on predetermined chemical parameters. ENVy provides detailed reports on environmental quality based on the specified parameters, enabling users to make informed decisions and take appropriate actions. This application empowers users to become agents of change who care about the environment.

## Background
Research shows that poor environmental quality can have a negative impact on both human health and the environment. However, information about environmental quality is often difficult to obtain and hard for the general public to understand. Therefore, our team aims to solve this problem by creating a mobile application that can predict environmental quality based on chemical parameters. This application will allow users to obtain accurate and up-to-date information about environmental quality in their surroundings and help them take appropriate preventive measures. We also want to assist the government in making decisions regarding environmental policies by providing data that has been collected

## Project Goals
- The goal is to simplify the complex information related to environmental quality, making it easier for the general public to comprehend
- Enable the general public to make informed decisions regarding their environment. By providing accessible and understandable information,
the application should empower users to take appropriate actions to
protect their health and the environment.
- Assist the government in making informed decisions about environmental
policies. By providing reliable and comprehensive data on environmental
quality, the application can contribute to evidence-based decision-making
and help shape effective environmental regulations.

## Building Model and Deploy Model

### Dataset
We use dataset from online resources, for specific link you can cek in this list :
- For Soil Dataset you can klik [here.](https://www.kaggle.com/datasets/aksahaha/crop-recommendation)
- For Water Dataset you can klik [here.](https://data.amerigeoss.org/dataset/wqi-parameter-scores-1994-2013-b0941)
- For Air Dataset you can klik [here.](https://www.kaggle.com/datasets/hasibalmuzdadid/global-air-pollution-dataset)

### Build Model
We build model with Tensorflow squential model after we do some prepocessing from the dataset and save model in to model.h5. After that, the model is deployed with FAST API and docker. for detail code that we use you can click this :
  - [Soil Predict Quality](https://colab.research.google.com/drive/1ePbPR4LnEpe2FCwHuwFDZhwKMnxiz2Fw?usp=drive_link)
  - [Water Predict Quality](https://colab.research.google.com/drive/19MmQ6BhpWw09TwLgfmosaj2tB80bjAg1?usp=drive_link) 
  - [Air Predict Quality](https://colab.research.google.com/drive/17gD6_P7ClBwBsklMLaXzZ-QMBHeKwxyG?usp=drive_link) 

### Project Installation 
### How to setup Google Cloud Platform using Cloud Run
1. Open Google Cloud Console: Open the Google Cloud Console by visiting the following URL: https://console.cloud.google.com/

2. Activate Cloud Shell: Click on the Cloud Shell icon in the top-right corner of the console. This will open a Cloud Shell terminal at the bottom of the console.

3. Select or Create a Project: Ensure that you have a project selected in the Cloud Shell. If not, create a new project or select an   existing project using the project selection drop-down at the top of the Cloud Shell.

4. Set the project id
   ```
   gcloud config set project PROJECT_ID
   ```
5. Enable Cloud Run API: Run the following command to enable the Cloud Run API:
   ``` 
   gcloud services enable run.googleapis.com
   ```
6. Clone repository following this command
   ```
   git clone -b CC https://github.com/ykbintang/Envy-Bangkit2023.git
   ```
7. Open the app folder
   ```
   cd Envy-Bangkit2023
   ```
8. Config **.env** and **service_account** file.

9. Build and Push Docker Image: Build and push your Docker image to a container registry. Use the following commands as an example:
   ```
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/[IMAGE_NAME]
   gcloud auth configure-docker
   docker push gcr.io/[PROJECT_ID]/[IMAGE_NAME]
   ```
   Replace **[PROJECT_ID]** with your Google Cloud project ID and **[IMAGE_NAME]** with the desired name for your Docker image.
 
10. Deploy to Cloud Run: Deploy your Docker image to Cloud Run using the following command:
    ```
    gcloud run deploy [SERVICE_NAME] --image gcr.io/[PROJECT_ID]/[IMAGE_NAME]
    ```
    Replace **[SERVICE_NAME]** with the desired name for your Cloud Run service.
   
11. Configure Service Settings: Follow the prompts to configure the desired settings for your Cloud Run service, such as region, authentication, and concurrency.

12. Wait for Deployment: Wait for the deployment process to complete. Cloud Run will automatically set up the necessary resources and provide you with the service URL.

## Features
  - Soil Predict Quality: Predict soil quality with Nitrogen,Phosphorus, Potassium, pH parameters (accuracy 94.03% and validation accuracy 91.14%)
  - Water Predict Quality: Predict water quality with FC, Oxygen, pH,Total Suspended Sediment, Temperature, Nitrogen,Phosphorus,Turbidity parameters (accuracy 87.77% and validation accuracy 81.48%)
  - Air Predict Quality: Predict air quality with Nitrogen     Dioxide,Ozone, Carbon Monoxide, Particulate Matter parameters (accuracy 98% and validation accuracy 98%)

## Screenshots
![1](https://github.com/ykbintang/Envy-Bangkit2023/assets/126853793/2a448379-b9f7-4a18-8fc4-d8822ee80fb4)
![2](https://github.com/ykbintang/Envy-Bangkit2023/assets/126853793/8f172509-36f1-467f-b993-9d31383c89a3)

## Workflow ENVy
1. Get the chemical parameter value input from the user from the HTML form and then put it in an array for inference.

2. Predict user input using a model that has been created using TensorFlow.

3. Issue predictive labels on several categories of various environmental aspects

4. The final prediction result is returned to the prediction page to be displayed to the user.

## Bussines Plan
This is our bussines plan for ENVy application, you can see the document in [here.](https://drive.google.com/file/d/1Qss7or5RHQc1q9VPp-fwTRJWWADnSgC1/view?usp=drive_link)

## Presentation Video
To see the presentation from our team you can see in [here](https://youtu.be/U66PEWyMAVc) 

## Demo Video
To see the video ENVy application demo, please see it [here](https://youtu.be/k7WVqg96EsE). And this is our [application demo](https://drive.google.com/file/d/1-cupzojoiS6rcPTpDWw2Za_UTSVmtFtn/view?usp=sharing)

## Support By
- Kampus Merdeka
- Bangkit Academy 2023
- Google
- GoTo
- Traveloka

## API Reference
We also provide API documentation for developers who are interested in integrating with our application. Visit our [API documentation](https://crossroads-mbd2rndo6a-et.a.run.app/docs).




