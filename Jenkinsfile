def tag

pipeline {
    environment {
        IMAGE_NAME = 'fnsdev/gitrello'
    }
    agent {
        kubernetes {
            defaultContainer 'jnlp'
            yaml """
              apiVersion: v1
              kind: Pod
              metadata:
                name: ci
                labels:
                  app: jenkins
              spec:
                nodeSelector:
                  type: ci
                containers:
                  - name: python
                    image: python:3.8.5-slim-buster
                    command:
                      - cat
                    tty: true
                    resources:
                      requests:
                        memory: "400Mi"
                        cpu: "0.5"
                      limits:
                        memory: "400Mi"
                        cpu: "0.5"
                  - name: docker
                    image: docker:19.03
                    command:
                      - cat
                    tty: true
                    resources:
                      requests:
                        memory: "200Mi"
                        cpu: "0.2"
                      limits:
                        memory: "200Mi"
                        cpu: "0.2"
                    volumeMounts:
                      - name: dockersock
                        mountPath: /var/run/docker.sock
                  - name: helm
                    image: lachlanevenson/k8s-helm:v3.3.1
                    command:
                      - cat
                    tty: true
                volumes:
                  - name: dockersock
                    hostPath:
                      path: /var/run/docker.sock
            """
        }
    }
    stages {
        stage ('Run tests') {
            environment {
                DJANGO_DB_NAME = credentials('test-db-name')
                DJANGO_DB_USER = credentials('test-db-user')
                DJANGO_DB_HOST = credentials('test-db-host')
                DJANGO_DB_PORT = credentials('test-db-port')
                DJANGO_DB_PASSWORD = credentials('test-db-password')
            }
            steps {
                telegramSend(message: 'Build started $BUILD_URL', chatId: 1001347488559)
                telegramSend(message: 'Running tests', chatId: 1001347488559)
                container('python') {
                    sh """
                      apt-get update && \
                        apt-get install --no-install-recommends -y libpq-dev git gcc libc6-dev && \
                        apt-get clean && \
                        rm -rf /var/lib/apt/lists/*
                    """
                    sh "pip install -r requirements.txt"
                    sh "cd gitrello && python manage.py test --noinput"
                }
            }
        }
        stage ('Set tag') {
            steps {
                script {
                    tag = sh(script: 'git describe', returnStdout: true).trim()
                }
            }
        }
        stage('Build image') {
            steps {
                telegramSend(message: 'Building Docker image', chatId: 1001347488559)
                container('docker') {
                    sh "docker build -t ${IMAGE_NAME}:${tag} ."
                }
            }
        }
        stage('Publish image') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        sh "echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${tag}"
                    }
                }
            }
        }
        stage('Migrate database') {
            environment {
                DJANGO_DB_NAME = credentials('db-name')
                DJANGO_DB_USER = credentials('db-user')
                DJANGO_DB_HOST = credentials('db-host')
                DJANGO_DB_PORT = credentials('db-port')
                DJANGO_DB_PASSWORD = credentials('db-password')
            }
            steps {
                telegramSend(message: 'Migrating database', chatId: 1001347488559)
                container('python') {
                    sh "cd gitrello && python manage.py migrate"
                }
            }
        }
        stage('Collect static') {
            environment {
                GS_BUCKET_NAME = credentials('gs-bucket-name')
                GS_PROJECT_ID = credentials('gs-project-id')
            }
            steps {
                telegramSend(message: 'Collecting static files', chatId: 1001347488559)
                container('python') {
                    withCredentials([file(credentialsId: 'gs-credentials', variable: 'GS_CREDENTIALS')]) {
                        sh "cd gitrello && python manage.py collectstatic --noinput --settings=gitrello.settings_prod"
                    }
                }
            }
        }
        stage('Deploy chart') {
            steps {
                telegramSend(message: 'Deploying helm chart', chatId: 1001347488559)
                container('helm') {
                    withCredentials([file(credentialsId: 'gitrello-overrides', variable: 'OVERRIDES')]) {
                        sh "helm upgrade gitrello --install ./manifests/gitrello -f ${OVERRIDES} --set deployment.image.tag=${tag}"
                    }
                }
            }
        }
    }
    post {
        success {
            telegramSend(message: 'Build succeeded', chatId: 1001347488559)
        }
        failure {
            telegramSend(message: 'Build failed', chatId: 1001347488559)
        }
    }
}
