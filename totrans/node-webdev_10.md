Authenticating Users with a Microservice

Now that our Notes application can save its data in a database, we can think about the next phase of making this a real application—namely, authenticating our users. 

It's so natural to log in to a website to use its services. We do it every day, and we even trust banking and investment organizations to secure our financial information through login procedures on a website. The **HyperText Transfer Protocol** (**HTTP**) is a stateless protocol, and a web application cannot tell much about one HTTP request compared with another. Because HTTP is stateless, HTTP requests do not natively know the user's identity, whether the user driving the web browser is logged in, or even whether the HTTP request was initiated by a human being.

The typical method for user authentication is to send a cookie containing a token to the browser, to carry the user's identity, and indicate whether that browser is logged in.

With Express, the best way to do this is with the `express-session` middleware, which handles session management with a cookie. It is easy to configure but is not a complete solution for user authentication since it does not handle user login/logout.

The package that appears to be leading the pack in user authentication is Passport ([http://passportjs.org/](http://passportjs.org/)). In addition to authenticating users against local user information, it supports a long list of third-party services against which to authenticate. With this, a website can be developed that lets users sign up with credentials from another website—Twitter, for example. 

We will use Passport to authenticate users against either a locally stored database or a Twitter account. We'll also take this as an opportunity to explore a **representational state transfer** (**REST**)-based microservice with Node.js. 

The rationale is the greater opportunity to increase security by storing user information in a highly protected enclave. Many application teams store user information in a well-protected barricaded area with a strictly controlled **application programming interface** (**API**), and even physical access to the user information database, implementing as many technological barriers as possible against unapproved access. We're not going to go quite that far, but by the end of the book, the user information service will be deployed in its own Docker container.

 In this chapter, we'll discuss the following three aspects of this phase:

*   Creating a microservice to store user profile/authentication data.
*   Authenticating a user with a locally stored password.
*   Using OAuth2 to support authentication via third-party services. Specifically, we'll use Twitter as a third-party authentication service.

Let's get started!

The first thing to do is to duplicate the code used for the previous chapter. For example, if you kept that code in the `chap07/notes` directory, create a new directory, `chap08/notes`.

# Creating a user information microservice

We could implement user authentication and accounts by simply adding a user model and a few routes and views to the existing *Notes* application. While that's easy, is this what is done in a real-world production application?

Consider the high value of user identity information and the super-strong need for robust and reliable user authentication. Website intrusions happen regularly, and it seems the item most frequently stolen is user identities. To that end, we declared earlier an intention to develop a user information microservice, but we must first discuss the technical rationale for doing so.

Microservices are not a panacea, of course, meaning we shouldn't try to force-fit every application into the microservice box. By analogy, microservices fit with the Unix philosophy of small tools, each doing one thing well, which we mix/match/combine into larger tools. Another word for this is composability. While we can build a lot of useful software tools with that philosophy, does it work for applications such as Photoshop or LibreOffice?  

This is why microservices are popular today among application teams. Microservice architectures are more agile if used well. And, as we noted earlier, we're aiming for a highly secured microservice deployment.

With that decision out of the way, there are two other decisions to be made with regard to security implications. They are as follows:

*   Do we create our own REST application framework?
*   Do we create our own user login/authentication framework?

In many cases, it is better to use a well-regarded existing library where the maintainers have already stomped out lots of bugs, just as we used the Sequelize **ORM** (**Object-Relational Mapping**) library in the previous chapter, because of its maturity. We have identified two libraries for this phase of the Notes project.

We already mentioned using Passport for user login support, as well as authenticating Twitter users.

For REST support, we could have continued using Express, but instead will use Restify ([http://restify.com/](http://restify.com/)), which is a popular REST-centric application framework.

To test the service, we'll write a command-line tool for administering user information in the database. We won't be implementing an administrative user interface in the Notes application, and will instead rely on this tool to administer the users. As a side effect, we'll have a tool for testing the user service.

Once this service is functioning correctly, we'll set about modifying the Notes application to access user information from the service, while using Passport to handle authentication.

The first step is to create a new directory to hold the user information microservice. This should be a sibling directory to the Notes application. If you created a directory named `chap08/notes` to hold the Notes application, then create a directory named `chap08/users` to hold the microservice.

Then, in the `chap08/users` directory, run the following commands:

[PRE0]js\1

As with our Sequelize-based model for Notes, we will use a **YAML Ain't Markup Language** (**YAML**) file to store connection configuration. We're even using the same environment variable, `SEQUELIZE_CONNECT`, and the same approach to overriding fields of the configuration. The approach is similar, with a `connectDB` function setting up the connection and initializing the SQUsers table.

With this approach, we can use a base configuration file in the `SEQUELIZE_CONNECT` variable and then use the other environment variables to override its fields.  This will be useful when we start deploying Docker containers.

The user profile schema shown here is derived from the normalized profile provided by Passport—for more information, refer to [http://www.passportjs.org/docs/profile](http://www.passportjs.org/docs/profile). 

The Passport project developed this object by harmonizing the user information given by several third-party services into a single object definition. To simplify our code, we're simply using the schema defined by Passport.

There are several functions to create that will be an API to manage user data. Let's add them to the bottom of `users-sequelize.mjs`, starting with the following code:

[PRE1]js\1

When we fetch an SQUser object from the database, Sequelize obviously gives us a Sequelize object that has many extra fields and functions used by Sequelize. We don't want to send that data to our callers. Furthermore, we think it will increase security to not provide the *password* data beyond the boundary of this server. This function produces a simple, sanitized, anonymous JavaScript object from the SQUser instance. We could have defined a full JavaScript class, but would that have served any purpose? This anonymous JavaScript class is sufficient for this simple server, as illustrated in the following code block:

[PRE2]js\1

This is just like the configuration files we used in the previous chapter.

That's what we need for the database side of this service. Let's now move on to creating the REST service.

## Creating a REST server for user information

The user information service is a REST server to handle user information data and authentication. Our goal is, of course, to integrate that with the Notes application, but in a real project, such a user information service could be integrated with several web applications. The REST service will provide functions we found useful while developing the user login/logout support in Notes, which we'll show later in the chapter.

In the `package.json` file, change the `main` tag to the following line of code:

[PRE3]js\1

Clearly, this is how we'll start our server. It uses the configuration file from the previous section and specifies that we'll listen on port `5858`.

Then, create a file named `user-server.mjs` containing the following code:

[PRE4]js\1

This handler executes for every request and immediately follows `restify.plugins.authorizationParser`. It looks for authorization data—specifically, HTTP basic authorization—to have been supplied in the HTTP request. It then loops through the list of keys in the `apiKeys` array, and if the Basic Auth parameters supplied matched, then the caller is accepted.

This should not be taken as an example of a best practice since HTTP Basic Auth is widely known to be extremely insecure, among other issues. But it demonstrates the basic concept, and also shows that enforcing token-based authorization is easily done with a similar handler.

This also shows us the function signature of a Restify handler function—namely, that it is the same signature used for Express middleware, the `request` and `result` objects, and the `next` callback. 

There is a big difference between Restify and Express as to how the `next` callback is used. In Express, remember that a middleware function calls `next` unless that middleware function is the last function on the processing chain—for example if the function has called `res.send` (or equivalent) to send a response to the caller. In Restify, every handler function calls `next`. If a handler function knows it should be the last function on the handler chain, then it uses `next(false)`; otherwise, it calls `next()`. If a handler function needs to indicate an error, it calls `next(err)`, where `err` is an object where `instanceof Error` is `true`.

Consider the following hypothetical handler function:

[PRE5]js\1

This is just the starting point of the command-line tool. For most of the REST handler functions, we'll also implement a sub-command in this tool. We'll take care of that code in the subsequent sections. For now, let's focus on how the command-line tool is set up.

The Commander project suggests we name the default import `program`, as shown in the preceding code block. As mentioned earlier, we declare the command-line options and sub-commands by calling methods on this object.

In order to properly parse the command line, the last line of code in `cli.mjs` must be as follows:

[PRE6]js\1

This declares an option, either `-p` or `--port`, that Commander will parse out of the command line. Notice that all we do is write a text string and, from that, Commander knows it must parse these options. Isn't this easy?

When it sees one of these options, the `<port>` declaration tells Commander that this option requires an argument. It will parse that argument out of the command line, and then assign it to `program.port`.

Therefore, `program.port`, `program.host`, and `program.url` were all declared in a similar way. When Commander sees those options, it will create the matching variables, and then our `client` function will take that data and modify `connect_url` appropriately.

One of the side effects of these declarations is that Commander can generate help text automatically. The result we'll achieve is being able to type the following code:

[PRE7]js\1

This handles a `POST` request on the `/create-user` URL. This should look very similar to an Express route handler function, apart from the use of the `next` callback. Refer back to the discussion on this. As we did with the Notes application, we declare the handler callback as an async function and then use a `try`/`catch` structure to catch all errors and report them as errors.

The handler starts with `connectDB` to ensure the database is set up. Then, if you refer back to the `createUser` function, you see it gathers up the user data from the request parameters and then uses `SQUser.create` to create an entry in the database. What we will receive here is the sanitized user object, and we simply return that to the caller.

Let's also add the following code to `user-server.mjs`:

[PRE8]js\1

By using `program.command`, we are declaring a sub-command—in this case, `add`. The `<username>` declaration says that this sub-command takes an argument. Commander will provide that argument value in the `username` parameter to the function passed in the `action` method.

The structure of a `program.command` declaration is to first declare the syntax of the sub-command. The `description` method provides user-friendly documentation. The `option` method calls are options for this sub-command, rather than global options. Finally, the `action` method is where we supply a callback function that will be invoked when Commander sees this sub-command in the command line.

Any arguments declared in the `program.command` string end up as parameters to that callback function.

Any values for the options for this sub-command will land in the `cmdObj` object. By contrast, the value for global options is attached to the `program` object.

With that understanding, we can see that this sub-command gathers information from the command line and then uses the `client` function to connect to the server. It invokes the `/create-user` URL, passing along the data gathered from the command line. Upon receiving the response, it will print either the error or the result object.

Let's now add the sub-command corresponding to the `/find-or-create` URL, as follows:

[PRE9]js\1

We run this in one command window to start the server. In another command window, we can run the following command:

[PRE10]js\1

Likewise, we have success with the `find-or-create` command.

That gives us the ability to create SQUser objects. Next, let's see how to read from the database.

### Reading user data from the user information service

The next thing we want to support is to look for users in the user information service. Instead of a general search facility, the need is to retrieve an SQUser object for a given username. We already have the utility function for this purpose; it's just a matter of hooking up a REST endpoint.

In `user-server.mjs`, add the following function:

[PRE11]js\1

We know from the previous chapter that the `findAll` operation retrieves all matching objects and that passing an empty query selector such as this causes `findAll` to match every SQUser object. Therefore, this performs the task we described, to retrieve information on all users. 

Then, in `cli.mjs`, we add the following sub-command declarations:

[PRE12]js\1

And, indeed, the results came in as we expected.

The next operation we need is to update an SQUser object.

### Updating user information in the user information service

The next functionality to add is to update user information. For this, we can use the Sequelize `update` function, and simply expose it as a REST operation.

To that end, add the following code to `user-server.mjs`:

[PRE13]js\1

As expected, this sub-command must take the same set of user information parameters. It then bundles those parameters into an object, posting it to the `/update-user` endpoint on the REST server. 

Then, to test the result, we run the command, like so:

[PRE14]js\1

This is simple enough. We first look up the user to ensure it exists, and then call the `destroy` function on the SQUser object. There's no need for any result, so we send an empty object.

To exercise this function, add the following code to `cli.mjs`:

[PRE15]js\1

First, we deleted Snuffy's user record, and it gave us an empty response, as expected. Then, we tried to retrieve his record and, as expected, there was an error.

While we have completed the CRUD operations, we have one final task to cover.

### Checking the user's password in the user information service

How can we have a user login/logout service without being able to check their password? The question is: Where should the password check occur? It seems, without examining it too deeply, that it's better to perform this operation inside the user information service. We earlier described the decision that it's probably safer to never expose the user password beyond the user information service. As a result, the password check should occur in that service so that the password does not stray beyond the service.

Let's start with the following function in `user-server.mjs`:

[PRE16]js\1

And, as expected, the code to invoke this operation is simple. We take the `username` and `password` parameters from the command line, send them to the server, and then print the result.

To verify that it works, run the following command:

[PRE17]js\1

Then, create a new file, `models/users-superagent.mjs`, containing the following code:

[PRE18]js\1

These are our `create` and `update` functions. In each case, they take the data provided, construct an anonymous object, and `POST` it to the server. The function is to be provided with the values corresponding to the SQUser schema. It bundles the data provided in the `send` method, sets various parameters, and then sets up the Basic Auth token.

The SuperAgent library uses an API style called *method chaining*. The coder chains together method calls to construct a request. The chain of method calls can end in a `.then` or `.end` clause, either of which takes a callback function. But leave off both, and it will return a Promise, and, of course, Promises let us use this directly from an async function.

The `res.body` value at the end of each function contains the value returned by the REST server. All through this library, we'll use the `.auth` clause to set up the required authentication key. 

These anonymous objects are a little different than normal. We're using a new **ECMAScript 2015** (**ES-2015**) feature here that we haven't discussed so far. Rather than specifying the object fields using the `fieldName: fieldValue` notation, ES-2015 gives us the option to shorten this when the variable name used for `fieldValue` matches the desired `fieldName`. In other words, we can just list the variable names, and the field name will automatically match the variable name.

In this case, we've purposely chosen variable names for the parameters to match the field names of the object with parameter names used by the server. In doing so, we can use this shortened notation for anonymous objects, and our code is a little cleaner by using consistent variable names from beginning to end.

Now, add the following function to support the retrieval of user records:

[PRE19]js\1

One point about this method is worth noting. It could have taken the parameters in the URL instead of the request body, as is done here. But since request URLs are routinely logged to files, putting the username and password parameters in the URL means user identity information would be logged to files and be part of activity reports. That would obviously be a very bad choice. Putting those parameters in the request body not only avoids that bad result but if an HTTPS connection to the service were used, the transaction would be encrypted.

Then, let's create our `find-or-create` function, as follows:

[PRE20]js\1

As before, this is very straightforward.

With this module, we can interface with the user information service, and we can now proceed with modifying the Notes user interface.

## Incorporating login and logout routing functions in the Notes application

What we've built so far is a user data model, with a REST API wrapping that model to create our authentication information service. Then, within the Notes application, we have a module that requests user data from this server. As yet, nothing in the Notes application knows that this user model exists. The next step is to create a routing module for login/logout URLs and to change the rest of Notes to use user data.

The routing module is where we use `passport` to handle user authentication. The first task is to install the required modules, as follows:

[PRE21]js\1

Express Session support, including all the various Session Store implementations, is documented on its GitHub project page at [https://github.com/expressjs/session](https://github.com/expressjs/session). 

The strategy implemented in the `passport-local` package authenticates solely using data stored locally to the application—for example, our user authentication information service. Later, we'll add a strategy module to authenticate the use of OAuth with Twitter.

Let's start by creating the routing module, `routes/users.mjs`, as follows:

[PRE22]js\1

The `initPassport` function will be called from `app.mjs`, and it installs the Passport middleware in the Express configuration. We'll discuss the implications of this later when we get to `app.mjs` changes, but Passport uses sessions to detect whether this HTTP request is authenticated. It looks at every request coming into the application, looks for clues about whether this browser is logged in, and attaches data to the request object as `req.user`.

The `ensureAuthenticated` function will be used by other routing modules and is to be inserted into any route definition that requires an authenticated logged-in user. For example, editing or deleting a note requires the user to be logged in and, therefore, the corresponding routes in `routes/notes.mjs` must use `ensureAuthenticated`. If the user is not logged in, this function redirects them to `/users/login` so that they can log in.

Add the following route handlers in `routes/users.mjs`:

[PRE23]js\1

When the user requests to log out of Notes, they are to be sent to `/users/logout`. We'll be adding a button to the header template for this purpose. The `req.logout` function instructs Passport to erase their login credentials, and they are then redirected to the home page.

This function deviates from what's in the Passport documentation. There, we are told to simply call `req.logout`, but calling only that function sometimes results in the user not being logged out. It's necessary to destroy the session object, and to clear the cookie, in order to ensure that the user is logged out. The cookie name is defined in `app.mjs`, and we imported `sessionCookieName` for this function.

Add the `LocalStrategy` to Passport, as follows:

[PRE24]js\1

The preceding functions take care of encoding and decoding authentication data for the session. All we need to attach to the session is the `username`, as we did in `serializeUser`. The `deserializeUser` object is called while processing an incoming HTTP request and is where we look up the user profile data. Passport will attach this to the request object.

### Login/logout changes to app.mjs

A number of changes are necessary in `app.mjs`, some of which we've already touched on. We did carefully isolate the Passport module dependencies to `routes/users.mjs`. The changes required in `app.mjs` support the code in `routes/users.mjs`.

Add an import to bring in functions from the User router module, as follows:

[PRE25]js\1

Because Passport uses sessions, we need to enable session support in Express, and these modules do so. The `session-file-store` module saves our session data to disk so that we can kill and restart the application without losing sessions. It's also possible to save sessions to databases with appropriate modules. A filesystem session store is suitable only when all Notes instances are running on the same server computer. For a distributed deployment situation, you'll need to use a session store that runs on a network-wide service, such as a database.

We're defining `sessionCookieName` here so that it can be used in multiple places. By default, `express-session` uses a cookie named `connect.sid` to store the session data. As a small measure of security, it's useful when there's a published default to use a different non-default value. Any time we use the default value, it's possible that an attacker might know a security flaw, depending on that default. 

Add the following code to `app.mjs`:

[PRE26]js\1

This is the same initialization, but using `MemoryStore` instead of `FileStore`.

To learn more about session store implementations see:  [http://expressjs.com/en/resources/middleware/session.html#compatible-session-stores](http://expressjs.com/en/resources/middleware/session.html#compatible-session-stores)

Mount the User router, as follows:

[PRE27]js\1

Remember that we ensured that `req.user` has the user profile data, which we did in `deserializeUser`. We simply check for this and make sure to add that data when rendering the views template.

We'll be making similar changes to most of the other route definitions. After that, we'll go over the changes to the view templates, in which we use `req.user` to show the correct buttons on each page.

### Login/logout changes required in routes/notes.mjs

The changes required here are more significant but still straightforward, as shown in the following code snippet:

[PRE28]js\1

We'll be making similar changes throughout this module, adding calls to `ensureAuthenticated` and using `req.user` to check whether the user is logged in. The goal is for several routes to ensure that the route is only available to a logged-in user, and—in those and additional routes—to pass the `user` object to the template.

The first thing we added is to call `usersRouter.ensureAuthenticated` in the route definition. If the user is not logged in, they'll be redirected to `/users/login` thanks to that function.

Because we've ensured that the user is authenticated, we know that `req.user` will already have their profile information. We can then simply pass it to the view template.

For the other routes, we need to make similar changes.

Modify the `/save` route handler, as follows:

[PRE29]js\1

For this route, we don't require the user to be logged in. We do need the user's profile information, if any, sent to the view template.

Modify the `/edit` and `/destroy` route handlers, as follows:

[PRE30]js\1

What we're doing here is controlling which buttons to display at the top of the screen, depending on whether the user is logged in. The earlier changes ensure that the `user` variable will be `undefined` if the user is logged out; otherwise, it will have the user profile object. Therefore, it's sufficient to check the `user` variable, as shown in the preceding code block, to render different user interface elements.

A logged-out user doesn't get the ADD Note button and gets a Log in button. Otherwise, the user gets an ADD Note button and a Log Out button. The Log in button takes the user to `/users/login`, while the Log Out button takes them to `/users/logout`. Both of those buttons are handled in `routes/users.js` and perform the expected function.

The Log Out button has a Bootstrap badge component displaying the username. This adds a little visual splotch in which we'll put the username that's logged in. As we'll see later, it will serve as a visual clue to the user as to their identity.

Because `nav` is now supporting login/logout buttons, we have changed the `navbar-toggler` button so that it controls a `<div>` with `id="navbarLogIn"`.

We need to create `views/login.hbs`, as follows:

[PRE31]js\1

That's straightforward—if the user is logged in, display the form; otherwise, display the message in `partials/not-logged-in.hbs`. We determine which of these to display based on the `user` variable.

We could insert something such as the code shown in the following block in `partials/not-logged-in.hbs`:

[PRE32]js\1

That is, at the bottom we add a segment that, for non-logged-in users, pulls in the `not-logged-in` partial.

The **Bootstrap jumbotron** component makes a nice and large text display that stands out nicely and will catch the viewer's attention. However, the user should never see this because each of those templates is used only when we've pre-verified the fact that the user is logged in.

A message such as this is useful as a check against bugs in your code. Suppose that we slipped up and failed to properly ensure that these forms were displayed only to logged-in users. Suppose that we had other bugs that didn't check the form submission to ensure it's requested only by a logged-in user. Fixing the template in this way is another layer of prevention against displaying forms to users who are not allowed to use that functionality.

We have now made all the changes to the user interface and are ready to test the login/logout functionality.

## Running the Notes application with user authentication

We have created the user information REST service, created a module to access that service from Notes,  modified the router modules to correctly access the user information service, and changed other things required to support login/logout.  

The final task that is necessary is to change the scripts section of `package.json`, as follows:

[PRE33]js\1

Then, in another window, start the Notes application, as follows:

[PRE34]js\1

The documentation says we should load the `dotenv` package and then call `dotenv.config()` very early in the start up phase of our application, and that we must do this before accessing any environment variables. However, reading the documentation more closely, it seems best to add the following code to `app.mjs`:

[PRE35]js\1

This is exactly the syntax we'd expect since it is the same as for shell scripts. In this file, we need two variables to be defined, `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET`. We will use these variables in the code we'll write in the next section. Since we are putting configuration values in the `scripts` section of `package.json`, feel free to add those environment variables to `.env` as well. 

The next step is to avoid committing this file to a source code control system such as Git. To ensure that this does not happen, you should already have a `.gitignore` file in the `notes` directory, and make sure its contents are something like this:

[PRE36]js\1

In `routes/users.mjs`, let's start making some changes, as follows:

[PRE37]js\1

This registers a `TwitterStrategy` instance with `passport`, arranging to call the user authentication service as users register with the Notes application. This `callback` function is called when users successfully authenticate using Twitter.

If the environment variables containing the Twitter tokens are not set, then this code does not execute. Clearly, it would be an error to set up Twitter authentication without the keys, so we avoid the error by not executing the code. 

To help other code know whether Twitter support is enabled, we export a flag variable - `twitterLogin`.

We defined the `usersModel.findOrCreate` function specifically to handle user registration from third-party services such as Twitter. Its task is to look for the user described in the profile object and, if that user does not exist, to create that user account in Notes.

The `consumerKey` and `consumerSecret` values are supplied by Twitter, after you've registered your application. These secrets are used in the OAuth protocol as proof of identity to Twitter.

The `callbackURL` setting in the `TwitterStrategy` configuration is a holdover from Twitter's OAuth1-based API implementation. In OAuth1, the callback URL was passed as part of the OAuth request. Since `TwitterStrategy` uses Twitter's OAuth1 service, we have to supply the URL here. We'll see in a moment where that URL is implemented in Notes.

The `callbackURL`, `consumerKey`, and `consumerSecret` settings are all injected using environment variables. Earlier, we discussed how it is a best practice to not commit the values for `consumerKey` and `consumerSecret` to a source repository, and therefore we set up the `dotenv` package and a `.env` file to hold those configuration values. In Chapter 10,* Deploying Node.js Applications to Linux Servers*, we'll see that these keys can be declared as environment variables in a Dockerfile. 

Add the following route declaration:

[PRE38]js\1

This route handles the callback URL, and it corresponds to the `callbackURL` setting configured earlier. Depending on whether it indicates a successful registration, Passport will redirect the browser to either the home page or back to the `/users/login` page. 

Because `router` is mounted on `/user`, this URL is actually `/user/auth/twitter/callback`. Therefore, the full URL to use in configuring the `TwitterStrategy`, and to supply to Twitter, is `http://localhost:3000/user/auth/twitter/callback`. 

In the process of handling the callback URL, Passport will invoke the callback function shown earlier. Because our callback uses the `usersModel.findOrCreate` function, the user will be automatically registered if necessary.

We're almost ready, but we need to make a couple of small changes elsewhere in Notes.

In `partials/header.hbs`, make the following changes to the code:

[PRE39]js\1

This imports the variable, and then, in the data passed to `res.render`, we add this variable. This will ensure that the value reaches `partials/header.hbs`.

In `routes/notes.mjs`, we have a similar change to make in several router functions:

[PRE40]js\1

Then, use a browser to visit `http://localhost:3000`, as follows:

![](img/2eaeb209-1f22-424a-ab86-0563fa7474c1.png)

Notice the new button. It looks about right, thanks to having used the official Twitter branding image. The button is a little large, so maybe you want to consult a designer. Obviously, a different design is required if you're going to support dozens of authentication services.

Run it while leaving out the Twitter token environment variables, and the Twitter login button should not appear.

Clicking on this button takes the browser to `/users/auth/twitter`, which is meant to start Passport running the OAuth protocol transactions necessary to authenticate. Instead, you may receive an error message that states Callback URL not approved for this client application. Approved callback URLs can be adjusted in your application settings. If this is the case, it is necessary to adjust the application configuration on `developer.twitter.com`. The error message is clearly saying that Twitter saw a URL being used that was not approved.

On the page for your application, on the App Details tab, click the Edit button. Then, scroll down to the Callback URLs section and add the following entries:

![](img/cbe8f693-9128-44b9-b8f4-928b960c9770.png)

As it explains, this box lists the URLs that are allowed to be used for Twitter OAuth authentication. At the moment, we are hosting the application on our laptop using port `3000`. If you are accessing it from other base URLs, such as `http://MacBook-Pro-4.local`, then that base URL should be used in addition.

Once you have the callback URLs correctly configured, clicking on the Login with Twitter button will take you to a normal Twitter OAuth authentication page. Simply click for approval, and you'll be redirected back to the Notes application.

And then, once you're logged in with Twitter, you'll see something like the following screenshot:

![](img/0e324c9a-3128-40c1-9d5c-1d90d2682130.png)

We're now logged in, and will notice that our Notes username is the same as our Twitter username. You can browse around the application and create, edit, or delete notes. In fact, you can do this to any note you like, even ones created by others. That's because we did not create any sort of access control or permissions system, and therefore every user has complete access to every note. That's a feature to put on the backlog.

By using multiple browsers or computers, you can simultaneously log in as different users, one user per browser.

You can run multiple instances of the Notes application by doing what we did earlier, as follows:

[PRE41]js\1

In another command window, run the following command:

[PRE42]js\1

This is after logging in using a Twitter account. You can see that the Twitter account name is stored here in the session data.

What if you want to clear a session? It's just a file in the filesystem. Deleting the session file erases the session, and the user's browser will be forcefully logged out.

The session will time out if the user leaves their browser idle for long enough. One of the `session-file-store` options, `ttl`, controls the timeout period, which defaults to 3,600 seconds (an hour). With a timed-out session, the application reverts to a logged-out state.

In this section, we've gone through the full process of setting up support for login using Twitter's authentication service. We created a Twitter developer account and created an application on Twitter's backend. Then, we implemented the required workflow to integrate with Twitter's OAuth support. To support this, we integrated the storage of user authorizations from Twitter in the user information service.

Our next task is extremely important: to keep user passwords encrypted.

# Keeping secrets and passwords secure

We've cautioned several times about the importance of safely handling user identification information. The intention to handle that data safely is one thing, but it is important to follow through and actually do so. While we're using a few good practices so far, as it stands, the Notes application would not withstand any kind of security audit for the following reasons:

*   User passwords are kept in clear text in the database.
*   The authentication tokens for Twitter et al. are in clear text.
*   The authentication service API key is not a cryptographically secure anything; it's just a clear text **universally unique identifier** (**UUID**).

If you don't recognize the phrase *clear text*, it simply means unencrypted. Anyone could read the text of user passwords or the authentication tokens. It's best to keep both encrypted to avoid information leakage.

Keep this issue in the back of your mind because we'll revisit these—and other—security issues in [Chapter 14](4cccad1e-fe7e-495a-9e90-8818820b890a.xhtml), *Security in Node.js Applications*.

Before we leave this chapter, let's fix the first of those issues: storing passwords in plain text. We made the case earlier that user information security is extremely important. Therefore, we should take care of this from the beginning.

The `bcrypt` Node.js package makes it easy to securely store passwords. With it, we can easily encrypt the password right away, and never store an unencrypted password.  

For `bcrypt` documentation, refer to [https://www.npmjs.com/package/bcrypt](https://www.npmjs.com/package/bcrypt).

To install `bcrypt` in both the `notes` and `users` directories, execute the following command:

[PRE43]js\1

This brings in the `bcrypt` package, and then we configure a constant that governs the CPU time required to decrypt a password. The `bcrypt` documentation points to a blog post discussing why the algorithm of `bcrypt` is excellent for storing encrypted passwords. The argument boils down to the CPU time required for decryption. A brute-force attack against the password database is harder, and therefore less likely to succeed if the passwords are encrypted using strong encryption, because of the CPU time required to test all password combinations.

The value we assign to `saltRounds` determines the CPU time requirement. The documentation explains this further.

Next, add the following function:

[PRE44]js\1

That is, in each, we make the callback function an async function so that we can use `await`. Then, we call the `hashpass` function to encrypt the password.

This way, we are encrypting the password right away, and the user information server will be storing an encrypted password.

Therefore, in `user-server.mjs`, the `password-check` handler must be rewritten to accommodate checking an encrypted password.

At the top of `user-server.mjs`, add the following import:

[PRE45]js\1

The `bcrypt.compare` function compares a plain text password, which will be arriving as `req.params.password`, against the encrypted password that we've stored. To handle encryption, we needed to refactor the checks, but we are testing for the same three conditions. And, more importantly, this returns the same objects for those conditions.

To test it, start the user information server as we've done before, like this:

[PRE46]js\1

We've done both these steps before. Where it differs is what we do next.

Let's check the database to see what was stored, as follows:

[PRE47]js\1

We performed this same test earlier, but this time, it is against the encrypted password. 

We have verified that a REST call to check the password will work. Our next step is to implement the same changes in the Notes application.

## Implementing encrypted password support in the Notes application

Since we've already proved how to implement encrypted password checking, all we need to do is duplicate some code in the Notes server.

In `users-superagent.mjs`, add the following code to the top:

[PRE48]js\1

In those places where it is appropriate, we must encrypt the password. No other change is required.

Because the `password-check` backend performs the same checks, returning the same object, no change is required in the frontend code.

To test, start both the user information server and the Notes server. Then, use the application to check logging in and out with both a Twitter-based user and a local user.

We've learned how to use encryption to safely store user passwords. If someone steals our user database, cracking the passwords will take longer thanks to the choices made here.

We're almost done with this chapter. The remaining task is simply to review the application architecture we've created.

# Running the Notes application stack

Did you notice earlier when we said to run the Notes application stack? It's time to explain to the marketing team what's meant by that phrase. They may want to put an architecture diagram on marketing brochures or websites. It's also useful for developers such as us to take a step back and draw a picture of what we've created, or are planning to create. 

Here's the sort of diagram that an engineer might draw to show the marketing team the system design (the marketing team will, of course, hire a graphics artist to clean it up):

![](img/56c15d1d-4fe7-45a8-8e6d-5410f048234e.png)

The box labeled Notes Application in the preceding diagram is the public-facing code implemented by the templates and the router modules. As currently configured, it's visible from our laptop on port `3000`. It can use one of several data storage services. It communicates with the User Authentication Service backend over port `5858` (or port `3333`, as shown in the preceding diagram).

In [Chapter 10](176ce11c-dd6f-4ebf-ba14-529be6db28da.xhtml),* Deploying Node.js Applications to Linux Servers,* we'll be expanding this picture a bit as we learn how to deploy on a real server.

# Summary

You've covered a lot of ground in this chapter, looking at not only user authentication in Express applications, but also microservices development.

Specifically, you covered session management in Express, using Passport for user authentication—including Twitter/OAuth, using router middleware to limit access, creating a REST service with Restify, and when to create a microservice. We've even used an encryption algorithm to ensure that we only store encrypted passwords.

Knowing how to handle login/logout, especially OAuth login from third-party services, is an essential skill for web application developers. Now that you've learned this, you'll be able to do the same for your own applications.

In the next chapter, we'll take the Notes application to a new level with semi-real-time communication between application users. To do this, we'll write some browser-side JavaScript and explore how the Socket.io package can let us send messages between users.