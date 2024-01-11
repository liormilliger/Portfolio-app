pipeline{
    
    agent any
    
    environment {
        ECR_USER = '644435390668.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO_URL = '644435390668.dkr.ecr.us-east-1.amazonaws.com/liorm-portfolio'
        CONFIG_REPO = 'git@github.com:liormilliger/Portfolio-config.git'
        // PUBLIC_KEY_CONTENT = credentials('liorm-portfolio-key.pem')
        IAM_ROLE = "liorm-portfolio-roles" 
    }
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')    
    }

    stages{
        stage ("Checkout") {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage ('Build App-Image') {
            steps {
                sh """ cd app
                        docker build -t liorm-portfolio:${BUILD_NUMBER} .
                """
                // echo 'UNIT TEST (PyTest within Dockerfile)'
            }
        }
        // stage ('App-Image Sanity Test') {
        //     steps{
        //         script{
        //             sh """  docker compose up --build -d
        //                 sleep 15
        //                 responsecode1 = curl -fI http://3.94.61.106
        //                 responsecode2 = curl -fI http://localhost:80
        //                 responsecode3 = curl -fI http://10.0.3.87
        //                 echo "from EC2 public ip:" responsecode1
        //                 echo "from within Jenkins:" responsecode2
        //                 echo "from EC2 private ip:" responsecode3
        //                 docker compose down
        //             """
        //         }
        //     }
        // }
        
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

        // stage ('Containers Up!') {
        //     steps{
        //         sh "docker-compose up -d"
        //     }
        // }

        stage ('Update Config Repo') {
            steps {
                echo 'CONNECT TO ${CONFIG_REPO}'
                echo 'UPDATE RELEVANT YAML FILES'
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

    //     stage('get_commit_msg') {
    //         steps {
    //             script {
    //                 env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
    //             }
    //         }
    //     }

    //     stage('Clone Terraform Repo'){
    //         when {
    //             expression { return env.GIT_COMMIT_MSG.contains("#test") }
    //         }
            
    //         steps {
    //             script {
    //                 sshagent(credentials: ['SSH-Key-for_GitLab']) {
    //                     sh "git clone git@gitlab.com:liormilliger/terraform-modules.git"
    //                 }
    //             }
    //         }
    //     }

    //     stage('Terraform apply'){
    //         steps {
    //             script {
    //                 dir("./terraform-modules"){
    //                         sh """
    //                             terraform init -migrate-state
    //                             terraform workspace new ${params.DEVELOPER_NAME}-${BUILD_NUMBER}
    //                             terraform destroy -auto-approve
    //                             terraform apply -auto-approve
    //                         """
    //                         // // Capture the EC2 public IP from Terraform output
    //                         // def initialec2PublicIp = sh(script: 'terraform output -json public_ips-1a', returnStdout: true).trim()
                            
    //                         // // Remove the first and last characters using regex
    //                         // def ec2PublicIp = initialec2PublicIp.replaceAll(/^.\s*|\s*.$/, "")
    //                         // // Export the EC2 public IP to a Jenkins environment variable
    //                         // env.EC2_PUBLIC_IP = ec2PublicIp
    //                         // // echo "EC2 Public IP: ${EC2_Public_IP}"
    //                 }
    //             }
    //         }
    //     }

    //     // stage('E2E Test') {
    //     //     steps {
    //     //         script {
    //     //             sh """
    //     //                 sleep 240
    //     //                 curl http://${env.EC2_PUBLIC_IP}/api/search?q=music

    //     //             """
    //     //         }
    //     //     }
    //     // }
    // }   

    post {
        always {
            cleanWs()
            // script{
            //     // sh 'docker rm -f $(docker ps -aq)'
            //     // sh "docker rm -f mongo app nginx"
            //     sh "docker rmi mongo:5.0 liorm-portfolio:${BUILD_NUMBER}"
            // }
        }
    }
}