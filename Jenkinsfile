pipeline {
    agent any
    stages {
        stage('Clone repository') {
            steps {
                //Git clone repository
                git branch: 'main', url: 'git@github.com:haniieh/DocAppoint.git'
            }
        }
        stage('Pull changes') {
            steps {
                //Pulling the changes from git
                git branch: 'main', url: 'git@github.com:haniieh/DocAppoint.git', changelog: true, poll: true
            }
        }
        stage('Build') {
            steps {
                // Building the docker image
                sh "docker build -t docappcr.azurecr.io/docapp:${env.BUILD_NUMBER} ."

            }
        }
        stage('Push Image to ACR') {
            steps {
                // Login to ACR and Pushing the docker image with build number tag
                sh"az acr login --name docappcr --output json"
                sh "docker push docappcr.azurecr.io/docapp:${env.BUILD_NUMBER}"
            }
        }
    }
    post {
        always {
            // Delete the Docker image
            sh "docker rmi docappcr.azurecr.io/docapp:${env.BUILD_NUMBER}"
            //to cleean the workspace
            deleteDir()

        }
    }
}

