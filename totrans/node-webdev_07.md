Your First Express Application

Now that we've got our feet wet building an Express application for Node.js, let's start developing an application that performs a useful function. The application we'll build will keep a list of notes and will eventually have users who can send messages to each other. Over the course of this book, we will use it to explore some aspects of real Express web applications.

In this chapter, we'll start with the basic structure of an application, the initial UI, and the data model. We'll also lay the groundwork for adding persistent data storage and all the other features that we will cover in later chapters.

The topics covered in this chapter include the following:

*   Using Promises and async functions in Express router functions
*   JavaScript class definitions and data hiding in JavaScript classes
*   The architecture of an Express application using the MVC paradigm
*   Building an Express application
*   Implementing the CRUD paradigm
*   Express application theming and Handlebars templates

To get started, we will talk about integrating Express router callbacks with async functions.

# Exploring Promises and async functions in Express router functions

Before we get into developing our application, we need to take a deeper look at using the `Promise` class and async functions with Express because Express was invented before these features existed, and so it does not directly integrate with them. While we should be using async functions wherever possible, we have to be aware of how to properly use them in certain circumstances, such as in an Express application.

The rules in Express for handling asynchronous execution are as follows:

*   Synchronous errors are caught by Express and cause the application to go to the error handler.
*   Asynchronous errors must be reported by calling `next(err)`.
*   A successfully executing middleware function tells Express to invoke the next middleware by calling `next()`.
*   A router function that returns a result to the HTTP request does not call `next()`.

In this section, we'll discuss three ways to use Promises and async functions in a way that is compatible with these rules.

Both Promises and async functions are used for deferred and asynchronous computation and can make intensely nested callback functions a thing of the past:

*   A `Promise` class represents an operation that hasn't completed yet but is expected to be completed in the future. We've used Promises already, so we know that the `.then` or `.catch` functions are invoked asynchronously when the promised result (or error) is available.
*   Inside an async function, the `await` keyword is available to automatically wait for a Promise to resolve. It returns the result of a Promise, or else throws errors, in the natural location at the next line of code, while also accommodating asynchronous execution. 

The magic of async functions is that we can write asynchronous code that looks like synchronous code. It's still asynchronous code—meaning it works correctly with the Node.js event loop—but instead of results and errors landing inside callback functions, errors are thrown naturally as exceptions and results naturally land on the next line of code. 

Because this is a new feature in JavaScript, there are several traditional asynchronous coding practices with which we must correctly integrate. You may come across some other libraries for managing asynchronous code, including the following:

