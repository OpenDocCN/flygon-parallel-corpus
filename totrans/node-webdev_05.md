HTTP Servers and Clients

Now that you've learned about Node.js modules, it's time to put this knowledge to use by building a simple Node.js web application. The goal of this book is to learn about web application development with Node.js. The next step in that journey is getting a basic understanding of the `HTTPServer` and `HTTPClient` objects. To do that, we'll create a simple application that will enable us to explore a popular application framework for Node.js—Express. In later chapters, we'll do more complex work on the application, but before we can walk, we must learn to crawl.

The goal of this chapter is to start to understand how to create applications on the Node.js platform. We'll create a handful of small applications, which means we'll be writing code and talking about what it does. Beyond learning about some specific technologies, we want to get comfortable with the process of initializing a work directory, creating the Node.js code for an application, installing dependencies required by the application, and running/testing the application.

The Node.js runtime includes objects such as `EventEmitter`, `HTTPServer`, and `HTTPClient`, which provide a foundation on which we can build applications. Even if we rarely use these objects directly, it is useful to understand how they work, and in this chapter, we will cover a couple of exercises using these specific objects.

We'll first build a simple application directly using the `HTTPServer` object. Then, we'll move on to using Express to create an application for computing Fibonacci numbers. Because this can be computationally expensive, we'll use this to explore why it's important to not block the event queue in Node.js and what happens to applications that do. This will give us an excuse to develop a simple background **Representational State Transfer** (**REST**) server, an HTTP client for making requests on that server, and the implementation of a multi-tier web application.

In today's world, the microservice application architecture implements background REST servers, which is what we'll do in this chapter.

We will cover the following topics in this chapter:

*   Sending and receiving events using the `EventEmitter` pattern
*   Understanding an HTTP server application by building a simple application
*   Web application frameworks
*   Using the Express framework to build a simple application
*   Handling computationally intensive calculations in an Express application and the Node.js event loop
*   Making HTTP Client requests
*   Creating a simple REST service with Express

By going through these topics, you'll gain an understanding of several aspects of designing HTTP-based web services. The goal is for you to understand how to create or consume an HTTP service and to get an introduction to the Express framework. By the end of this chapter, you'll have a basic understanding of these two tools.

That's a lot to cover, and it will give us a good foundation for the rest of this book.

# Sending and receiving events with EventEmitter

`EventEmitter` is one of the core idioms of Node.js. If Node.js's core idea is an event-driven architecture, emitting events from an object is one of the primary mechanisms of that architecture. `EventEmitter` is an object that gives notifications (events) at different points in its life cycle. For example, an `HTTPServer` object emits events concerning each stage of the startup/shutdown of the Server object and at each stage of processing HTTP requests from HTTP clients.

Many core Node.js modules are `EventEmitter` objects, and `EventEmitter` objects are an excellent skeleton on which to implement asynchronous programming. `EventEmitter` objects are so much a part of the Node.js woodwork that you may skip over their existence. However, because they're used everywhere, we need some understanding of what they are and how to use them when necessary.

In this chapter, we'll work with the `HTTPServer` and `HTTPClient` objects. Both are subclasses of the `EventEmitter` class and rely on it to send events for each step of the HTTP protocol. In this section, we'll first learn about using JavaScript classes, and then we will create an `EventEmitter` subclass so that we can learn about `EventEmitter`.

## JavaScript classes and class inheritance

Before getting started on the `EventEmitter` class, we need to take a look at another one of the ES2015 features: classes. JavaScript has always had objects and the concept of a class hierarchy, but nothing as formal as in other languages. The ES2015 class object builds on the existing prototype-based inheritance model, but with a syntax that looks a lot like class definitions in other languages.

For example, consider the following class, which we'll be using later in this book:

[PRE0]js\1

Functions marked with the `get` or `set` keywords are getters and setters, used as follows:

[PRE1]js\1

Finally, you declare a subclass using the `extends` operator, similar to how you would in other languages:

[PRE2]js\1

This is an ES6 module that defines a class named `Pulser`. The class inherits from `EventEmitter` and provides a few methods of its own.

