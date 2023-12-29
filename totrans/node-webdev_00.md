Preface

Node.js is a server-side JavaScript platform that allows developers to build fast and scalable applications using JavaScript outside of web browsers. It is playing an ever-wider role in the software development world, having started as a platform for server applications but now seeing wide use in command-line developer tools and even in GUI applications, thanks to toolkits such as Electron. Node.js has liberated JavaScript from being stuck in the browser.

It runs on top of the ultra-fast JavaScript engine at the heart of Google's Chrome browser, V8\. The Node.js runtime follows an ingenious event-driven model that's widely used for concurrent processing capacity despite using a single-thread model.

The primary focus of Node.js is high-performance, highly scalable web applications, but it is seeing adoption in other areas. For example, Electron, the Node.js-based wrapper around the Chrome engine, lets Node.js developers create desktop GUI applications and is the foundation on which many popular applications have been built, including the Atom and Visual Studio Code editors, GitKraken, Postman, Etcher, and the desktop Slack client. Node.js is popular on Internet of Things devices. Its architecture is especially well suited to microservice development and often helps form the server side of full-stack applications.

The key to providing high throughput on a single-threaded system is Node.js's model for asynchronous execution. It's very different from platforms that rely on threads for concurrent programming, as those systems often have high overheads and complexity. By contrast, Node.js uses a simple event dispatch model that originally relied on callback functions but today relies on the JavaScript Promise object and async functions.  

Because Node.js is on top of Chrome's V8 engine, the platform is able to quickly adopt the latest advances in the JavaScript language. The Node.js core team works closely with the V8 team, letting it quickly adopt new JavaScript language features as they are implemented in V8\. Node.js 14.x is the current release and this book is written for that release.

# Who this book is for

Server-side engineers may find JavaScript to be an excellent alternative programming language. Thanks to advances in the language, JavaScript long ago stopped being a simplistic toy language suitable only for animating buttons in browsers. We can now build large systems with the language, and Node.js has many built-in features, such as a top-notch module system, that help in larger projects.  

Developers experienced with browser-side JavaScript may find it attractive to broaden their horizons to include server-side development using this book.

# What this book covers

[Chapter 1](3cd3b221-f9a7-47f2-9159-203c0130088e.xhtml), *About Node.js*, introduces you to the Node.js platform. It covers its uses, the technological architecture choices in Node.js, its history, the history of server-side JavaScript, why JavaScript should be liberated from the browser, and important recent advances in the JavaScript scene.

[Chapter 2](bd2253cb-6a41-4fc5-ae86-cc9632d44da4.xhtml), *Setting Up Node.js*, goes over setting up a Node.js developer environment. This includes installing Node.js on Windows, macOS, and Linux. Important tools are covered, including the `npm` and `yarn` package management systems and Babel, which is used to transpile modern JavaScript into a form that's runnable on older JavaScript implementations.

[Chapter 3](516a5cd0-bdae-4e8c-bb0a-d508f85d483a.xhtml), *Exploring Node.js Modules*, delves into the module as the unit of modularity in Node.js applications. We will dive deep into understanding and developing Node.js modules and using `npm` to maintain dependencies. We will learn about the new module format, ES6 modules, and how to use it in Node.js now that it is natively supported.

[Chapter 4](a883aeee-aa28-44c6-a02e-8238829cea90.xhtml), *HTTP Servers and Clients*, starts exploring web development with Node.js. We will develop several small webserver and client applications in Node.js. We will use the Fibonacci algorithm to explore the effects of heavy-weight, long-running computations on a Node.js application. We will also learn several mitigation strategies and get our first experience with developing REST services.

[Chapter 5](582d3898-0135-430c-8b6e-8326f287e18b.xhtml), *Your First Express Application*, begins the main journey of this book, which is developing an application for creating and editing notes. In this chapter, we get a basic notes application running and get started with the Express framework.

[Chapter 6](db8b0ab8-181f-4d8d-9088-a9962ec461b8.xhtml), *Implementing the Mobile-First Paradigm*, uses the Bootstrap V4 framework to implement responsive web design in the notes application. This includes integrating a popular icon set and the steps required to customize Bootstrap.

[Chapter 7](ae8529e5-3a08-45cc-89e9-82895eb45641.xhtml), *Data Storage and Retrieval*, explores several database engines and a method to easily switch between databases at will. The goal is to robustly persist data to disk.

[Chapter 8](1ef2de06-5b7d-44c8-a132-55f822d113cf.xhtml), *Authenticating Users with a Microservice*, adds user authentication to the notes application. We will learn about handling login and logout using PassportJS. Authentication is supported both for locally stored user credentials and for using OAuth with Twitter.

[Chapter 9](3d687da9-7857-4c79-915b-b5b79873748c.xhtml), *Dynamic Client/Server Interaction with Socket.IO*, looks at letting our users talk with each other in real time. We will use a popular framework for dynamic interaction between client and server, Socket.IO, to support dynamic updates of content and a simple commenting system. Everything is dynamically updated by users in pseudo-real time, giving us the opportunity to learn about real-time dynamic updating.

[Chapter 10](176ce11c-dd6f-4ebf-ba14-529be6db28da.xhtml), *Deploying Node.js Applications to Linux Servers*, is where we begin the deployment journey. In this chapter, we will use the traditional methods of deploying background services on Ubuntu using Systemd.

