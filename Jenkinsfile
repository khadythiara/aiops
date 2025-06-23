pipeline {
    agent any

    environment {
        APP_NAME = 'flask-log-app'
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/ton-utilisateur/ton-projet.git'
            }
        }

        stage('Build Docker') {
            steps {
                sh 'docker build -t ${APP_NAME}:latest ./flask-app'
                sh 'docker build -t ml-api:latest ./ml-api'
            }
        }

        stage('Start Stack') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }

        stage('Analyse ML') {
            steps {
                sh 'curl -X POST http://localhost:8000/analyze'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/*.log', onlyIfSuccessful: false
        }
    }
}