Another thing to examine is how `this.emit` in the callback function refers to the `Pulser` object instance. This implementation relies on the ES2015 arrow function. Before arrow functions, our callbacks used a regular function, and `this` would not have referred to the `Pulser` object instance. Instead, `this` would have referred to some other object related to the `setInterval` function. One of the attributes of arrow functions is that `this` inside the arrow function has the same value as `this` in the surrounding context. This means, in this case, that `this` does refer to the `Pulser` object instance.

Back when we had to use `function`, rather than an arrow function, we had to assign `this` to another variable, as follows:

[PRE3]js\1

The purpose of the `Pulser` class is to send a timed event once a second to any listeners. The `start` method uses `setInterval` to kick off a repeated callback execution that is scheduled for every second and calls `emit` to send the `pulse` events to any listeners.

Now, let's see how we can use the `Pulser` object. Create a new file called `pulsed.mjs`, containing the following code:

[PRE4]js\1

For each `pulse` event received, a `pulse received` message is printed.

That gives you a little practical knowledge of the `EventEmitter` class. Let's now look at its operational theory.

## The EventEmitter theory

With the `EventEmitter` class, your code emits events that other code can receive. This is a way of connecting two separated sections of your program, kind of like how quantum entanglement means two electrons can communicate with each other from any distance. It seems simple enough.

The event name can be anything that makes sense to you, and you can define as many event names as you like. Event names are defined simply by calling `.emit` with the event name. There's nothing formal to do and no registry of event names is required. Simply making a call to `.emit` is enough to define an event name.

By convention, the `error` event name indicates an error.

An object sends events using the `.emit` function. Events are sent to any listeners that have registered to receive events from the object. The program registers to receive an event by calling that object's `.on` method, giving the event name and an event handler function.

There is no central distribution point for all events. Instead, each instance of an `EventEmitter` object manages its own set of listeners and distributes its events to those listeners.

Often, it is required to send data along with an event. To do so, simply add the data as arguments to the `.emit` call, as follows:

[PRE5]js\1

There is no handshaking between event receivers and the event sender. That is, the event sender simply goes on with its business and it gets no notifications about any events that were received, any action taken, or any errors that occurred.

In this example, we used another one of the ES2015 features—the `rest` operator—used here in the form of `...theArgs.` The `rest` operator catches any number of remaining function parameters into an array. Since `EventEmitter` can pass along any number of parameters and the `rest` operator can automatically receive any number of parameters, it's a match made in heaven—or at least in the TC-39 committee.

We've now learned how to use JavaScript classes and how to use the `EventEmitter` class. What's next is examining how the `HTTPServer` object uses `EventEmitter`.

# Understanding HTTP server applications

The `HTTPServer` object is the foundation of all Node.js web applications. The object itself is very close to the HTTP protocol, and its use requires knowledge of this protocol. Fortunately, in most cases, you'll be able to use an application framework, such as Express, to hide the HTTP protocol details. As application developers, we want to focus on business logic.

We already saw a simple HTTP server application in [Chapter 2](bd2253cb-6a41-4fc5-ae86-cc9632d44da4.xhtml), *Setting Up Node.js. *Because `HTTPServer` is an `EventEmitter` object, the example can be written in another way to make this fact explicit by separately adding the event listener:

[PRE6]js\1

The `request` event is emitted by `HTTPServer` every time a request arrives from a web browser. In this case, we want to respond differently based on the request URL, which arrives as `req.url`. This value is a string containing the URL from the HTTP request. Since there are many attributes to a URL, we need to parse the URL so that we can correctly match the pathname for one of two paths: `/` and `/osinfo`. 

Parsing a URL with the URL class requires a **base URL**, which we've supplied in the `listenOn` variable. Notice how we're reusing this same variable in a couple of other places, using one string to configure multiple parts of the application.

Depending on the path, either the `homePage` or `osInfo` functions are called.

This is called **request routing**, where we look at attributes of the incoming request, such as the request path, and route the request to handler functions.

