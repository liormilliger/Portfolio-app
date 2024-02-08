pipeline{
    
    agent any

    environment {
        ECR_USER = '644435390668.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO_URL = '644435390668.dkr.ecr.us-east-1.amazonaws.com/liorm-portfolio'
        CONFIG_REPO = 'git@github.com:liormilliger/Portfolio-config.git'
        IAM_ROLE = "liorm-portfolio-roles"
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
// insert logic for new branch or main
// for main - leave as is
// for branch - image name includes {BRANCH_NAME}:{BUILD_NUMBER}
        stage ('Build App-Image') {
            steps {
                sh """ cd app
                        docker build -t liorm-portfolio:${BUILD_NUMBER} .
                """
            }
        }

        
        stage ('Containers Up!') {
            steps{
                sh "docker-compose up -d"
            }
        }

        stage("Test"){
            steps{
                echo "========executing Test=========="
                script{
                    sh """#!/bin/bash
                                for ((i=1; i<=5; i++)); do
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
        stage ('E2E Tests') {
            steps {
                echo 'SOME TESTS TO CHECK ALL IS UP AND READY'
                echo 'docker-compoes up & API check'
            }
        }
// Build logic for branch or main
// if main - leave as is
//if branch - push to Release-ECR
        stage('Push App image to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'AWS Credentials'
                ]]) {
                        script {
                            sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_USER}"
                            sh "docker tag liorm-portfolio:${BUILD_NUMBER} ${ECR_REPO_URL}:1.0.${BUILD_NUMBER}"
                            sh "docker push ${ECR_REPO_URL}:1.0.${BUILD_NUMBER}"
                        }
                    }
            }
        }
// applies to main branch only
        stage ( 'Update Config-Repo' ) {
            steps {
                sshagent(["${GIT_SSH_KEY}"]) {

                    script {
                        // Clone the configuration repository
                        sh "git clone ${CONFIG_REPO} config-repo"

                        dir('config-repo') {
                            sh "ls -la"
                            String imageTag = "1.0.${BUILD_NUMBER}"
                            sh "sed -i 's|${ECR_REPO_URL}:1.0.[0-9]*|${ECR_REPO_URL}:${imageTag}|' blog-app/values.yaml"
                            
                           // Git commit and push
                            sh """
                                git config user.email "jenkins@example.com"
                                git config user.name "Jenkins"
                                git add blog-app/values.yaml
                                git commit -m "Update image to ${imageTag} with love, Jenkins"
                                git push origin main
                            """
                        }
                    }
                }    
            }
        }

        stage ('You got half minute to work') {
            steps{
                sh "sleep 30"
            }
        }

        stage ('Containers Down') {
            steps{
                sh "docker-compose down"
            }
        }
    }


        // stage('E2E Test') {
        //     steps {
        //         script {
        //             sh """
        //                 sleep 240
        //                 curl http://${env.EC2_PUBLIC_IP}/api/search?q=music

        //             """
        //         }
        //     }
        // }
       

    post {
        always {
            cleanWs()
            
            script {
                sh '''
                    docker rmi -f $(docker images -q)
                    docker volume rm -f $(docker volume ls -q)
                '''
            }
        }
    }
}