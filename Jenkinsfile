def tag

pipeline {
    environment {
        IMAGE_NAME = 'fnsdev/gitrello'
        BOT_TOKEN = credentials('bot-token')
        CHAT_ID = '-1001347488559'
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
                script {
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Build started $BUILD_URL %F0%9F%AA%92&'"
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Running tests %F0%9F%AA%92&'"
                }
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
                script {
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Building Docker image %F0%9F%AA%92&'"
                }
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
                script {
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Migrating database %F0%9F%AA%92&'"
                }
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
                script {
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Collecting static files %F0%9F%AA%92&'"
                }
                container('python') {
                    withCredentials([file(credentialsId: 'gs-credentials', variable: 'GS_CREDENTIALS')]) {
                        sh "cd gitrello && python manage.py collectstatic --noinput --settings=gitrello.settings_prod"
                    }
                }
            }
        }
        stage('Deploy chart') {
            steps {
                script {
                    sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Deploying helm chart %F0%9F%AA%92&'"
                }
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
            script {
               sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Build succeeded %F0%9F%AA%92&'"
            }
        }
        failure {
            script {
                sh "curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage -d chat_id=$CHAT_ID -d text='%F0%9F%AA%92& Build failed %F0%9F%AA%92&'"
            }
        }
    }
}
