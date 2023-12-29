Deploying a Docker Swarm to AWS EC2 with Terraform

So far in this book, we've created a Node.js-based application stack comprising two Node.js microservices, a pair of MySQL databases, and a Redis instance. In the previous chapter, we learned how to use Docker to easily launch those services, intending to do so on a cloud hosting platform. Docker is widely used for deploying services such as ours, and there are lots of options available to us for deploying Docker on the public internet.

Because **Amazon Web Services** (**AWS**) is a mature feature-filled cloud hosting platform, we've chosen to deploy there. There are many options available for hosting Notes on AWS. The most direct path from our work in [Chapter 11](b3de2a00-b4df-4552-9cf6-b3f356ef05b9.xhtml), *Deploying Node.js Microservices with Docker*, is to create a Docker Swarm cluster on AWS. That enables us to directly reuse the Docker compose file we created.

Docker Swarm is one of the available Docker orchestration systems. These systems manage a set of Docker containers on one or more Docker host systems. In other words, building a swarm requires provisioning one or more server systems, installing Docker Engine on each, and enabling swarm mode. Docker Swarm is built into Docker Engine, and it's a matter of a few commands to join those servers together in a swarm. We can then deploy Docker-based services to the swarm, and the swarm distributes the containers among the server systems, monitoring each container, restarting any that crash, and so on.

Docker Swarm can be used in any situation with multiple Docker host systems. It is not tied to AWS because we can rent suitable servers from any of hundreds of web hosting providers around the world. It's sufficiently lightweight that you can even experiment with Docker Swarm using **virtual machine** (**VM**) instances (Multipass, VirtualBox, and so on) on a laptop.

In this chapter, we will use a set of AWS **Elastic Compute Cloud** (**EC2**) instances. EC2 is the AWS equivalent of a **virtual private server** (**VPS**) that we would rent from a web hosting provider. The EC2 instances will be deployed within an AWS **virtual private cloud** (**VPC**), along with a network infrastructure on which we'll implement the deployment architecture we outlined earlier.

Let's talk a little about the cost since AWS can be costly. AWS offers what's called the Free Tier, where, for certain services, the cost is zero as long as you stay below a certain threshold. In this chapter, we'll strive to stay within the free tier, except that we will have three EC2 instances deployed for a while, which is beyond the free tier for EC2 usage. If you are sensitive to the cost, it is possible to minimize it by destroying the EC2 instances when not needed. We'll discuss how to do this later.

The following topics will be covered in this chapter:

*   Signing up with AWS and configuring the AWS **command-line interface** (**CLI**)
*   An overview of the AWS infrastructure to be deployed
*   Using Terraform to create an AWS infrastructure
*   Setting up a Docker Swarm cluster on AWS EC2
*   Setting up **Elastic Container Registry** (**ECR**) repositories for Notes Docker images
*   Creating a Docker stack file for deployment to Docker Swarm
*   Provisioning EC2 instances for a full Docker Swarm
*   Deploying the Notes stack file to the swarm

You will be learning a lot in this chapter, starting with how to get started with the AWS Management Console, setting up **Identity and Access Management** (**IAM**) users on AWS, and how to set up the AWS command-line tools. Since the AWS platform is so vast, it is important to get an overview of what it entails and the facilities we will use in this chapter. Then, we will learn about Terraform, a leading tool for configuring services on all kinds of cloud platforms. We will learn how to use it to configure AWS resources such as the VPC, the associated networking infrastructure, and how to configure EC2 instances. We'll next learn about Docker Swarm, the orchestration system built into Docker, how to set up a swarm, and how to deploy applications in a swarm.

For that purpose, we'll learn about Docker image registries, the AWS **Elastic Container Registry** (**ECR**), how to push images to a Docker registry, and how to use images from a private registry in a Docker application stack. Finally, we'll learn about creating a Docker stack file, which lets you describe Docker services to deploy in a swarm.

Let's get started.

# Signing up with AWS and configuring the AWS CLI

To use AWS services you must, of course, have an AWS account. The AWS account is how we authenticate ourselves to AWS and is how AWS charges us for services.

