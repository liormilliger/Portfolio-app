def findLatestTag(tags, releaseVersion) {
    def tagArray = tags.split('\n')
    def latestTag = null

    // Iterate through the tags to find a tag starting with releaseVersion
    for (tag in tagArray) {
        if (tag.startsWith(releaseVersion)) {
            latestTag = tag
            break
        }
    }

    return latestTag // returns latestTag variable
}

pipeline {
    
    agent any

    environment {
        ECR_USER = '644435390668.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO_URL = '644435390668.dkr.ecr.us-east-1.amazonaws.com/liorm-portfolio'
        CONFIG_REPO = 'git@github.com:liormilliger/Portfolio-config.git'
        CONFIG_REPO_DIR = 'Portfolio-config'
        APP_REPO = 'git@github.com:liormilliger/Portfolio-app.git'
        GIT_SSH_KEY = "GitHub-key"
    }

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')    
    }

    stages{

        stage ("Checkout") {
            steps {
                checkout scm
            }
        }

        stage('Version calculation') {
            steps {
                script {
                    sshagent(credentials: ["${GIT_SSH_KEY}"]) {
                        def releaseVersion = sh(script: 'cat version.txt', returnStdout: true).trim()

                        // Get all tags
                        sh 'git fetch --tags'
                        def tags = sh(script: 'git tag -l --merge | sort -r -V', returnStdout: true).trim()

                        def latestTag = findLatestTag(tags, releaseVersion)
                        def calculatedVersion = ''

                        if (latestTag) {
                            /* groovylint-disable-next-line UnusedVariable */
                            def (major, minor, patch) = latestTag.tokenize('.')
                            patch = patch.toInteger() + 1
                            calculatedVersion = "${releaseVersion}.${patch}"
                        } else {
                            calculatedVersion = "${releaseVersion}.0"
                        }

                        env.CALCULATED_VERSION = calculatedVersion
                    }
                }
            }
        }

        stage('Environment variable configuration') {
            steps {
                script {
                    REMOTE_IMG_TAG = "${ECR_REPO_URL}:${CALCULATED_VERSION}"
                    REMOTE_IMG_LTS_TAG = "${ECR_REPO_URL}:latest"
                    LOCAL_IMG_TAG = "blogapp:${CALCULATED_VERSION}"
                }
            }
        }

        stage ('Build App-Image') {
            steps {
                dir('app') {
                    sh """ 
                        docker build -t ${LOCAL_IMG_TAG} .
                    """
                }            
            }
        }

        stage("Test"){
            stages {
                stage ("Containers UP") {
                    steps {
                        echo "========CONTAINERS UP=========="
                        sh "docker-compose up -d"
                    }
                }
                stage ("Test") {
                    steps {
                        echo "========EXECUTING TESTS=========="

                        script{
                            sh """#!/bin/bash
                                for ((i=1; i<=10; i++)); do
                                    responseCode=\$(curl -s -o /dev/null -w '%{http_code}' http://localhost:80)
                                            
                                    if [[ \${responseCode} == '200' ]]; then
                                        echo "Health check succeeded. HTTP response code: \${responseCode}"
                                        break
                                    else
                                        echo "Health check failed. HTTP response code: \${responseCode}. Retrying in 5 seconds..."
                                        sleep 5
                                    fi
                                done
                            """
                        }
                    }
                }
            }

            post {
                always {
                    sh """
                        docker compose down -v
                    """
                }
            }
        }

        stage('Publish Images') {

            when {
                anyOf {
                    branch 'main'
                    expression {
                        return BRANCH_NAME.startsWith('dev')
                    }
                }
            }

            stages {
                stage("Tag Images") {
                    steps {
                        echo 'Tagging Images'

                        sh """
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_TAG}
                            docker tag ${LOCAL_IMG_TAG} ${REMOTE_IMG_LTS_TAG}
                        """
                    }
                }

                stage("Push Images") {
                    steps {
                        echo 'Pushing Images to Registry'
                        // // DO I Reallly need withCredentials??????
                        // withCredentials([[
                        //     $class: 'AmazonWebServicesCredentialsBinding',
                        //     credentialsId: 'AWS Credentials'
                        // ]]) {
                        script {
                            sh """
                                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_USER}
                                docker push ${REMOTE_IMG_TAG}
                                docker push ${REMOTE_IMG_LTS_TAG}
                                """
                        }
                        // }
                    }
                }

                stage('Git Tag & Clean') {
                    steps {
                        sshagent(credentials: ["${GIT_SSH_KEY}"]) {
                            sh """
                                git clean -f
                                git reset --hard
                                git tag ${CALCULATED_VERSION}
                                git push origin ${CALCULATED_VERSION}
                            """
                        }
                    }
                }
            }

            post {
                always {
                    sh """
                        docker rmi ${LOCAL_IMG_TAG}
                        docker rmi "${REMOTE_IMG_TAG}"
                        docker rmi "${REMOTE_IMG_LTS_TAG}"
                        docker logout ${ECR_REPO_URL}
                    """
                }
            }
        }

        stage ("Update Config-Repo") {
            when {
                anyOf {
                    branch 'main'
                    expression {
                        return BRANCH_NAME.startsWith('dev')
                    }                    
                }
            }

            stages {
                stage("Clone Config-Repo"){
                    steps {
                        cleanWs()

                        sshagent(["${GIT_SSH_KEY}"]) {

                            // Clone the configuration repository
                            sh "git clone ${CONFIG_REPO}"

                            dir(CONFIG_REPO_DIR) {

                            // Git commit and push
                                sh """
                                    git checkout main
                                    git config user.email "jenkins@example.com"
                                    git config user.name "Jenkins"

                                """
                            }
                        }
                    }
                }
                stage('Change Deployment Image') {
                    steps {
                        dir("${CONFIG_REPO_DIR}/blog-app") {
                            sh """
                                yq -i \'.blogapp.appImage = \"${REMOTE_IMG_TAG}\"\' values.yaml
                            """
                        }
                    }
                }

                stage('Push Changes') {
                    when {
                        anyOf {
                            branch 'main'
                            expression {
                                return BRANCH_NAME.startsWith('jenkins-vers')
                            }                    
                        }
                    }

                    steps {
                        sshagent(credentials: ["${GIT_SSH_KEY}"]) {
                            dir(CONFIG_REPO_DIR) {
                                sh """
                                    git add .
                                    git commit -m 'Jenkins Deploy - Build No. ${BUILD_NUMBER}, Version ${CALCULATED_VERSION}'
                                    git push origin main
                                """
                            }
                        }
                    }
                }
            }

            post {
                always {
                    cleanWs()
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            sh '''
                docker image prune -af
                docker volume prune -af
                docker container prune -f
                docker network prune -f
            '''
        }
    }
}    
