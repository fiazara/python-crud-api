
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is ready'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t python-crud-api:manual .'
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat 'docker image inspect python-crud-api:manual'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}