In the handler functions, the `req` and `res` parameters correspond to the `request` and `response` objects. Where `req` contains data about the incoming request, we send the response using `res`. The `writeHead` function sets up the return status (`200` means success, while `404` means the page is not found) and the `end` function sends the response. 

If the request URL is not recognized, the server sends back an error page using a `404` result code. The result code informs the browser about the status of the request, where a `200` code means everything is fine and a `404` code means the requested page doesn't exist. There are, of course, many other HTTP response codes, each with their own meaning.

There are plenty more functions attached to both objects, but that's enough to get us started.

To run it, type the following command:

[PRE7]js\1

Before ES2015, one way to implement a multiline string was to use the following construct:

[PRE8]js\1

This is more succinct and straightforward. The opening quote is on the first line, the closing quote is on the last line, and everything in between is part of our string.

The real purpose of the template strings feature is to support easily substituting values directly into strings. Many other programming languages support this ability, and now JavaScript does, too.

Pre-ES2015, a programmer would have written their code like this:

[PRE9]js\1

Within a template string, the part within the `${ .. }` brackets is interpreted as an expression. This can be a simple mathematical expression, a variable reference, or, as in this case, a function call.

Using template strings to insert data carries a security risk. Have you verified that the data is safe? Will it form the basis of a security attack? As always, data coming from an untrusted source, such as user input, must be properly encoded for the target context where the data is being inserted. In the example here, we should have used a function to encode this data as HTML, perhaps. But for this case, the data is in the form of simple strings and numbers and comes from a known, safe data source—the built-in `os` module—and so we know that this application is safe.

For this and many other reasons, it is often safer to use an external template engine. Applications such as Express make it easy to do so.

We now have a simple HTTP-based web application. To gain more experience with HTTP events, let's add to one to a module for listening to all HTTP events.

# HTTP Sniffer – listening to the HTTP conversation

The events emitted by the `HTTPServer` object can be used for additional purposes beyond the immediate task of delivering a web application. The following code demonstrates a useful module that listens to all of the `HTTPServer` events. It could be a useful debugging tool, which also demonstrates how `HTTPServer` objects operate.

Node.js's `HTTPServer` object is an `EventEmitter` object, and HTTP Sniffer simply listens to every server event, printing out information pertinent to each event.

Create a file named `httpsniffer.mjs`, containing the following code:

[PRE10]js\1

Then, change the server setup, as follows:

[PRE11]js\1

You now have a tool for snooping on `HTTPServer` events. This simple technique prints a detailed log of event data. This pattern can be used for any `EventEmitter` objects. You can use this technique as a way to inspect the actual behavior of `EventEmitter` objects in your program.

Before we move on to using Express, we need to discuss why we use application frameworks at all.

# Web application frameworks

The `HTTPServer` object is very close to the HTTP protocol. While this is powerful in the same way that driving a stick shift car gives you low-level control over the driving experience, typical web application programming is better done at a higher level. Does anyone use assembly language to write web applications? It's better to abstract away the HTTP details and concentrate on your application.

