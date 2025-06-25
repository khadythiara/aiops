pipeline {
    agent any

    environment {
        CHAT_WEBHOOK_URL = 'https://chat.googleapis.com/v1/spaces/AAQA39W9xSk/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=lRVS-nOpraJquu3gGwyrtm0HTHxShCL-bi8vynKRjZQ'
        ARTIFACTS_URL = "${env.BUILD_URL}artifact/logs/"
    }

    stages {
        stage('Build') {
            steps {
                echo "🔧 Build en cours..."
                sh '''
                    mkdir -p logs
                    echo "INFO: User logged in" >> logs/logs.txt
                    echo "ERROR: Database connection failed" >> logs/logs.txt
                '''
            }
        }

        stage('Analyse') {
            steps {
                echo "📊 Analyse des anomalies..."
                writeFile file: 'logs/anomalies.json', text: '''
[
    {"timestamp": 0, "anomaly": true},
    {"timestamp": 8, "anomaly": true}
]
'''.trim()
            }
        }
    }

    post {
        always {
            script {
                // Lire les logs
                def recentLogs = ""
                if (fileExists('logs/logs.txt')) {
                    def logFile = readFile('logs/logs.txt')
                    recentLogs = logFile.readLines().takeRight(10).join('\n')
                }

                // Lire les anomalies
                def anomalyFormatted = ""
                if (fileExists('logs/anomalies.json')) {
                    def anomalyJson = readFile('logs/anomalies.json')
                    def anomalyList = new groovy.json.JsonSlurper().parseText(anomalyJson)
                    def anomalies = anomalyList.findAll { it.anomaly == true }
                    anomalyFormatted = anomalies.collect { groovy.json.JsonOutput.toJson(it) }.join('\n')
                }

                // Construire le message Google Chat
                def textMessage = """
📣 *Pipeline terminé* : ${currentBuild.currentResult}
🔗 *Job* : ${env.JOB_NAME} #${env.BUILD_NUMBER}

📄 *Logs récents :*
