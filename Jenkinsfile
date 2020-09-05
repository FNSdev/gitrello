def tag

pipeline {
    environment {
        IMAGE_NAME = 'fnsdev/test'
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
                containers:
                  - name: python
                    image: python:3.8.5-slim-buster
                    command:
                      - cat
                    tty: true
                  - name: docker
                    image: docker:19.03
                    command:
                      - cat
                    tty: true
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
                DJANGO_DB_NAME = credentials('django-db-name')
                DJANGO_DB_USER = credentials('django-db-user')
                DJANGO_DB_HOST = credentials('django-db-host')
                DJANGO_DB_PORT = credentials('django-db-port')
                DJANGO_DB_PASSWORD = credentials('django-db-password')
            }
            steps {
                container('python') {
                    sh """
                      apt-get update && \
                        apt-get install --no-install-recommends -y libpq-dev git gcc libc6-dev && \
                        apt-get clean && \
                        rm -rf /var/lib/apt/lists/*
                    """
                    sh "pip install -r requirements.txt"
                    sh "cd gitrello && python manage.py test"
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
//         stage('Deploy chart') {
//             steps {
//                 container('helm') {
//                     withCredentials([file(credentialsId: 'overrides', variable: 'OVERRIDES')]) {
//                         sh "helm upgrade test --install ./helm/test -f ${OVERRIDES} --set deployment.image.tag=${tag}"
//                     }
//                 }
//             }
//         }
    }
}
