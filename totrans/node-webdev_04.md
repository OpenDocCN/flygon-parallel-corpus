Exploring Node.js Modules

Modules and packages are the building blocks for breaking down your application into smaller pieces. A module encapsulates some functionality, primarily JavaScript functions, while hiding implementation details and exposing an API for the module. Modules can be distributed by third parties and installed for use by our modules. An installed module is called a package. 

The npm package repository is a huge library of modules that's available for all Node.js developers to use. Within that library are hundreds of thousands of packages you can be used to accelerate the development of your application.

Since modules and packages are the building blocks of your application, understanding how they work is vital to your success with Node.js. By the end of this chapter, you will have a solid grounding in both CommonJS and ES6 modules, how to structure the modules in an application, how to manage dependencies on third-party packages, and how to publish your own packages.

In this chapter, we will cover the following topics:

*   Definitions of all types of Node.js modules and how to structure both simple and complex modules
*   Using CommonJS and ES2015/ES6 modules and when to use each
*   Understanding how Node.js finds modules and installed packages, so you can better structure your application
*   Using the npm package management system (and Yarn) to manage application dependencies, to publish packages, and to record administrative scripts for the project

So, let's get on with it.

# Defining a Node.js module

Modules are the basic building blocks for constructing Node.js applications. A Node.js module encapsulates functions, hiding details inside a well-protected container, and exposing an explicitly declared API.

When Node.js was created, the ES6 module system, of course, did not yet exist. Ryan Dahl, therefore, based on the Node.js module system on the CommonJS standard. The examples we've seen so far are modules written to that format. With ES2015/ES2016, a new module format was created for use with all JavaScript implementations. This new module format is used by both front-end engineers in their in-browser JavaScript code and by Node.js engineers, and for any other JavaScript implementation.

Because ES6 modules are now the standard module format, the Node.js **Technical Steering Committee** (**TSC**) committed to first-class support for ES6 modules alongside the CommonJS format. Starting with Node.js 14.x, the Node.js TSC delivered on that promise.

Every source file used in an application on the Node.js platform is a *module*. Over the next few sections, we'll examine the different types of modules, starting with the CommonJS module format. 

Throughout this book, we'll identify traditional Node.js modules as CommonJS modules, and the new module format as ES6 modules.

To start our exploration of Node.js modules, we must, of course, start at the beginning.

## Examining the traditional Node.js module format

We already saw CommonJS modules in action in the previous chapter. It's now time to see what they are and how they work. 

In the `ls.js` example in [Chapter 2](bd2253cb-6a41-4fc5-ae86-cc9632d44da4.xhtml), *Setting Up Node.js*, we wrote the following code to pull in the `fs` module, giving us access to its functions:

[PRE0]js\1

Whether you use `module.exports` or `exports` is up to you. However, do not ever do anything like the following:

[PRE1]js\1

Some modules do export a single function because that's how the module author envisioned delivering the desired functionality.

When we said `ls.js` does not export anything, we meant that `ls.js` did not assign anything to `module.exports`.

To give us a brief example, let's create a simple module, named `simple.js`:

[PRE2]js\1

The `exports` object in the module is the object that is returned by `require('./simple')`. Therefore, each call to `s.next` calls the `next` function in `simple.js`. Each returns (and increments) the value of the local variable, `count`. An attempt to access the private field, `count`, shows it's unavailable from outside the module.

This is how Node.js solves the global object problem of browser-based JavaScript. The variables that look like they are global variables are only global to the module containing the variable. These variables are not visible to any other code.

