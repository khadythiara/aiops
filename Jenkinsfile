pipeline {
    agent any

    environment {
        APP_NAME = 'flask-log-app'
        CHAT_WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAQA39W9xSk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lRVS-nOpraJquu3gGwyrtm0HTHxShCL-bi8vynKRjZQ'
        ARTIFACTS_URL = "${env.BUILD_URL}artifact/logs/"
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
                $maxAttempts = 50
                $url = "http://127.0.0.1:8000/analyze"
                $attempt = 0

                while ($attempt -lt $maxAttempts) {
                    try {
                        $response = Invoke-WebRequest -Uri $url -Method POST -UseBasicParsing -TimeoutSec 3
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
                def logContent = ''
                def anomalyContent = ''

                if (isUnix()) {
                    logContent = sh(returnStdout: true, script: 'tail -n 20 logs/app.log || echo "app.log missing"').trim()
                    anomalyContent = sh(returnStdout: true, script: 'tail -n 20 logs/anomalies.json || echo "anomalies.json missing"').trim()
                } else {
                    logContent = bat(returnStdout: true, script: 'powershell -Command "Get-Content logs/app.log -Tail 20"').trim()
                    anomalyContent = bat(returnStdout: true, script: 'powershell -Command "Get-Content logs/anomalies.json -Tail 20"').trim()
                }

                def payload = """
                {
                  "text": "📢 *Pipeline terminé avec le statut:* ${currentBuild.currentResult}\\n" +
                          "📂 *Job:* ${env.JOB_NAME} (#${env.BUILD_NUMBER})\\n\\n" +
                          "📄 *Logs récents :*\\n```\\n${logContent}\\n```\\n\\n" +
                          "🚨 *Anomalies détectées :*\\n```\\n${anomalyContent}\\n```\\n\\n" +
                          "📎 *Fichiers artifacts :* ${ARTIFACTS_URL}"
                }
                """

                httpRequest(
                    httpMode: 'POST',
                    url: CHAT_WEBHOOK_URL,
                    contentType: 'APPLICATION_JSON',
                    requestBody: payload,
                    validResponseCodes: '100:399'
                )
            }
        }
    }
}
