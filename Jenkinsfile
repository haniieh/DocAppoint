pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Server') {
            steps {
                sh 'python manage.py runserver'
            }
        }
    }
}