The Node.js package format is derived from the CommonJS module system ([http://commonjs.org](http://commonjs.org)). When developed, the CommonJS team aimed to fill a gap in the JavaScript ecosystem. At that time, there was no standard module system, making it trickier to package JavaScript applications. The `require` function, the `exports` object, and other aspects of Node.js modules come directly from the CommonJS `Modules/1.0` spec.

The `module` object is a global-to-the-module object injected by Node.js. It also injects two other variables: `__dirname` and `__filename`. These are useful for helping code in a module know where it is located in the filesystem. Primarily, this is used for loading other files using a path relative to the module's location. 

For example, one can store assets like CSS or image files in a directory relative to the module. An app framework can then make the files available via an HTTP server. In Express, we do so with this code snippet:

[PRE3]js\1

This lets us see the values we receive:

[PRE4]js\1

This is similar to `simple.js` but with a few additions to demonstrate further features. As before `count` is a private variable that isn't exported, and `next` is an exported function that increments `count`.

The `export` keyword declares what is being exported from an ES6 module. In this case, we have several exported functions and two exported variables. The `export` keyword can be put in front of any top-level declaration, such as variable, function, or class declarations:

[PRE5]js\1

The intent of both is essentially the same: to make a function or other object available to code outside the module. But instead of explicitly creating an object, `module.exports`, we're simply declaring what is to be exported. A statement such as `export function next()` is a named export, meaning the exported function (as here) or object has a name, and that code outside the module uses that name to access the object. As we see here, named exports can be functions or objects, and they may also be class definitions.

The *default export* from a module, defined with `export default`, can be done once per module. The default export is what code outside the module accesses when using the module object itself, rather than when using one of the exports from the module.

You can also declare something, such as the `squared` function, and then export it later.

Now let's see how to use the ES2015 module. Create a `simpledemo.mjs` file with the following:

[PRE6]js\1

In the past, the ES6 module format was hidden behind an option flag, `--experimental-module`, but as of Node.js 13.2 that flag is no longer required. Accessing the `default` export is accomplished by accessing the field named `default`. Accessing an exported value, such as the `meaning` field, is done without parentheses because it is a value and not a function.

Now to see a different way to import objects from a module, create another file, named `simpledemo2.mjs`, containing the following:

[PRE7]js\1

This is a reimplementation of the `ls.js` example in [Chapter 2](bd2253cb-6a41-4fc5-ae86-cc9632d44da4.xhtml), *Setting Up Node.js*. In both cases, we're using the `promises` submodule of the `fs` package. To do this with the `import` statement, we access the `promises` export from the `fs` module, and use the `as` clause to rename `fs.promises` to `fs`. This way we can use an async function rather than deal with callbacks.

Otherwise, we have an `async` function, `listFiles`, that performs filesystem operations to read filenames from a directory. Because `listFiles` is `async`, it returns a Promise, and we must catch any errors using a `.catch` clause.

Executing the script gives the following:

[PRE8]js\1

That innocent bit of code results in an error:

[PRE9]js\1

Since `__dirname` and `__filename` are not part of the JavaScript specification, they are not available within ES6 modules. Enter the `import.meta.url` object, from which we can compute `__dirname` and `__filename`. To see it in action, create a `dirname-fixed.mjs` file containing the following:

[PRE10]js\1

And we see the `file://` URL of the module, and the computed values for `__dirname` and `__filename` using the built-in core functions.

We've talked about both the CommonJS and ES6 module formats, and now it's time to talk about using them together in an application.

## Using CommonJS and ES6 modules together

Node.js supports two module formats for JavaScript code: the CommonJS format originally developed for Node.js, and the new ES6 module format. The two are conceptually similar, but there are many practical differences. Because of this, we will face situations of using both in the same application and will need to know how to proceed.

First is the question of file extensions and recognizing which module format to use. The ES6 module format is used in the following situations:

*   Files where the filename ends in `.mjs`.
*   If the `package.json` has a field named `type` with the value `module`, then filenames ending with `.js`.
*   If the `node` binary is executed with the `--input-type=module` flag, then any code passed through the `--eval` or `--print` argument, or piped in via STDIN (the standard input), is interpreted as ES6 module code.

That's fairly straight-forward. ES6 modules are in files named with the `.mjs` extension, unless you've declared in the `package.json` that the package defaults to ES6 modules, in which case files named with the `.js` extension are also interpreted as ES6 modules.

The CommonJS module format is used in the following situations:

*   Files where the file name ends in `.cjs`.
*   If the `package.json` does not contain a `type` field, or if it contains a `type` field with a value of `commonjs`, the filenames will end with `.js`.
*   If the `node` binary is executed with the `--input-type` flag or with the `--type-type=commonjs` flag, then any code passed through the `--eval` or `--print` argument, or piped in via STDIN (the standard input), is interpreted as CommonJS module code.

Again this is straight-forward, with Node.js defaulting to CommonJS modules for the `.js` files. If the package is explicitly declared to default to CommonJS modules, then Node.js will interpret the `.js` files as CommonJS.

The Node.js team strongly recommends that package authors include a `type` field in `package.json`, even if the type is `commonjs`.

Consider a `package.json` with this declaration:

[PRE11]js\1

This command will do the same, even without the `package.json` entry:

[PRE12]js\1

This is a CommonJS module that's using an ES6 module we created earlier. It simply calls a few of the functions, nothing exciting except that it is using an ES6 module when we said earlier `import` only works in ES6 modules. Let's see this module in action:

[PRE13]js\1

It's the same code but running in the global scope. In the global scope, we cannot use the `await` keyword, so we should expect that `simple2` will contain a pending Promise. Running the script gives us this failure:

[PRE14]js\1

Thus, everything within the module is contained within an anonymous private namespace context. This is how the global object problem is resolved: everything in a module that looks global is actually contained within a private context. This also explains how the injected variables are actually injected into the module. They are parameters to the function that creates the module.

The other advantage is code safety. Because the private code in a module is stashed in a private namespace, it is impossible for code outside the module to access the private code or data.

Let's take a look at a practical demonstration of the encapsulation. Create a file named `module1.js`, containing the following:

[PRE15]js\1

Using these two modules we can see how each module is its own protected bubble.

Then run it as follows:

[PRE16]js\1

That is, the JSON file is read synchronously, and the text is parsed as JSON. The resultant object is available as the object exported from the module. Create a file named `data.json`, containing the following:

[PRE17]js\1

It will execute as follows:

[PRE18]js\1

So far that is equivalent to the CommonJS version of this script, but using `import` rather than `require`.

[PRE19]js\1

There are two ways to use this module: 

*   In a CommonJS module, invoke `require('esm')`.
*   On the command line, use `--require esm`, as shown here.

In both cases, the effect is the same, to load the `esm` module. This module only needs to be loaded once, and we do not have to call any of its methods. Instead `esm` retrofits ES6 module support into the Node.js runtime, and is compatible with version 6.x and later.

So, we can use this module to retrofit ES6 module support; it does not retrofit other features such as `async` functions. Successfully executing the `ls.mjs` example requires support for both the `async` functions and arrow functions. Since Node.js 6.x does not support either, the `ls.mjs` example will load correctly, but will still fail because it uses other unsupported features.

[PRE20]js\1

This uses an extension-less module identifier to load a module we've already discussed, `simple.js`:

[PRE21]js\1

We get the error message making it clear that Node.js could not resolve the file name. Similarly, in an ES6 module, the file name given to the `import` statement must have the file extension.

Next, let's discuss another side effect of ES6 module identifiers being a URL.

### The ES6 import statement takes a URL

The module identifier in the ES6 `import` statement is a URL. There are several important considerations. 

Since Node.js only supports the `file://` URLs, we're not allowed to retrieve a module over from a web server. There are obvious security implications, and the corporate security team would rightfully get anxious if modules could be loaded from `http://` URLs.

Referencing a file with an absolute pathname must use the `file:///path/to/file.ext` syntax, as mentioned earlier. This is different from `require`, where we would use `/path/to/file.ext` instead.

Since `?` and `#` have special significance in a URL, they also have special significance to the `import` statement, as in the following example:

[PRE22]js\1

And the equivalent in an ES6 module would be as follows:

[PRE23]js\1

The `name` field gives the name of the package. If the `main` field is present, it names the JavaScript file to use instead of `index.js` to load when the package is loaded. The package manager applications like npm and Yarn support many more fields in `package.json`, which they use to manage dependencies and versions and everything else.

If there is no `package.json`, then Node.js will look for either `index.js` or `index.node`. In such a case, `require('some-library')` will load the file module in `/path/to/some-library/index.js`.

Installed packages are kept in a directory named `node_modules`. When JavaScript source code has `require('some-library')` or `import 'some-library'`, Node.js searches through one or more `node_modules` directories to find the named package.

Notice that the module identifier, in this case, is just the package name. This is different from the file and directory module identifiers we studied earlier since both those are pathnames. In this case, the module identifier is somewhat abstract, and that's because Node.js has an algorithm for finding packages within the nested structure of the `node_modules` directories.

To understand how that works, we need a deeper dive into the algorithm.

## Finding the installed package in the file system 

One key to why the Node.js package system is so flexible is the algorithm used to search for packages.

For a given `require`, `import()`, or `import` statement, Node.js searches upward in the file system from the directory containing the statement. It is looking for a directory named `node_modules` containing a module satisfying the module identifier.

For example, with a source file named `/home/david/projects/notes/foo.js` and a `require` or `import` statement requesting the module identifier `bar.js`, Node.js tries the following options:

![](img/b20040f4-8a85-4f12-b445-b49a673a904a.png)

As just said, the search starts at the same level of the file system as `foo.js`. Node.js will look either for a file module named `bar.js` or else a directory named `bar.js` containing a module as described earlier in *Using a* *Directory as a module*. Node.js will check for this package in the `node_modules` directory next to `foo.js` and in every directory above that file. It will not, however, descend into any directory such as `express` or `express/node_modules`. The traversal only moves upward in the file system, not downward.

While some of the third-party packages have a name ending in `.js`, the vast majority do not. Therefore, we will typically use `require('bar')`. Also typically the 3rd party installed packages are delivered as a directory containing a `package.json` file and some JavaScript files. Therefore, in the typical case, the package module identifier would be `bar`, and Node.js will find a directory named `bar` in one of the `node_modules` directories and access the package from that directory.

This act of searching upward in the file system means Node.js supports the nested installation of packages. A Node.js package that in turn depends on other modules that will have its own `node_modules` directory; that is, the `bar` package might depend on the `fred` package. The package manager application might install `fred` as `/home/david/projects/notes/node_modules/bar/node_modules/fred`:

![](img/0d84888b-cc4d-4f3c-881e-dd3dc6c71008.png)

In such a case, when a JavaScript file in the `bar` package uses `require('fred')` its search for modules starts in `/home/david/projects/notes/node_modules/bar/node_modules`, where it will find the `fred` package. But if the package manager detects that other packages used by `notes` also use the `fred` package, the package manager will install it as `/home/david/projects/notes/node_modules/fred`.

Because the search algorithm traverses the file system upwards, it will find `fred` in either location.

The last thing to note is that this nesting of `node_modules` directories can be arbitrarily deep. While the package manager applications try to install packages in a flat hierarchy, it may be necessary to nest them deeply.

One reason for doing so is to enable using two or more versions of the same package.

### Handling multiple versions of the same installed package

The Node.js package identifier resolution algorithm allows us to install two or more versions of the same package. Returning to the hypothetical *notes* project, notice that the `fred` package is installed not just for the `bar` package but also for the `express` package. 

Looking at the algorithm, we know that `require('fred')` in the `bar` package, and in the `express` package, will be satisfied by the corresponding `fred` package installed locally to each.

Normally, the package manager applications will detect the two instances of the `fred` package and install only one. But, suppose the `bar` package required the `fred` version 1.2, while the `express` package required the `fred` version 2.1.

In such a case, the package manager application will detect the incompatibility and install two versions of the `fred` package as so:

*   In `/home/david/projects/notes/node_modules/bar/node_modules`, it will install `fred` version 1.2.
*   In `/home/david/projects/notes/node_modules/express/node_modules`, it will install `fred` version 2.1.

When the `express` package executes `require('fred')` or `import 'fred'`, it will be satisfied by the package in `/home/david/projects/notes/node_modules/express/node_modules/fred`. Likewise, the `bar` package will be satisfied by the package in `/home/david/projects/notes/node_modules/bar/node_modules/fred`. In both cases, the `bar` and `express` packages have the correct version of the `fred` package available. Neither is aware there is another version of `fred` installed.

The `node_modules` directory is meant for packages required by an application. Node.js also supports installing packages in a global location so they can be used by multiple applications.

## Searching for globally installed packages

We've already seen that with npm we can perform a *global install* of a package. For example, command-line tools like `hexy` or `babel` are convenient if installed globally. In such a case the package is installed in another folder outside of the project directory. Node.js has two strategies for finding globally installed packages.

Similar to the `PATH` variable, the `NODE_PATH` environment variable can be used to list additional directories in which to search for packages. On Unix-like operating systems, `NODE_PATH` is a colon-separated list of directories, and on Windows it is semicolon-separated. In both cases, it is similar to how the `PATH` variable is interpreted, meaning that `NODE_PATH` has a list of directory names in which to find installed modules.

The `NODE_PATH` approach is not recommended, because of surprising behavior that can happen if people are unaware that this variable must be set. If a specific module located in a specific directory referenced in `NODE_PATH` is required for a proper function and the variable is not set, the application will likely fail. The best practice is for all dependencies to be explicitly declared, and with Node.js that means listing all dependencies in the `package.json` file so that `npm` or `yarn` can manage the dependencies.

This variable was implemented before the module resolution algorithm just described was finalized. Because of that algorithm, `NODE_PATH` is largely unnecessary. 

There are three additional locations that can hold modules:

*   `$HOME/.node_modules`
*   `$HOME/.node_libraries`
*   `$PREFIX/lib/node`

In this case, `$HOME` is what you expect (the user's home directory), and `$PREFIX` is the directory where Node.js is installed.

Some recommend against using global packages. The rationale is the desire for repeatability and deployability. If you've tested an app and all its code is conveniently located within a directory tree, you can copy that tree for deployment to other machines. But, what if the app depended on some other file that was magically installed elsewhere on the system? Will you remember to deploy such files? The application author might write documentation saying to *install this* then *install that* and *install something-else* before running *npm install*, but will the users of the application correctly follow all those steps? 

The best installation instructions is to simply run *npm install* or *yarn install*. For that to work, all dependencies must be listed in `package.json`.

Before moving forward, let's review the different kinds of module identifiers.

## Reviewing module identifiers and pathnames

That was a lot of details spread out over several sections. It's useful, therefore, to quickly review how the module identifiers are interpreted when using the `require`, `import()`, or `import` statements:

*   **Relative module identifiers**: These begin with `./` or `../`, and absolute identifiers begin with `/`. The module name is identical to POSIX filesystem semantics. The resultant pathname is interpreted relative to the location of the file being executed. That is, a module identifier beginning with `./` is looked for in the current directory, whereas one starting with `../` is looked for in the parent directory.
*   **Absolute module identifiers**: These begin with `/` (or `file://` for ES6 modules) and are, of course, looked for in the root of the filesystem. This is not a recommended practice.
*   **Top-level module identifiers**: These do not begin with those strings and are just the module name. These must be stored in a `node_modules` directory, and the Node.js runtime has a nicely flexible algorithm for locating the correct `node_modules` directory.
*   **Core modules**: These are the same as the *top-level module identifiers*, in that there is no prefix, but the core modules are prebaked into the Node.js binary.

In all cases, except for the core modules, the module identifier resolves to a file that contains the actual module, and which is loaded by Node.js. Therefore, what Node.js does is to compute the mapping between the module identifier and the actual file name to load.

Using a package manager application is not required. The Node.js module resolution algorithm does not depend on a package manager, like npm or Yarn, to set up the `node_modules` directories. There is nothing magical about those directories, and it is possible to use other means to construct a `node_modules` directory containing installed packages. But the simplest mechanism is to use a package manager application.

Some packages offer what we might call a sub-package included with the main package, let's see how to use them.

## Using deep import module specifiers

In addition to a simple module identifier like `require('bar')`, Node.js lets us directly access modules contained within a package. A different module specifier is used that starts with the module name, adding what's called a *deep import* path. For a concrete example, let's look at the `mime` module ([https://www.npmjs.com/package/mime](https://www.npmjs.com/package/mime)), which handles mapping a file name to its corresponding MIME type.

In the normal case, you use `require('mime')` to use the package. However, the authors of this package developed a lite version of this package that leaves out a lot of vendor-specific MIME types. For that version, you use `require('mime/lite')` instead. And of course, in an ES6 module, you use `import 'mime'` and `import 'mime/lite'`, as appropriate.

The specifier `mime/lite` is an example of a deep import module specifier.

With such a module identifier, Node.js first locates the `node_modules` directory containing the main package. In this case, that is the `mime` package. By default, the deep import module is simply a path-name relative to the package directory, for example, `/path/to/node_modules/mime/lite`. Going by the rules we've already examined, it will be satisfied by a file named `lite.js` or a by a directory named `lite` containing a file named `index.js` or `index.mjs`.

But it is possible to override the default behavior and have the deep import specifier refer to a different file within the module.

### Overriding a deep import module identifier

The deep import module identifier used by code using the package does not have to be the pathname used within the package source. We can put declarations in `package.json` describing the actual pathname for each deep import identifier. For example, a package with interior modules named `./src/cjs-module.js` and `./src/es6-module.mjs` can be remapped with this declaration in `package.json`:

[PRE24]js\1

This says the `cookie-parser` module depends on version 0.1.3 of `cookie`, while Express depends on version 0.1.5.

Now that we can recognize what a module is and how they're found in the file system, let's discuss when we can use each of the methods to load modules.

## Loading modules using require, import, and import()

Obviously `require` is used in CommonJS modules, and `import` is used in ES6 modules, but there are some details to go over. We've already discussed the format and filename differences between CommonJS and ES6 modules, so let's focus here on loading the modules.

The `require` function is only available in CommonJS modules, and it is used for loading a CommonJS module. The module is loaded synchronously, meaning that when the `require` function returns, the module is completely loaded.

By default, a CommonJS module cannot load an ES6 module. But as we saw with the `simple-dynamic-import.js` example, a CommonJS module can load an ES6 module using `import()`. Since the `import()` function is an asynchronous operation, it returns a Promise, and we, therefore, cannot use the resulting module as a top-level object. But we can use it inside a function:

[PRE25]js\1

It's the same as the `simple-dynamic-import.js` example, but we are explicitly handling the Promise returned by `import()` rather than using an async function. While we could assign `simple2` to a global variable, other code using that variable would have to accommodate the possibility the assignment hasn't yet been made.

The module object provided by `import()` contains the fields and functions exported with the `export` statements in the ES6 module. As we see here, the default export has the `default` name.

In other words, using an ES6 module in a CommonJS module is possible, so long as we accommodate waiting for the module to finish loading before using it.

The `import` statement is used to load ES6 modules, and it only works inside an ES6 module. The module specifier you hand to the `import` statement is interpreted as a URL.

An ES6 module can have multiple named exports. In the `simple2.mjs` we used earlier, these are the functions `next`, `squared`, and `hello`, and the values `meaning` and `nocount`. ES6 modules can have a single default export, as we saw in `simple2.mjs`.

With `simpledemo2.mjs`, we saw that we can import only the required things from the module:

[PRE26]js\1

In this case, we can invoke the function as `simple()`. We can also use what's called a namespace import; that is similar to how we import CommonJS modules:

[PRE27]js\1

This is similar to the *default export* method shown for ES6 modules, and we can think of the `module.exports` object inside the CommonJS module as the default export. Indeed, the `import` can be rewritten as follows:

[PRE28]js\1

A basic `package.json` file is as follows:

[PRE29]js\1

The help text will be shown on your screen.

Help information is also available on the npm website at: [https://docs.npmjs.com/cli-documentation/](https://docs.npmjs.com/cli-documentation/).

Before we can look for and install Node.js packages, we must have a project directory initialized.

## Initializing a Node.js package or project with npm init

The npm tool makes it easy to initialize a Node.js project directory. Such a directory contains at the minimum a `package.json` file and one or more Node.js JavaScript files. 

All Node.js project directories are therefore modules, going by the definition we learned earlier. However, in many cases, a Node.js project is not meant to export any functionality but instead is an application. Such a project will likely require other Node.js packages, and those packages will be declared in the `package.json` file so that they're easy to install using npm. The other common use case of a Node.js project is a package of functionality meant to be used by other Node.js packages or applications. These also consist of a `package.json` file plus one or more Node.js JavaScript files, but in this case, they're Node.js modules that export functions and can be loaded using `require`, `import()`, or `import`.

What this means is the key to initializing a Node.js project directory is creating the `package.json` file.

While the `package.json` file can be created by hand – it's just a JSON file after all - the npm tool provides a convenient method:

[PRE30]js\1

But what if you don't know the module name? How do you discover the interesting modules? The website [http://npmjs.com](http://npmjs.com) publishes a searchable index of the modules in the registry. The npm package also has a command-line search function to consult the same index:

![](img/de2ec86a-0e7d-4a98-ad55-6ee68f3e0d15.png)

Of course, upon finding a module, it's installed as follows:

[PRE31]js\1

The `npm view` command shows us information from `package.json` file for a given package, and with the `--json` flag we're shown the raw JSON.

The `name` tag is of course the package name, and it is used in URLs and command names, so choose one that's safe for both. If you desire to publish a package in the public `npm` repository, it's helpful to check whether a particular name is already being used by searching on [https://npmjs.com](https://npmjs.com) or by using the `npm search` command.

The `description` tag is a short description that's meant as a brief/terse description of the package. 

It is the name and description tags that are shown in npm search results.

The `keywords` tag is where we list attributes of the package. The npm website contains pages listing all packages using a particular keyword. These keyword indexes are useful when searching for a package since it lists the related packages in one place, and therefore when publishing a package it's useful to land on the correct keyword pages.

Another source is the contents of the `README.md` file. This file should be added to the package to provide basic package documentation. This file is shown on the package page on `npmjs.com`, and therefore it is important for this file to convince potential users of your package to actually use it. As the file name implies, this is a Markdown file.

Once you have found a package to use, you must install it in order to use the package.

## Installing an npm package

The `npm install` command makes it easy to install packages upon finding one of your dreams, as follows:

[PRE32]js\1

The `version` field obviously declares the current package version. The `dist-tags` field lists symbolic tags that the package maintainer can use to aid their users in selecting the correct version. This field is maintained by the `npm dist-tag` command.

The `npm install` command supports these variants:

[PRE33]js\1

*   **GitHub shortcut**: For GitHub repositories, you can list just the repository specifier, such as `expressjs/express`. A tag or a commit can be referenced using `expressjs/express#tag-name`.
*   **GitLab, BitBucket, and GitHub URL shortcuts**: In addition to the GitHub shortcut, npm supports a special URL format for specific Git services with URLs like `github:user/repo`, `bitbucket:user/repo`, and `gitlab:user/repo`.
*   **Local filesystem**: You can install from a local directory using a URL with the: `file:../../path/to/dir`.

Sometimes we need to install a package for use by several projects, without requiring that each project installs the package.

## Global package installs

In some instances, you want to install a module globally, so that it can be used from any directory. For example, the Grunt or Babel build tools are widely useful, and conceivably you will find it useful if these tools are installed globally. Simply add the `-g` option:

[PRE34]js\1

This variant, of course, runs `npm install` with elevated permissions.

The npm website offers a guideline with more information at [https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally).

If a local package install lands in `node_modules`, where does a global package install land? On a Unix-like system, it lands in `PREFIX/lib/node_modules`, and on Windows, it lands in `PREFIX/node_modules`. In this case, `PREFIX` means the directory where Node.js is installed. You can inspect the location of the directory as follows:

[PRE35]js\1

With the `--save` flag, npm will add a `dependencies` tag to `package.json`:

[PRE36]js\1

This installs the "production" version, which means to install only the modules listed in `dependencies` and none of the `devDependencies` modules. For example, if we use a build tool like Babel in development, the tool should not be installed in production.

While we can manually maintain dependencies in `package.json`, npm can handle this for us.

### Automatically updating package.json dependencies

With npm@5 (also known as npm version 5), one change was that it's no longer required to add `--save` to the `npm install` command. Instead, `npm` by default acts as if you ran the command with `--save`, and will automatically add the dependency to `package.json`. This is meant to simplify using `npm`, and it is arguably more convenient that `npm` now does this. At the same time, it can be very surprising and inconvenient for `npm` to go ahead and modify `package.json` for you. The behavior can be disabled by using the `--no-save` flag, or it can be permanently disabled using the following:

[PRE37]js\1

This freezes your dependency on the specific version number. You're free, then, to take your time updating your code to work against later releases of the module. Once your code is updated, or the upstream project is updated, change the dependency appropriately.

When listing dependencies in `package.json`, it's tempting to be lazy, but that leads to trouble.

## Explicitly specifying package dependency version numbers

As we've said several times in this chapter, explicitly declaring your dependencies is A Good Thing. We've already touched on this, but it's worth reiterating and to see how npm makes this easy to accomplish.

The first step is ensuring that your application code is checked into a source code repository. You probably already know this, and even have the best of intentions to ensure that everything is checked in. With Node.js, each module should have its own repository rather than putting every single last piece of code in one repository.

Each module can then progress on its own timeline. A breakage in one module is easy to back out by changing the version dependency in `package.json`.

The next step is to explicitly declare all dependencies of every module. The goal is simplifying and automating the process of setting up every module. Ideally, on the Node.js platform, the module setup is as simple as running `npm install`.

Any additional required steps can be forgotten or executed incorrectly. An automated setup process eliminates several kinds of potential mistakes.

With the `dependencies` and `devDependencies` sections of `package.json`, we can explicitly declare not only the dependencies but the precise version numbers.

The lazy way of declaring dependencies is putting `*` in the version field. That uses the latest version in the npm repository. This will seem to work, until that one day the maintainers of that package introduce a bug. You'll type `npm update`, and all of a sudden your code doesn't work. You'll head over to the GitHub site for the package, look in the issue queue, and possibly see that others have already reported the problem you're seeing. Some of them will say that they've pinned on the previous release until this bug is fixed. What that means is their `package.json` file does not depend on `*` for the latest version, but on a specific version number before the bug was created.

Don't do the lazy thing, do the smart thing.

The other aspect of explicitly declaring dependencies is to not implicitly depend on global packages. Earlier, we said that some people in the Node.js community caution against installing modules in the global directories. This might seem like an easy shortcut to sharing code between applications. Just install it globally, and you don't have to install the code in each application.

But, doesn't that make deployment harder? Will the new team member be instructed on all the special files to install here and there to make the application run? Will you remember to install that global module on all destination machines?

For Node.js, that means listing all the module dependencies in `package.json`, and then the installation instructions are simply `npm install`, followed perhaps by editing a configuration file.

While most packages in the npm repository are libraries with an API, some are tools we can run from the command line.

## Packages that install commands

Some packages install command-line programs. A side effect of installing such packages is a new command that you can type at the shell prompt or use in shell scripts. An example is the `hexy` program that we briefly used in [Chapter 2](bd2253cb-6a41-4fc5-ae86-cc9632d44da4.xhtml), *Setting Up Node.js*. Another example is the widely used Grunt or Babel build tools.

The recommendation to explicitly declare all dependencies in `package.json` applies to command-line tools as well as any other package. Therefore these packages will typically be installed locally. This requires special care in setting up the `PATH` environment variable correctly. As you should already be aware, the `PATH` variable is used on both Unix-like systems and Windows to list the directories in which the command-line shell searches for commands.

The command can be installed to one of two places:

*   **Global install**: It is installed either to a directory, such as `/usr/local`, or to the `bin` directory where Node.js was installed. The `npm bin -g` command tells you the absolute pathname for this directory. In this case, it's unlikely you'll have to modify the PATH environment variable.
*   **Local install**: Installs to `node_modules/.bin` in the package where the module is being installed, the `npm bin` command tells you the absolute pathname for the directory. Because the directory is inconveniently located to run commands, a change to the PATH variable is useful.

To run the command, simply type the command name at a shell prompt. This works correctly if the directory where the command is installed happens to be in the PATH variable. Let's look at how to configure the PATH variable to handle locally installed commands.

### Configuring the PATH variable to handle locally installed commands

Assume we have installed the `hexy` command like so:

[PRE38]js\1

But this breaks because the command is not in a directory listed in the `PATH`. The workaround is to use the full pathname or relative pathname:

[PRE39]js\1

The next step is adding the command to your login scripts so the variable is always set. On `bash`, add the corresponding line to `~/.bashrc`, and on `csh` add it to `~/.cshrc`.

Once this is accomplished the command-line tool executes correctly.

### Configuring the PATH variable on Windows

On Windows, this task is handled through a system-wide settings panel:

![](img/4e178c1e-2d36-4402-8e8e-713142886014.png)

This pane of the System Properties panel is found by searching for `PATH` in the Windows Settings screen. Click on the Environment Variables button, then select the Path variable, and finally click on the Edit button. On the screen here, click the New button to add an entry to this variable, and enter `.\node_modules\.bin` as shown. You'll have to restart any open command shell windows. Once you do, the effect will be as shown previously.

As easy as it is to modify the PATH variable, we don't want to do this in all circumstances.

### Avoiding modifications to the PATH variable

What if you don't want to add these variables to your `PATH` at all times? The `npm-path` module may be of interest. This is a small program that computes the correct `PATH` variable for your shell and operating system. See the package at [https://www.npmjs.com/package/npm-path](https://www.npmjs.com/package/npm-path).

Another option is to use the `npx` command to execute such commands. This tool is automatically installed alongside the `npm` command. This command either executes commands from a locally installed package or it silently installs commands in a global cache:

[PRE40]js\1

The report shows the current npm packages, the currently installed version, as well as the current version in the `npm` repository. Updating outdated packages is very simple:

[PRE41]js\1

What's important here is that we can add any script we like, and the `scripts` entry records the command to run:

[PRE42]js\1

With this combination, if the test author types `npm publish`, the `prepublish` script will cause the `test` script to run, which in turn uses `mocha` to run the test suite.

It is a well-known best practice to automate all administrative tasks, if only so that you never forget how to run those tasks. Creating the `scripts` entries for every such task not only prevents you from forgetting how to do things, but it also documents the administrative tasks for the benefit of others.

Next, let's talk about how to ensure the Node.js platform on which a package is executed supports the required features.

## Declaring Node.js version compatibility

It's important that your Node.js software runs on the correct version of Node.js. The primary reason being that the Node.js platform features required by your package are available every time your package is run. Therefore, the package author must know which Node.js releases are compatible with the package, and then describe in `package.json` that compatibility.

This dependency is declared in `package.json` using the `engines` tag:

```js\1

The version string is similar to what we can use in `dependencies` and `devDependencies`. In this case, we've defined that the package is compatible with Node.js 8.x, 9.x, and 10.x. 

Now that we know how to construct a package, let's talk about publishing packages.

## Publishing an npm package

All those packages in the npm repository came from people like you with an idea of a better way of doing something. It is very easy to get started with publishing packages.

Online docs about publishing packages can be found at [https://docs.npmjs.com/getting-started/publishing-npm-packages](https://docs.npmjs.com/getting-started/publishing-npm-packages).

Also consider this: [https://xkcd.com/927/](https://xkcd.com/927/).

You first use the `npm adduser` command to register yourself with the npm repository. You can also sign up with the website. Next, you log in using the `npm login` command.

Finally, while sitting in the package root directory, use the `npm publish` command. Then, stand back so that you don't get stampeded by the crush of thronging fans, or, maybe not. There are several zillion packages in the repository, with hundreds of packages added every day. To get yours to stand out, you will require some marketing skill, which is another topic beyond the scope of this book.

It is suggested that your first package be a scoped package, for example, `@my-user-name/my-great-package`. 

We've learned a lot in this section about using npm to manage and publish packages. But npm is not the only game in town for managing Node.js packages.

# The Yarn package management system

As powerful as npm is, it is not the only package management system for Node.js. Because the Node.js core team does not dictate a package management system, the Node.js community is free to roll up their sleeves and develop any system they feel best. That the vast majority of us use npm is a testament to its value and usefulness. But, there is a significant competitor.

Yarn (see [https://yarnpkg.com/en/](https://yarnpkg.com/en/)) is a collaboration between engineers at Facebook, Google, and several other companies. They proclaim that Yarn is ultrafast, ultra-secure (by using checksums of everything), and ultrareliable (by using a `yarn-lock.json` file to record precise dependencies).

Instead of running their own package repository, Yarn runs on top of the npm package repository at `npmjs.com`. This means that the Node.js community is not forked by Yarn, but enhanced by having an improved package management tool.

The npm team responded to Yarn in npm@5 (also known as npm version 5) by improving performance and by introducing a `package-lock.json` file to improve reliability. The npm team has implemented additional improvements in npm@6. 

Yarn has become very popular and is widely recommended over npm. They perform extremely similar functions, and the performance is not that different from npm@5\. The command-line options are worded differently. Everything we've discussed for npm is also supported by Yarn, albeit with slightly different command syntax. An important benefit Yarn brings to the Node.js community is that the competition between Yarn and npm seems to be breeding faster advances in Node.js package management overall.

To get you started, these are the most important commands:

*   `yarn add`: Adds a package to use in your current package
*   `yarn init`: Initializes the development of a package
*   `yarn install`: Installs all the dependencies defined in a `package.json` file
*   `yarn publish`: Publishes a package to a package manager
*   `yarn remove`: Removes an unused package from your current package

Running `yarn` by itself does the `yarn install` behavior. There are several other commands in Yarn, and `yarn help` will list them all.

# Summary

You learned a lot in this chapter about modules and packages for Node.js. Specifically, we covered implementing modules and packages for Node.js, the different module structures we can use, the difference between CommonJS and ES6 modules, managing installed modules and packages, how Node.js locates modules, the different types of modules and packages, how and why to declare dependencies on specific package versions, how to find third-party packages, and we gained a good grounding in using npm or Yarn to manage the packages we use and to publish our own packages.

Now that you've learned about modules and packages, we're ready to use them to build applications, which we'll look at in the next chapter.