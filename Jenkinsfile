pipeline {
    agent any  // Runs on any available agent

    environment {
        // Customizable variables
        DOCKER_HUB = "pathums"                  // Your Docker Hub username
        APP_NAME = "calculator-app"          // Your application name
        // Dynamic tag using timestamp + Git SHA
        BUILD_TAG = "${env.BUILD_NUMBER}-${sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()}"
        DOCKER_REGISTRY = "https://registry.hub.docker.com"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out code from repository..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/PathumSandaruwanD/simple-docker-pipeline.git',
                        credentialsId: 'github_token'
                    ]]
                ])
                // Verify code was pulled
                sh 'ls -la'
                echo "Code checkout completed"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image with tag ${BUILD_TAG}..."
                    try {
                        docker.build("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}")
                        docker.build("${DOCKER_HUB}/${APP_NAME}:latest")
                        echo "Docker images built successfully"
                    } catch (Exception e) {
                        error "Docker build failed: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing images to Docker Hub..."
                    try {
                        docker.withRegistry(DOCKER_REGISTRY, 'docker-hub-creds') {
                            docker.image("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}").push()
                            docker.image("${DOCKER_HUB}/${APP_NAME}:latest").push()
                        }
                        echo "Images pushed successfully"
                    } catch (Exception e) {
                        error "Failed to push images: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('Deploy (Optional)') {
            when {
                anyOf{
                    branch 'main'
                    branch 'master'
                }
            }
            script {
            echo "⚡ Deploying application..."
            // Add this to verify branch detection
            echo "Current branch: ${env.BRANCH_NAME}" 
            
            sh '''
            docker stop running-app || true
            docker rm running-app || true
            docker run -d --name running-app -p 5000:5000 ${DOCKER_HUB}/${APP_NAME}:latest
            '''
            echo "🌐 Application deployed at http://<server-ip>:5000"
        }
        }
    }

    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
            echo "Cleaning up Docker system..."
            sh 'docker system prune -f --filter "until=24h"'
            echo "Cleanup completed"
        }
        success {
            echo "✅ Pipeline succeeded!"
            // Add any success notifications here if needed
        }
        failure {
            echo "❌ Pipeline failed!"
            // Add any failure notifications here if needed
        }
    }
}