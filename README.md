# Portfolio-app

## Project Overview

This repo is a part of 3 repositories for deploying a blog application with a database using ArgoCD app-of-apps on AWS EKS using Terraform.

### Portfolio-infra at https://github.com/liormilliger/Portfolio-infra.git

with terraform IaC files that deployes AWS EKS cluster with ArgoCD

### Portfolio-config at https://github.com/liormilliger/Portfolio-config.git

with kubernetes configuration files

## About

- Portfolio-app is a development repo with dev and test options for a 3-tier application with a database and proxy-server.
- It has the application files, Dockerfiles to create images and a docker-compose file to deploy as microservices with docker-compose,
for local deployment and testing.
- It also has the Jenkinsfile for CI
To Deploy the whole infrastructure, change to Portfolio-infra and perform `terraform init`
- This repo has a webhook to Jenkins - whenever there is a push to this repo, it initiates a build, test and push of a new app image to an ECR


## Full Deployment Workflow Chart


![Workflow-Architecture](https://github.com/liormilliger/Portfolio-app/assets/64707466/477be583-fe86-4343-bee2-9209c57b2afe)


## Prerequisites

Before you begin, ensure you have the following:
- Docker and docker-compose installed
- Jenkins installed and configured with your repository
- AWS account
- AWS ECR for storing images

## Docker-compose file

The docker-compose file deploys 3 microservices - application, database and nginx
- The application service can be exposed on port 5000 (hashed) and belongs to both frontend and backend networks
- The MongoDB is exposed within the backend network on port 27017 (default) and is being injected with an init file
- The Nginx is being used both as a reverse proxy and also serves static files, and exposes the app on port 80 on the frontend network
- Nginx image has a Dockerfile that takes the static files from the app

## Usage

Deployment of the 3-tier microservices application, simply `docker compose up --build`
and check `localhost` in the browser to get the app's UI

## 3-tier Microservices Application Architecture

![app-arch (1)](https://github.com/liormilliger/Portfolio-app/assets/64707466/071a66ba-35e3-4e59-9640-ffcc52f020f2)


## Jenkinsfile
### Configuration
- Configure Jenkins with the proper credentials for your AWS account and this repo (SSH)
- Install plugins for sshagent, AWS, docker and git
- Build a Multibranch Pipeline for further development
- Configure a webhook with this repository
- See the environment section and make sure it is adjusted with your values

### Stages

- Jenkins will build an image of the app,
- Then it will build a local microservices app with the docker-compose file
- For the next stage the microservices will go through a series of tests
- If tests go well - the image will be tagged and pushed to the ECR
- Since ArgoCD listens to the `Portfolio-config` repository, and in order to maintain CD, Jenkinsfile will update the application deployment file in `Portfolio-config` with the latest image
- Next stage is giving the app some time up for development or testing purposes - change it as you wish
- And to take down the testing environment, jenkins shuts down the microservices and perform a cleanup
- NOTES - Jenkinsfile can be further developed to contain versioning and push new images by branches
- NOTES - Jenkinsfile can be further developed to send messages for success/failure of tests



## Integration with Argo CD

Jenkins is making a change in `Portfolio-Config` repo - in file /blog-app/templates/app-deployment.yaml to update the application deployment image.

As ArgoCD listens to this repository, a seamless update of the application will be performed.

## Contributing

We welcome contributions! Please read our contributing guidelines for how to propose changes.

## License

This project is licensed under the [MIT License](LICENSE).
