# Development

## Initial Setup

This application uses a virtual environment using `pip`. Below is an example of how to create the virtual environment with a directory called venv.

```sh
python -m venv venv
```

To activate it, run:

```sh
. ./venv/bin/activate
```

To deactivate it, run

```sh
deactivate
```

The code for the Python application is located in the `src` directory. 

You can use the provided requirements.txt file to install libraries.

```sh
cd src
pip install -r requirements.txt
```

## Usage

To run the application:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
flask run
```

## Implementation Notes

This application uses Flask and SQLAlchemy to manage events. The web interface is styled using Bootstrap. 

## Testing

This project implements the following tests:

- Unit tests
- DB-based (DAO) tests

To run:

```sh
python -m pytest
```

## Developing

The schema is managed with Flask-Migrate. It supports 3 environments: test, dev and prod. These are defined in `config.py`. Below is an explanation of these environments:

- The `test` environment uses an in-memory SQLite database
- The `dev` environment uses a SQLite database persisted to a file
- The `prod` environment uses an external database such as postgres

When updating the schema, 

1. Make sure you have set your environment variables for Flask. For example:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
export RUNTIME_MODE=dev
```

2. Create a migration: `flask db migrate -m "Add a new column`

3. Apply the changes: `flask db upgrade`

Do NOT remove the instance directory.

## Running

Make sure your environment variables are set correctly.

For example, for the `dev` environment:

```sh
export FLASK_APP=app.py
export FLASK_DEBUG=True
export RUNTIME_MODE=dev
```

Then:

```sh
flask run
```

For the `prod` environment, be sure to also set DATABASE_URI. Below is the URI for the Postgres docker container.

```sh
export DATABASE_URI=postgresql://admin:secret@localhost:5432/db
```

## Running in Docker

The goals of running this app using docker are:

- Create a docker image using Dockerfile
- Use docker-compose to orchestrate containers
- Deploy our image to a remote docker registry
- Update docker-compose to use the image in the remote docker registry
- Start an EC2 instance and deploy the application to the instance

To build the docker container, run:

```sh
docker build -f docker/Dockerfile -t community-homepage .
```

To run the container, you can run:

```sh
docker run -d -p 5000:5000 --name homepage community-homepage
```

This will use SQLite as the backing database.

To see the logs:

```sh
[taro@zaxman community-homepage]$ docker logs homepage 
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3e4596be74fa, Initial migration
 * Serving Flask app 'app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 107-418-025
```

This will use the dev configuration but can be overridden. 

The docker-compose file will use Postgres as the backing database.

```sh
docker compose -f docker/docker-compose.yaml up -d
```

There are two services in the docker-compose file. The first service is the Postgres database. The second sevice runs the Flask application. Since the database needs to have the correct schema, this can take a while before it is available for use. To handle this suituation, the docker-compose file defines both a dependency asnd a healthcheck; this pattern is discussed at https://docs.docker.com/compose/how-tos/startup-order/. Furthermore, the Flask application service defines the POSTGRES_URL so that it can connect to the external database. 

To tag and push the docker image to hub.docker.com:

```sh
 docker tag community-homepage tarof429/community-homepage:1.0
 docker push tarof429/community-homepage:1.0
```

In the last step, the goal is to deploy the application to an EC2 instance. The EC2 instance can be created using the AWS console. To install docker on it, see https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-docker.html. 

Make sure the instance opens port 22 for SSH access and 5000 for web access. 

To install docker-compose, see https://github.com/docker/compose?tab=readme-ov-file#linux. Basically,

- Download the latest executable to the EC2 instance.
- Change the permission to executalbe and copy it to /usr/lib/docker/cli-plugins. 
- Run `docker compose up -d`


On the remote server, refresh the image to get the latest code changes.

```sh
docker compose down
docker compose pull
docker compose up -d
```

## Creating the webserver with Terraform

Terraform is a tool that can be used to create EC2 instances and other resources needed to deploy applications in the cloud. 

The `terraform-webserver` project is used to create an EC2 instance to which we can deploy our Flask application.

```sh
cd terraform-webserver
terraform plan
terraform apply -auto-approve
```

Afterwards, you need to:

- Install docker
= Install docker-compose
- Copy the docker-compose file to the server
- Run the server and related database using docker-compose

## Configuring the webserver with Ansible

Ansible can be used to configure the server. Since the server is running in AWS, we need to install the amazon.aws collection, which requires some additional packages so that it can talk to AWS using APIs.

```sh
sudo pacman -S ansible
sudo pacman -S python-boto3 python-botocore
ansible-galaxy collection install amazon.aws
```

We can use dynamic inventory to discover any EC2 instances. Enable the dynamic inventory plugin by adding the following in ansible.cfg:

```sh
enable_plugins = aws_ec2
```

Next, we're going to create a plugin configuration; the filename must contain `aws_ec2` or the plugin will not be able to find it. 

```sh
$ ansible-inventory -i inventory_aws_ec2.yaml --list
```

Alternatively (for shorter output):

