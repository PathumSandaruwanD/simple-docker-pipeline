pipeline {
    agent any

    environment {
        // Customizable variables
        DOCKER_HUB = "pathums"
        APP_NAME = "calculator-app"
        // Dynamic tag using build number + Git SHA
        BUILD_TAG = "${env.BUILD_NUMBER}-${sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()}"
        DOCKER_REGISTRY = "https://registry.hub.docker.com"
    }

    stages {
        stage('🔍 Checkout Code') {
            steps {
                echo "🚀 Checking out code..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],  // Checks out main branch
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/PathumSandaruwanD/simple-docker-pipeline.git',
                        credentialsId: 'github_token'
                    ]]
                ])
                // Verify code was pulled
                sh 'ls -la && echo "✅ Code ready!"'
            }
        }

        stage('🐳 Build Docker Image') {
            steps {
                script {
                    echo "🏗️ Building Docker image (tag: ${BUILD_TAG})..."
                    try {
                        docker.build("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}")
                        docker.build("${DOCKER_HUB}/${APP_NAME}:latest")
                        echo "🎉 Images built successfully!"
                    } catch (Exception e) {
                        error "❌ Docker build failed: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('📤 Push to Docker Hub') {
            steps {
                script {
                    echo "🚚 Pushing to Docker Hub..."
                    try {
                        docker.withRegistry(DOCKER_REGISTRY, 'docker-hub-creds') {
                            docker.image("${DOCKER_HUB}/${APP_NAME}:${BUILD_TAG}").push()
                            docker.image("${DOCKER_HUB}/${APP_NAME}:latest").push()
                        }
                        echo "📦 Images pushed successfully!"
                    } catch (Exception e) {
                        error "❌ Failed to push images: ${e.getMessage()}"
                    }
                }
            }
        }

        stage('🚀 Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                script {
                    echo "⚡ Deploying application..."
                    echo "Current branch: ${env.BRANCH_NAME}"
                    
                    try {
                        sh '''
                        # Stop and remove existing container
                        docker stop running-app || true
                        docker rm running-app || true
                        
                        # Run new container
                        docker run -d \
                            --name running-app \
                            -p 5000:5000 \
                            ${DOCKER_HUB}/${APP_NAME}:latest
                        '''
                        echo "🌐 Application deployed at http://<server-ip>:5000"
                    } catch (Exception e) {
                        error "❌ Deployment failed: ${e.getMessage()}"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning up Docker..."
            sh 'docker system prune -f --filter "until=24h"'
        }
        success {
            echo "🏆 PIPELINE SUCCESS! All stages completed successfully!"
            sh '''
            echo "Docker Images:"
            docker images | grep ${DOCKER_HUB}/${APP_NAME}
            '''
        }
        failure {
            echo "🔥 PIPELINE FAILED! Check logs for details."
        }
        unstable {
            echo "⚠️  PIPELINE UNSTABLE! Tests or other quality gates failed."
        }
    }
}