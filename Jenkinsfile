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
                bat '''
                @echo off
                echo ===== Waiting for ml-api to be ready =====
                set RETRY_COUNT=0
                set MAX_RETRIES=10

                :retry
                curl -s -o nul -w "%%{http_code}" http://localhost:8000/analyze > result.txt
                set /p STATUS=<result.txt
                echo Status: !STATUS!

                if "!STATUS!"=="200" (
                    echo [OK] ML API is ready.
                ) else (
                    echo [WAIT] ML API not ready yet, waiting 5s...
                    timeout /T 5 > nul
                    set /A RETRY_COUNT+=1
                    if !RETRY_COUNT! LSS !MAX_RETRIES! goto retry
                    echo [FAIL] Timeout waiting for ML API to respond.
                    exit /B 1
                )
                '''

                bat 'curl.exe -X POST http://localhost:8000/analyze'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/*.log', onlyIfSuccessful: false

            script {
                def payload = """
                {
                  "text": "📢 Pipeline terminé avec le statut: ${currentBuild.currentResult}\\nJob: ${env.JOB_NAME} (#${env.BUILD_NUMBER})"
                }
                """

                httpRequest(
                    httpMode: 'POST',
                    url: 'https://chat.googleapis.com/v1/spaces/AAQA39W9xSk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lRVS-nOpraJquu3gGwyrtm0HTHxShCL-bi8vynKRjZQ',
                    contentType: 'APPLICATION_JSON',
                    requestBody: payload
                )
            }
        }
    }
}
