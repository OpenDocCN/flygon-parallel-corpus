Deploying Node.js Applications to Linux Servers

Now that the Notes application is fairly complete, it's time to think about how to deploy it to a real server. We've created a minimal implementation of the collaborative note concept that works fairly well. To grow, *Notes* must escape our laptop and live on a real server.

The user story to fulfill is access to a hosted application that's available even when your laptop is turned off, for evaluation. The developer stories are to identify one of several deployment solutions, to have enough reliability so that the system restarts when it crashes, and for the users can access the app without taking too much of the developers time.

In this chapter, we will cover the following topics:

*   A discussion of the application architecture, and thoughts on how to implement the deployment
*   A traditional LSB-compliant Node.js deployment on a Linux server
*   Configuring Ubuntu to manage background tasks
*   Adjusting Twitter settings for application authentication
*   Using PM2 to reliably manage background tasks
*   Deployment to a virtual Ubuntu instance, which could be a **Virtual Machine** (**VM**) on our laptop or a **Virtual Private Server** (**VPS**) provider

There are two services making up the *Notes* application: *Notes* itself, and the user authentication service, along with the corresponding database instances. For them to be reliably available to the users, these services must be deployed on servers visible on the public internet, along with system management tools to keep the services running, handle service failures, and scale the service up to handle large traffic loads. One common way to do this is the traditional method of relying on scripts executing during server boot-up to start the required background processes.

Even though our end goal is deployment on a cloud-based platform with auto-scaling and all the buzzwords, you must still start from the basics of how to get an application to run in the background on a Unix-like system. 

Let's start the chapter by again reviewing the architecture, and think about how to best deploy on a server.

# Notes application architecture and deployment considerations

Before we get into deploying the *Notes *application, we need to review its architecture and understand what we're planning to do. We have segmented the services into two groups, as shown in the following diagram:

![](img/27cc847a-c683-4bd3-9897-0a95dc242e1e.png)

The user-facing portion is the Notes service along with its database. The backend, the user authentication service, and its database require more security. On our laptop, we weren't able to create the envisioned protective wall around that service, but we're about to implement one form of such protection.

One strategy to enhance security is to expose as few ports as possible. That reduces the so-called attack surface, simplifying our work in hardening the application against security bugs. With the *Notes* application, we have exactly one port to expose: the HTTP service through which users access the application. The other ports – two for the MySQL servers, and one for the user authentication service port – should not be visible to the public internet since they are for internal use only. Therefore, in the final system, we should arrange to expose that one HTTP port and keep everything else walled off from the public internet.

Internally, the *Notes* application needs to access both the Notes database and the user authentication service. That service, in turn, needs to access the user authentication database. The Notes service does not need to access the user authentication database, and the user authentication service does not need to access the Notes database. As currently envisaged, no external access to either database or the authentication service is required.

This gives us a sense of what will be implemented. To get started, let's learn the traditional way to deploy applications on Linux.

# Traditional Linux deployment for Node.js services

In this section, we will explore the traditional Linux/Unix service deployment. We'll do this with a virtual Ubuntu instance running on our laptop. The goal is to create background processes that automatically start during boot-up, restart if the process crashes, and allow us to monitor log files and system state.

Traditional Linux/Unix server application deployment uses an **init script** to manage background processes. They are to start every time the system boots, and cleanly shut down when the system is halted. The name "init script" comes from the name of the first process launched in the system, whose traditional name is `/etc/init`. The init scripts are usually stored in `/etc/init.d`, and are typically simple shell scripts. Some operating systems use other process managers, such as `upstart`, `systemd`, or `launchd`, while following the same model. While it's a simple model, the specifics of this vary widely from one **operating system** (**OS**) to another.

The Node.js project itself does not include any scripts to manage server processes on any OS. Implementing a complete web service based on Node.js means that we must create the scripting to integrate with process management on your OS. 

Having a web service on the internet requires having background processes running on a server, and those processes have to be the following:

*   **Reliable**: For example, they should auto-restart when the server process crashes.
*   **Manageable**: They should integrate well with system management practices.
*   **Observable**: The administrator must be able to get status and activity information from the service.

