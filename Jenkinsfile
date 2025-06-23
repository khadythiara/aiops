pipeline {
    agent any

    environment {
        APP_NAME = 'flask-log-app'
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/khadythiara/aiops.git'
            }
        }

        stage('Build Docker') {
            steps {
                bat "docker build -t %APP_NAME%:latest ./flask-app"
                bat "docker build -t ml-api:latest ./ml-api"
            }
        }

        stage('Start Stack') {
            steps {
                bat 'docker-compose down || echo "Nothing to stop"'
                bat 'docker-compose up -d --build'
            }
        }

        stage('Analyse ML') {
            steps {
                bat 'curl -X POST http://localhost:8000/analyze'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/*.log', onlyIfSuccessful: false
        }
    }
}
