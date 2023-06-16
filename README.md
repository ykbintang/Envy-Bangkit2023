# How to setup Google Cloud Platform using Cloud Run
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
