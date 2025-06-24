pipeline {
    agent any

    environment {
        APP_NAME = 'flask-log-app'
        GCHAT_WEBHOOK = 'https://chat.googleapis.com/v1/spaces/AAQA39W9xSk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lRVS-nOpraJquu3gGwyrtm0HTHxShCL-bi8vynKRjZQ'
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

        stage('Clean containers') {
            steps {
                bat 'docker rm -f ml-api || echo "ml-api not running"'
                bat 'docker rm -f flask-log-app || echo "flask-log-app not running"'
                bat 'docker rm -f elasticsearch || echo "elasticsearch not running"'
                bat 'docker rm -f kibana || echo "kibana not running"'
                bat 'docker rm -f logstash || echo "logstash not running"'
            }
        }

        stage('Start Stack') {
            steps {
                bat 'docker-compose down --remove-orphans || echo "Nothing to stop"'
                bat 'docker-compose up -d --build'
            }
        }

    

        stage('Analyse ML') {
            steps {
                bat 'Invoke-RestMethod -Uri http://127.0.0.1:8000/analyze -Method POST'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/*.log', onlyIfSuccessful: false

            script {
                def buildStatus = currentBuild.currentResult
                def message = (buildStatus == 'SUCCESS') ?
                    "✅ Pipeline terminé avec succès !" :
                    "❌ Le pipeline a échoué à l'étape : ${env.STAGE_NAME}"

                httpRequest httpMode: 'POST',
                    contentType: 'APPLICATION_JSON',
                    requestBody: "{\"text\": \"${message}\"}",
                    url: "${GCHAT_WEBHOOK}"
            }
        }
    }
}
