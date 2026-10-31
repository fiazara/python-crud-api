
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

        stage('Deploy Container') {
            steps {
                bat 'docker rm -f production-api-container || exit /b 0'
                bat 'docker run -d --name production-api-container -p 5000:5000 -v production-api-data:/var/lib/backend_data python-crud-api:manual'
            }
        }

        stage('Health Check') {
            steps {
                bat '''
                powershell -NoProfile -Command "$ok=$false; for ($i=0; $i -lt 15; $i++) { try { $r=Invoke-RestMethod -Uri 'http://localhost:5000/health' -TimeoutSec 2; if ($r.status -eq 'active') { $ok=$true; break } } catch {}; Start-Sleep -Seconds 2 }; if (-not $ok) { docker logs production-api-container; exit 1 }"
                '''
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
