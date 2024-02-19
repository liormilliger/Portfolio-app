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

                        env.LATEST_TAG = latestTag
                        env.RELEASE_VERSION = releaseVersion
                        env.CALCULATED_VERSION = calculatedVersion
                    }
                }
            }
        }

        stage('Environment variable configuration') {
            steps {
                script {
                    // main
                    def remoteRegistry = "${ECR_REPO_URL}"

                    // // devops
                    // if (BRANCH_NAME =~ /^devops.*/) {
                    //     remoteRegistry = '644435390668.dkr.ecr.eu-central-1.amazonaws.com/taskit-test'
                    // }

                    // Remote
                    REMOTE_REGISTRY = "${remoteRegistry}"
                    REMOTE_IMG_TAG = "${REMOTE_REGISTRY}:${CALCULATED_VERSION}"
                    REMOTE_IMG_LTS_TAG = "${REMOTE_REGISTRY}:latest"

                    // Local
                    LOCAL_IMG_TAG = "localhost/taskit:${CALCULATED_VERSION}"
                    TEST_NET = "taskit-nginx-net-${CALCULATED_VERSION}"
                }
            }
        }

        stage('Debug') {
            steps {
                echo '---------------DEBUG----------------------'

                echo "LATEST_TAG: ${LATEST_TAG}"
                echo "RELEASE_VERSION: ${RELEASE_VERSION}"
                echo "CALCULATED_VERSION: ${CALCULATED_VERSION}"
                echo "REMOTE_REGISTRY: ${REMOTE_REGISTRY}"
                echo "REMOTE_IMG_TAG: ${REMOTE_IMG_TAG}"
                echo "REMOTE_IMG_LTS_TAG: ${REMOTE_IMG_LTS_TAG}"
                echo "LOCAL_IMG_TAG: ${LOCAL_IMG_TAG}"
                echo "TEST_NET: ${TEST_NET}"

                echo '---------------DEBUG----------------------'
            }
        }


        stage ('Build App-Image') {
            steps {
                    sh """ 
                        cd app
                        docker build -t ${LOCAL_IMG_TAG} .
                    """
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
                // anyOf {
                //     branch 'main'
                //     expression {
                //         return BRANCH_NAME.startsWith('devops')
                //     }
                // }
                branch 'main'
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
                        // DO I Reallly need withCredentials??????
                        withCredentials([[
                            $class: 'AmazonWebServicesCredentialsBinding',
                            credentialsId: 'AWS Credentials'
                        ]]) {
                            script {
                                sh """
                                    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_USER}
                                    docker push ${REMOTE_IMG_TAG}
                                    docker push ${REMOTE_IMG_LTS_TAG}
                                    """
                            }
                        }
                    }
                }

                stage('Git Tag & Clean') {
                    steps {
                        sshagent(credentials: ["${GIT_SSH_KEY}"]) {
                            // is it necessary to have both clean and reset?????
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
                        docker logout ${REMOTE_REGISTRY}
                    """
                }
            }
        }



// applies to main branch only
        
        stage ("Update Config-Repo") {
            when {
                anyOf {
                    branch 'main'
                    // expression {
                    //     return BRANCH_NAME.startsWith('devops')
                    // }                    
                }
            }

            stages {
                stage("Clone Config-Repo"){
                    steps {
                        cleanWs()

                        sshagent(["${GIT_SSH_KEY}"]) {

                            // Clone the configuration repository
                            sh "git clone ${CONFIG_REPO} config-repo"

                            dir('config-repo') {

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
                        dir("${CONFIG_REPO}/blog-app") {
                            sh """
                                yq -yi \'.blogapp.appImage = \"${REMOTE_IMG_TAG}\"\' values.yaml
                            """
                        }
                    }
                }

                stage('Push Changes') {
                    when {
                        branch 'main'
                    }

                    steps {
                        sshagent(credentials: ["${GITOPS_REPO_CRED_ID}"]) {
                            dir(GITOPS_REPO_NAME) {
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