As a first step, go to [https://aws.amazon.com](https://aws.amazon.com) and sign up for an account.

The Amazon Free Tier is a way to experience AWS services at zero cost: [https://aws.amazon.com/free/](https://aws.amazon.com/free/). [](https://aws.amazon.com/free/) Documentation is available at[ ](https://aws.amazon.com/free/)[https://docs.aws.amazon.com](https://docs.aws.amazon.com).

AWS has two kinds of accounts that we can use, as follows:

*   The** root account** is what's created when we sign up for an AWS account. The root account has full access to AWS services.
*   An **IAM user account** is a less privileged account you can create within your root account. The owner of a root account creates IAM accounts, assigning the scope of permissions to each IAM account.

It is bad form to use the root account directly since the root account has complete access to AWS resources. If the account credentials for your root account were to be leaked to the public, significant damage could be done to your business. If the credentials for an IAM user account were leaked, the damage is limited to the resources controlled by that user account as well as by the privileges assigned to that account. Furthermore, IAM user credentials can be revoked at any time, and then new credentials generated, preventing anyone who is holding the leaked credentials from doing any further damage. Another security measure is to enable **multi-factor authentication** (**MFA**) for all accounts.

If you have not already done so, proceed to the AWS website at one of the preceding links and sign up for an account. Remember that the account created that way is your AWS root account.

Our first step is to familiarize ourselves with the AWS Management Console.

## Finding your way around the AWS account

Because there are so many services on the AWS platform, it can seem like a maze of twisty little passages, all alike. However, with a little orientation, we can find our way around.

First, look at the navigation bar at the top of the window. On the right, there are three dropdowns. The first has your account name and has account-related choices. The second lets you select which AWS region is your default. AWS has divided its infrastructure into *regions*, which essentially means the area of the world where AWS data centers are located. The third connects you with AWS Support.

On the left is a dropdown marked **Services**. This shows you the list of all AWS services. Since the Services list is unwieldy, AWS gives you a search box. Simply type in the name of the service, and it will show up. The AWS Management Console home page also has this search box.

While we are finding our way around, let's record the account number for the root account. We'll need this information later. In the Account dropdown, select My Account. The account ID is there, along with your account name.

It is recommended to set up MFA on your AWS root account. MFA simply means to authenticate a person in multiple ways. For example, a service might use a code number sent via a text message as a second authentication method, alongside asking for a password. The theory is that the service is more certain of who we are if it verifies both that we've entered a correct password and that we're carrying the same cell phone we had carried on other days.

To set up MFA on your root account, go to the My Security Credentials dashboard. A link to that dashboard can be found in the AWS Management Console menu bar. This brings you to a page controlling all forms of authentication with AWS. From there, you follow the directions on the AWS website. There are several possible tools for implementing MFA. The simplest tool is to use the Google Authenticator application on your smartphone. Once you set up MFA, every login to the root account will require a code to be entered from the authenticator app.

So far, we have dealt with the online AWS Management Console. Our real goal is to use command-line tools, and to do that, we need the AWS CLI installed and configured on our laptop. Let's take care of that next.

## Setting up the AWS CLI using AWS authentication credentials

The AWS CLI tool is a download available through the AWS website. Under the covers, it uses the AWS **application programming interface** (**API**), and it also requires that we download and install authentication tokens.

Once you have an account, we can prepare the AWS CLI tool.

The AWS CLI enables you to interact with AWS services from the command line of your laptop. It has an extensive set of sub-commands related to every AWS service.

Instructions to install the AWS CLI can be found here: [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

Instructions to configure the AWS CLI can be found here: [https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Once you have installed the AWS CLI tool on your laptop, we must configure what is known as a *profile*. 

AWS supplies an AWS API that supports a broad range of tools for manipulating the AWS infrastructure. The AWS CLI tools use that API, as do third-party tools such as Terraform. Using the API requires access tokens, so of course, both the AWS CLI and Terraform require those same tokens.

To get the AWS API access tokens, go to the My Security Credentials dashboard and click on the Access Keys tab.

There will be a button marked Create New Access Key. Click on this and you will be shown two security tokens, the Access Key ID and the Secret Access Key. You will be given a chance to download a **comma-separated values** (**CSV**) file containing these keys. The CSV file looks like this:

[PRE0]js\1

For the first two prompts, paste in the keys you downloaded. The Region name prompt selects the default Amazon AWS data center in which your service will be provisioned. AWS has facilities all around the world, and each locale has a code name such as `us-west-2` (located in Oregon). The last prompt asks how you wish the AWS CLI to present information to you. 

For the region code, in the AWS console, take a look at the Region dropdown. This shows you the available regions, describing locales, and the region code for each. For the purpose of this project, it is good to use an AWS region located near you. For production deployment, it is best to use the region closest to your audience. It is possible to configure a deployment that works across multiple regions so that you can serve clients in multiple areas, but that implementation is way beyond what we'll cover in this book.

By using the `--profile` option, we ensured that this created a named profile. If we had left off that option, we would have instead created a profile named `default`. For any of the `aws` commands, the `--profile` option selects which profile to use. As the name suggests, the default profile is the one used if we leave off the `--profile` option.

A better choice is to be explicit at all times in which an AWS identity is being used. Some guides suggest to not create a default AWS profile at all, but instead to always use the `--profile` option to be certain of always using the correct AWS profile.

An easy way to verify that AWS is configured is to run the following commands:

[PRE1]js\1

This describes the policy created for the Administrators group. It gives that group the rights we specified in the admin role earlier. The Resource tag is where we enter the ARN for the admin group that was created earlier. Make sure to put the entire ARN into this field.

Navigate back to the Groups area, and click on Create Group again. We'll create a group, `NotesDeveloper`, for use by developers assigned to the Notes project. It will give those user accounts some additional privileges. Perform the following steps:

1.  Enter `NotesDeveloper` as the group name. Then, click Next.
2.  For the Attach Policy page, there is a long list of policies to consider; for example, `AmazonRDSFullAccess`, `AmazonEC2FullAccess`, `IAMFullAccess`, `AmazonEC2ContainerRegistryFullAccess`, `AmazonS3FullAccess`, `AdministratorAccess`, and `AmazonElasticFileSystemFullAccess`.
3.  Then, click Next, and if everything looks right on the Review page, click **Create Group**.

These policies cover the services required to finish this chapter. AWS error messages that stipulate that the user is not privileged enough to access that feature do a good job of telling you the required privilege. If it is a privilege the user needs, then come back to this group and add the privilege.

In the left-hand navigation, click on Users and then on Create User. This starts the steps involved in creating an IAM user, described as follows:

1.  For the username, enter `notes-app`, since this user will manage all resources related to the Notes application. For Access type, click on both Programmatic access and AWS management console access since we will be using both. The first grants the ability to use the AWS CLI tools, while the second covers the AWS console. Then, click on Next.
2.  For permissions, select Add User to Group and then select both the Administrators and NotesDeveloper groups. This adds the user to the groups you select. Then, click on Next. 
3.  There is nothing more to do, so keep clicking Next until you get to the Review page. If you're satisfied, click on Create user.

You'll be taken to a page that declares Success. On this page, AWS makes available access tokens (a.k.a. security credentials) that can be used with this account. Download these credentials before you do anything else. You can always revoke the credentials and generate new access tokens at any time.

Your newly created user is now listed in the Users section. Click on that entry, because we have a couple of data items to record. The first is obviously the ARN for the user account. The second is a **Uniform Resource Locator** (**URL**) you can use to sign in to AWS as this user. For that URL, click on the Security Credentials tab and the sign-in link will be there.

It is recommended to also set up MFA for the IAM account. The My Security Credentials choice in the AWS taskbar gets you to the screen containing the button to set up MFA. Refer back a few pages to our discussion of setting up MFA for the root account.

To test the new user account, sign out and then go to the sign-in URL. Enter the username and password for the account, and then sign in.

Before finishing this section, return to the command line and run the following command:

[PRE2]js\1

This is another way to verify that the AWS CLI is correctly installed. This command queries the user information from AWS, and if it executes without error then you've configured the CLI correctly.

AWS CLI commands follow a similar structure, where there is a series of sub-commands followed by options. In this case, the sub-commands are `aws`, `iam`, and `list-users`. The AWS website has extensive online documentation for the AWS CLI tool.

### Creating an EC2 key pair

Since we'll be using EC2 instances in this exercise, we need an EC2 key pair. This is an encrypted certificate that serves the same purpose as the normal **Secure Shell** (**SSH**) key we use for passwordless login to a server. In fact, the key-pair file serves the same purpose, allowing passwordless login with SSH to EC2 instances. Perform the following steps:

1.  Log in to the AWS Management Console and then select the region you're using. 
2.  Next, navigate to the EC2 dashboard—for example, by entering `EC2` in the search box.
3.  In the navigation sidebar, there is a section labeled Network & Security, containing a link for Key pair.
4.  Click on that link. In the upper-right corner is a button marked Create key pair. Click on this button, and you will be taken to the following screen:

![](img/dfe865a3-6172-4b2b-ad97-760498cd6af6.png)

5.  Enter the desired name for the key pair. Depending on the SSH client you're using, use either a pem (used for the `ssh` command) or a ppk (used for PuTTY) formatted key-pair file.

6.  Click on Create key pair and you'll be returned to the dashboard, and the key-pair file will download in your browser.
7.  After the key-pair file is downloaded, it is required to make it read-only, which you can do by using the following command:

[PRE3]js\1

Terraform files have a `.tf` extension and use a fairly simple, easy-to-understand declarative syntax. Terraform doesn't care which filenames you use or the order in which you create the files. It simply reads all the files with a `.tf` extension and looks for resources to deploy. These files do not contain executable code, but declarations. Terraform reads these files, constructs a graph of dependencies, and works out how to implement the declarations on the cloud infrastructure being used.

An example declaration is as follows:

[PRE4]js\1

The block types include resource, which declares something related to the cloud infrastructure, variable, which declares a named value, output, which declares a result from a module, and a few others.

The structure of the block labels varies depending on the block type. For resource blocks, the first block label refers to the kind of resource, while the second is a name for the specific instance of that resource.

The type of arguments also varies depending on the block type. The Terraform documentation has an extensive reference to every variant.

A Terraform module is a directory containing Terraform scripts. When the `terraform` command is run in a directory, it reads every script in that directory to build a tree of objects.

Within modules, we are dealing with a variety of values. We've already discussed resources, variables, and outputs. A resource is essentially a value that is an object related to something on the cloud hosting platform being used. A variable can be thought of as an input to a module because there are multiple ways to provide a value for a variable. The output values are, as the name implies, the output from a module. Outputs can be printed on the console when a module is executed, or saved to a file and then used by other modules. The code relating to this can be seen in the following snippet:

[PRE5]js\1

In this case, we've defined several locals related to the CIDR of subnets to be created within a VPC. The `cidrsubnet` function is used to calculate subnet masks such as `10.1.1.0/24`.

Another important feature of Terraform is the provider plugin. Each cloud system supported by Terraform requires a plugin module that defines the specifics of using Terraform with that platform.

One effect of the provider plugins is that Terraform makes no attempt to be platform-independent. Instead, all declarable resources for a given platform are unique to that platform. You cannot directly reuse Terraform scripts for AWS on another system such as Azure because the resource objects are all different. What you can reuse is the knowledge of how Terraform approaches the declaration of cloud resources.

Another task is to look for a Terraform extension for your programming editor. Some of them have support for Terraform, with syntax coloring, checking for simple errors, and even code completion.

That's enough theory, though. To really learn this, we need to start using Terraform. In the next section, we'll begin by implementing the VPC structure within which we'll deploy the Notes application stack.

## Configuring an AWS VPC with Terraform

An AWS VPC is what it sounds like—namely, a service within AWS to hold cloud services that you've defined. The AWS team designed the VPC service to look something like what you would construct in your own data center, but implemented on the AWS infrastructure. 

In this section, we will construct a VPC consisting of a public subnet and a private subnet, an internet gateway, and security group definitions.

In the project work area, create a directory, `terraform-swarm`, that is a sibling to the `notes` and `users` directories. 

In that directory, create a file named `main.tf` containing the following:

[PRE6]js\1

The `default` attribute sets a default value for the variable. As we saw earlier, the declaration can also specify the data type for a variable, and a description. 

With this, we can now run our first Terraform command, as follows:

[PRE7]js\1

This declares the VPC. This will be the container for the infrastructure we're creating.

The `cidr_block` attribute determines the IPv4 address space that will be used for this VPC. The CIDR notation is an internet standard, and an example would be `10.0.0.0/16`. That CIDR would cover any IP address starting with the `10.0` octets.

The `enable_dns_support` and `enable_dns_hostnames` attributes determine whether **Domain Name System** (**DNS**) names will be generated for certain resources attached to the VPC. DNS names can assist with one resource finding other resources at runtime.

The `tags` attribute is used for attaching name/value pairs to resources. The name tag is used by AWS to have a display name for the resource. Every AWS resource has a computer-generated, user-unfriendly name with a long coded string and, of course, we humans need user-friendly names for things. The name tag is useful in that regard, and the AWS Management Console will respond by using this name in the dashboards.

In `variables.tf`, add this to support these resource declarations:

[PRE8]js\1

Where `resource` blocks declare something on the hosting platform (in this case, AWS), `data` blocks retrieve data from the hosting platform. In this case, we are retrieving a list of AZs for the currently selected region. We'll use this later when declaring certain resources.

### Configuring the AWS gateway and subnet resources

Remember that a public subnet is associated with an internet gateway, and a private subnet is associated with a NAT gateway. The difference determines what type of internet access devices attached to each subnet have.

Create a file named `gw.tf` containing the following:

[PRE9]js\1

This declares the public and private subnets. Notice that these subnets are assigned to a specific AZ. It would be easy to expand this to support more subnets by adding subnets named `public2`, `public3`, `private2`, `private3`, and so on. If you do so, it would be helpful to spread these subnets across AZs. Deployment is recommended in multiple AZs so that if one AZ goes down, the application is still running in the AZ that's still up and running.

This notation with `[0]` is what it looks like—an array. The value, `data.aws_availability_zones.available.names`, is an array, and adding `[0]` does access the first element of that array, just as you'd expect. Arrays are just one of the data structures offered by Terraform.

Each subnet has its own CIDR (IP address range), and to support this, we need these CIDR assignments listed in `variables.tf`, as follows:

[PRE10]js\1

To configure the routing table for the public subnets, we modify the routing table connected to the main routing table for the VPC. What we're doing here is adding a rule to that table, saying that public internet traffic is to be sent to the internet gateway. We also have a route table association declaring that the public subnet uses this route table.

For `aws_route_table.private`, the routing table for private subnets, the declaration says to send public internet traffic to the NAT gateway. In the route table associations, this table is used for the private subnet.

Earlier, we said the difference between a public and private subnet is whether public internet traffic is sent to the internet gateway or the NAT gateway. These declarations are how that's implemented.

In this section, we've declared the VPC, subnets, gateways, and routing tables—in other words, the infrastructure within which we'll deploy our Docker Swarm.

Before attaching the EC2 instances in which the swarm will live, let's deploy this to AWS and explore what gets set up.

## Deploying the infrastructure to AWS using Terraform

We have now declared the bones of the AWS infrastructure we'll need. This is the VPC, the subnets, and routing tables. Let's deploy this to AWS and use the AWS console to explore what was created.

Earlier, we ran `terraform init` to initialize Terraform in our working directory. When we did so, it suggested that we run the following command:

[PRE11]js\1

Terraform's error messages are usually self-explanatory. In this case, the cause was a decision to use only one public and one private subnet. This code was left over from there being two of each. Therefore, this error referred to stale code that was easy to remove.

The other thing `terraform plan` does is construct a graph of all the declarations and print out a listing. This gives you an idea of what Terraform intends to deploy on to the chosen cloud platform. It is therefore your opportunity to examine the intended infrastructure and make sure it is what you want to use.

Once you're satisfied, run the following command:

[PRE12]js\1

This lists the parameters for the VPC that was created.

Remember to either configure the `AWS_PROFILE` environment variable or use `--profile` on the command line.

To list data on the subnets, run the following command:

[PRE13]js\1

In the Terraform AWS provider, the resource name for EC2 instances is `aws_instance`. Since this instance is attached to our public subnet, we'll call it `aws_instance.public`. Because it is a public EC2 instance, the `associate_public_ip_address` attribute is set to `true`.

The attributes include the AMI ID, the instance type, the ID for the subnet, and more. The `key_name` attribute refers to the name of an SSH key we'll use to log in to the EC2 instance. We'll discuss these key pairs later. The `vpc_security_group_ids` attribute is a reference to a security group we'll apply to the EC2 instance. The `depends_on` attribute causes Terraform to wait for the creation of the resources named in the array. The `user_data` attribute is a shell script that is executed inside the instance once it is created.

For the AMI, instance type, and key-pair data, add these entries to `variables.tf`, as follows:

[PRE14]js\1

This script is derived from the official instructions for installing Docker Engine **Community Edition** (**CE**) on Ubuntu. The first portion is support for `apt-get` to download packages from HTTPS repositories. It then configures the Docker package repository into Ubuntu, after which it installs Docker and related tools. Finally, it ensures that the `docker` group is created and ensures that the `ubuntu` user ID is a member of that group. The Ubuntu AMI defaults to this user ID, `ubuntu`, to be the one used by the EC2 administrator.

For this EC2 instance, we also run `docker swarm init` to initialize the Docker Swarm. For other EC2 instances, we do not run this command. The method used for initializing the `user_data` attribute lets us easily have a custom configuration script for each EC2 instance. For the other instances, we'll only run `docker_install.sh`, whereas for this instance, we'll also initialize the swarm.

Back in `ec2-public.tf`, we have two more things to do, and then we can launch the EC2 instance. Have a look at the following code block:

[PRE15]js\1

This will let us know the public IP address and public DNS name. If we're interested, the outputs also tell us the private IP address and DNS name.

### Launching the EC2 instance on AWS

We have added to the Terraform declarations for creating an EC2 instance.

We're now ready to deploy this to AWS and see what we can do with it. We already know what to do, so let's run the following command:

[PRE16]js\1

This built our EC2 instance, and we have the IP address and domain name. Because the initialization script will have required a couple of minutes to run, it is good to wait for a short time before proceeding to test the system.

The `ec2-public-ip` value is the public IP address for the EC2 instance. In the following examples, we will put the text `PUBLIC-IP-ADDRESS`, and you must of course substitute the IP address your EC2 instance is assigned.

We can log in to the EC2 instance like so:

[PRE17]js\1

It can be inconvenient to remember to add the `-i` flag every time we use SSH. To avoid having to use this option, run this command:

[PRE18]js\1

The setup script was also supposed to have initialized this EC2 instance as a Docker Swarm node, and the following command verifies whether that happened:

[PRE19]js\1

The `docker node` command is for managing the nodes in a swarm. In this case, there is only one node—this one, and it is shown as not only a manager but as the swarm leader. It's easy to be the leader when you're the only node in the cluster, it seems.

The `docker service` command is for managing the services deployed in the swarm. In this context, a service is roughly the same as an entry in the `services` section of a Docker compose file. In other words, a service is not the running container but is an object describing the configuration for launching one or more instances of a given container.

To see what this means, let's start an `nginx` service, as follows:

[PRE20]js\1

Once a service is deployed, we can modify the deployment using the `docker service update` command. In this case, we told it to increase the number of instances using the `--replicas` option, and we now have three instances of the `nginx` container all running on the `notes-public` node.

We can also run the normal `docker ps` command to see the actual containers, as illustrated in the following code block:

[PRE21]js\1

Exit the shell on the EC2 instance so that you're at the command line on your laptop.

Run the following command:

[PRE22]js\1

Normally with an EC2 instance, we would use the `-i` option, as shown earlier. But after running `ssh-add`, the `-i` option is no longer required.

That enables us to create the following environment variable:

[PRE23]js\1

We begin by deleting the environment variable because we'll replace it with something better, as follows:

[PRE24]js\1

There are times when we must be cognizant of which is the current Docker context and when to use which context. This will be useful in the next section when we learn how to push the images to AWS ECR.

We've learned a lot in this section, so before heading to the next task, let's clean up our AWS infrastructure. There's no need to keep this EC2 instance running since we used it solely for a quick familiarization tour. We can easily delete this instance while leaving the rest of the infrastructure configured. The most effective way to so is by renaming `ec2-public.tf` to `ec2-public.tf-disable`, and to rerun `terraform apply`, as illustrated in the following code block:

[PRE25]js\1

This command switches the Docker context to the local system.

To hold the scripts and other files related to managing AWS ECR repositories, create a directory named `ecr` as a sibling to `notes`, `users`, and `terraform-swarm`. 

There are several commands required for a build process to create Docker images, tag them, and push them to a remote repository. To simplify things, let's create a few shell scripts, as well as PowerShell scripts, to record those commands.

The first task is to connect with the AWS ECR service. To this end, create a file named `login.sh` containing the following:

[PRE26]js\1

This relies on the AWS Tools for PowerShell package (see [https://aws.amazon.com/powershell/](https://aws.amazon.com/powershell/)), which appears to offer some powerful tools that are useful with AWS services. In testing, however, this command was not found to work very well. 

Instead, the following command was found to work much better, which you can put in a file named `login.ps1`:

[PRE27]js\1

This script is, of course, following the syntax of the Bash shell. For other command environments, you must transliterate it appropriately. To set these variables in the Bash shell, run the following command:

[PRE28]js\1

These should be the same values, just in a syntax recognized by Windows.

We have defined the environment variables being used. Let's now get back to defining the process to build Docker images and push them to the ECR.

## Defining a process to build Docker images and push them to the AWS ECR

We were exploring a build procedure for pushing Docker containers to ECR repositories until we started talking about environment variables. Let's return to the task at hand, which is to easily build Docker images, create ECR repositories, and push the images to the ECR.

As mentioned at the beginning of this section, make sure to switch to the *default* Docker context. We must do so because it is a policy with Docker Swarm to not use the swarm hosts for building Docker images.

To build the images, let's add a file named `build.sh` containing the following:

[PRE29]js\1

Also, create a companion file named `delete.sh` containing the following:

[PRE30]js\1

The `aws ecr create-repository` command outputs these descriptors for the image repositories. The important piece of data to note is the `repositoryUri` value. This will be used later in the Docker stack file to name the image to be retrieved.

The `create.sh` script only needs to be executed once.

Beyond creating the repositories, the workflow is as follows:

*   Build the images, for which we've already created a script named `build.sh`.
*   Tag the images with the ECR repository **Uniform Resource Identifier** (**URI**).
*   Push the images to the ECR repository.

For the latter two steps, we still have some scripts to create.

Create a file named `tag.sh` containing the following:

[PRE31]js\1

The `docker push` command causes the target image to be sent to the ECR repository. And again, for Windows, create a file named `push.ps1` containing the same commands but with Windows-style environment variable references.

In both the `tag` and `push` scripts, we are using the repository URI value, but have plugged in the two environment variables. This will make it generalized in case we deploy Notes to another AWS region.

We have the workflow implemented as scripts, so let's see now how it is run, as follows:

[PRE32]js\1

The `docker build` command automatically adds the tag, `latest`, if we do not specify a tag.

Then, to push the images to the ECR repositories, we execute these commands:

[PRE33]js\1

Remember that swarm hosts are not to be used for building Docker images. At the beginning of this section, we switched to the default context so that builds would occur on our laptop.

In this section, we learned how to set up a build procedure to push our Docker images to repositories on the AWS ECR service. This included using some interesting tools that simplify building complex build procedures in `package.json` scripts.

Our next step is learning how to use Docker compose files to describe deployment on Docker Swarm.

# Creating a Docker stack file for deployment to Docker Swarm

In the previous sections, we learned how to set up an AWS infrastructure using Terraform. We've designed a VPC that will house the Notes application stack, we experimented with a single-node Docker Swarm cluster built on a single EC2 instance, and we set up a procedure to push the Docker images to the ECR.

Our next task is to prepare a Docker stack file for deployment to the swarm. A stack file is nearly identical to the Docker compose file we used in [Chapter 11](b3de2a00-b4df-4552-9cf6-b3f356ef05b9.xhtml), *Deploying Node.js Microservices with Docker*. Compose files are used with normal Docker hosts, but stack files are used with swarms. To make it a stack file, we add some new tags and change a few things, including the networking implementation.

Earlier, we kicked the tires of Docker Swarm with the `docker service create` command to launch a service on a swarm. While that was easy, it does not constitute code that can be committed to a source repository, nor is it an automated process. 

In swarm mode, a service is a definition of the tasks to execute on swarm nodes. Each service consists of a number of tasks, with this number depending on the replica settings. Each task is a container that has been deployed to a node in the swarm. There are, of course, other configuration parameters, such as network ports, volume connections, and environment variables.

The Docker platform allows the use of the compose file for deploying services to a swarm. When used this way, the compose file is referred to as a stack file. There is a set of `docker stack` commands for handling the stack file, as follows:

*   On a regular Docker host, the `docker-compose.yml` file is called a compose file. We use the `docker-compose` command on a compose file.
*   On a Docker swarm, the `docker-compose.yml` file is called a stack file. We use the `docker stack` command on a stack file.

Remember that a compose file has a `services` tag, and each entry in that tag is a container configuration to deploy. When used as a stack file, each `services` tag entry is, of course, a service in the sense just described. This means that just as there was a lot of similarity between the `docker run` command and container definitions in the compose file, there is a degree of similarity between the `docker service create` command and the service entries in the stack file.

One important consideration is a policy that builds must not happen on Swarm host machines. Instead, these machines must be used solely for deploying and executing containers. This means that any `build` tag in a service listed in a stack file is ignored. Instead, there is a `deploy` tag that has parameters for the deployment in the swarm, and the `deploy` tag is ignored when the file is used with Compose. Put more simply, we can have the same file serve both as a compose file (with the `docker compose` command) and as a stack file (with the `docker stack` command), with the following conditions:

*   When used as a compose file, the `build` tag is used and the `deploy` tag is ignored.
*   When used as a stack file, the `build` tag is ignored and the `deploy` tag is used.

Another consequence of this policy is the necessity of switching the Docker context as appropriate. We have already discussed this issue—that we use the *default* Docker context to build images on our laptop and we use the EC2 context when interacting with the swarm on the AWS EC2 instances.

To get started, create a directory named `compose-stack` that's a sibling to `compose-local`, `notes`, `terraform-swarm`, and the other directories. Then, copy `compose-local/docker-compose.yml` into `compose-stack`. This way, we can start from something we know is working well.

This means that we'll create a Docker stack file from our compose file. There are several steps involved, which we'll cover over the next several sections. This includes adding deploy tags, configuring networking for the swarm, controlling the placement of services in the swarm, storing secrets in the swarm, and other tasks.

## Creating a Docker stack file from the Notes Docker compose file

With that theory under our belts, let's now take a look at the existing Docker compose file and see how to make it useful for deployment to a swarm.

Since we will require some advanced `docker-compose.yml` features, update the version number to the following:

[PRE34]js\1

This tells Docker that we want one instance of each service. Later, we will experiment with adding more service instances. We will add other parameters later, such as placement constraints. Later, we will want to experiment with multiple replicas for both `svc-notes` and `svc-userauth`. It is tempting to put CPU and memory limits on the service, but this isn't necessary.

It is nice to learn that with swarm mode, we can simply change the `replicas` setting to change the number of instances.

The next thing to take care of is the image name. While the `build` tag is present, remember that it is ignored. For the Redis and database containers, we are already using images from Docker Hub, but for `svc-notes` and `svc-userauth`, we are building our own containers. This is why, earlier in this chapter, we set up a procedure for pushing the images to ECR repositories. We can now reference those images from the stack file. This means that we must make the following change:

[PRE35]js\1

To support switching between using this for a swarm, or for a single-host deployment, we can leave the `bridge` network setting available but commented out. We would then change whether `overlay` or `bridge` networking is active by changing which is commented, depending on the context.

The `overlay` network driver sets up a virtual network across the swarm nodes. This network supports communication between the containers and also facilitates access to the externally published ports.

The `overlay` network configures the containers in a swarm to have a domain name automatically assigned that matches the service name. As with the `bridge` network we used before, containers find each other via the domain name. For a service deployed with multiple instances, the `overlay` network ensures that requests to that container can be routed to any of its instances. If a connection is made to a container but there is no instance of that container on the same host, the `overlay` network routes the request to an instance on another host. This is a simple approach to service discovery, by using domain names, but extending it across multiple hosts in a swarm.

That took care of the easy tasks for converting the compose file to a stack file. There are a few other tasks that will require more attention, however.

### Placing containers across the swarm

We haven't done it yet, but we will add multiple EC2 instances to the swarm. By default, swarm mode distributes tasks (containers) evenly across the swarm nodes. However, we have two considerations that should force some containers to be deployed on specific Docker hosts—namely, the following:

1.  We have two database containers and need to arrange persistent storage for the data files. This means that the databases must be deployed to the same instance every time so that it can use the same data directory.
2.  The public EC2 instance, named `notes-public`, will be part of the swarm. To maintain the security model, most of the services should not be deployed on this instance but on the instances that will be attached to the private subnet. Therefore, we should strictly control which containers deploy to `notes-public`.

Swarm mode lets us declare the placement requirements for any service. There are several ways to implement this, such as matching against the hostname, or against labels that can be assigned to each node.

For documentation on the stack file `placement` tag, refer to [https://docs.docker.com/compose/compose-file/#placement](https://docs.docker.com/compose/compose-file/#placement). [](https://docs.docker.com/compose/compose-file/#placement) The documentation for the `docker stack create` command includes a further explanation of deployment parameters:[ ](https://docs.docker.com/compose/compose-file/#placement)[https://docs.docker.com/engine/reference/commandline/service_create](https://docs.docker.com/engine/reference/commandline/service_create).

Add this `deploy` tag to the `db-userauth` service declaration:

[PRE36]js\1

This command attaches a label named `type`, with the value `public`, to the node named `notes-public`. We use this to set labels, and, as you can see, the label can have any name and any value. The labels can then be used, along with other attributes, as influence over the placement of containers on swarm nodes.

For the rest of the stack file, add the following placement constraints:

[PRE37]js\1

This is how we store a secret in a Docker swarm. The `docker secret create` command first takes the name of the secret, and then a specifier for a file containing the text for the secret. This means we can either store the data for the secret in a file or—as in this case—we use `-` to specify that the data comes from the standard input. In this case, we are using the `printf` command, which is available for macOS and Linux, to send the value into the standard input. 

Docker Swarm securely records the secrets as encrypted data. Once you've given a secret to Docker, you cannot inspect the value of that secret.

In `compose-stack/docker-compose.yml`, add this declaration at the end:

[PRE38]js\1

This notifies the swarm that the Notes service requires the two secrets. In response, the swarm will make the data for the secrets available in the filesystem of the container as `/var/run/secrets/TWITTER_CONSUMER_KEY` and `/var/run/secrets/TWITTER_CONSUMER_SECRET`. They are stored as in-memory files and are relatively secure.

To summarize, the steps required are as follows:

*   Use `docker secret create` to register the secret data with the swarm.
*   In the stack file, declare `secrets` in a top-level secrets tag.
*   In services that require the secrets, declare a `secrets` tag that lists the secrets required by this service.
*   In the environments tag for the service, create an environment variable pointing to the `secrets` file.

The Docker team has a suggested convention for configuration of environment variables. You could supply the configuration setting directly in an environment variable, such as `TWITTER_CONSUMER_KEY`. However, if the configuration setting is in a file, then the filename should be given in a different environment variable whose name has `_FILE` appended. For example, we would use `TWITTER_CONSUMER_KEY` or `TWITTER_CONSUMER_KEY_FILE`, depending on whether the value is directly supplied or in a file.

This then means that we must rewrite Notes to support reading these values from the files, in addition to the existing environment variables.

To support reading from files, add this import to the top of `notes/routes/users.mjs`:

[PRE39]js\1

This is similar to the code we've already used but organized a little differently. It first tries to read the Twitter tokens from the environment. Failing that, it tries to read them from the named files. Because this code is executing in the global context, we must read the files using `readFileSync`.

If the tokens are available from either source, the `twitterLogin` variable is set, and then we enable the support for `TwitterStrategy`. Otherwise, Twitter support is disabled. We had already organized the views templates so that if `twitterLogin` is `false`, the Twitter login buttons do not appear.

All of this is what we did in [Chapter 8](1ef2de06-5b7d-44c8-a132-55f822d113cf.xhtml), *Authenticating Users with a Microservice*, but with the addition of reading the tokens from a file.

### Persisting data in a Docker swarm

The data persistence strategy we used in [Chapter 11](b3de2a00-b4df-4552-9cf6-b3f356ef05b9.xhtml), *Deploying Node.js Microservices with Docker*, required the database files to be stored in a volume. The directory for the volume lives outside the container and survives when we destroy and recreate the container.

That strategy relied on there being a single Docker host for running containers. The volume data is stored in a directory in the host filesystem. But in swarm mode, volumes do not work in a compatible fashion.

With Docker Swarm, unless we use placement criteria, containers can deploy to any swarm node. The default behavior for a named volume in Docker is that the data is stored on the current Docker host. If the container is redeployed, then the volume is destroyed on the one host and a new one is created on the new host. Clearly, that means that the data in that volume is not persistent.

For documentation about using volumes in a Docker Swarm, refer to [https://docs.docker.com/compose/compose-file/#volumes-for-services-swarms-and-stack-files](https://docs.docker.com/compose/compose-file/#volumes-for-services-swarms-and-stack-files).

What's recommended in the documentation is to use placement criteria to force such containers to deploy to specific hosts. For example, the criteria we discussed earlier deploy the databases to a node with the `type` label equal to `db`. 

In the next section, we will make sure that there is exactly one such node in the swarm. To ensure that the database data directories are at a known location, let's change the declarations for the `db-userauth` and `db-notes` containers, as follows:

[PRE40]js\1

This declares two EC2 instances that are attached to the private subnet. There's no difference between these instances other than the name. Because they're on the private subnet, they are not assigned a public IP address.

Because we use the `private-db1` instance for databases, we have allocated 50 **gigabytes** (**GB**) for the root device. The `root_block_device` block is for customizing the root disk of an EC2 instance. Among the available settings, `volume_size` sets its size, in GB.

Another difference in `private-db1` is the `instance_type`, which we've hardcoded to `t2.medium`. The issue is about deploying two database containers to this server. A `t2.micro` instance has 1 GB of memory, and the two databases were observed to overwhelm this server. If you want the adventure of debugging that situation, change this value to be `var.instance_type`, which defaults to `t2.micro`, then read the section at the end of the chapter about debugging what happens.

Notice that for the `user_data` script, we only send in the script to install Docker Support, and not the script to initialize a swarm. The swarm was initialized in the public EC2 instance. The other instances must instead join the swarm using the `docker swarm join` command. Later, we will go over initializing the swarm, and see how that's accomplished. For the `public-db1` instance, we also create the `/data/notes` and `/data/users` directories, which will hold the database data directories.

Add the following code to `ec2-private.tf`:

[PRE41]js\1

This is literally not a best practice since it allows any network traffic from any IP address to reach the public EC2 instance. However, it does give us the freedom to develop the code without worrying about protocols at this moment. We will address this later and implement the best security practice. Have a look at the following code snippet:

[PRE42]js\1

This is largely the same as before, but with two changes. The first is to add references to the private EC2 instances to the `depends_on` attribute. This will delay the construction of the public EC2 instance until after the other two are running.  

The other change is to extend the shell script attached to the `user_data` attribute. The first addition to that script is to set the `type` label on the `notes-public` node. That label is used with service placement.

The last change is a script with which we'll set up the swarm. Instead of setting up the swarm in the `user_data` script directly, it will generate a script that we will use in creating the swarm. In the `sh` directory, create a file named `swarm-setup.sh` containing the following:

[PRE43]js\1

The part between `<<EOF` and `EOF` is supplied as the standard input to the `cat` command. The result is, therefore, for `/home/ubuntu/swarm-setup.sh` to end up with the text between those markers. An additional detail is that a number of variable references are escaped, as in `PEM=\$1`. This is necessary so that those variables are not evaluated while setting up this script but are present in the generated script.

This script is processed using the `templatefile` function so that we can use template commands. Primarily, that is the `%{for .. }` loop with which we generate the commands for configuring each EC2 instance. You'll notice that there is an array of data for each instance, which is passed through the `templatefile` invocation.

Therefore, the `swarm-setup.sh` script will contain a copy of the following pair of commands for each EC2 instance:

[PRE44]js\1

The word `manager` here means that we are requesting a token to join as a manager node. To connect a node as a worker, simply replace `manager` with `worker`.

Once the EC2 instances are deployed, we could log in to `notes-public`, and then run this command to get the join token and run that command on each of the EC2 instances. The `swarm-setup.sh` script, however, handles this for us. All we have to do, once the EC2 hosts are deployed, is to log in to `notes-public` and run this script.

It runs the `docker swarm join-token manager` command, piping that user-friendly text through a couple of `sed` commands to extract out the important part. That leaves the `join` variable containing the text of the `docker swarm join` command, and then it uses SSH to execute that command on each of the instances.

In this section, we examined how to automate, as far as possible, the setup of the Docker swarm.

Let's now do it.

## Preparing the Docker Swarm before deploying the Notes stack

When you make an omelet, it's best to cut up all the veggies and sausage, prepare the butter, and whip the milk and eggs into a mix before you heat up the pan. In other words, we prepare the ingredients before undertaking the critical action of preparing the dish. What we've done so far is to prepare all the elements of successfully deploying the Notes stack to AWS using Docker Swarm. It's now time to turn on the pan and see how well it works.

We have everything declared in the Terraform files, and we can deploy our complete system with the following command:

[PRE45]js\1

We have already run `ssh-add` on our laptop, and therefore SSH and **secure copy** (**SCP**) commands can run without explicitly referencing the PEM file. However, the SSH on the `notes-public` EC2 instance does not have the PEM file. Therefore, to access the other EC2 instances, we need the PEM file to be available. Hence, we've used `scp` to copy it to the `notes-public` instance.

If you want to verify the fact that the instances are running and have Docker active, type the following command:

[PRE46]js\1

We can see this using SSH to execute the `docker swarm join` command on each EC2 instance, causing these two systems to join the swarm, and to set the labels on the instances, as illustrated in the following code snippet:

[PRE47]js\1

We've already seen how this works and that, having done this, we will be able to run Docker commands on our laptop; for example, have a look at the following code snippet:

[PRE48]js\1

Remember that a newly created swarm does not have any secrets. To install the secrets requires these commands to be rerun.

If you wish to create a shell script to automate this process, consider the following:

[PRE49]js\1

Our primary requirement is to adjust the `TWITTER_CALLBACK_HOST` variable. The domain name for the `notes-public` instance changes every time we deploy the AWS infrastructure. Therefore, `TWITTER_CALLBACK_HOST` must be updated to match.

Similarly, we must go to the Twitter developers' dashboard and update the URLs in the application settings. As we already know, this is required every time we have hosted Notes on a different IP address or domain name. To use the Twitter login, we must change the list of URLs recognized by Twitter.

Updating `TWITTER_CALLBACK_HOST` and the Twitter application settings will let us log in to Notes using a Twitter account.

While here, we should review the other variables and ensure that they're correct as well.

The last preparatory step is to log in to the ECR repository. To do this, simply execute the following commands:

[PRE50]js\1

This deploys the services, and the swarm responds by attempting to launch each service. The `--with-registry-auth` option sends the Docker Registry authentication to the swarm so that it can download container images from the ECR repositories. This is why we had to log in to the ECR first.

### Verifying the correct launch of the Notes application stack

It will be useful to monitor the startup process using these commands:

[PRE51]js\1

The error, `no suitable node`, means that the swarm was not able to find a node that matches the placement criteria. In this case, the `type=public` label might not have been properly set.

The following command is helpful:

[PRE52]js\1

As soon as this is run, the swarm will place the `svc-notes` service on the `notes-public` node.

If this happens, it may be useful to add the following command to the `user_data` script for `aws_instance.public` (in `ec2-public.tf`), just ahead of setting the `type=public` label:

[PRE53]js\1

The output will tell you the current status, such as any error in deploying the service. However, to investigate connectivity with the EC2 instances, we must log in to the `notes-public` instance as follows:

[PRE54]js\1

This should work, but the output from `docker node ls` may show the node as `Unreachable`. Ask yourself: what happens if a computer runs out of memory? Then, recognize that we've deployed two database instances to an EC2 instance that has only 1 GB of memory—the memory capacity of `t2.micro` EC2 instances as of the time of writing. Ask yourself whether it is possible that the services you've deployed to a given server have overwhelmed that server.

To test that theory, make the following change in `ec2-private.tf`:

[PRE55]js\1

The `notes_svc-userauth` task has been deployed to `notes-private-svc1`, as expected.

To run `cli.mjs`, we must get shell access inside the container. Since it is deployed on a private instance, this means that we must first SSH to the `notes-public` instance; from there, SSH to the `notes-private-svc1` instance; and from there, run the `docker exec` command to launch a shell in the running container, as illustrated in the following code block:

[PRE56]js\1

This verifies that the user authentication server works and that it can communicate with the database. To verify this even further, we can access the database instance, as follows:

[PRE57]js\1

This will print the full error, including the originating error that caused the failure. You may see the following message printed: `getaddrinfo EAI_AGAIN api.twitter.com`. That may be puzzling because that domain name is certainly available. However, it might not be available inside the `svc-notes` container due to the DNS configuration.

From the `notes-public` instance, we will be able to ping that domain name, as follows:

[PRE58]js\1

Ideally, this will work from inside the container as well. If this fails inside the container, it means that the Notes service cannot reach Twitter to handle the OAuth dance required to log in with Twitter credentials.

The problem is that, in this case, Docker set up an incorrect DNS configuration, and the container was unable to make DNS queries for many domain names. In the Docker Compose documentation, it is suggested to use the following code in the service definition:

[PRE59]js\1

This increases the number of replicas. Because of the existing placement constraints, both instances will deploy to the node with a `type` label of `public`. To update the services, it's just a matter of rerunning the following command:

[PRE60]js\1

And indeed, it shows two instances of the `svc-notes` service. The `2/2` notation says that two instances are currently running out of the two instances that were requested.

To view the details, run the following command:

[PRE61]js\1

Ultimately, each service deployed to a Docker swarm contains one or more running containers.

You'll notice that this shows `svc-notes` listening on port `3000`. In the environment setup, we did not set the `PORT` variable, and therefore `svc-notes` will default to listening to port `3000`. Refer back to the output for `docker service ls`, and you should see this: `*:80->3000/tcp`, meaning that there is mapping being handled in Docker from port `80` to port `3000`.

That is due to the following setting in `docker-swarm/docker-compose.yml`:

```js\1

This says to publish port `80` and to map it to port `3000` on the containers.

In the Docker documentation ([https://docs.docker.com/network/overlay/#bypass-the-routing-mesh-for-a-swarm-service](https://docs.docker.com/network/overlay/#bypass-the-routing-mesh-for-a-swarm-service)), we learned that services deployed in a swarm are reachable by the so-called *routing mesh*. Connecting to a published port routes the connection to one of the containers handling that service. As a result, Docker acts as a load balancer, distributing traffic among the service instances you configure.

In this section, we have—finally—deployed the Notes application stack to a cloud hosting environment we built on AWS EC2 instances. We created a Docker swarm, configured the swarm, created a stack file with which to deploy our services, and we deployed to that infrastructure. We then tested the deployed system and saw that it functioned well.

With that, we can wrap up this chapter.

# Summary

This chapter is the culmination of a journey of learning Node.js application deployment. We developed an application existing solely on our laptop and added a number of useful features. With the goal of deploying that application on a public server to gain feedback, we worked on three types of deployment. In [Chapter 10](176ce11c-dd6f-4ebf-ba14-529be6db28da.xhtml), *Deploying Node.js Applications to Linux Servers*, we learned how to launch persistent background tasks on Linux using PM2\. In [Chapter 11](b3de2a00-b4df-4552-9cf6-b3f356ef05b9.xhtml), *Deploying Node.js Microservices with Docker*, we learned how to dockerize the Notes application stack, and how to get it running with Docker.

In this chapter, we built on that and learned how to deploy our Docker containers on a Docker Swarm cluster. AWS is a powerful and comprehensive cloud hosting platform with a long list of possible services to use. We used EC2 instances in a VPC and the related infrastructure.

To facilitate this, we used Terraform, a popular tool for describing cloud deployments not just on AWS but on many other cloud platforms. Both AWS and Terraform are widely used in projects both big and small.

In the process, we learned a lot about AWS, and Terraform, and using Terraform to deploy infrastructure on AWS; how to set up a Docker Swarm cluster; and how to deploy a multi-container service on that infrastructure.

We began by creating an AWS account, setting up the AWS CLI tool on our laptop, and setting up Terraform. We then used Terraform to define a VPC and the network infrastructure within which to deploy EC2 instances. We learned how to use Terraform to automate most of the EC2 configuration details so that we can quickly initialize a Docker swarm.

We learned that a Docker compose file and a Docker stack file are very similar things. The latter is used with Docker Swarm and is a powerful tool for describing the deployment of Docker services.

In the next chapter, we will learn about both unit testing and functional testing. While a core principle of test-driven development is to write the tests before writing the application, we've done it the other way around and put the chapter about unit testing at the end of the book. That's not to say unit testing is unimportant, because it certainly is important.