To demonstrate what's involved, we'll use PM2 to implement background server process management for *Notes*. PM2 bills itself as a *process manager*, meaning it tracks the state of processes it is managing and makes sure the processes execute reliably and are observable. PM2 detects the system type and can automatically integrate itself with the native process management system. It will create an LSB-style init script ([http://wiki.debian.org/LSBInitScripts](http://wiki.debian.org/LSBInitScripts)), or other scripts as required for your server. 

Our goal in this chapter is exploring how to do this, and there are several routes to achieving this goal:

*   Traditional VM management applications including VirtualBox, Parallels, and VMware let us install Ubuntu or any other OS within a virtual environment. On Windows, Hyper-V comes with Windows 10 Pro and offers a similar capability. In these cases, you download an ISO image of the boot CD-ROM, boot the VM from that ISO image, and run the full OS installation as if it was a regular computer.
*   You can rent inexpensive VPSes from one of hundreds of web hosting providers around the world. Often the choice is limited to Ubuntu servers. In these cases, you're handed a pre-baked server system ready to go for installing server software to run websites.
*   A new product, Multipass, is a lightweight VM management tool, based on lightweight hypervisor technology, and is available for every desktop computer OS. It gives you the exact same starting point as you'd get by renting a VPS or using VM software like VirtualBox, with a much lower system impact than traditional VM applications such as VirtualBox. It is like getting a VPS from a hosting provider, but it's on your laptop.

There is no practical difference between these choices from the standpoint of the tools and commands required to launch background processes. The Ubuntu instance installed in VirtualBox is the same as the Ubuntu on the VPS rented from a web-hosting provider, and is the same as the Ubuntu launched in a Multipass instance. It's the same OS, the same command-line tools, and the same system management practices. The difference is in the performance impact on your laptop. With Multipass, we can set up a virtual Ubuntu instance in a few seconds, and it is easy to have multiple instances running on a laptop with little or no performance impact. The experience of using VirtualBox, Hyper-V, or other VM solutions is that using the laptop feels quickly like walking through molasses, especially when running multiple VMs at once.

Therefore, in this chapter, we will run this exercise on Multipass. Everything shown in this chapter is easily transferrable to Ubuntu on VirtualBox/VMware/and so on or to a VPS rented from a web hosting provider.

For this deployment, we will create two Ubuntu instances with Multipass: one instance for the Notes service and the other for the user service. In each instance, there will be a MySQL instance for the corresponding database. Then we'll use PM2 to configure these systems to start our services in the background when launched.

Because of apparent incompatibilities between Multipass and WSL2, there might be difficulties using Multipass on Windows. If you run into problems, we have a section describing what to do.

The first task is to duplicate the source code from the previous chapter. It's suggested you create a new directory, `chap10`, as a sibling of the `chap09` directory, and copy everything from `chap09` to `chap10`.

To get started, let's install Multipass, and after that we'll start by deploying and testing the user authentication service, followed by deploying and testing Notes. We'll also cover setup issues on Windows.

## Installing Multipass

Multipass is an open source tool developed by Canonical. It is an extremely lightweight tool for managing VMs, specifically Ubuntu-based VMs. It is light enough to enable running a mini-sized cloud hosting system on your laptop.

To install Multipass, get an installer from [https://multipass.run/](https://multipass.run/). It may also be available through package management systems.

With Multipass installed, you can run some of the following commands to try it out:

[PRE0]js\1

This works as expected, in that you see `apt-get` first update its list of available packages, and then ask you to approve downloading and installing the packages to update, after which it does so. Anyone who is familiar with Ubuntu will find this normal. The difference is doing this from the command-line environment of the host computer.

That was fun, but we have some work to do, and we're not pleased with this mustang-based machine name Multipass saddled us with. Let's learn how to delete Multipass instances:

[PRE1]js\1

It goes through all the steps of setting up an instance, but in the last step, we get this message instead of success. Running `multipass list` might show the instance in a `Running` state, but no IP address has been assigned, and running `multipass shell` also results in a timeout.

This timeout is observed if WSL2 is installed on the computer along with Multipass. WSL2 is a lightweight Linux subsystem for Windows, that is billed as an excellent environment for running Linux commands on Windows. Running WSL2 and Multipass at the same time may result in unwanted behavior. 

For the purposes of this chapter, WSL2 is not useful. This is because WSL2 does not, at this time, support installing a background service that persists after a reboot, because it does not support `systemd`. Remember that our goal is to learn about setting up persistent background services. 

It may be necessary to disable WSL2\. To do so, use the Search box in the Windows taskbar to look for the Turn Windows Features On or Off control panel. Because WSL2 is a feature rather than an application that is installed or uninstalled, it is turned off or on using this control panel. Simply scroll down to find the feature, untick the checkbox, and then reboot the computer.

The Multipass online documentation has a troubleshooting page for Windows that has some useful hints, at [https://multipass.run/docs/troubleshooting-networking-on-windows](https://multipass.run/docs/troubleshooting-networking-on-windows).

Both WSL2 and Multipass use Hyper-V. This is a virtualization engine for Windows, and it also supports installing VMs in a mode similar to VirtualBox or VMware. It is easy to download an ISO for Ubuntu or any other OS and install it on Hyper-V. This results in a full OS in which to experiment with background process deployment. You may prefer to run these examples inside Hyper-V instead.

Once the virtual machine is installed most of the instructions in the rest of this chapter will work. Specifically, the `install-packages.sh` script will be useful for installing the Ubuntu packages required to complete the instructions, and the two configure-svc scripts are useful for "deploying" the services into `/opt/notes and /opt/userauth`. It is recommended to use Git inside the virtual machine to clone the repository associated with this book. Finally, the scripts in the pm2-single directory are useful for running the Notes and Users services under PM2.

Our purpose is to learn how to deploy Node.js services on a Linux system, without having to leave our laptop. For that purpose, we've familiarized ourselves with Multipass since it is an excellent tool for managing Ubuntu instances. We've also learned about alternatives such as Hyper-V or VirtualBox that also can be used for managing Linux instances.

Let's start exploring deployment with the user authentication service.

## Provisioning a server for the user authentication service

Since we want to have a segmented infrastructure, with the user authentication service in a walled-off area, let's make the first attempt at building that architecture. Using Multipass we will create two server instances, `svc-userauth` and `svc-notes`. Each will contain its own MySQL instance and the corresponding Node.js-based service. In this section, we'll set up `svc-userauth`, then in another section, we'll replicate the process to set up `svc-notes`.

Feeling kindly to our DevOps team, who've requested automation for all administrative tasks, we'll create some shell scripts to manage the server setup and configuration. 

The scripts shown here handle deployment to two servers, with one server holding the authentication service and the other holding the *Notes* application. In the GitHub repository accompanying this book, you'll find other scripts to handle deployment to a single server. The single server scenario might be required if you're using a heavier-weight virtualization tool such as VirtualBox rather than Multipass.

In this section, we will create the user authentication backend server, `svc-userauth`, and in a later section, we will create the server for the *Notes* frontend, `svc-notes`. Since the two server instances will be set up similarly, we might question why we're setting up two servers. It's because of the security model we decided on.

There are several steps involved, including a few scripts for automating Multipass operations, as follows:

1.  Create a directory named `chap10/multipass` for scripts related to managing Multipass instances. 
2.  Then, in that directory, create a file named `create-svc-userauth.sh`, containing the following:

[PRE2]js\1

The two are nearly the same, except for the method to compute the current directory.

The `mount` command in Multipass attaches a host directory into the instance at the given location. Therefore, we attach the `multipass` directory as `/build` and `users` as `/build-users`.

The ``pwd`` notation is a feature of the Unix/Linux shell environment. It means to run the `pwd` process and capture its output, supplying it as a command-line argument to the `multipass` command. For Windows, we use `(get-location)` for the same purpose in PowerShell.

3.  Create the instance by running the script:

[PRE3]js\1

Either one runs the commands in the scripts that will launch the instance and mount directories from the host filesystem.

4.  Create a file named `install-packages.sh` containing the following:

[PRE4]js\1

The `exec` command, as we discussed earlier, causes a command to execute inside the container by running this command on the host system.

6.  In the `users` directory, edit `user-server.mjs` and change the following:

[PRE5]js\1

This is our configuration for allowing the user service to connect with a local MySQL instance. The `dbname`, `username`, and `password` parameters must match the values in the configuration script shown earlier.

8.  Then, in the `users/package.json` file, add these entries to the scripts section:

[PRE6]js\1

Since we're now using MySQL, we must have the driver package installed.

10.  Now create a file named `configure-svc-userauth.sh` containing the following:

[PRE7]js\1

Remember that the `multipass` directory in the source tree is mounted inside the instance as `/build`. As soon as we created this file, it showed up in the `/build` directory, and we can execute it inside the instance.

Several times in this book, we've talked about the value of explicitly declaring all dependencies and of automating everything. This demonstrates this value, because now, we can just run a couple of shell scripts and the server is configured. And we don't have to remember how to launch the server because of the `scripts` section in `package.json`.

12.  We can now start the user authentication server, like so:

[PRE8]js\1

Multipass assigned an IP address to the instance. Your IP address will likely be different.

On our laptop is a copy of the source code, including a copy of `cli.mjs`. This means we can run `cli.mjs` on our laptop, telling it to access the service on `svc-userauth`. That's because we thought ahead and added `--host` and `--port` options to `cli.mjs`. In theory, using those options, we can access this server anywhere on the internet. At the moment, we simply need to reach into the virtual environment on our laptop.

On your laptop, in the regular command environment rather than inside Multipass, run these commands:

[PRE9]js\1

This shows database entries for the users we created. Notice that while logged in to the Multipass instance, we can use any Ubuntu command because we have the full OS in front of us.

We have not only launched the user authentication service on an Ubuntu server, but we've verified that we can access that service from outside the server.

In this section, we set up the first of the two servers we want to run. We still have to create the `svc-notes` server.

But before we do that, we first need to discuss running scripts on Windows.

## Script execution in PowerShell on Windows

In this chapter, we'll write several shell scripts. Some of these scripts need to run on your laptop, rather than on a Ubuntu-hosted server. Some developers use Windows, and therefore we need to discuss running scripts on PowerShell.

Executing scripts on Windows is different because it uses PowerShell rather than Bash, along with a large number of other considerations. For this and the scripts that follow, make the following changes.

PowerShell script filenames must end with the `.ps1` extension. For most of these scripts, all that is required is to duplicate the `.sh` scripts as `.ps1` files, because the scripts are so simple. To execute the script, simply type `.\scriptname.ps1` in the PowerShell window. In other words, on Windows, the script just shown must be named `configure-svc-userauth.ps1`, and is executed as `.\configure-svc-userauth.ps1`.

To execute the scripts, you may need to change the PowerShell execution policy:

[PRE10]js\1

This is tasked with launching the Multipass instance, and is very similar to `create-svc-userauth` but changed to use the word `notes`.

For Windows, instead create a file called `multipass/create-svc-notes.ps1` containing the following:

[PRE11]js\1

Or, on Windows, run the following command:

[PRE12]js\1

This script installs Node.js, the MySQL server, and a few other required packages.

4.  Now create a file, `notes/models/sequelize-mysql.yaml`, containing the following:

[PRE13]js\1

We need the MySQL driver package to use MySQL.

6.  Then, in the `notes/package.json` file, add this entry to the `scripts` section:

[PRE14]js\1

The `on-server` script will have to be updated appropriately.

7.  Duplicate `multipass/configure-svc-userauth.sh` to create a script named `multipass/configure-svc-notes.sh`, and change the final two sections to the following:

[PRE15]js\1

Remember that the `multipass` directory in the source tree is mounted inside the instance as `/build`. As soon as we created this file, it showed up in the `/build` directory, and we can execute it inside the instance.

9.  We can now run the Notes service with the following command:

[PRE16]js\1

The change is to use `sudo` to execute the command as `root`.

To test this we must of course use a browser to connect with the Notes service. For that, we need to use the IP address for `svc-notes`, which we learned from Multipass earlier. Using that example, the URL is `http://172.23.89.142:3000`.

You'll find that since we haven't changed anything in the look-and-feel category, that our *Notes* application looks like it has all along. Functionally, you will be unable to log in using Twitter credentials, but you can log in using one of the local accounts we created during testing.

Once both services are running, you can use your browser to interact with the *Notes* application and run it through its paces.

What we've done is build the second of two servers, `svc-userauth` and `svc-notes`, on which we'll run the Notes application stack. That gives us two Ubuntu instances each of which are configured with a database and a Node.js service. We were able to manually run the authentication and Notes services together, connecting from one Ubuntu instance to the other, each working with their corresponding database. To have this as a fully deployed server, we will use PM2 in a later section.

We have learned a little about configuring Ubuntu servers, though there is an outstanding issue of running the services as background processes. Before we get to that, let's rectify the situation with the Twitter login functionality. The issue with Twitter login is that the application is now on a different IP address, so to resolve this, we now have to add that IP address in Twitter's management backend.

# Adjusting Twitter authentication to work on the server

As we just noted, the *Notes* application as currently deployed does not support Twitter-based logins. Any attempt will result in an error. Obviously we can't deploy it like this.

The Twitter application we set up for *Notes* previously won't work because the authentication URL that refers to our laptop is incorrect for the server. To get OAuth to work with Twitter, while deployed on this new server, go to `developer.twitter.com/en/apps` and reconfigure the application to use the IP address of your server. 

That page is the dashboard of your applications that you've registered with Twitter. Click on the Detail*s* button, and you'll see the details of the configuration. Click on the Edit button, and edit the list of Callback URLs like so:

![](img/100f13e0-7055-4914-b2b6-19352f3bc230.png)

Of course, you must substitute the IP address of your server. The URL shown here is correct if your Multipass instance was assigned an IP address of `192.168.64.9`. This informs Twitter of a new correct callback URL that will be used. Likewise, if you have configured *Notes* to listen to port `80`, the URL you point Twitter to must also use port `80`. You must update this list for any callback URL you use in the future.

The next thing is to change the *Notes* application so as to use this new callback URL on the `svc-notes` server. In `routes/users.mjs`, the default value was `http://localhost:3000` for use on our laptop. But we now need to use the IP address for the server. Fortunately, we thought ahead and the software has an environment variable for this purpose. In `notes/package.json`, add the following environment variable to the `on-server` script:

[PRE17]js\1

This should not be added in `package.json`, but supplied via another means. We have not yet identified a suitable method, but we did identify that adding these variables to `package.json` means committing them to a source code repository, which might allow those values to leak to the public.

For now, the server can be started as follows:

[PRE18]js\1

The server instances were running under Multipass, and the `restart` command caused the named instance to `stop` and then `start`. This emulates a server reboot. Since both were running in the foreground, you'll see each command window exit to the host command shell, and running `multipass list` again will show both instances in the `Running` state. The big takeaway is that both services are no longer running.

There are many ways to manage server processes, to ensure restarts if the process crashes, and so on. We'll use **PM2** ([http://pm2.keymetrics.io/](http://pm2.keymetrics.io/)) because it's optimized for Node.js processes. It bundles process management and monitoring into one application.

Let's now see how to use PM2 to correctly manage the Notes and user authentication services as background processes. We'll start by familiarizing ourselves with PM2, then creating scripts to use PM2 to manage the services, and finally, we'll see how to integrate it with the OS so that the services are correctly managed as background processes. 

## Familiarizing ourselves with PM2

To get ourselves acquainted with PM2, let's set up a test using the `svc-userauth` server. We will create a directory to hold a `pm2-userauth` project, install PM2 in that directory, then use it to start the user authentication service. Along the way, we'll learn how to use PM2.

Start by running these commands on the `svc-userauth` server:

[PRE19]js\1

This boils down to running `pm2 start ./user-server.mjs`, except that we are adding the environment variables containing configuration values, and we are specifying the full path to PM2\. This runs our user server in the background.

We can repeat our test of using `cli.mjs` to list users known to the authentication server:

[PRE20]js\1

Because PM2 captures the standard output from the server process, any output is saved away. The `logs` command lets us view that output.

Some other useful commands are as follows:

*   `pm2 status`: Lists all the commands PM2 is currently managing, and their status
*   `pm2 stop SERVICE`: Stops the named service
*   `pm2 start SERVICE` or `pm2 restart SERVICE`: Starts the named service
*   `pm2 delete SERVICE`: Makes PM2 forget about the named service

There are several other commands, and the PM2 website contains complete documentation for them. [https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/](https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/)

For the moment, let's shut it down and delete the managed process:

[PRE21]js\1

This records for us the dependency on PM2, so it can easily be installed, along with some useful scripts we can run with PM2.

Then in the same directory, create an `ecosystem.json` file, containing the following:

[PRE22]js\1

This is the same as for `pm2-notes`, with the names changed.

Then, in `pm2-userauth`, create a file named `ecosystem.json` containing the following:

[PRE23]js\1

Doing so starts the service running on both server instances. The `npm run logs` command lets us see the log output as it happens. We've configured both services in a more DevOps-friendly logging configuration, without the DEBUG log enabled, and using the *common* log format.

For testing, we go to the same URL as before, but to port `80` rather than port `3000`.

Because the Notes service on `svc-notes` is now running on port `80`, we need to update the Twitter application configuration again, as follows:

![](img/86efbfc1-e3a4-402c-8cce-22a36e1d88da.png)

This drops the port `3000` from the URLs on the server. The application is no longer on port `3000`, but on port `80`, and we need to tell Twitter about this change.

## Integrating the PM2 setup as persistent background processes

The *Notes* application should be fully functioning. There is one remaining small task to perform, and that is to integrate it with the OS.

The traditional way on Unix-like systems is to add a shell script in a directory in `/etc`. The Linux community has defined the LSB Init Script format for this purpose, but since each OS has a different standard for scripts to manage background processes, PM2 has a command to generate the correct script for each.

Let's start with `svc-userauth`, and run these commands:

[PRE24]js\1

The machines should restart correctly, and with no intervention on our part, the services will be running. You should be able to put the *Notes* application through its paces and see that it works. The Twitter login functionality will not work at this time because we did not supply Twitter tokens.

It is especially informative to run this on each server:

[PRE25]js\1

This, of course, shuts down the service instances. Because of the work we've done, you'll be able to start them back up at any time.

We've learned a lot in this section about configuring the *Notes* application as a managed background process. With a collection of shell scripts and configuration files, we put together a system to manage these services as background processes using PM2\. By writing our own scripts, we got a clearer idea of how the underlying plumbing works.

With that, we are ready to wrap up the chapter.

# Summary

In this chapter, we started a journey to learn about deploying Node.js services to live servers. The goal was to learn deployment to cloud hosting, but to get there we learned the basics of getting reliable background processes on Linux systems.

We started by reviewing the Notes application architecture and seeing how that will affect deployment. That enabled us to understand the requirements for server deployment.

Then we learned the traditional way to deploy services on Linux using an init script. To do that, we learned how to use PM2 to manage processes, and used it to integrate as a persistent background process. PM2 is a useful tool for managing background processes on Unix/Linux systems. Deploying and managing persistence is a key skill for anyone developing web applications.

While that was performed on your laptop, the exact same steps could be used on a public server such as a VPS rented from a web hosting company. With a little bit of work, we could use these scripts to set up a test server on a public VPS. We do need to work on better automation since the DevOps team requires fully automated deployments.

Even in this age of cloud hosting platforms, many organizations deploy services using the same techniques we discussed in this chapter. Instead of cloud-based deployments, they rent one or a few VPSes. But even in cloud-based deployments using Docker, Kubernetes, and the like, the developer must know how to implement a persistent service on Unix-like systems. Docker containers are typically Linux environments, and must contain reliable persistent background tasks that are observable and maintainable.

In the next chapter, we will pivot to a different deployment technology: Docker. Docker is a popular system for packaging application code in a *container* that can be executed on our laptop or executed unchanged at scale on a cloud hosting platform.