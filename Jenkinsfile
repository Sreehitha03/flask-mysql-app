pipeline {
  agent any

  environment {
    REPO = "Sreehitha23/flask-mysql-app"   
    IMAGE_TAG = "${env.BUILD_ID}"
    DOCKERHUB_CREDENTIALS = "dockerhub-creds"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          dockerImage = docker.build("${REPO}:${IMAGE_TAG}")
        }
      }
    }

    stage('Integration Test') {
      steps {
        script {
          sh "docker network create jenkins_test_net || true"

          sh """
             docker rm -f test_db || true
             docker run -d --name test_db --network jenkins_test_net \
               -e MYSQL_ROOT_PASSWORD=rootpassword \
               -e MYSQL_DATABASE=exampledb \
               -e MYSQL_USER=user \
               -e MYSQL_PASSWORD=password \
               mysql:8.0
          """

          // Wait for MySQL to be healthy
          sh '''
            echo "Waiting for MySQL..."
            for i in $(seq 1 30); do
              docker run --rm --network jenkins_test_net mysql:8.0 \
                mysqladmin ping -h test_db -uuser -ppassword >/dev/null 2>&1 && break
              sleep 2
            done
          '''

          sh """
            docker rm -f test_app || true
            docker run -d --name test_app --network jenkins_test_net \
              -e DB_HOST=test_db -e DB_USER=user -e DB_PASS=password -e DB_NAME=exampledb \
              ${REPO}:${IMAGE_TAG}
          """

          sh "sleep 5"
          sh "docker exec test_app curl -sSf http://localhost:5000/users > result.json"
          sh "cat result.json"
        }
      }
      post {
        always {
          sh "docker rm -f test_app || true"
          sh "docker rm -f test_db || true"
          sh "docker network rm jenkins_test_net || true"
          sh "rm -f result.json || true"
        }
      }
    }

    stage('Push to Docker Hub') {
      steps {
        script {
          withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
            sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
            sh "docker tag ${REPO}:${IMAGE_TAG} ${REPO}:latest"
            sh "docker push ${REPO}:${IMAGE_TAG}"
            sh "docker push ${REPO}:latest"
            sh "docker logout"
          }
        }
      }
    }

    stage('Deploy (Optional)') {
      steps {
        echo "🧩 Deployment placeholder — add SSH or Kubernetes steps here."
      }
    }
  }

  post {
    success {
      echo "✅ Build and push completed successfully!"
    }
    failure {
      echo "❌ Build failed — check logs!"
    }
  }
}
