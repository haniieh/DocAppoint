pipeline {
    agent any
    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'git@github.com:haniieh/DocAppoint.git'
            }
        }
        stage('Pull changes') {
            steps {
                git branch: 'main', url: 'git@github.com:haniieh/DocAppoint.git', changelog: true, poll: true
            }
        }
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }
    }
}