```sh
$ ansible-inventory -i inventory_aws_ec2.yaml --graph
@all:
  |--@ungrouped:
  |--@aws_ec2:
  |  |--ip-10-0-10-139.us-west-2.compute.internal
  |--@tag_Name_prod_webserver:
  |  |--ip-10-0-10-139.us-west-2.compute.internal
  |--@instance_type_t2_micro:
  |  |--ip-10-0-10-139.us-west-2.compute.internal
```

Note the inventory name with the tag.

In case you have not configured terraform to assign public DNS names, these are private DNS names. And in that case we would not be able to connect to the servers from outside the VPC. The fix is obviously to configure Terraform to assign public DNS names and this would be done within the **aws_vpc** resource. 

For ansible to connect to these servers, we could configure the playbooks to use the **aws_ec2** group. 

For example:

```sh
$ ansible-playbook -i inventory_aws_ec2.yaml sshping.yaml 

PLAY [Ping server] *************************************************************
[WARNING]: Found variable using reserved name 'tags'.
Origin: <unknown>

tags


TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Ping] ********************************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com] => {
    "msg": "Ping!"
}

PLAY RECAP *********************************************************************
ec2-1-2-3-4.us-west-2.compute.amazonaws.com : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

To install docker, docker-compose, and add ec2-user to the docker group, use the install-docker-webserver playbook.

```sh
$ ansible-playbook -i inventory_aws_ec2.yaml 1-install-docker-webserver.yaml 

PLAY [Install docker] **********************************************************
[WARNING]: Found variable using reserved name 'tags'.
Origin: <unknown>

tags


TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Install docker] **********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Start docker daemon] *****************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

PLAY [Install docker-compose] **************************************************

TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Create docker-compose directory] *****************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Get architecture of remote server] ***************************************
changed: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Download and install docker-compose] *************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

PLAY [Add ec2-user to docker group] ********************************************

TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Add ec2-user to docker group] ********************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Reconnect to server session] *********************************************

PLAY [Log into DockerHub] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Login to dockerhub] ******************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

PLAY [Test docker pull] ********************************************************

TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Pull hello-world] ********************************************************
changed: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

PLAY RECAP *********************************************************************
ec2-1-2-3-4.us-west-2.compute.amazonaws.com : ok=13   changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

This playbook requires authentication to docker hub; create a file called `myvars` and populate it with the following:

```
docker_user: <some value>
docker_password: <access token>
```

This file should NOT be committed to git.

To deploy the webapp, use the playbook `2-deploy-webapp-to-dc2.yaml`.

This playbook ends with a message that explains how to access the webapp.

```sh
$ ansible-playbook 2-deploy-webapp-to-ec2.yaml -i inventory_aws_ec2.yaml 

PLAY [Start docker containers] *************************************************
[WARNING]: Found variable using reserved name 'tags'.
Origin: <unknown>

tags


TASK [Gathering Facts] *********************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com]

TASK [Show final message] ******************************************************
ok: [ec2-1-2-3-4.us-west-2.compute.amazonaws.com] => {
    "msg": "Web application will be available at http://1.2.3.4:5000"
}

PLAY RECAP *********************************************************************
ec2-1-2-3-4.us-west-2.compute.amazonaws.com : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## Creating the Jenkins server with KVM

Running Jenkins on a VM is a great way to get familiar with CI/CD without incurring AWS cloud usage costs. On a Linux machine, KVM is a grat way to create VMs. This does require additional setup however, and will not be explained in detail here. Below are resources to get started with KVM on ArchLinux (which I have authored):

- https://github.com/tarof429/stuckathome has a section that describes how to setup KVM
- https://github.com/tarof429/magarin has scripts to create VMs with KVM

A VM with 4 GB RAM and 2 CPU is recommended, and either Ubuntu 22 or 24 should be fine, provided that the OS is still supported.

## Installing docker on the KVM with Ansible

Once the server is running, we need to add the user who will run Jenkins. This user will run Jenkins using. The `3-install-docker-on-jenkins-server.yaml` playbook:

- Installs docker and docker-compose
- Create a user called `jenkins` and add it to the docker group
- Login to dockerhub
- Pull a docker image

To run:

```sh
ANSIBLE_CONFIG=ansible_kvm.cfg ansible-playbook 3-install-docker-on-jenkins-server.yaml 
```

It's vital that the `-i` flag is passed to `sudo` when running docker commands so that the environment variables are set correctly.

## Installing Jenkins on the KVM

Before running the Jenkins docker container, you should know that there are 2 wqys to run docker containers: rootless and rootful. 

### Rootful docker method

For a rootful docker, we mount the docker socket on the host to the container. 

First, note the default permissions for the socker:

```sh
jenkins@jenkins-server:~$ ls -l /var/run/docker.sock 
srw-rw---- 1 root docker 0 Jan 12 22:25 /var/run/docker.sock
```

Change the permissions for the docker socket on the host:

```sh
chmod 666 /var/run/docker.sock
```

Change the user to jenkins and run the container:

```sh
su - jenkins
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins --restart=on-failure -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock jenkins/jenkins:lts-jdk21
```

In our Jenkins jobs, we need to run docker commands such as `docker pull` and `docker run`. Install docker so we can use the docker CLI within the container. Below is a quick way to install docker daemon.

```sh
docker exec -ti -u 0 jenkins bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh ./get-docker.sh
```

### Rootless docker method

Alternatively we can setup rootless docker. However, since docker is designed to be run as a system service, it is very tricky to get docker working for this setup. Podman addresses this limitation, but will not be explored here. 

### Logging into Jenkins

Once the container is running, access the web interface at http://192.168.1.30:8080. It will prompt for the admin's password. To retrieve the pasword, login to the container as root and examine the contents of the file containing the pasword:

```sh
docker exec -ti -u 0 jenkins bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