*   The `async` library is a collection of functions for various asynchronous patterns. It was originally completely implemented around the callback function paradigm, but the current version can handle async functions and is available as an ES6 package. Refer to [https://www.npmjs.com/package/async](https://www.npmjs.com/package/async) for more information.
*   Before Promises were standardized, at least two implementations were available: Bluebird ([http://bluebirdjs.com/](http://bluebirdjs.com/)) and Q ([https://www.npmjs.com/package/q](https://www.npmjs.com/package/q)). Nowadays, we focus on using the standard, built-in `Promise` object, but both of these packages offer additional features. What's more likely is that we will come across older code that uses these libraries.

These and other tools were developed to make it easier to write asynchronous code and to solve the **pyramid of doom** problem. This is named after the shape that the code takes after a few layers of nesting. Any multistage process written as callbacks can quickly escalate to code that is nested many levels deep. Consider the following example:

[PRE0]js\1

A function like this creates the `Promise` object, giving it a callback function, within which is your asynchronous operation. The `resolve` and `reject` functions are passed into that function and are called when the Promise is resolved as either a success or failure state. A typical use of `new Promise` is a structure like this:

[PRE1]js\1

The `Promise` object is fluid enough that the function passed in a `.then` handler can return something, such as another Promise, and you can chain the `.then` calls together. The value returned in a `.then` handler (if any) becomes a new `Promise` object, and in this way, you can construct a chain of `.then` and `.catch` calls to manage a sequence of asynchronous operations. 

With the `Promise` object, a sequence of asynchronous operations is called a **Promise chain**, consisting of chained `.then` handlers, as we will see in the next section.

## Promises and error handling in Express router functions

It is important that all errors are correctly handled and reported to Express. With synchronous code, Express will correctly catch a thrown exception and send it to the error handler. Take the following example:

[PRE2]js\1

This is an example of the error indicator landing in an inconvenient place in the callback function. The exception is thrown in a completely different stack frame than the one invoked by Express. Even if we arranged to return a Promise, as is the case with an async function, Express doesn't handle the Promise. In this example, the error is lost; the caller would never receive a response and nobody would know why.

It is important to reliably catch any errors and respond to the caller with results or errors. To understand this better, let's rewrite the pyramid of doom example:

[PRE3]js\1

The goal here is to avoid blocking the event loop with a long operation. Deferring the processing of results or errors using callback functions is an excellent solution and is the founding idiom of Node.js. The implementation of callback functions led to this pyramid-shaped problem. Promises help flatten the code so that it is no longer in a pyramid shape. They also capture errors, ensuring delivery to a useful location. In both cases, errors and results are buried inside an anonymous function and are not delivered to the next line of code.

Generators and the iteration protocol are an intermediary architectural step that, when combined with Promises, lead to the async function. We won't use either of these in this book, but they are worth learning about.

For the documentation for the iteration protocol, refer to [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols).

For the documentation for the generator functions, refer to [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator). 

We've already used async functions and learned about how they let us write clean-looking asynchronous code. For example, the `db.query` example as an async function looks as follows:

[PRE4]js\1

Other than `try/catch`, this example is very clean compared to its earlier forms, both as a callback pyramid and as a Promise chain. All the boilerplate code is erased, and the intent of the programmer shines through clearly. Nothing is lost inside a callback function. Instead, everything lands on the next line of code where it is convenient.

The `await` keyword looks for a Promise. Therefore, `doSomething` and the other functions are expected to return a Promise, and `await` manages its resolution. Each of these functions could be an async function, and thereby automatically returns a Promise, or it could explicitly create a Promise to manage an asynchronous function call. A generator function is also involved, but we don't need to know how that works. We just need to know that `await` manages the asynchronous execution and the resolution of the Promise.

More importantly, each statement with an `await` keyword executes asynchronously. That's a side effect of `await`—managing asynchronous execution to ensure the asynchronous result or error is delivered correctly. However, Express cannot catch an asynchronous error and requires us to notify it of asynchronous results using `next()`.

The `try/catch` structure is needed for integration with Express. For the reasons just given, we must explicitly catch asynchronously delivered errors and notify Express with `next(err)`.

In this section, we discussed three methods for notifying Express about asynchronously delivered errors. The next thing to discuss is some architectural choices to structure the code.

# Architecting an Express application in the MVC paradigm

Express doesn't enforce an opinion on how you should structure the **Model,**** View, and Controller** (**MVC**) modules of your application, or whether you should follow any kind of MVC paradigm at all. The MVC pattern is widely used and involves three main architectural pieces. The **controller** accepts inputs or requests from the user, converting that into commands sent to the model. The **model** contains the data, logic, and rules by which the application operates. The **view** is used to present results to the user.

As we learned in the previous chapter, the blank application created by the Express generator provides two aspects of the MVC model:

*   The `views` directory contains template files, controlling the display portion, corresponding to the view.
*   The `routes` directory contains code implementing the URLs recognized by the application and coordinates the data manipulation required to generate the response to each URL. This corresponds to the controller.

Since the router functions also call the function to generate the result using a template, we cannot strictly say that the router functions are the controller and that the `views` templates are the view. However, it's close enough to the MVC model for it to be a useful analogy.

This leaves us with a question of where to put the model code. Since the same data manipulation can be used by multiple router functions, clearly the router functions should use a standalone module (or modules) containing the model code. This will also ensure a clean separation of concerns—for example, to ease the unit testing of each.

The approach we'll use is to create a `models` directory as a sibling of the `views` and `routes` directories. The `models` directory will hold modules to handle data storage and other code that we might call **business logic**. The API of the modules in the `models` directory will provide functions to create, read, update, or delete data items—a **C****reate,** **R****ead,** **Update, and D****elete**/**Destroy **(**CRUD**) model—and other functions necessary for the view code to do its thing.

The CRUD model includes the four basic operations of persistent data storage. The `Notes` application is structured as a CRUD application to demonstrate the implementation each of these operations.

We'll use functions named `create`, `read`, `update`, and `destroy` to implement each of the basic operations.

We're using the `destroy` verb, rather than `delete`, because `delete` is a reserved word in JavaScript.

With that architectural decision in mind, let's proceed with creating the `Notes` application.

# Creating the Notes application

Since we're starting a new application, we can use the Express generator to give us a starting point. It is not absolutely necessary to use this tool since we can definitely write the code ourselves. The advantage, however, is that it gives us a fully fleshed out starting point:

[PRE5]js\1

The supplied script uses `bin/www`, but shortly, we'll restructure the generated code to put everything into a single ES6 script named `app.mjs`. 

Then, install `cross-env`, as follows:

[PRE6]js\1

We'll finish this up later, but what we've done is restructured the code we were given. We can import the Express package, and then export the `router` object. Adding router functions is, of course, the done in the same way, whether it is a CommonJS or an ES6 module. We made the router callback an async function because it will be using async code.

We'll need to follow the same pattern for any other router modules we create.

Having converted this to an ES6 module, the next step is to merge code from `bin/www` and `app.js` into an ES6 module named `app.mjs`.

## Creating the Notes application wiring – app.mjs

Since the `express-generator` tool gives us a slightly messy application structure that does not use ES6 modules, let's reformulate the code it gave us appropriately. The first, `app.mjs`, contains the *wiring* of the application, meaning it configures the objects and functions from which the application is built while not containing any functions of its own. The other code, `appsupport.mjs`, contains the callback functions that appeared in the generated `app.js` and `bin/www` modules.

In `app.mjs`, start with this:

[PRE7]js\1

In the `dirname-fixed.mjs` example in [Chapter 3](516a5cd0-bdae-4e8c-bb0a-d508f85d483a.xhtml), *Exploring Node.js Modules*, we imported specific functions from the `path` and `url` core modules. We have used that code and then exported the value for `__dirname` as `approotdir`. Other parts of the `Notes` application simply need the pathname of the root directory of the application in order to calculate the required pathnames.

Return your attention to `app.mjs` and you'll see that the router modules are imported as `indexRouter` and `notesRouter`. For the moment, `notesRouter` is commented out, but we'll get to that in a later section.

Now, let's initialize the `express` application object:

[PRE8]js\1

This section of code wraps the Express application in an HTTP server and gets it listening to HTTP requests. The `server` object is also exported in case other code wants to access it.

Compare `app.mjs` with the generated `app.js` and `bin/www` code and you will see that we've covered everything in those two modules except for the inline functions. These inline functions could be written at the end of `app.mjs`, but we've elected instead to create a second module to hold them.

Create `appsupport.mjs` to hold the inline functions, starting with the following:

[PRE9]js\1

The preceding code handles errors from the HTTP server object. Some of these errors will simply cause the server to exit:

[PRE10]js\1

These were previously inline functions implementing error handling for the Express application.

The result of these changes is that `app.mjs` is now clean of distracting code, and it instead focuses on connecting together the different parts that make up the application. Since Express is not opinionated, it does not care that we restructured the code like this. We can structure the code in any way that makes sense to us and that correctly calls the Express API.

Since this application is about storing data, let's next talk about the data storage modules.

## Implementing the Notes data storage model

Remember that we decided earlier to put data model and data storage code into a directory named `models` to go along with the `views` and `routes` directories. Together, these three directories will separately store the three sides of the MVC paradigm.

The idea is to centralize the implementation details of storing data. The data storage modules will present an API for storing and manipulating application data, and over the course of this book, we'll make several implementations of this API. To switch between one storage engine to another, we will just require a configuration change. The rest of the application will use the same API methods, regardless of the storage engine being used.

To start, let's define a pair of classes to describe the data model. Create a file named `models/Notes.mjs` with the following code in it:

[PRE11]js\1

Creating a `Symbol` instance is done with `Symbol('symbol-name')`. The resulting `Symbol` instance is a unique identifier, and even if you call `Symbol('symbol-name')` again, the uniqueness is preserved. Each `Symbol` instance is unique from all other `Symbol` instances, even ones that are formed from the same string. In this example, the `b` and `b1` variables were both formed by calling `Symbol('b')`, but they are not equivalent.

Let's see how we can use a `Symbol` instance to attach fields to an object:

[PRE12]js\1

With the `Note` class defined, we can create a `Note` instance, and then dump it and see the resulting fields. The keys to these fields are indeed `Symbol` instances. These `Symbol` instances are hidden inside the module. The fields themselves are visible to code outside the module. As we can see here, an attempt to subvert the instance with `note[Symbol('key')] = 'new key'` does not overwrite the field but instead adds a second field. 

With our data types defined, let's start implementing the application, beginning with a simple in-memory datastore.

## Implementing an in-memory Notes datastore

Eventually, we will create a `Notes` data storage module that persists the notes to long-term storage. But to get us started, let's implement an in-memory datastore so that we can get on with implementing the application. Because we designed an abstract base class, we can easily create new implementations of that class for various storage services.

Create a file named `notes-memory.mjs` in the `models` directory with the following code:

[PRE13]js\1

This creates an instance of the class and exports it as `NotesStore`. This will work so long as we have a single `NotesStore` instance, but in [Chapter 7](ae8529e5-3a08-45cc-89e9-82895eb45641.xhtml), *Data Storage and Retrieval*, we will change this around to support dynamically selecting a `NotesStore` instance.

We're now ready to start implementing the web pages and associated code for the application, starting with the home page.

## The Notes home page

We're going to modify the starter application to support creating, editing, updating, viewing, and deleting notes. Let's start by changing the home page to show a list of notes, and have a top navigation bar linking to an ADD Note page so that we can always add a new note.

There's no change required in `app.mjs` because the home page is generated in routes controlled in this router module:

[PRE14]js\1

We showed the outline for this earlier, and having defined the `Notes` data storage model, we can fill in this function.

This uses the `AbstractNotesStore` API that we designed earlier. The `keylist` method returns a list of the key values for notes currently stored by the application. Then, it uses the `read` method to retrieve each note and pass that list to a template that renders the home page. This template will render a list of the notes.

What's the best way to retrieve all the notes? We could have written a simple `for` loop, as follows:

[PRE15]js\1

This is the file generated by `express-generator`, with the addition of a `header` partial for the page header. 

Remember that in the Fibonacci application, we used a *partial* to store the HTML snippet for the navigation. Partials are just that—HTML template snippets that can be reused in one or more templates. In this case, the `header` partial will appear on every page and serve as a common navigation bar across the application. Create `partials/header.hbs`, containing the following:

[PRE16]js\1

This simply steps through the array of note data and formats a simple listing. Each item links to the `/notes/view` URL with a `key` parameter. We have yet to write code to handle that URL, but will obviously display the note. Another thing to note is that no HTML for the list is generated if `notelist` is empty.

There is, of course, a whole lot more that could be put into this. For example, it's easy to add jQuery support to every page just by adding the appropriate `script` tags here.

We have now written enough to run the application, so let's view the home page:

[PRE17]js\1

We'll end up with this in `app.mjs`. We import both routers and then add them to the application configuration.

Create a file named `routes/notes.mjs` to hold `notesRouter`, starting with the following content:

[PRE18]js\1

This template supports both creating new notes and updating existing notes. We'll reuse this template to support both scenarios via the `docreate` flag.

Notice that the `note` and `notekey` objects passed to the template are empty in this case. The template detects this condition and ensures that the input areas are empty. Additionally, a flag, `docreate`, is passed in so that the form records whether it is being used to create or update a note. At this point, we're adding a new note, so no `note` objects exist. The template code is written defensively to not throw errors.

When creating HTML forms like this, you have to be careful with using whitespace in the elements holding the values. Consider a scenario where the `<textarea>` element was instead formatted like this:

[PRE19]js\1

Because this URL will also be used for both creating and updating notes, we check the `docreate` flag to call the appropriate model operation.

Both `notes.create` and `notes.update` are async functions, meaning we must use `await`. 

This is an HTTP `POST` handler. Because of the `bodyParser` middleware, the form data is added to the `req.body` object. The fields attached to `req.body` correspond directly to elements in the HTML form.

In this, and most of the other router functions, we use the `try/catch` construct that we discussed earlier to ensure errors are caught and forwarded correctly to Express. The difference between this and the preceding `/notes/add` router function is whether the router uses an async callback function. In this case, it is an async function, whereas for `/notes/add`, it is not async. Express knows how to handle errors in non-async callbacks, but it does not know how to handle errors in async callback functions.

Now, we can run the application again and use the Add a Note form:

![](img/c949b296-32e0-4690-be97-a94016e40b5e.png)

However, upon clicking on the Submit button, we get an error message. This is because there isn't anything (yet) to implement the `/notes/view` URL.

You can modify the URL in the `Location` box to revisit `http://localhost:3000`, and you'll see something similar to the following screenshot on the home page:

![](img/94936122-5cf1-4959-999d-0fc10d3766b3.png)

The note is actually there; we just need to implement `/notes/view`. Let's get on with that.

## Viewing notes – read

Now that we've looked at how to create notes, we need to move on to reading them. This means implementing controller logic and view templates for the `/notes/view` URL.

Add the following `router` function to `routes/notes.mjs`:

[PRE20]js\1

This is straightforward; we are taking data out of the `note` object and displaying it using HTML. At the bottom are two links—one to `/notes/destroy` to delete the note and the other to `/notes/edit` to edit it.

Neither of these corresponding codes exists at the moment, but that won't stop us from going ahead and executing the application:

![](img/1f551683-feb4-41c4-86a4-c5fcdabafde8.png)

As expected, with this code, the application correctly redirects to `/notes/view`, and we can see our handiwork. Also, as expected, clicking on either the Delete or Edit links will give us an error because the code hasn't yet been implemented.

We'll next create the code to handle the Edit link and later, one to handle the Delete link.

## Editing an existing note – update

Now that we've looked at the `create` and `read` operations, let's look at how to update or edit a note. 

Add the following router function to `routes/notes.mjs`:

[PRE21]js\1

Destroying a note is a significant step, if only because there's no trash can to retrieve it from if the user makes a mistake. Therefore, we need to ask the user whether they're sure that they want to delete the note. In this case, we retrieve the note and then render the following page, displaying a question to ensure they definitely want to delete the note.

Add a `notedestroy.hbs` template to the `views` directory:

[PRE22]js\1

This calls the `notes.destroy` function in the model. If it succeeds, the browser is redirected to the home page. If not, an error message is shown to the user. Rerunning the application, we can now view it in action:

![](img/bafe62b3-9c7a-4c38-a32a-e0ca175fad05.png)

Now that everything is working in the application, you can click on any button or link and keep all the notes you want.

We've implemented a bare-bones application for managing notes. Let's now see how to change the look, since in the next chapter, we'll implement a mobile-first UI.

# Theming your Express application

The Express team has done a decent job of making sure Express applications look okay out of the gate. Our `Notes` application won't win any design awards, but at least it isn't ugly. There's a lot of ways to improve it, now that the basic application is running. Let's take a quick look at theming an Express application. In Chapter 6, *Implementing the Mobile-First Paradigm*, we'll take a deeper dive into this, focusing on that all-important goal of addressing the mobile market.

If you're running the `Notes` application using the recommended method, `npm start`, a nice log of activity is being printed in your console window. One of these is the following:

[PRE23]js\1

This file was autogenerated for us by the Express generator at the outset and was dropped in the `public` directory. The `public` directory is managed by the Express static file server, using the following line in `app.mjs`:

[PRE24]js\1

Something that leaps out is that the application content has a lot of whitespace at the top and left-hand sides of the screen. The reason for this is that the `body` tags have the `padding: 50px` style. Changing it is a quick business.

Since there is no caching in the Express static file server, we can simply edit the CSS file and reload the page, and the CSS will be reloaded as well. 

Let's make a couple of tweaks:

[PRE25]js\1

The `server1` script runs on `PORT 3001`, while the `server2` script runs on `PORT 3002`. Isn't it nice to have all of this documented in one place?

Then, in one command window, run the following:

[PRE26]js\1

This gives us two instances of the `Notes` application. Use two browser windows to visit `http://localhost:3001` and `http://localhost:3002`. Enter a couple of notes, and you might see something like this:

![](img/2c6d2829-f1c9-4df4-9131-d8163de6210a.png)

After editing and adding some notes, your two browser windows could look as in the preceding screenshot. The two instances do not share the same data pool; each is instead running in its own process and memory space. You add a note to one and it does not show on the other screen.

Additionally, because the model code does not persist data anywhere, the notes are not saved. You might have written the greatest Node.js programming book of all time, but as soon as the application server restarts, it's gone.

Typically, you run multiple instances of an application to scale performance. That's the old *throw more servers at it* trick. For this to work, the data, of course, must be shared, and each instance must access the same data source. Typically, this involves a database, and when it comes to user identity information, it might even entail armed guards. 

All that means databases, more data models, unit testing, security implementation, a deployment strategy, and much more. Hold on—we'll get to all of that soon! 

# Summary

We've come a long way in this chapter.

We started by looking at the pyramid of doom and how Promise objects and async functions can help us tame asynchronous code. Because we're writing an Express application, we looked at how to use async functions in Express. We'll be using these techniques throughout this book.

We quickly moved on to writing the foundation of a real application with Express. At the moment, our application keeps its data in memory, but it has the basic functionality of what will become a note-taking application that supports real-time collaborative commenting on notes.

In the next chapter, we'll dip our toes into the water of responsive, mobile-friendly web design. Due to the growing popularity of mobile computing devices, it's become necessary to address mobile devices first before desktop computer users. In order to reach those millions of users a day, the `Notes` application users need a good user experience when using their smartphones.

In the following chapters, we'll keep growing the capabilities of the `Notes` application, starting with database storage models. But first, we have an important task in the next chapter—implementing a mobile-first UI using Bootstrap.