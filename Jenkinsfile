
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is ready'
            }
        }

        stage('Syntax Check') {
            steps {
                bat 'docker run --rm -v "%WORKSPACE%:/app" -w /app python:3.11-slim python -m py_compile app.py'
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
