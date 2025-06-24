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

        stage('Wait for ML API') {
            steps {
                powershell '''
                $maxAttempts = 40
                $url = "http://127.0.0.1:8000/analyze"
                $attempt = 0

                while ($attempt -lt $maxAttempts) {
                    try {
                        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
                        if ($response.StatusCode -eq 200) {
                            Write-Host "✅ ML API is UP!"
                            break
                        }
                    } catch {
                        Write-Host "⏳ Waiting for ML API... ($($attempt+1)/$maxAttempts)"
                    }
                    Start-Sleep -Seconds 5
                    $attempt++
                }

                if ($attempt -eq $maxAttempts) {
                    Write-Error "❌ Timeout: ML API is not responding."
                    exit 1
                }
                '''
            }
        }

        stage('Analyse ML') {
            steps {
                powershell 'Invoke-RestMethod -Uri http://127.0.0.1:8000/analyze -Method POST'
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
