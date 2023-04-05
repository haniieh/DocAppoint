pipeline {
    agent any
       environment {
       HELM_RELEASE_NAME = "apps-1"
       HELM_CHART_PATH = "/home/azureuser/helm-application/apps"
       GIT_REPO ="git@github.com:haniieh/DocAppoint.git"
       CONTAINER_REGISTERY="docappcr"
       APPLICATION_NAME="docapp"
   }
    

    stages {
          stage('Clear Workspace') {
            steps {
                //Clean workspace before build
                cleanWs()
            }
        }
        stage('Clone Application repository') {
            steps {
                //Git clone repository
                git branch: 'main', url: "$GIT_REPO"
            }
        }

        stage('Build') {
            steps {
                // Building the docker image
                sh "docker build -t ${CONTAINER_REGISTERY}.azurecr.io/${APPLICATION_NAME}:${env.BUILD_NUMBER} ."

            }
        }
        stage('Push Image to ACR') {
            steps {
                // Login to ACR and Pushing the docker image with build number tag
                sh"az acr login --name $CONTAINER_REGISTERY --output json"
                sh "docker push ${CONTAINER_REGISTERY}.azurecr.io/${APPLICATION_NAME}:${env.BUILD_NUMBER}"
            }
        }
        stage('Deploy application using Helm') {
           steps {
               sh "helm upgrade --install --set doc-appoint.image.tag=${env.BUILD_NUMBER} --wait --namespace default --atomic $HELM_RELEASE_NAME $HELM_CHART_PATH"
               }
        }
    }
    post {
        always {
            // Delete the Docker image
            sh "docker rmi ${CONTAINER_REGISTERY}.azurecr.io/${APPLICATION_NAME}:${env.BUILD_NUMBER}"
            //to cleean the workspace
            deleteDir()

        }
    }
}

