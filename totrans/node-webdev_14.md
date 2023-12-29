Deploying Node.js Microservices with Docker

Now that we've experienced the traditional Linux way to deploy an application, let's turn to Docker, which is a popular new way to manage application deployment.

Docker ([http://docker.com](http://docker.com)) is a cool new tool in the software industry. It is described as *an open platform for distributed applications for developers and sysadmins*. It is designed around Linux containerization technology and focuses on describing the configuration of software on any variant of Linux.

A Docker container is a running instantiation of a Docker image. A Docker image is a bundle containing a specific Linux OS, system configuration, and application configuration. Docker images are described using a **Dockerfile**, which is a fairly simple-to-write script describing how to build a Docker image. The Dockerfile starts by specifying a *base image* from which to build, meaning we derive Docker images from other images. The rest of the Dockerfile describes what files to add to the image, which commands to run in order to build or configure the image, which network ports to expose, which directories to mount in the image, and more.

Docker images are stored on a Docker Registry server, with each image stored in its own repository. The largest registry is Docker Hub, but there are also third-party registries available, including registry servers that you can install on your own hardware. Docker images can be uploaded to a repository, and, from the repository, deployed to any Docker server.

We instantiate a Docker image to launch a Docker container. Typically, launching a container is very fast, and often, containers are instantiated for a short time and then discarded when no longer needed.

A running container feels like a virtual server running on a virtual machine. However, Docker containerization is very different from a virtual machine system such as VirtualBox or Multipass. A container is not a virtualization of a complete computer. Instead, it is an extremely lightweight shell creating the appearance of an installed OS. For example, the processes running inside the container are actually running on the host OS with certain Linux technologies (cgroups, kernel namespaces, and so on) creating the illusion of running a specific Linux variant. Your host OS could be Ubuntu and the container OS could be Fedora or OpenSUSE, or even Windows; Docker makes it all work. 

While Docker is primarily targeted at x86 flavors of Linux, it is available on several ARM-based OSes, as well as other processors. You can even run Docker on single-board computers, such as Raspberry Pi, for hardware-oriented **Internet of Things** (**IoT**) projects.

The Docker ecosystem contains many tools, and their number is increasing rapidly. For our purposes, we'll focus on the following two tools:

*   **Docker Engine**: This is the core execution system that orchestrates everything. It runs on a Linux host system, exposing a network-based API that client applications use to make Docker requests, such as building, deploying, and running containers.
*   **Docker Compose**: This helps you define, in a single file, a multi-container application with all of its dependencies defined.

There are other tools closely associated with Docker, such as Kubernetes, but it all starts with building a container to house your application. By learning about Docker, we learn how to containerize an application, a skill we can use with both Docker and Kubernetes. 

Learning how to use Docker is a gateway to learning about other popular systems, such as Kubernetes or AWS ECS. These are two popular orchestration systems for managing container deployments at a large scale on cloud-hosting infrastructure. Typically, the containers are Docker containers, but they are deployed and managed by other systems, whether that is Kubernetes, ECS, or Mesos. That makes learning how to use Docker an excellent starting point for learning these other systems.

In this chapter, we will cover the following topics:

*   Installing Docker on our laptop
*   Developing our own Docker containers and using third-party containers
*   Setting up the user authentication service and its database in Docker
*   Setting up the Notes service and its database in Docker
*   Deploying MySQL instances in Docker infrastructure, and data persistence for applications such as databases in Docker
*   Using Docker Compose to describe the Docker deployment of a full application
*   Scaling container instances in Docker infrastructure and using Redis to mitigate scaling issues

The first task is to duplicate the source code from the previous chapter. It's suggested that you create a new directory, `chap11`, as a sibling of the `chap10` directory and copy everything from `chap10` to `chap11`.

By the end of this chapter, you will have a solid grounding of using Docker, creating Docker containers, and using Docker Compose to manage the services required by the Notes application.

With the help of Docker, we will design, on our laptop, the system shown in the diagram in [Chapter 10](176ce11c-dd6f-4ebf-ba14-529be6db28da.xhtml), *Deploying Node.js Applications to Linux Servers*. That chapter, this one, and [Chapter 12](8551a26c-6834-4df6-b392-60a15c20f6ff.xhtml), *Deploying a Docker Swarm to AWS EC2 with Terraform*, form an arc covering three styles of Node.js deployment to servers. 

# Setting up Docker on your laptop or computer

The best place to learn how to install Docker on your laptop is the Docker documentation. What we're looking for is the Docker **Community Edition** (**CE**), which is all we need:

*   macOS installation: [https://docs.docker.com/docker-for-mac/install/](https://docs.docker.com/docker-for-mac/install/)
*   Windows installation: [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)
*   Ubuntu installation: [https://docs.docker.com/install/linux/docker-ce/ubuntu/](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Instructions are also available for several other distributions. Some useful post-install Linux instructions are available at [https://docs.docker.com/install/linux/linux-postinstall/](https://docs.docker.com/install/linux/linux-postinstall/).

Docker runs natively on Linux, and the installation is simply the Docker daemon and command-line tools. To run Docker on macOS or Windows, you need to install the Docker for Windows or Docker for Mac applications. These applications manage a virtual Linux environment in a lightweight virtual machine, within which is a Docker Engine instance running on Linux. In the olden days (a few years ago), we had to handcraft that setup. Thanks must be given to the Docker team, who have made this as easy as installing an application, and all the complexity is hidden away. The result is very lightweight, and Docker containers can be left running in the background with little impact. 

Let's now learn how to install Docker on a Windows or macOS machine.

## Installing and starting Docker with Docker for Windows or macOS

The Docker team has made installing Docker on Windows or macOS very easy. You simply download an installer and, as with most other applications, you run the installer. It takes care of installation and provides you with an application icon that is used to launch Docker. On Linux, the installation is a little more involved, so it is best to read and follow the official instructions.

Starting Docker for Windows or macOS is very simple, once you've followed the installation instructions. You simply find and double-click on the application icon. There are settings available so that Docker automatically launches every time you start your laptop.

On both Docker for Windows and Docker for Mac, the CPU must support **virtualization**. Bundled inside Docker for Windows and Docker for Mac is an ultra-lightweight hypervisor, which, in turn, requires virtualization support from the CPU. 

For Windows, this may require a BIOS configuration. Refer to [https://docs.docker.com/docker-for-windows/troubleshoot/#virtualization-must-be-enabled](https://docs.docker.com/docker-for-windows/troubleshoot/#virtualization-must-be-enabled) for more information.

For macOS, this requires hardware from 2010 or later, with Intel's hardware support for **Memory Management Unit** (**MMU**) virtualization, including **Extended Page Tables** (**EPTs**) and unrestricted mode. You can check for this support by running `sysctl kern.hv_support`. It also requires macOS 10.11 or later.

Having installed the software, let's try it out and familiarize ourselves with Docker.

## Familiarizing ourselves with Docker

With the setup accomplished, we can use the local Docker instance to create Docker containers, run a few commands, and, in general, learn how to use it.

As in so many software journeys, this one starts with *Hello World*:

[PRE0]js\1

The `Unable to find image` phrase means that Docker has not downloaded the named image yet. Therefore, it downloaded not only the Ubuntu image but also the images it depends on. Any Docker image can be built in layers, meaning we always define an image in terms of a base image. In this instance, we see that the Ubuntu image required four layers in total.

Images are identified by an SHA-256 hash, and there is both a long-form identifier and a short-form identifier. We can see both the long and short identifiers in this output.

The `docker run` command downloads an image, configures it for execution, and executes the image. The `-it` flag means to run the image interactively in the terminal.

In the `docker run` command line, the part after the image name to execute is passed into the container as command options to execute. In this case, the command option says to run `bash`, which is the default command shell. Indeed, we were given a command prompt and can run Linux commands.

You can query your computer to see that while the `hello-world` container has executed and finished, it still exists:

![](img/fc4a87f1-2ca6-44b6-aa62-a8b206cf9a98.png)

The `docker ps` command lists the running Docker containers. As we see here, the `hello-world` container is no longer running, but the Ubuntu container is. With the `-a` switch, `docker ps` also shows those containers that exist but are not currently running. 

The last column is the container name. Since we didn't specify a container name when launching the container, Docker created a semi-random name for us.

When you're done using a container, you can clean up with the following command:

[PRE1]js\1

It's also possible to specify the hex ID. However, it is, of course, more user friendly to have a name for the container than a hex ID. When creating a container, it's easy to specify any container name you like.

We've installed Docker on our laptop or computer and tried a couple of simple commands to familiarize ourselves with Docker. Let's now get down to some work. We'll start by setting up the user authentication service in Docker containers.

# Setting up the user authentication service in Docker

With all that theory spinning around in our heads, it's time to do something practical. Let's start by setting up the user authentication service. We'll call this AuthNet, and it comprises a MySQL instance to store the user database, the authentication server, and a private subnet to connect them.

It is best for each container to focus on providing one service. Having one service per container is a useful architectural decision because we can focus on optimizing each container for a specific purpose. Another rationale has to do with scaling, in that each service has different requirements to satisfy the traffic it serves. In our case, we might need a single MySQL instance, and 10 user authentication instances, depending on the traffic load. 

There is a large library of predefined Docker images available on Docker Hub ([https://hub.docker.com](https://hub.docker.com)). It is best to reuse one of those images as a starting point to build our desired service.

The Docker environment lets us not only define and instantiate Docker containers but also the networking connections between containers. That's what we meant by a *private subnet* earlier. With Docker, we not only manage containers, but we can also configure subnets, data storage services, and more.

In the next few sections, we'll carefully dockerize the user authentication service infrastructure. We'll learn how to set up a MySQL container for Docker and launch a Node.js service in Docker.

Let's start by learning how to launch a MySQL container in Docker.

## Launching a MySQL container in Docker

Among the publicly available Docker images, there are over 11,000 available for MySQL. Fortunately, the image provided by the MySQL team, `mysql/mysql-server`, is easy to use and configure, so let's use that. 

A Docker image name can be specified, along with a *tag* that is usually the software version number. In this case, we'll use `mysql/mysql-server:8.0`, where `mysql/mysql-server` is the image repository URL, `mysql-server` is the image name, and `8.0` is the tag. The MySQL 8.x release train is the current version as of the time of writing. As with many projects, the MySQL project tags the Docker images with the version number.

Download the image, as follows:

[PRE2]js\1

There are two images currently available—the `mysql-server` image we just downloaded and the `hello-world` image we ran earlier.

We can remove unwanted images with the following command:

[PRE3]js\1

The `docker run` command takes an image name, along with various arguments, and launches it as a running container.

We started this service in the foreground, and there is a tremendous amount of output as MySQL initializes its container. Because of the `--name` option, the container name is `mysql`. Using an environment variable, we tell the container to initialize the `root` password.

Since we have a running server, let's use the MySQL CLI to make sure it's actually running. In another window, we can run the MySQL client inside the container, as follows:

[PRE4]js\1

This closes out and cleans up the container we created. To reiterate the point made earlier, the database in that container went away. If that database contained critical information, you just lost it, with no chance of recovering the data.

Before moving on, let's discuss how this impacts the design of our services.

## The ephemeral nature of Docker containers

Docker containers are designed to be easy to create and easy to destroy. In the course of kicking the tires, we've already created and destroyed three containers.

In the olden days (a few years ago), setting up a database required the provisioning of specially configured hardware, hiring a database admin with special skills, and carefully optimizing everything for the expected workload. In the space of a few paragraphs, we just instantiated and destroyed three database instances. What a brave new world this is!

In terms of databases and Docker containers, the database is relatively eternal, and the Docker container is ephemeral. Databases are expected to last for years, or perhaps even decades. In computer years, that's practically immortal. By contrast, a Docker container that is used and then immediately thrown away is merely a brief flicker of time compared to the expected lifetime of a database. 

Those containers can be created and destroyed quickly, and this gives us a lot of flexibility. For example, orchestration systems, such as Kubernetes or AWS ECS, can automatically increase or decrease the number of containers to match traffic volume, restart containers that crash, and more.

But where does the data in a database container live? With the commands we ran in the previous section, the database data directory lives inside the container. When the container was destroyed, the data directory was destroyed, and any data in our database was vaporized. Obviously, this is not compatible with the life cycle requirements of the data we store in a database.

Fortunately, Docker allows us to attach a variety of mass storage services to a Docker container. The container itself might be ephemeral, but we can attach eternal data to the ephemeral container. It's just a matter of configuring the database container so that the data directory is on the correct storage system.

Enough theory, let's now do something. Specifically, let's create the infrastructure for the authentication service.

## Defining the Docker architecture for the authentication service

Docker supports the creation of virtual bridge networks between containers. Remember that a Docker container has many of the features of an installed Linux OS. Each container can have its own IP address and exposed ports. Docker supports the creation of what amounts to a virtual Ethernet segment, called a **bridge network**. These networks live solely within the host computer and, by default, are not reachable by anything outside the host computer.

A Docker bridge network, therefore, has strictly limited access. Any Docker containers attached to a bridge network can communicate with other containers attached to that network and, by default, that network does not allow external traffic. The containers find each other by hostname, and Docker includes an embedded DNS server to set up the hostnames required. That DNS server is configured to not require dots in domain names, meaning the DNS/hostname of each container is simply the container name. We'll find later that the hostname of the container is actually `container-name.network-name`, and that the DNS configuration lets you skip using the `network-name` portion of the hostname. This policy of using hostnames to identify containers is Docker's implementation of service discovery.

Create a directory named `authnet` as a sibling to the `users` and `notes` directories. We'll be working on `authnet` in that directory.

In that directory, create a file—`package.json`—which we'll use solely to record commands for managing AuthNet:

[PRE5]js\1

This creates a Docker bridge network. The long coded string is the identifier for this network. The `docker network ls` command lists the existing networks in the current Docker system. In addition to the short hex ID, the network has the name we specified.

Look at details regarding the network with this command:

[PRE6]js\1

This command lets us remove a network from the Docker system. However, since we need this network, rerun the command to recreate it.

We have explored setting up a bridge network, and so our next step is to populate it with a database server.

## Creating the MySQL container for the authentication service

Now that we have a network, we can start connecting containers to that network. In addition to attaching the MySQL container to a private network, we'll be able to control the username and password used with the database, and we'll also give it external storage. That will correct the issues we named earlier.

To create the container, we can run the following command:

[PRE7]js\1

In other words, Docker lets you mount not only a directory but also a single file.

The command line follows this pattern:

[PRE8]js\1

This will ensure that you are starting with a fresh database each time, as well as ensuring that the container initialization runs. 

This also suggests an administrative pattern to follow. Any time you wish to update to a later MySQL release, simply stop the container, leaving the data directory in place. Then, delete the container and re-execute the `docker run` command with a new `mysql/mysql-server` tag. That will cause Docker to recreate the container using a different image, but using the same data directory. Using this technique, you can update the MySQL version by pulling down a newer image.

Once you have the MySQL container running, type this command:

![](img/f8b581a3-5b69-4a4c-9725-32697e2a774b.png)

This will show the current container status. If we use `docker ps -a`, we see that the `PORTS` column says `0.0.0.0:3306->3306/tcp, 33060/tcp`. That says that the container is listening to access from anywhere (`0.0.0.0`) to port `3306`, and this traffic will connect to port `3306` inside the container. Additionally, there is a port `33060` that is available, but it is not exposed outside the container.

Even though it is configured to listen to the whole world, the container is attached to `authnet`, which limits where connections can come from. Limiting the scope of processes that can attach to the database is a good thing. However, since we used the `-p` option, the database port is exposed to the host, and it's not as secure as we want. We'll fix this later.

### Security in the database container

A question to ask is whether setting the `root` password like this is a good idea. The `root` user has broad access to the entire MySQL server, where other users, such as `userauth`, have limited access to the given database. Since one of our goals is security, we must consider whether this has created a secure or insecure database container.

We can log in as the `root` user with the following command:

[PRE9]js\1

A connection to a MySQL server includes a user ID, a password, and the source of the connection. This connection might come from inside the same computer, or it might come over a TCP/IP socket from another computer. To approve the connection, the server looks in the `mysql.user` table for a row matching the `user`, `host` (source of connection), and `password` fields. The username and password are matched as a simple string comparison, but the host value is a more complex comparison. Local connections to the MySQL server are matched against rows where the host value is `localhost`.

For remote connections, MySQL compares the IP address and domain name of the connection against entries in the `host` column. The `host` column can contain IP addresses, hostnames, or wildcard patterns. The wildcard character for SQL is `%`. A single `%` character matches against any connection source, while a pattern of `172.%` matches any IP address where the first IPv4 octet is `172`, or `172.20.%.%` matches any IP address in the `172.20.x.x` range.

Therefore, since the only row for `userauth` specifies a host value of `%`, we can use `userauth` from anywhere. By contrast, the `root` user can only be used with a `localhost` connection.

The next task is to examine the access rights for the `userauth` and `root` user IDs:

[PRE10]js\1

We've demonstrated four modes of accessing the database, showing that indeed, the `userauth` ID can be accessed either from the same container or from a remote container, while the `root` ID can only be used from the local container.

Using `docker run --it --rm ... container-name ..` starts a container, runs the command associated with the container, and then exits the container and automatically deletes it when it's done.

Therefore, with those last two commands, we created a separate `mysql/mysql-server:8.0` container, connected to `authnet`, to run the `mysql` CLI program. The `mysql` arguments are to connect using the given username (`root` or `userauth`) to the MySQL server on the host named `db-userauth`. This demonstrates connecting to the database from a separate connector and shows that we can connect remotely with the `userauth` user, but not with the `root` user.

Then, the final access experiment involves leaving off the `--network` option:

[PRE11]js\1

In other words, the `authnet` network has the `172.20.0.0/16` network number, and the `db-userauth` container was assigned the `172.20.0.2` IP address. This level of detail is rarely important, but it is useful on the first occasion to carefully examine the setup so that we understand what we're dealing with.

There is a gaping security issue that violates our design. Namely, the database port is visible to the host, and therefore, anyone with access to the host can access the database. This happened because we used `-p 3306:3306` in a misguided belief that this was required so that `svc-userauth`, which we'll build in the next section, can access the database. We'll fix this later by removing that option.

Now that we have the database instance set up for the authentication service, let's see how to Dockerize it.

## Dockerizing the authentication service

The word *Dockerize* means to create a Docker image for a piece of software. The Docker image can then be shared with others or be deployed to a server. In our case, the goal is to create a Docker image for the user authentication service. It must be attached to `authnet` so that it can access the database server we just configured in the `db-userauth` container.

We'll name this new container `svc-userauth` to indicate that this is the user authentication REST service, while the `db-userauth` container is the database.

Docker images are defined using Dockerfiles, which are files to describe the installation of an application on a server. They document the setup of the Linux OS, installed software, and configuration required in the Docker image. This is literally a file named `Dockerfile`, containing Dockerfile commands. Dockerfile commands are used to describe how the image is constructed.

Refer to [https://docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/) for the documentation. 

### Creating the authentication service Dockerfile 

In the `users` directory, create a file named `Dockerfile` containing the following content:

[PRE12]js\1

The difference is that instead of `localhost` as the database host, we use `db-userauth`. Earlier, we explored the `db-userauth` container and determined that this was the hostname of the container. By using `db-userauth` in this file, the authentication service will use the database in the container.

The `EXPOSE` command informs Docker that the container listens on the named TCP port. This does not expose the port beyond the container. The `-p` flag is what exposes a given port outside the container.

Finally, the `CMD` command documents the process to launch when the container is executed. The `RUN` commands are executed while building the container, while `CMD` says what's executed when the container starts.

We could have installed `PM2` in the container, and then used a `PM2` command to launch the service. However, Docker is able to fulfill the same function because it automatically supports restarting a container if the service process dies.

### Building and running the authentication service Docker container

Now that we've defined the image in a Dockerfile, let's build it.

In `users/package.json`, add the following line to the `scripts` section:

[PRE13]js\1

The `docker build` command builds an image from a Dockerfile. Notice that the build executes one step at a time, and that the steps correspond exactly to the commands in the Dockerfile.

Each step is stored in a cache so that it doesn't have to be rerun. On subsequent builds, the only steps executed are the step that changed and all subsequent steps.

In `authnet/package.json`, we require quite a few scripts to manage the user authentication service:

[PRE14]js\1

This option requires absolute pathnames and specifying the path this way works on Windows.

Another thing to notice is the absence of the `-p 3306:3306` option. It was determined that this was not necessary for two reasons. First, the option exposed the database in `db-userauth` to the host, when our security model required otherwise, and so removing the option got us the desired security. Second, `svc-userauth` was still able to access the `db-userauth` database after this option was removed.

With these commands, we can now type the following to build and then run the containers:

[PRE15]js\1

This stops and starts both containers making up the user authentication service.

We have created the infrastructure to host the user authentication service, plus a collection of scripts to manage the service. Our next step is to explore what we've created and learn a few things about the infrastructure Docker creates for us.

## Exploring AuthNet

Remember that AuthNet is the connection medium for the authentication service. To understand whether this network provides the security gains we're looking for, let's explore what we just created:

[PRE16]js\1

The `/userauth` directory is inside the container and contains the files placed in the container using the `COPY` command, plus the installed files in `node_modules`:

[PRE17]js\1

The process listing is interesting to study. Process `PID 1` is the `node ./user-server.mjs` command in the Dockerfile. The format we used for the `CMD` line ensured that the `node` process ended up as process 1\. This is important so that process signals are handled correctly, allowing Docker to manage the service process correctly. The tail end of the following blog post has a good discussion of the issue:

[https://www.docker.com/blog/keep-nodejs-rockin-in-docker/](https://www.docker.com/blog/keep-nodejs-rockin-in-docker/)

A `ping` command proves that the two containers are available as hostnames matching the container names:

[PRE18]js\1

As with `authnet`, this is just the starting point as we have several more scripts to add.

Let's go ahead and create the `frontnet` bridge network:

[PRE19]js\1

This is largely the same as for `db-userauth`, with the word `notes` substituted for `userauth`. Remember that on Windows the -`-mount` option requires a Windows-style absolute pathname.

Let's now run the script:

[PRE20]js\1

Since `db-notes` is on a different network segment, we've achieved separation. But we can notice something interesting. The `ping` command tells us that the full domain name for `db-userauth` is `db-userauth.authnet`. Therefore, it stands to reason that `db-notes` is also known as `db-notes.frontnet`. But either way, we cannot reach containers on `frontnet` from a container on `authnet`, and so we have achieved the desired separation.

We're able to move more quickly to construct FrontNet because it's so much like AuthNet. We just have to do what we did before and tweak the names. 

In this section, we created a database container. In the next section, we will create the Dockerfile for the Notes application.

## Dockerizing the Notes application

Our next step is, of course, to Dockerize the Notes application. This starts by creating a Dockerfile, and then adding another Sequelize configuration file, before finishing up by adding more scripts to the `frontnet/package.json` file.

In the `notes` directory, create a file named `Dockerfile` containing the following:

[PRE21]js\1

However, the multiple `COPY` commands let us control exactly what's copied. It's most important to avoid copying the `node_modules` directory into the container. Not only is the `node_modules` file on the host large, which would bloat the container if copied, but it is set up for the host OS and not the container OS. The `node_modules` directory must be built inside the container, with the installation happening on the container's OS. That constraint led to the choice to explicitly copy specific files to the destination.

We also have a new `SEQUELIZE_CONNECT` file. Create `models/sequelize-docker-mysql.yaml` containing the following:

[PRE22]js\1

As with the authentication server, this lets us build the container image for the Notes application service. 

Then, in `frontnet/package.json`, add these scripts:

[PRE23]js\1

This creates the container image and then launches the container.

Notice that the exposed port `3000` is mapped with `-p 80:3000` onto the normal HTTP port. Since we're getting ready for deployment on a real service, we can stop using port `3000`.

At this point, we can connect our browser to `http://localhost` and start using the Notes application. However, we'll quickly run into a problem:

![](img/11e5e001-7757-4392-9277-62ce82f78a64.png)

The user experience team is going to scream about this ugly error message, so put it on your backlog to generate a prettier error screen. For example, a flock of birds pulling a whale out of the ocean is popular.

This error means that Notes cannot access anything at the host named `svc-userauth`. That host does exist because the container is running, but it's not on `frontnet`, and is not reachable from the `notes` container. Instead, it is on `authnet`, which is currently not reachable by `svc-notes`:

[PRE24]js\1

In the architecture diagram presented in [Chapter 10](176ce11c-dd6f-4ebf-ba14-529be6db28da.xhtml), *Deploying Node.js Applications to Linux Servers,* we showed a connection between the `svc-notes` and `svc-userauth` containers. This connection is required so that Notes can authenticate its users. But that connection does not yet exist.

Docker requires you to take a second step to attach the container to a second network:

[PRE25]js\1

The first time around, we connected `svc-notes` to `authnet`, then we disconnected it from `authnet`, and then connected `svc-userauth` to `frontnet`. That means we tried both combinations and, as expected, in both cases, `svc-notes` and `svc-userauth` were able to communicate.

This is a question for security experts since the consideration is the attack vectors available to any intruders. Suppose Notes has a security hole allowing an invader to gain access. How do we limit what is reachable via that hole?

The primary observation is that by connecting `svc-notes` to `authnet`, `svc-notes` not only has access to `svc-userauth` but also to `db-userauth`. To see this, run these commands:

[PRE26]js\1

Primarily, this adds a command, `connect-userauth`, to connect `svc-userauth` to `frontnet`. That helps us remember our decision on how to join the containers. We also took the opportunity to do a little reorganization.

We've learned a lot in this section about Docker—using Docker images, creating Docker containers from images, and configuring a group of Docker containers with some security constraints in mind. We came out of this section having implemented our initial architecture idea. We have two private networks with the containers connected to their appropriate network. The only exposed TCP port is the Notes application, visible on port `80`. The other containers connect with one another using TCP/IP connections that are not available from outside the containers.

Before proceeding to the next section, you may want to shut down the services we've launched. Simply execute the following command:

[PRE27]js\1

That's the description of the entire Notes deployment. It's at a fairly high level of abstraction, roughly equivalent to the options in the command-line tools we've used so far. It's fairly succinct and self-explanatory, and, as we'll see, the `docker-compose` command makes these files a convenient way to manage Docker services.

The `version` line says that this is a version 3 Compose file. The version number is inspected by the `docker-compose` command so that it can correctly interpret its content. The full documentation is worth reading at [https://docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/).

There are three major sections used here: `services`, `volumes`, and `networks`. The `services` section describes the containers being used, the `networks` section describes the networks, and the `volumes` section describes the volumes. The content of each section matches the containers we created earlier. The configuration we've already dealt with is all here, just rearranged. 

There are the two database containers—`db-userauth` and `db-notes`—and the two service containers—`svc-userauth` and `svc-notes`. The service containers are built from a Dockerfile located in the directory named in the `build` attribute. The database containers are instantiated from images downloaded from Docker Hub. Both correspond directly to what we did previously, using the `docker run` command to create the database containers and using `docker build` to generate the images for the services.

The `container_name` attribute is equivalent to the `--name` attribute and specifies a user-friendly name for the container. We must specify the container name in order to specify the container hostname to effect a Docker-style service discovery.

The `networks` attribute lists the networks to which this container must be connected and is exactly equivalent to the `--net` argument. Even though the `docker` command doesn't support multiple `--net` options, we can list multiple networks in the Compose file. In this case, the networks are bridge networks. As we did earlier, the networks themselves must be created separately and, in a Compose file, this is done in the `networks` section.

The `ports` attribute declares the ports that are to be published and the mapping to container ports. In the `ports` declaration, we have two port numbers, the first being the published port number and the second being the port number inside the container. This is exactly equivalent to the `-p` option used earlier.

The `depends_on` attribute lets us control the start up order. A container that depends on another will wait to start until the depended-on container is running.

The `volumes` attribute describes mappings of a container directory to a `host` directory. In this case, we've defined two volume names—`db-userauth-data` and `db-notes-data`—and then used them for the volume mapping. However, when we deploy to Docker Swarm on AWS EC2, we'll need to change how this is implemented.

Notice that we haven't defined a host directory for the volumes. Docker will assign a directory for us, which we can learn about by using the `docker volume inspect` command. 

The `restart` attribute controls what happens if or when the container dies. When a container starts, it runs the program named in the `CMD` instruction, and when that program exits, the container exits. But what if that program is meant to run *forever*; shouldn't Docker know that it should restart the process? We could use a background process supervisor, such as Supervisord or PM2\. However, the Docker `restart` option takes care of it.

The `restart` attribute can take one of the following four values:

*   `no`: Do not restart.
*   `on-failure:count`: Restart up to *N* times.
*   `always`: Always restart.
*   `unless-stopped`: Start the container unless it was explicitly stopped.

In this section, we've learned how to build a Docker Compose file by creating one that describes the Notes application stack. With that in hand, let's see how to use this tool to launch the containers.

## Building and running the Notes application with Docker Compose

With the Docker Compose CLI tool, we can manage any sets of Docker containers that can be described in a `docker-compose.yml` file. We can build the containers, bring them up and down, view the logs, and more. On Windows, we're able to run the commands in this section unchanged.

Our first task is to create a clean slate by running these commands:

[PRE28]js\1

This builds the images listed in `docker-compose.yml`. Note that the image names we end up with all start with `compose-local`, which is the name of the directory containing the file. Because this is the equivalent of running `docker build` in each of the directories, it only builds the images. 

Having built the containers, we can start them all at once using either `docker-compose up` or `docker-compose start`:

[PRE29]js\1

If necessary, `docker-compose up` will first build the containers. In addition, it keeps the containers all in the foreground so that we can see the logging. It combines the log output for all the containers together in one output, with the container name shown at the beginning of each line. For a multi-container system such as Notes, this is very helpful.

We can check the status using this command:

[PRE30]js\1

This means that the REST service port for `svc-userauth` was published. Indeed, in the status output, we see that the port is published. That violates our security design, but it does let us run the tests with `users/cli.mjs` from our laptop. That is, we can add users to the database as we've done so many times before.

This security violation is acceptable so long as it stays on our laptop. The `compose-local` directory is named specifically to be used with Docker Compose on our laptop.

Alternatively, we can run commands inside the `svc-userauth` container just as before:

[PRE31]js\1

From there, we can try pinging each of the containers to see which containers can be reached. That will serve as a simplistic security audit to ensure that what we've created fits the security model we desired.

While doing this, we find that `svc-userauth` can ping every container, including `db-notes`. This violates the security plan and has to be changed. 

Fortunately, this is easy to fix. Simply by changing the configuration, we can add a new network named `svcnet` to `docker-compose.yml`:

[PRE32]js\1

As shown here, this stops the whole set of containers. Occasionally, it will instead exit the user to the shell, and the containers will still be running. In that case, the user will have to use an alternative method to shut down the containers:

[PRE33]js\1

This is the service definition for the `svc-notes-2` container we just described. Because we set the `PORT` variable, the container will listen on port `3020`, which is what is advertised in the `ports` attribute.

As before, when we quickly reconfigured the network configuration, notice that a simple edit to the Docker Compose file was all that was required to change things around.

Then, relaunch the Notes stack, as follows:

[PRE34]js\1

This sets up a Redis server in a container named `redis`. This means that other services wanting to use Redis will access it at the host named `redis`.

For any `svc-notes` services you've defined (`svc-notes` and `svc-notes-2`), we must now tell the Notes application where to find the Redis server. We can do this by using an environment variable.

2.  In `compose-local/docker-compose.yml`, add the following environment variable declaration to any such services:

[PRE35]js\1

This installs the required packages. The `redis` package is a client for using Redis from Node.js and the `connect-redis` package is the Express session store for Redis. 

4.  We need to change the initialization in `app.mjs` to use the `connect-redis` package in order to store session data:

[PRE36]js\1

Because source file changes were made, the containers need to be rebuilt. These options ensure that this happens.

We'll now be able to connect to both the Notes service on `http://localhost:3000` (`svc-notes`) and the service on `http://localhost:3020` (`svc-notes-2`), and it will handle the login session on both services.

Another issue should be noted, however, and this is the fact that real-time notifications are not sent between the two servers. To see this, set up four browser windows, two for each of the servers. Navigate all of them to the same note. Then, add and delete some comments. Only the browser windows connected to the same server will dynamically show changes to the comments. Browser windows connected to the other server will not.

This is the second horizontal scaling issue. Fortunately, its solution also involves the use of Redis.

## Distributing Socket.IO messages using Redis

While testing what happens when we have multiple `svc-notes` containers, we found that login/logout was not reliable. We fixed this by installing a Redis-based session store to keep session data in a place that is accessible by multiple containers. But we also noticed another issue: the fact that the Socket.IO-based messaging did not reliably cause updates in all browser windows.

Remember that the updates we want to happen in the browser are triggered by updates to the `SQNotes` or `SQMessages` tables. The events emitted by updating either table are emitted by the server making the update. An update happening in one service container (say, `svc-notes-2`) will emit an event from that container, but not from the other one (say, `svc-notes`). There is no mechanism for the other containers to know that they should emit such events.

The Socket.IO documentation talks about this situation: 

[https://socket.io/docs/using-multiple-nodes/](https://socket.io/docs/using-multiple-nodes/)

The Socket.IO team provides the `socket.io-redis` package as the solution to this problem. It ensures that events emitted through Socket.IO by any server will be passed along to other servers so that they can also emit those events.

Since we already have the Redis server installed, we simply need to install the package and configure it as per the instructions. Again, we will not need to learn anything about Redis:

[PRE37]js\1

The only change is to add the lines in bold. The `socket.io-redis` package is what the Socket.IO team calls an adapter. Adapters are added to Socket.IO by using the `io.adapter` call.

We only connect this adapter if a Redis endpoint has been specified. As before, this is so that Notes can be run without Redis as needed.

Nothing else is required. If you relaunch the Notes application stack, you will now receive updates in every browser window connected to every instance of the Notes service.

In this section, we thought ahead about deployment to a cloud-hosting service. Knowing that we might want to implement multiple Notes containers, we tested this scenario on our laptop and found a couple of issues. They were easily fixed by installing a Redis server and adding a couple of packages.

We're getting ready to finish this chapter, and there's one task to take care of before we do. The `svc-notes-2` container was useful for ad hoc testing, but it is not the correct way to deploy multiple Notes instances. Therefore, in `compose-local/docker-compose.yml`, comment out the `svc-notes-2` definition.

This gave us some valuable exposure to a new tool that's widely used—Redis. Our application now also appears to be ready for deployment. We'll take care of that in the next chapter.

# Summary

In this chapter, we took a huge step toward the vision of deploying Notes on a cloud-hosting platform. Docker containers are widely used on cloud-hosting systems for application deployment. Even if we don't end up using the Docker Compose file once, we can still carry out the deployment and we have worked out how to Dockerize every aspect of the Notes stack.

In this chapter, we learned not only about creating Docker images for Node.js applications, but also about launching a whole system of services comprising a web application. We have learned that a web application is not just about the application code but also the databases, the frameworks we use, and even other services, such as Redis.

For that purpose, we learned both how to create our own Docker containers as well as how to use third-party containers. We learned how to launch containers using `docker run` and Docker Compose. We learned how to build custom Docker containers using a Dockerfile, and how to customize third-party containers.

For connecting containers, we learned about the Docker bridge network. This is useful on a single-host Docker installation and is a private communication channel where containers can find each other. As a private channel, the bridge network is relatively safe from outside intrusion, giving us a way to securely tie services together. We had the opportunity to try different network architectures inside Docker and to explore the security implications of each. We learned that Docker offers an excellent way to securely deploy persistent services on a host system.

Looking ahead to the task of deploying Notes on a cloud hosting service, we did some ad hoc testing with multiple instances of the Notes service. This highlighted a few issues that will crop up with multiple instances, and we remedied those issues by adding Redis to the application stack.

This gave us a well-rounded view of how Node.js services are prepared for deployment to cloud-hosting providers. Remember that our goal is to deploy the Notes application as Docker containers on AWS EC2 as an example of cloud deployment. In this chapter, we explored different aspects of Dockerizing a Node.js application stack, giving us a solid grounding in deploying services with Docker. We're now ready to take this application to a server on the public internet.

In the next chapter, we will learn about two very important technologies. The first is **Docker Swarm**, which is a Docker orchestrator that comes bundled with Docker. We'll learn how to deploy our Docker stack as services in a Swarm that we'll build on the AWS EC2 infrastructure. The second technology we'll learn about is Terraform, which is an open source tool for describing service configuration on cloud-hosting systems. We'll use it to describe the AWS EC2 configuration for the Notes application stack.