Install the recommended plugins, and the UI should be ready to use.

## Creating an initial pipeline script

The first pipeline script `1-Jenkinsfile` does the following:

- Run tests
- Build the docker image
- Push the docker image

For convenience, we will build a separate docker image that will run the tests automatically. 

As required, create credentials in Jenkins so that Jenkins can push the docker image.

A couple notes on issues that I ran into and how they were resolved:

- The initial docker image that I used for for Jenkins was based on JDK 17. But since this image is deprecated, I upgraded to the image based on JDK 21. I thought that was all I had to do, but later realized that docker had to be reinstalled and the permissions on the docker sockety had to be fixed.

- I added github credentials in Jenkins but I had used the token type instead of username/password. The username/password is the only credential type that will work.

- Jenkins warned that there could be a memory leak if I didn't use the `def` keyword in front of variables.

## Dealing with versions

One potential issue with our pipeline is that we always push and pull the image with the `latest` tag. When dealing with images in production, we never want to rely on this tag. Rather, we need some way to work with clearly identifiable tags. In some scenarios, this could come from the version of the project stored in a file like `pom.xml` if this wew a Maven project. For Python, `setuptools` provides a method for tracking versions for distribution to Pypi. However, in our project we could opt for an even simpler soltion and just use the git commmit hash. This has the advantage that there are no extra files to parse and manage.

The `2-Jenkinsfile` pipeline script sets the image tag to the git version. However, there were several issues that had to be resolved before getting it to work. 

My first attempt tried to set the git version to ba variable:

```groovy
stage("Build image") {
    steps {
        script {
            def IMAGE_TAG = "$(git describe --tags --always)"

            sh "docker build -f docker/Dockerfile -t ${env.IMAGE_PREFIX}:${IMAGE_TAG} ."
        }
    }
}
```

The problem is that groovy cannot run shell commands like this. But further attempts to resolve that issue still did not work. In the final version, we define the variable before the pipeline so that it can be reused across multiple stages. We also define or set the variable in a stage. Moreover, we trim the string so that it doesn't have a newline. 

```groovy
  stage("Get git veresion") {
      steps {
          script {
              IMAGE_TAG = sh(
                  script: "git rev-parse --short=7 HEAD",
                  returnStdout: true
              ).trim()
          }
      }
  }
```

## Using Groovy Scripts

At times, it is convenient to use functions inside Jenkins pipelines. To mdo this, we can create groovy scripts. These are scripts stored in the same git repository as the pipeline scripts written in groovy.

For example, lets say we want to define a function to help us troubleshoot environment issues. See `app.groovy` for an example groovy script, and `3-Jenkinsfile` to see how to load and use it. A sample output is showen below.

```sh
Showing environment
[Pipeline] sh
+ which docker
/usr/bin/docker
[Pipeline] sh
+ whoami
jenkins
[Pipeline] sh
+ pwd
/var/jenkins_home/workspace/community-homepage
```

## Variables

Earlier we defined variables to define the image name and to determine whether tests passed or not. Jenkins has a few other variable types. These include builtin  environment variables and parameters. The builtin variables are provided by bJenkins and include things like BUILD_NUMBER and WORKSPACE; see https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables. Jobs can also be parameterized so that when the build is triggered, the user can provide a variable value. 

A special type of Jenkins job called the multibranch pipeline can be used to take advantage of the BRANCH_NAME variable. This job scans git repositories and  creates child jobs for each of the remote branches. In this kind of job, we can use BRANCH_NAME to trigger certain stages only if it is part of a particular branch.

See `4-Jenkinsfile` for an example.

## Shared Libraries

A common practice is to create a shared library that can be reused across multiple pipeline scripts. See `5-Jenkinsfile` for an example. There are multiple ways to load shared libraries; what we have done is load the library and use steps in `vars/*.groovy`.  The shared library is commited to git at https://github.com/tarof429/community-homepage-shared-lib.git and in `Jenkins | System` we make this library globally available to any pipeline jobs.

## Creating the Jenkins server with Terraform

## Creating the CI/CD pipeline

## References

https://flask-migrate.readthedocs.io/en/latest/
