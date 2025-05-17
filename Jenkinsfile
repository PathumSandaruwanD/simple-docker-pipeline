pipeline {
    agent any  // Runs on any available agent

    environment {
        // Customizable variables
        DOCKER_HUB = "pathums"  // Your Docker Hub username
        APP_NAME = "calculator-app"              // Your application name
        // Dynamic tag using timestamp + Git SHA
        BUILD_TAG = "${env.BUILD_NUMBER}-${sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],  // Explicitly checks out 'main' branch
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/PathumSandaruwanD/simple-docker-pipeline.git',
                        credentialsId: 'github_token'  // If using private repo
                    ]]
                ])
                // Verify code was pulled
                sh 'ls -la'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build with both versioned and 'latest' tags
                    docker.build("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}")
                    docker.build("${DOCKER_HUB}/${APP_NAME}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-creds') {
                        // Push both tags
                        docker.image("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}").push()
                        docker.image("${DOCKER_HUB}/${APP_NAME}:latest").push()
                    }
                }
            }
        }

        stage('Deploy (Optional)') {
            steps {
                sh '''
                # Example deployment command
                docker stop running-app || true
                docker run -d --name running-app -p 5000:5000 ${DOCKER_HUB}/${APP_NAME}:latest
                '''
            }
        }
    }

    post {
        always {
            echo "Build completed with status: ${currentBuild.currentResult}"
            // Clean unused Docker images
            sh 'docker system prune -f --filter "until=24h"'
        }
        success {
            slackSend(message: "✅ Success: ${env.JOB_NAME} build ${env.BUILD_NUMBER}")
        }
        failure {
            slackSend(message: "❌ Failed: ${env.JOB_NAME} build ${env.BUILD_NUMBER}")
        }
    }
}