The Node.js developer community has developed quite a few application frameworks to help with different aspects of abstracting away HTTP protocol details. Of these frameworks, Express is the most popular, and Koa ([http://koajs.com/](http://koajs.com/)) should be considered because it has fully integrated support for async functions.

The Express.js wiki has a list of frameworks built on top of Express.js or tools that work with it. This includes template engines, middleware modules, and more. The Express.js wiki is located at [https://github.com/expressjs/express/wiki](https://github.com/expressjs/express/wiki).

One reason to use a web framework is that they often have well-tested implementations of the best practices used in web application development for over 20 years. The usual best practices include the following:

*   Providing a page for bad URLs (the `404` page)
*   Screening URLs and forms for any injected scripting attacks
*   Supporting the use of cookies to maintain sessions
*   Logging requests for both usage tracking and debugging
*   Authentication
*   Handling static files, such as images, CSS, JavaScript, or HTML
*   Providing cache-control headers to caching proxies
*   Limiting things such as the page size or execution time

Web frameworks help you invest your time in a task without getting lost in the details of implementing the HTTP protocol. Abstracting away details is a time-honored way for programmers to be more efficient. This is especially true when using a library or framework that provides prepackaged functions that take care of the details.

With that in mind, let's turn to a simple application implemented with Express.

# Getting started with Express

Express is perhaps the most popular Node.js web app framework. Express is described as being Sinatra-like, which refers to a popular Ruby application framework. It is also regarded as not being an opinionated framework, meaning the framework authors don't impose their opinions about structuring an application. This means Express is not at all strict about how your code is structured; you just write it the way you think is best.

You can visit the home page for Express at [http://expressjs.com/](http://expressjs.com/).

As of the time of writing this book, Express 4.17 is the current version, and Express 5 is in alpha testing. According to the Express.js website, there are very few differences between Express 4 and Express 5.

Let's start by installing `express-generator`. While we can just start with writing some code, `express-generator` provides a blank starting application, which we'll take and modify.

Install `express-generator` using the following commands:

[PRE12]js\1

Run the `express` command, as follows:

[PRE13]js\1

This executes exactly the same, without having to install `express-generator` and (as we'll see in a moment) remembering to uninstall it when you're done using the command.

Now that you've installed `express-generator` in the `fibonacci` directory, use it to set up the blank framework application:

[PRE14]js\1

This uninstalls the `express-generator` tool. The next thing to do is to run the blank application in the way that we're told. The `npm start` command relies on a section of the supplied `package.json` file:

[PRE15]js\1

Setting the `DEBUG` variable this way turns on the debugging output, which includes a message about listening on port `3000`. Otherwise, we aren't told this information. This syntax is what's used in the Bash shell to run a command with an environment variable. If you get an error when running `npm start`, then refer to the next section.

We can modify the supplied `npm start` script to always run the app with debugging enabled. Change the `scripts` section to the following:

[PRE16]js\1

Then, the command is executed, as follows:

[PRE17]js\1

This means that `app.js` is a CommonJS module that exports the application object generated by the `express` module. Our task in `app.js` is to configure that application object. This task does not include starting the `HTTPServer` object, however. 

Now, let's turn to the `bin/www` script. It is in this script where the HTTP server is started. The first thing to notice is that it starts with the following line:

[PRE18]js\1

We can also see that the script was made executable by `express-generator`. 

It calls the `app.js` module, as follows:

[PRE19]js\1

By specifying an environment variable for `PORT`, we can tell the application to listen in on port `4242`, where you can ponder the meaning of life.

The `app` object is next passed to `http.createServer()`. A look at the Node.js documentation tells us that this function takes `requestListener`, which is simply a function that takes the `request` and `response` objects that we saw previously. Therefore, the `app` object is the same kind of function.

Finally, the `bin/www` script starts the server listening process on the port we specified.

Let's now go through `app.js` in more detail:

[PRE20]js\1

The `app.use` function mounts middleware functions. This is an important piece of Express jargon, which we will discuss shortly. At the moment, let's say that middleware functions are executed during the processing of requests. This means all the features named here are enabled in `app.js`:

*   Logging is enabled using the `morgan` request logger. Refer to [https://www.npmjs.com/package/morgan](https://www.npmjs.com/package/morgan) for its documentation.
*   The `body-parser` module handles parsing HTTP request bodies. Refer to [https://www.npmjs.com/package/body-parser](https://www.npmjs.com/package/body-parser) for its documentation.
*   The `cookie-parser` module is used to parse HTTP cookies. Refer to [https://www.npmjs.com/package/cookie-parser](https://www.npmjs.com/package/cookie-parser) for its documentation.
*   A static file web server is configured to serve the asset files in the `public` directory. Refer to [http://expressjs.com/en/starter/static-files.html](http://expressjs.com/en/starter/static-files.html) for its documentation.
*   Two router modules—`routes` and `users`—to set up which functions handle which URLs.

The static file web server arranges to serve, via HTTP requests, the files in the named directory. With the configuration shown here, the `public/stylesheets/style.css` file is available at `http://HOST/stylesheets/style.css`.

We shouldn't feel limited to setting up an Express application this way. This is the recommendation of the Express team, but there is nothing constraining us from setting it up another way. For example, later in this book, we'll rewrite this entirely as ES6 modules, rather than sticking to CommonJS modules. One glaring omission is handlers for uncaught exceptions and unhandled Promise rejections. We'll go over both of these later in this book.

Next, we will discuss Express **middleware** functions.

## Understanding Express middleware

Let's round out our walkthrough of `app.js` by discussing what Express middleware functions do for our application. Middleware functions are involved in processing requests and sending results to HTTP clients. They have access to the `request` and `response` objects and are expected to process their data and perhaps add data to these objects. For example, the cookie parser middleware parses HTTP cookie headers to record in the `request` object the cookies sent by the browser.

We have an example of this at the end of our script:

[PRE21]js\1

This does not call `next` but instead calls `res.send`. The HTTP response is sent for certain functions on the `response` object, such as `res.send` or `res.render`. This is the correct method for ending the request-response cycle, by sending a response (`res.send`) to the request. If neither `next` nor `res.send` are called, the request never gets a response and the requesting client will hang.

So, a middleware function does one of the following four things:

*   Executes its own business logic. The request logger middleware shown earlier is an example of this.
*   Modifies the `request` or `response` objects. Both `body-parser` and
    `cookie-parser` do this, looking for data to add to the `request` object.
*   Calls `next` to proceed to the next middleware function or otherwise signals an error.
*   Sends a response, ending the cycle.

The ordering of middleware execution depends on the order that they're added to the `app` object. The first function added is executed first, and so on.

The next thing to understand is request handlers and how they differ from middleware functions.

## Contrasting middleware and request handlers

We've seen two kinds of middleware functions so far. In one, the first argument is the handler function. In the other, the first argument is a string containing a URL snippet and the second argument is the handler function.

What's actually going on is `app.use` has an optional first argument: the path that the middleware is mounted on. The path is a pattern match against the request URL, and the given function is triggered if the URL matches the pattern. There's even a method to supply named parameters in the URL:

[PRE22]js\1

The required behavior of `GET` is to retrieve data, while the behavior of `PUT` is to store data. However, as the example was written above, it would match either of the HTTP methods when the handler function is only correct for the `GET` verb. However, using `app.get`, as is the case here, ensures that the application correctly matches the desired HTTP method.

Finally, we get to the `Router` object. This is the kind of middleware used explicitly for routing requests based on their URL. Take a look at `routes/users.js`:

[PRE23]js\1

This takes the `router` object, with its zero-or-more router functions, and mounts it on the `/users` URL. As Express looks for a matching routing function, it first scans the functions attached to the `app` object, and for any router object, it scans its functions as well. It then invokes any routing functions that match the request.

Going back to the issue of the `/` URL, the fact that the router is *mounted on* the `/users` URL is important. That's because the actual URL it considers matching is the mount point (`/users`) concatenated with the URL in the `router` function.

The effect is that the mount prefix is stripped from the request URL for the purpose of matching against the `router` functions attached to the `router` object. So, with that mount point, an incoming URL of `/users/login` would be stripped to just `/login` in order to find a matching `router` function.

Since not everything goes according to plan, our applications must be capable of handling error indications and showing error messages to users.

## Error handling

Now, we can finally get back to the generated `app.js` file, the `404 Error page not found` error, and any other errors that the application might show to the user.

A middleware function indicates an error by passing a value to the `next` function call, namely by calling `next(err)`. Once Express sees the error, it skips over any remaining non-error routings and only passes the error to error handlers instead. An error handler function has a different signature than what we saw earlier.

In `app.js`, which we're examining, the following is our error handler, provided by `express-generator`:

[PRE24]js\1

In a Handlebars template, the `{{value}}` markup means to substitute into the template the value of the expression or variable. The values referenced by this template—`message` and `error`—are provided by setting `res.locals` as shown here.

To see the error handler in action, let's add the following to `routes/index.js`:

[PRE25]js\1

Most of this is what `express-generator` gave us. The `var` statements have been changed to `const` for that little teensy bit of extra comfort. We explicitly imported the `hbs` module so that we could do some configuration. We also imported a router module for `Fibonacci`, which we'll see in a minute.

For the `Fibonacci` application, we don't need to support users and so we have deleted the routing module. The `routes/fibonacci.js` module, which we'll show next, serves to query a number for which we'll calculate the Fibonacci number.

In the top-level directory, create a file, `math.js`, containing the following extremely simplistic Fibonacci implementation:

[PRE26]js\1

This file contains the structure that we'll use for the HTML pages. Going by the Handlebars syntax, we can see that `{{title}}` appears within the HTML `title` tag. This means that when we call `res.render`, we should supply a `title` attribute. The `{{{body}}}` tag is where the `view` template content lands.

Change `views/index.hbs` to just contain the following:

[PRE27]js\1

This will serve as a navigation bar that's included on every page.

Create a file, `views/fibonacci.hbs`, containing the following code:

[PRE28]js\1

The anonymous object passed to `res.render` contains the data values we provide to the layout and view templates. We're now passing a new welcome message.

Then, finally, in the `routes` directory, create a file named `fibonacci.js`, containing the following code:

[PRE29]js\1

As this suggests, you can visit `http://localhost:3000/` and see what we have:

![](img/1be8113c-faf7-4ee3-b759-0c221f0bc703.png)

This page is rendered from the `views/index.hbs` template. Simply click on the Fibonacci's link to go to the next page, which is, of course, rendered from the `views/fibonacci.hbs` template. On that page, you'll be able to enter a number, click on the Submit button, and get an answer (hint—pick a number below `40` if you want your answer in a reasonable amount of time):

![](img/55b25999-812a-4621-aa47-3f9cf3dcda98.png)

We asked you to enter a number less than `40`. Go ahead and enter a larger number, such as `50`, but go take a coffee break because this is going to take a while to calculate. Or, proceed on to reading the next section, where we will start to discuss the use of computationally intensive code.

## Computationally intensive code and the Node.js event loop

This Fibonacci example is purposely inefficient to demonstrate an important consideration for your applications. What happens to the Node.js event loop when long computations are run? To see the effect, open two browser windows, each viewing the Fibonacci page. In one, enter the number `55` or greater, and in the other, enter `10`. Note how the second window freezes, and if you leave it running long enough, the answer will eventually pop up in both windows. What's happening in the Node.js event loop is blocked from processing events because the Fibonacci algorithm is running and does not ever yield to the event loop.

Since Node.js has a single execution thread, processing requests depends on request handlers quickly returning to the event loop. Normally, the asynchronous coding style ensures that the event loop executes regularly.

This is true even for requests that load data from a server halfway around the globe because the asynchronous request is non-blocking and control is quickly returned to the event loop. The naïve Fibonacci function we chose doesn't fit into this model because it's a long-running blocking operation. This type of event handler prevents the system from processing requests and stops Node.js from doing what it's meant to do—namely, to be a blisteringly fast web server.

In this case, the long-response-time problem is obvious. The response time to calculate a Fibonacci number quickly escalates to the point where you can take a vacation to Tibet, become a Lama, and perhaps get reincarnated as a llama in Peru in the time it takes to respond! However, it's also possible to create a long-response-time problem without it being as obvious as this one. Of the zillion-and-one asynchronous operations in a large web service, which one is both blocking and takes a long time to compute the result? Any blocking operations like this will cause a negative effect on the server throughput.

To see this more clearly, create a file named `fibotimes.js`, containing the following code:

[PRE30]js\1

This quickly calculates the first 40 or so members of the Fibonacci sequence, but after the 40^(th) member, it starts taking a couple of seconds per result and quickly degrades from there. It is untenable to execute code of this sort on a single-threaded system that relies on a quick return to the event loop. A web service containing code like this would give a poor performance to the users.

There are two general ways to solve this problem in Node.js:

*   **Algorithmic refactoring**: Perhaps, like the Fibonacci function we chose, one of your algorithms is suboptimal and can be rewritten to be faster. Or, if it is not faster, it can be split into callbacks dispatched through the event loop. We'll look at one method for this in a moment.
*   **Creating a backend service**: Can you imagine a backend server that is dedicated to calculating Fibonacci numbers? Okay, maybe not, but it's quite common to implement backend servers to offload work from frontend servers, and we will implement a backend Fibonacci server at the end of this chapter.

With that in mind, let's examine these possibilities.

### Algorithmic refactoring

To prove that we have an artificial problem on our hands, here is a much more efficient Fibonacci function:

[PRE31]js\1

Sometimes, your performance problems will be this easy to optimize, but other times, they won't.

The discussion here isn't about optimizing mathematics libraries but about dealing with inefficient algorithms that affect event throughput in a Node.js server. For that reason, we will stick with the inefficient Fibonacci implementation.

It is possible to divide the calculation into chunks and then dispatch the computation of those chunks through the event loop. Add the following code to `math.js`:

[PRE32]js\1

We're back to an inefficient algorithm, but one where calculations are distributed through the event loop. Running this version of `fibotimes.js` demonstrates its inefficiency. To demonstrate it in the server, we need to make a few changes.

Because it's an asynchronous function, we will need to change our router code. Create a new file, named `routes/fibonacci-async1.js`, containing the following code:

[PRE33]js\1

With this change, the server no longer freezes when calculating a large Fibonacci number. The calculation, of course, still takes a long time, but at least other users of the application aren't blocked.

You can verify this by again opening two browser windows in the application. Enter `60` in one window, and in the other, start requesting smaller Fibonacci numbers. Unlike with the original `fibonacci` function, using `fibonacciAsync` allows both windows to give answers, although if you really did enter `60` in the first window, you might as well take that three-month vacation to Tibet:

![](img/08f9d3d1-d06b-4c79-8b9b-944cd2928f9d.png)

It's up to you and your specific algorithms to choose how best to optimize your code and handle any long-running computations you may have.

We've created a simple Express application and demonstrated that there is a flaw that affects performance. We've also discussed algorithmic refactoring, which just leaves us to discuss how to implement a backend service. But first, we need to learn how to create and access a REST service.

# Making HTTPClient requests

Another way to mitigate computationally intensive code is to push the calculation to a backend process. To explore that strategy, we'll request computations from a backend Fibonacci server, using the `HTTPClient` object to do so. However, before we look at that, let's first talk in general about using the `HTTPClient` object.

Node.js includes an `HTTPClient` object, which is useful for making HTTP requests. It has the capability to issue any kind of HTTP request. In this section, we'll use the `HTTPClient` object to make HTTP requests similar to calling a REST web service.

Let's start with some code inspired by the `wget` or `curl` commands to make HTTP requests and show the results. Create a file named `wget.js`, containing the following code:

[PRE34]js\1

Yes, `example.com` is a real website—visit it someday. There's more in the printout, namely the HTML of the page at `http://example.com/`. What we've done is demonstrated how to invoke an HTTP request using the `http.request` function.

The `options` object is fairly straightforward, with the `host`, `port`, and `path` fields specifying the URL that is requested. The `method` field must be one of the HTTP verbs (`GET`, `PUT`, `POST`, and so on). You can also provide a `headers` array for the headers in the HTTP request. For example, you might need to provide a cookie:

[PRE35]js\1

This is a stripped-down Express application that gets right to the point of providing a Fibonacci calculation service. The one route it supports handles the Fibonacci computation using the same functions that we've already worked with.

This is the first time we've seen `res.send` used. It's a flexible way to send responses that can take an array of header values (for the HTTP response header) and an HTTP status code. As used here, it automatically detects the object, formats it as JSON text, and sends it with the correct `Content-Type` parameter.

In `package.json`, add the following to the `scripts` section:

[PRE36]js\1

Then, in a separate command window, we can use the `curl` program to make some requests against this service:

[PRE37]js\1

That's easy—using `curl`, we can make HTTP `GET` requests. Now, let's create a simple client program, `fiboclient.js`, to programmatically call the Fibonacci service:

[PRE38]js\1

Then, run the `client` app:

[PRE39]js\1

This is a new variant of the Fibonacci route handler, this time calling the REST backend service. We've transplanted the `http.request` call from `fiboclient.js` and integrated the events coming from the `client` object with the Express route handler. In the normal path of execution, the `HTTPClient` issues a `response` event, containing a `response` object. When that object issues a `data` event, we have our result. The result is JSON text, which we can parse and then return to the browser as the response to its request.

In `app.js`, make the following change:

[PRE40]js\1

How can we have the same value for `SERVERPORT` for all three `scripts` entries? The answer is that the variable is used differently in different places. In `startrest`, this variable is used in `routes/fibonacci-rest.js` to know at which port the REST service is running. Likewise, in `client`, `fiboclient.js` uses this variable for the same purpose. Finally, in `server`, the `fiboserver.js` script uses the `SERVERPORT` variable to know which port to listen on.

In `start` and `startrest`, no value is given for `PORT`. In both cases, `bin/www` defaults to `PORT=3000` if a value is not specified.

In a command window, start the backend server, and in another, start the application. Open a browser window, as before, and make a few requests. You should see an output similar to the following:

[PRE41]js\1

Because we haven't changed the templates, the screen will look exactly as it did earlier.

We may run into another problem with this solution. The asynchronous implementation of our inefficient Fibonacci algorithm may cause the Fibonacci service process to run out of memory. In the Node.js FAQs, [https://github.com/nodejs/node/wiki/FAQ](https://github.com/nodejs/node/wiki/FAQ), it's suggested to use the `--max_old_space_size` flag. You'd add this to `package.json`, as follows:

```js\1

However, the FAQs also say that if you're running into maximum memory space problems, your application should probably be refactored. This goes back to the point we made earlier that there are several approaches to addressing performance problems, one of which is the algorithmic refactoring of your application.

Why go through the trouble of developing this REST server when we could just directly use `fibonacciAsync`?

The main advantage is the ability to push the CPU load for this heavyweight calculation to a separate server. Doing so preserves the CPU capacity on the frontend server so that it can attend to the web browsers. GPU coprocessors are now widely used for numerical computing and can be accessed via a simple network API. The heavy computation can be kept separate, and you can even deploy a cluster of backend servers sitting behind a load balancer, evenly distributing requests. Decisions such as this are made all the time to create multi-tier systems.

What we've demonstrated is that it's possible to implement simple multi-tier REST services in a few lines of Node.js and Express. This whole exercise gave us a chance to think about computationally intensive code in Node.js and the value of splitting a larger service into multiple services.

Of course, Express isn't the only framework that can help us create REST services.

## Some RESTful modules and frameworks

Here are a few available packages and frameworks to assist your REST-based projects:

*   **Restify** ([>http://restify.com/](http://restify.com/)): This offers both client-side and server-side frameworks for both ends of REST transactions. The server-side API is similar to Express.
*   **Loopback** ([http://loopback.io/](http://loopback.io/)): This is an offering from StrongLoop. It offers a lot of features and is, of course, built on top of Express.

In this section, we've done a big thing in creating a backend REST service.

# Summary

You learned a lot in this chapter about Node.js's `EventEmitter` pattern, `HTTPClient`, and server objects, at least two ways to create an HTTP service, how to implement web applications, and even how to create a REST client and REST service integrated into a customer-facing web application. Along the way, we again explored the risks of blocking operations, the importance of keeping the event loop running, and a couple of ways to distribute work across multiple services.

Now, we can move on to implementing a more complete application: one for taking notes. We will use the `Notes` application in several upcoming chapters as a vehicle to explore the Express application framework, database access, deployment to cloud services or on your own server, user authentication, semi-real-time communication between users, and even hardening an application against several kinds of attacks. We'll end up with an application that can be deployed to cloud infrastructure.

There's still a lot to cover in this book, and it starts in the next chapter with creating a basic Express application.