[Chapter 11](b3de2a00-b4df-4552-9cf6-b3f356ef05b9.xhtml), *Deploying Node.js Microservices with Docker*, sees us start to explore cloud-based deployment using Docker to treat the notes application as a cluster of microservices.  

[Chapter 12](8551a26c-6834-4df6-b392-60a15c20f6ff.xhtml), *Deploying a Docker Swarm to AWS EC2 with Terraform*, literally takes us to the cloud by looking at building a cloud hosting system using AWS EC2 systems. We will use a popular tool, Terraform, to create and manage an EC2 cluster, and we will learn how to almost completely automate the deployment of a Docker Swarm cluster using Terraform features.

[Chapter 13](1c1eb7f2-8b1a-4f70-9f0a-94d865c739ef.xhtml), *Unit Testing and Functional Testing*, has us explore three testing modes: unit testing, REST testing, and functional testing. We will use popular test frameworks, Mocha and Chai, to drive test cases in all three modes. For function testing, we will use Puppeteer, a popular framework for automating test execution in a Chrome instance.

[Chapter 14](4cccad1e-fe7e-495a-9e90-8818820b890a.xhtml), *Security in Node.js Applications*, is where we integrate security techniques and tools to mitigate security intrusions. We will start by implementing HTTPS on the AWS EC2 deployment using Let's Encrypt. We will then discuss several tools in Node.js to implement security settings and discuss the best security practices for both Docker and AWS environments.

# To get the most out of this book

The basic requirement is installing Node.js and having a programmer-oriented text editor. The editor need not be anything fancy; even vi/vim will do in a pinch. We will show you how to install everything that's needed, and it's all open source, so there's no barrier to entry.

The most important tool is the one between your ears, and we aren't referring to ear wax.

| **Software/hardware covered in the book** | **OS requirements** |
| Node.js and related frameworks such as Express, Sequelize, and Socket.IO | Any |
| The `npm`/`yarn` package management tools | Any |
| Python and C/C++ compilers | Any |
| MySQL, SQLite3, and MongoDB databases | Any |
| Docker | Any |
| Multipass | Any |
| Terraform | Any |
| Mocha and Chai | Any |

Every piece of software concerned is readily available. For C/C++ compilers on Windows and macOS, you will need to get either Visual Studio (Windows) or Xcode (macOS), but both are freely available.

It will be helpful to have some experience with JavaScript programming. It is a fairly easy language to learn if you are already experienced with other programming languages.

## Download the example code files

While we aim to have identical code snippets in the book and in the repository, there are going to be minor differences in some places. The repository may contain comments, debugging statements, or alternate implementations (commented-out) that are not shown in the book.

You can download the example code files for this book from your account at [www.packt.com](http://www.packt.com). If you purchased this book elsewhere, you can visit [www.packtpub.com/support](https://www.packtpub.com/support) and register to have the files emailed directly to you.

You can download the code files by following these steps:

1.  Log in or register at [www.packt.com](http://www.packt.com).
2.  Select the Support tab.
3.  Click on Code Downloads.
4.  Enter the name of the book in the Search box and follow the onscreen instructions.

Once the file is downloaded, please make sure that you unzip or extract the folder using the latest version of:

*   WinRAR/7-Zip for Windows
*   Zipeg/iZip/UnRarX for Mac
*   7-Zip/PeaZip for Linux

The code bundle for the book is also hosted on GitHub at [https://github.com/PacktPublishing/Node.js-Web-Development-Fifth-Edition](https://github.com/PacktPublishing/Node.js-Web-Development-Fifth-Edition). In case there's an update to the code, it will be updated on the existing GitHub repository.

We also have other code bundles from our rich catalog of books and videos available at **[https://github.com/PacktPublishing/](https://github.com/PacktPublishing/)**. Check them out!

## Conventions used

There are a number of text conventions used throughout this book.

`CodeInText`: Indicates code words in text, database table names, folder names, filenames, file extensions, pathnames, dummy URLs, user input, and Twitter handles. Here is an example: "Start by changing `package.json` to have the following `scripts` section."

A block of code is set as follows:

[PRE0]js\1

Any command-line input or output is written as follows:

```js\1

**Bold**: Indicates a new term, an important word, or words that you see onscreen. For example, words in menus or dialog boxes appear in the text like this. Here is an example: "Click on the Submit button."

Warnings or important notes appear like this.

Tips and tricks appear like this.

# Get in touch

Feedback from our readers is always welcome.

**General feedback**: If you have questions about any aspect of this book, mention the book title in the subject of your message and email us at `customercare@packtpub.com`.

**Errata**: Although we have taken every care to ensure the accuracy of our content, mistakes do happen. If you have found a mistake in this book, we would be grateful if you would report this to us. Please visit [www.packtpub.com/support/errata](https://www.packtpub.com/support/errata), selecting your book, clicking on the Errata Submission Form link, and entering the details.

**Piracy**: If you come across any illegal copies of our works in any form on the Internet, we would be grateful if you would provide us with the location address or website name. Please contact us at `copyright@packt.com` with a link to the material.

**If you are interested in becoming an author**: If there is a topic that you have expertise in and you are interested in either writing or contributing to a book, please visit [authors.packtpub.com](http://authors.packtpub.com/).

## Reviews

Please leave a review. Once you have read and used this book, why not leave a review on the site that you purchased it from? Potential readers can then see and use your unbiased opinion to make purchase decisions, we at Packt can understand what you think about our products, and our authors can see your feedback on their book. Thank you!

For more information about Packt, please visit [packt.com](http://www.packt.com/).