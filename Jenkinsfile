pipeline{
    
    agent any
    
    // environment {
    //     ECR_REPO_URL = '644435390668.dkr.ecr.us-east-1.amazonaws.com/liorm-portfolio'
    //     PUBLIC_IP = "???"
    //     // EC2_KEY = "EC2_TED_SSH"
    //     // PUBLIC_KEY_CONTENT = credentials('liorm-portfolio-key.pem')
    //     IAM_ROLE = "liorm-portfolio-roles" #attached to jenkins EC2 instance access to ECR, S3
    //     S3-BUCKET = "liorm-portfolio-tfstate-s3" 
        

    // }
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')    
    }

    stages{
        stage("Checkout") {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage ('Containerize App'){
            steps{
                sh "sudo docker-compose up --build"
            }
        }

    //     stage ('Test'){
    //         steps{
    //             sh "sleep 10"
    //             sh "curl http://localhost" 
    //         }
    //     }  
    //     stage('Build Nginx image') {
    //         steps {
    //             sh "docker build -t nginx-img -f ./Dockerfile.nginx ."
    //         }
    //     }

    //     stage('Push App image to ECR') {
    //         steps {
    //             withCredentials([[
    //                 $class: 'AmazonWebServicesCredentialsBinding',
    //                 credentialsId: 'AWS Credentials'
    //             ]]) {
    //                 script {
    //                     sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
    //                     sh "docker tag ted-search:latest ${ECR_REPO_URL}:ted-search"
    //                     sh "docker push ${ECR_REPO_URL}:ted-search"
    //                 }
    //             }
    //         }
    //     }

    //     stage('Push Nginx image to ECR') {
    //         steps {
    //             withCredentials([[
    //                 $class: 'AmazonWebServicesCredentialsBinding',
    //                 credentialsId: 'AWS Credentials'
    //             ]]) {
    //                 script {
    //                     sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
    //                     sh "docker tag nginx-img:latest ${ECR_REPO_URL}:nginx-img"
    //                     sh "docker push ${ECR_REPO_URL}:nginx-img"
    //                 }
    //             }
    //         }
    //     }  

    //     stage('Copy Files to S3') {
    //         steps {
    //             script {
    //                 // Set your AWS credentials (assuming you've already configured them in Jenkins)
    //                 withCredentials([[
    //                     $class: 'AmazonWebServicesCredentialsBinding',
    //                     credentialsId: 'AWS Credentials'
    //                 ]]) {
    //                     def bucketName = 'liorm-ted'
    //                     def s3Path = 'userdata/'
    //                     sh "aws s3 cp ./target/embedash-1.1-SNAPSHOT.jar s3://${bucketName}/${s3Path}embedash-1.1-SNAPSHOT.jar"
    //                     // sh "aws s3 cp ./Dockerfile s3://${bucketName}/${s3Path}Dockerfile"
    //                     // sh "aws s3 cp ./Dockerfile.nginx s3://${bucketName}/${s3Path}Dockerfile.nginx"
    //                     sh "aws s3 cp ./docker-compose.yaml s3://${bucketName}/${s3Path}docker-compose.yaml"
    //                     sh "aws s3 cp ./nginx.conf s3://${bucketName}/${s3Path}nginx.conf"
    //                 }
    //             }
    //         }
    //     }
   
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

    // post {
    //     always {
    //         // cleanWs()
    //         sh "docker rm -f test" 
    //     }
    }
}