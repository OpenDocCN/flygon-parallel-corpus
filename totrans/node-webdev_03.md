Setting Up Node.js

Before getting started with using Node.js, you must set up your development environment. While it's very easy to set up, there are a number of considerations to think about, including whether to install Node.js using the package management system, satisfying the requirements for installing native code Node.js packages, and deciding what the best editor is to use with Node.js. In the following chapters, we'll use this environment for development and non-production deployment.

In this chapter, we will cover the following topics:

*   How to install Node.js from source and prepackaged binaries on Linux, macOS, or Windows
*   How to install **node package manager** (**npm**) and some other popular tools 
*   The Node.js module system
*   Node.js and JavaScript language improvements from the ECMAScript committee

# System requirements

Node.js runs on POSIX-like OSes, various UNIX derivatives (Solaris, for example), and UNIX-workalike OSes (such as Linux, macOS, and so on), as well as on Microsoft Windows. It can run on machines both large and small, including tiny ARM devices, such as Raspberry Pi—a microscale embeddable computer for DIY software/hardware projects.

Node.js is now available via package management systems, limiting the need to compile and install from the source.

Because many Node.js packages are written in C or C++, you must have a C compiler (such as GCC), Python 2.7 (or later), and the `node-gyp` package. Since Python 2 will be end-of-lifed by the end of 2019, the Node.js community is rewriting its tools for Python 3 compatibility. If you plan on using encryption in your networking code, you will also need the OpenSSL cryptographic library. Modern UNIX derivatives almost certainly come with this and Node.js's configure script—used when installing from the source—will detect their presence. If you need to install it, Python is available at [http://python.org](http://python.org) and OpenSSL is available at [http://openssl.org](http://openssl.org).

Now that we have covered the requirements for running Node.js, let's learn how to install it.

# Installing Node.js using package managers

The preferred method for installing Node.js is to use the versions available in package managers, such as `apt-get`, or MacPorts. Package managers make your life easier by helping to maintain the current version of the software on your computer, ensuring to update dependent packages as necessary, all by typing a simple command, such as `apt-get update`. Let's go over installation from a package management system first.

For the official instructions on installing from package managers, go to [https://nodejs.org/en/download/package-manager/.](https://nodejs.org/en/download/package-manager/)

## Installing Node.js on macOS with MacPorts

The MacPorts project ([http://www.macports.org/](http://www.macports.org/)) has been packaging a long list of open-source software packages for macOS for years and they have packaged Node.js. The commands it manages are, by default, installed on `/opt/local/bin`. After you have installed MacPorts using the installer on their website, installing Node.js is very simple, making the Node.js binaries available in the directory where MacPorts installs commands:

[PRE0]js\1

Then, install like this:

[PRE1]js\1

This proves Node.js has been installed and the installed version matched what you asked for.

Of course, macOS is only one of many operating systems we might use.

## Installing Node.js on Linux, *BSD, or Windows from package management systems

Node.js is now available through most package management systems. Instructions on the Node.js website currently list packaged versions of Node.js for a long list of Linux, as well as FreeBSD, OpenBSD, NetBSD, macOS, and even Windows. Visit [https://nodejs.org/en/download/package-manager/](https://nodejs.org/en/download/package-manager/) for more information.

For example, on Debian and other Debian-based Linux distributions (such as Ubuntu), use the following commands:

[PRE2]js\1

The commands will be installed in `/usr/bin` and we can test whether the version downloaded is what we asked for.

Windows is starting to become a place where Unix/Linux geeks can work, thanks to a new tool called the **Windows subsystem for Linux** (**WSL**).

### Installing Node.js in WSL

**WSL** lets you install Ubuntu, openSUSE, or SUSE Linux Enterprise on Windows. All three are available via the store built into Windows 10\. You may need to update your Windows device for the installation to work. For the best experience, install WSL2, which is a major overhaul of WSL, offering an improved integration between Windows and Linux.

Once installed, the Linux-specific instructions will install Node.js in the Linux subsystem.

To install WSL, see [https://msdn.microsoft.com/en-us/commandline/wsl/install-win10](https://msdn.microsoft.com/en-us/commandline/wsl/install-win10).

To learn about and install WSL2, see [https://docs.microsoft.com/en-us/windows/wsl/wsl2-index](https://docs.microsoft.com/en-us/windows/wsl/wsl2-index).

The process may require elevated privileges on Windows.

### Opening an administrator-privileged PowerShell on Windows

Some of the commands that you'll run while installing tools on Windows are to be executed in a PowerShell window with elevated privileges. We are mentioning this because during the process of enabling WSL, a command will need to be run in a PowerShell window.

The process is simple:

1.  In the Start menu, enter `PowerShell` in the application's search box. The resulting menu will list PowerShell.
2.  Right-click the PowerShell entry.
3.  The context menu that comes up will have an entry called Run as Administrator. Click on that.

The resulting command window will have administrator privileges and the title bar will say Administrator: Windows PowerShell.

In some cases, you will be unable to use Node.js from package management systems.

## Installing the Node.js distribution from nodejs.org

The [https://nodejs.org/en/](https://nodejs.org/en/) website offers built-in binaries for Windows, macOS, Linux, and Solaris. We can simply go to the website, click on the Install button, and run the installer. For systems with package managers, such as the ones we've just discussed, it's better to use the package management system. That's because you'll find it easier to stay up to date with the latest version. However, that doesn't serve all people because of the following reasons:

*   Some will prefer to install a binary rather than deal with the package manager.
*   Their chosen system doesn't have a package management system.
*   The Node.js implementation in their package management system is out of date.

Simply go to the Node.js website and you'll see something as in the following screenshot. The page does its best to determine your OS and supply the appropriate download. If you need something different, click on the DOWNLOADS link in the header for all possible downloads:

![](img/63b156b2-8046-4789-a277-04a59cc77f3f.png)

For macOS, the installer is a `PKG` file that gives the typical installation process. For Windows, the installer simply takes you through the typical install wizard process.

Once you are finished with the installer, you have command-line tools, such as `node` and `npm`, which you can run Node.js programs with. On Windows, you're supplied with a version of the Windows command shell preconfigured to work nicely with Node.js.

As you have just learned, most of us will be perfectly satisfied with installing prebuilt packages. However, there are times when we must install Node.js from a source.

# Installing from the source on POSIX-like systems

Installing the prepackaged Node.js distributions is the preferred installation method. However, installing Node.js from a source is desirable in a few situations:

*   It can let you optimize the compiler settings as desired.
*   It can let you cross-compile, say, for an embedded ARM system.
*   You might need to keep multiple Node.js builds for testing.
*   You might be working on Node.js itself.

Now that you have a high-level view, let's get our hands dirty by mucking around in some build scripts. The general process follows the usual `configure`, `make`, and `make install` routine that you may have already performed with other open source software packages. If not, don't worry, we'll guide you through the process.

The official installation instructions are in `README.md`, contained in the source distribution at [https://github.com/nodejs/node/blob/master/README.md](https://github.com/nodejs/node/blob/master/README.md).

## Installing prerequisites

There are three prerequisites: a C compiler, Python, and the OpenSSL libraries. The Node.js compilation process checks for their presence and will fail if the C compiler or Python is not present. These sorts of commands will check for their presence:

[PRE3]js\1

This installs the Xcode command-line tools:

![](img/d8c5d5a8-8f7e-40e0-8f9d-3e8e892f2204.png)

For additional information, visit [http://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/](http://osxdaily.com/2014/02/12/install-command-line-tools-mac-os-x/).

Now that we have the required tools installed, we can proceed with compiling the Node.js source.

## Installing from the source for all POSIX-like systems

Compiling Node.js from the source follows this familiar process:

1.  Download the source from [http://nodejs.org/download.](http://nodejs.org/download)
2.  Configure the source for building using `./configure`.
3.  Run `make`, then `make install`.

The source bundle can be downloaded through your browser or as follows, substituting your preferred version:

[PRE4]js\1

To cause the installation to land in your `home` directory, run it this way:

[PRE5]js\1

A simpler way to install multiple Node.js versions is by using the `nvm` script, which will be described later.

If you want to install Node.js in a system-wide directory, simply leave off the `--prefix` option and it will default to installing in `/usr/local`.

After a moment, it'll stop and will likely have successfully configured the source tree for installation in your chosen directory. If this doesn't succeed, the error messages that are printed will describe what needs to be fixed. Once the configure script is satisfied, you can move on to the next step.

With the configure script satisfied, you compile the software:

[PRE6]js\1

Once installed, you should make sure that you add the installation directory to your `PATH` variable, as follows:

[PRE7]js\1

When the build is installed, it creates a directory structure, as follows:

[PRE8]js\1

It starts to get a little tedious maintaining this after a while. For each release, you have to set up Node.js, npm, and any third-party modules you desire in your Node.js installation. Also, the command shown to change `PATH` is not quite optimal. Inventive programmers have created several version managers to simplify managing multiple Node.js/npm releases and provide commands to change `PATH` the smart way:

*   Node version manager: [https://github.com/tj/n](https://github.com/tj/n)
*   Node version manager: [https://github.com/creationix/nvm](https://github.com/creationix/nvm)

Both maintain multiple, simultaneous versions of Node.js and let you easily switch between versions. Installation instructions are available on their respective websites.

For example, with `nvm`, you can run commands such as these:

[PRE9]js\1

This is done in a temporary directory, so you can delete it afterward. If your system does not have the tools installed to compile native code modules, you'll see error messages. Otherwise, you'll see a `node-gyp` execution in the output, followed by many lines of text obviously related to compiling C/C++ files.

The `node-gyp` tool has prerequisites similar to those for compiling Node.js from the source—namely, a C/C++ compiler, a Python environment, and other build tools, such as Git. For Unix, macOS, and Linux systems, those are easy to come by. For Windows, you should install the following:

*   Visual Studio build tools: [https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017](https://www.visualstudio.com/downloads/#build-tools-for-visual-studio-2017)
*   Git for Windows: [http://git-scm.com/download/win](http://git-scm.com/download/win)
*   Python for Windows: [https://www.python.org/](https://www.python.org/)

Normally, you don't need to worry about installing `node-gyp`. That's because it is installed behind the scenes as part of npm. That's done so that npm can automatically build native code modules.

Its GitHub repository contains documentation; go to [https://github.com/nodejs/node-gyp](https://github.com/nodejs/node-gyp).

Reading the `node-gyp` documentation in its repository will give you a clearer understanding of the compilation prerequisites discussed previously and of developing native code modules.

This is an example of a non-explicit dependency. It is best to explicitly declare all the things that a software package depends on. In Node.js, dependencies are declared in `package.json` so that the package manager (`npm` or `yarn`) can download and set up everything. But these compiler tools are set up by the OS package management system, which is outside the control of `npm` or `yarn`. Therefore, we cannot explicitly declare those dependencies.

We've just learned that Node.js supports modules written not just in JavaScript, but also in other programming languages. We've also learned how to support the installation of such modules. Next, we will learn about Node.js version numbers.

# Choosing Node.js versions to use and the version policy

We just threw around so many different Node.js version numbers in the previous section that you may have become confused about which version to use. This book is targeted at Node.js version 14.x and it's expected that everything we'll cover is compatible with Node.js 10.x and any subsequent release.

Starting with Node.js 4.x, the Node.js team has followed a dual-track approach. The even-numbered releases (4.x, 6.x, 8.x, and so on) are what they're calling **long term support** (**LTS**), while the odd-numbered releases (5.x, 7.x, 9.x, and so on) are where current new feature development occurs. While the development branch is kept stable, the LTS releases are positioned as being for production use and will receive updates for several years.

At the time of writing, Node.js 12.x is the current LTS release; Node.js 14.x has been released and will eventually become the LTS release.

A major impact of each new Node.js release, beyond the usual performance improvements and bug fixes, is the bringing in of the latest V8 JavaScript engine release. In turn, this means bringing in more of the ES2015/2016/2017 features as the V8 team implements them. In Node.js 8.x, the `async/await` functions arrived and in Node.js 10.x, support for the standard ES6 module format has arrived. In Node.js 14.x that module format will be completely supported.

A practical consideration is whether a new Node.js release will break your code. New language features are always being added as V8 catches up with ECMAScript and the Node.js team sometimes makes groundbreaking changes to the Node.js API. If you've tested on one Node.js version, will it work on an earlier version? Will a Node.js change break some assumptions we made?

What npm does is ensure that our packages execute on the correct Node.js version. This means that we can specify the compatible Node.js versions for a package in the `package.json` file (which we'll explore in [Chapter 3](516a5cd0-bdae-4e8c-bb0a-d508f85d483a.xhtml), *Exploring Node.js Modules)*.

We can add an entry to `package.json` as follows:

[PRE10]js\1

That was a lot of output but don't study it too closely. The key takeaway is that `node --help` provides a lot of useful information.

Note that there are options for both Node.js and V8 (not shown in the previous command line). Remember that Node.js is built on top of V8; it has its own universe of options that largely focus on details of bytecode compilation or garbage collection and heap algorithms. Enter `node --v8-options` to see the full list of these options.

On the command line, you can specify options, a single script file, and a list of arguments to that script. We'll discuss script arguments further in the following section, *Running a simple script with Node.js*.

Running Node.js with no arguments drops you in an interactive JavaScript shell:

[PRE11]js\1

Next, run it by typing the following command:

[PRE12]js\1

The `man` command, of course, lets you read manual pages and section `3` covers the C library.

Inside the function body, we read the directory and print its contents. Using `require('fs').promises` gives us a version of the `fs` module (filesystem functions) that returns Promises; it, therefore, works well in an async function. Likewise, the ES2015 `for..of` loop construct lets us loop over entries in an array in a way that works well in `async` functions.

By default, the `fs` module functions use the callback paradigm originally created for Node.js. As a result, most Node.js modules use the callback paradigm. Within `async` functions, it is more convenient if functions return Promises instead so that the `await` keyword can be used. The `util` module provides a function, `util.promisify`, which generates a wrapper function for old-style callback-oriented functions so it instead returns a Promise.

This script is hardcoded to list files in the current directory. The real `ls` command takes a directory name, so let's modify the script a little.

Command-line arguments land in a global array named `process.argv`. Therefore, we can modify `ls.js`, copying it as `ls2.js` (as follows) to see how this array works:

[PRE13]js\1

We simply checked whether a command-line argument was present, `if (process.argv[2])`. If it was, we override the value of the `dir` variable, `dir = process.argv[2]`, and we then use that as the `readdir` argument:

[PRE14]js\1

You can use this anywhere; for example, the function can be assigned to a variable or it can be passed as a callback to another function. When used with the `async` keyword, the body of the arrow function has all of the `async` function's behavior.

For the purpose of these examples, an async arrow function can be wrapped for immediate execution:

[PRE15]js\1

Whether this or the previous style is preferable is perhaps a matter of taste. However, you will find both styles in use and it is necessary to understand how both work.

When invoking an async function at the top level of a script, it is necessary to capture any errors and report them. Failure to catch and report errors can lead to mysterious problems that are hard to pin down. For the original version of this example, the errors were explicitly caught with a `try/catch` block. In this version, we catch errors using a `.catch` block.

Before we had async functions, we had the Promise object and before that, we had the callback paradigm. All three paradigms are still used in Node.js, meaning you'll need to understand each.

## Converting to async functions and the Promise paradigm

In the previous section, we discussed `util.promisify` and its ability to convert a callback-oriented function into one that returns a Promise. The latter plays well with async functions and therefore, it is preferable for functions to return a Promise.

To be more precise, `util.promisify` is to be given a function that uses the error-first-callback paradigm. The last argument of such functions is a callback function, whose first argument is interpreted as an error indicator, hence the phrase error-first-callback. What `util.promisify` returns is another function that returns a Promise. 

The Promise serves the same purpose as error-first-callback. If an error is indicated, the Promise resolves to the rejected status, while if success is indicated, the Promise resolves to a success status. As we see in these examples, the Promise is handled very nicely within an `async` function.

The Node.js ecosystem has a large body of functions that use error-first-callback. The community has began a conversion process where functions will return a Promise and possibly also take an error-first-callback for API compatibility.

One of the new features in Node.js 10 is an example of such a conversion. Within the `fs` module is a submodule, named `fs.promises`, with the same API but producing Promise objects. We wrote the previous examples using that API.

Another choice is a third-party module, `fs-extra`. This module has an extended API beyond the standard `fs` module. On one hand, its functions return a Promise if no callback function is provided or else invokes the callback. In addition, it includes several useful functions.

In the rest of this book, we will often use `fs-extra` because of those additional functions. For documentation on the module, go to [https://www.npmjs.com/package/fs-extra](https://www.npmjs.com/package/fs-extra).

The `util` module has another function, `util.callbackify`, which does as the name implies—it converts a function that returns a Promise into one that uses a callback function.

Now that we've seen how to run a simple script, let's look at a simple HTTP server.

## Launching a server with Node.js

Many scripts that you'll run are server processes; we'll be running lots of these scripts later on. Since we're still trying to verify the installation and get you familiar with using Node.js, we want to run a simple HTTP server. Let's borrow the simple server script on the Node.js home page ([http://nodejs.org](http://nodejs.org)).

Create a file named `app.js`, containing the following:

[PRE16]js\1

This is the simplest of web servers you can build with Node.js. If you're interested in how it works, flip forward to [Chapter 4](a883aeee-aa28-44c6-a02e-8238829cea90.xhtml), *HTTP Servers and Clients*, [Chapter 5](582d3898-0135-430c-8b6e-8326f287e18b.xhtml), *Your First Express Application*, and [Chapter 6](db8b0ab8-181f-4d8d-9088-a9962ec461b8.xhtml), *Implementing the Mobile-First Paradigm*. But for now, just type `http://127.0.0.1:8124` in your browser to see the Hello, World! message:

![](img/fec4c888-fe02-4660-b3a3-ed7810a88ef1.png)

A question to ponder is why this script didn't exit when `ls.js` did. In both cases, execution of the script reaches the end of the file; the Node.js process does not exit in `app.js`, while it does in `ls.js`.

The reason for this is the presence of active event listeners. Node.js always starts up an event loop and in `app.js`, the `listen` function creates an event, `listener`, that implements the HTTP protocol. This `listener` event keeps `app.js` running until you do something, such as press *Ctrl* + *C* in the terminal window. In `ls.js`, there is nothing there to create a long-running `listener` event, so when `ls.js` reaches the end of its script, the `node` process will exit.

To carry out more complex tasks with Node.js, we must use third-party modules. The npm repository is the place to go.

## Using npm, the Node.js package manager

Node.js, being a JavaScript interpreter with a few interesting asynchronous I/O libraries, is by itself a pretty basic system. One of the things that makes Node.js interesting is the rapidly growing ecosystem of third-party modules for Node.js.

At the center of that ecosystem is the npm module repository. While Node.js modules can be downloaded as source and assembled manually for use with Node.js programs, that's tedious to do and it's difficult to implement a repeatable build process. npm gives us a simpler method; npm is the de facto standard package manager for Node.js and it greatly simplifies downloading and using these modules. We will talk about npm at length in the next chapter.

The sharp-eyed among you will have noticed that npm is already installed via all the installation methods discussed previously. In the past, npm was installed separately, but today it is bundled with Node.js.

Now that we have `npm` installed, let's take it for a quick spin. The **hexy** program is a utility used for printing hex dumps of files. That's a very 1970s thing to do, but it is still extremely useful. It serves our purpose right now as it gives us something to quickly install and try out:

[PRE17]js\1

Once it is installed, you'll be able to run the newly–installed program this way:

[PRE18]js\1

Under the covers, `npx` uses `npm` to download the package to a cache directory, unless the package is already installed in the current project directory. Because the package is then in a cache directory, it is only downloaded once.

There are a number of interesting options to this tool; to learn more, go to [https://www.npmjs.com/package/npx](https://www.npmjs.com/package/npx).

We have learned a lot in this section about the command-line tools delivered with Node.js, as well as ran a simple script and HTTP server. Next, we will learn how advances in the JavaScript language affect the Node.js platform.

# Advancing Node.js with ECMAScript 2015, 2016, 2017, and beyond 

In 2015, the ECMAScript committee released a long-awaited major update of the JavaScript language. The update brought in many new features to JavaScript, such as Promises, arrow functions, and class objects. The language update sets the stage for improvement since it should dramatically improve our ability to write clean, understandable JavaScript code.

The browser makers are adding those much-needed features, meaning the V8 engine is adding those features as well. These features are making their way to Node.js, starting with version 4.x.

To learn about the current status of ES2015/2016/2017/and so on in Node.js, visit [https://nodejs.org/en/docs/es6/](https://nodejs.org/en/docs/es6/).

By default, only the ES2015, 2016, and 2017 features that V8 considers stable are enabled by Node.js. Further features can be enabled with command-line options. The almost-complete features are enabled with the `--es_staging` option. The website documentation gives more information.

The Node green website ([http://node.green/](http://node.green/)) has a table that lists the status of a long list of features in Node.js versions.

The ES2019 language spec is published at [https://www.ecma-international.org/publications/standards/Ecma-262.htm](https://www.ecma-international.org/publications/standards/Ecma-262.htm).

The TC-39 committee does its work on GitHub at [https://github.com/tc39](https://github.com/tc39).

The ES2015 (and later) features make a big improvement to the JavaScript language. One feature, the `Promise` class, should mean a fundamental rethinking of common idioms in Node.js programming. In ES2017, a pair of new keywords, `async` and `await`, simplifies writing asynchronous code in Node.js, which should encourage the Node.js community to further rethink the common idioms of the platform.

There's a long list of new JavaScript features but let's quickly go over the two of them that we'll use extensively.

The first is a lighter-weight function syntax called the arrow function:

[PRE19]js\1

You don't need to understand the code; it's just an outline of what happens in practice as we use callbacks. Depending on how many steps are required for a specific task, a code pyramid can get quite deep. Promises will let us unravel the code pyramid and improve reliability because error handling is more straightforward and easily captures all errors.

A `Promise` class is created as follows:

[PRE20]js\1

This works because the `Promise` class supports chaining if a `then` function returns a `Promise` object.

The `async/await` feature implements the promise of the `Promise` class to simplify asynchronous coding. This feature becomes active within an `async` function:

[PRE21]js\1

To see how much of an improvement the `async` function paradigm gives us, let's recode the earlier example as follows:

[PRE22]js\1

This demonstrates having an object with three fields but only extracting two of the fields.

To continue our exploration of advances in JavaScript, let's take a look at Babel.

## Using Babel to use experimental JavaScript features

The Babel transpiler is the leading tool for using cutting-edge JavaScript features or experimenting with new JavaScript features. Since you've probably never seen the word **transpiler**, it means to rewrite source code from one language to another. It is like a **compiler** in that Babel converts computer source code into another form, but instead of directly executable code, Babel produces JavaScript. That is, it converts JavaScript code into JavaScript code, which may not seem useful until you realize that Babel's output can target older JavaScript releases.

Put more simply, Babel can be configured to rewrite code with ES2015, ES2016, ES2017 (and so on) features into code conforming to the ES5 version of JavaScript. Since ES5 JavaScript is compatible with practically every web browser on older computers, a developer can write their frontend code in modern JavaScript then convert it to execute on older browsers using Babel.

To learn more about Babel, go to [https:// babeljs.io](https://%20babeljs.io).

The Node Green website makes it clear that Node.js supports pretty much all of the ES2015, 2016, and 2017 features. Therefore, as a practical matter, we no longer need to use Babel for Node.js projects. You may possibly be required to support an older Node.js release and you can use Babel to do so.

For web browsers, there is a much longer time lag between a set of ECMAScript features and when we can reliably use those features in browser-side code. It's not that the web browser makers are slow in adopting new features as the Google, Mozilla, and Microsoft teams are proactive about adopting the latest features. Apple's Safari team seems slow to adopt new features, unfortunately. What's slower, however, is the penetration of new browsers into the fleet of computers in the field. 

Therefore, modern JavaScript programmers need to familiarize themselves with Babel.

We're not ready to show example code for these features yet, but we can go ahead and document the setting up of the Babel tool. For further information on setup documentation, visit [http://babeljs.io/docs/setup/](http://babeljs.io/docs/setup/) and click on the CLI button.

To get a brief introduction to Babel, we'll use it to transpile the scripts we saw earlier to run on Node.js 6.x. In those scripts, we used async functions, a feature that is not supported on Node.js 6.x. 

In the directory containing `ls.js` and `ls2.js`, type these commands:

[PRE23]js\1

We have the same example we looked at earlier, but with a couple of changes. The `fs_readdir` function creates a Promise object then calls `fs.readdir`, making sure to either `reject` or `resolve` the Promise based on the result we get. This is more or less what the `util.promisify` function does.

Because `fs_readdir` returns a Promise, the `await` keyword can do the right thing and wait for the request to either succeed or fail. This code should run as is on Node.js releases, which support `async` functions. But what we're interested in—and the reason why we added the `fs_readdir` function—is how it works on older Node.js releases.

The pattern used in `fs_readdir` is what is required to use a callback-oriented function in an `async` function context.

Next, create a file named `.babelrc`, containing the following:

[PRE24]js\1

To transpile your code, run the following command:

[PRE25]js\1

This code isn't meant to be easy to read for humans. Instead, it means that you edit the original source file and then convert it for your target JavaScript engine. The main thing to notice is that the transpiled code uses a Generator function (the notation `function*` indicates a generator function) in place of the `async` function and the `yield` keyword in place of the `await` keyword. What a generator function is—and precisely what the `yield` keyword does—is not important; the only thing to note is that `yield` is roughly equivalent to `await` and that the `_asyncToGenerator` function implements functionality similar to async functions. Otherwise, the transpiled code is fairly clean and looks rather similar to the original code.

The transpiled script is run as follows:

```js\1

In other words, it runs the same as the `async` version but on an older Node.js release. Using a similar process, you can transpile code written with modern ES2015 (and so on) constructions so it can run in an older web browser.

In this section, we learned about advances in the JavaScript language, especially async functions, and then learned how to use Babel to use those features on older Node.js releases or in older web browsers.

# Summary

You learned a lot in this chapter about installing Node.js using its command-line tools and running a Node.js server. We also breezed past a lot of details that will be covered later in this book, so be patient.

Specifically, we covered downloading and compiling the Node.js source code, installing Node.js—either for development use in your home directory or for deployment in system directories—and installing npm, the de facto standard package manager used with Node.js. We also saw how to run Node.js scripts or Node.js servers. We then took a look at the new features in ES2015, 2016, and 2017\. Finally, we looked at how to use Babel to implement those features in your code.

Now that we've seen how to set up a development environment, we're ready to start working on implementing applications with Node.js. The first step is to learn the basic building blocks of Node.js applications and modules, meaning taking a more careful look at Node.js modules, how they are used, and how to use npm to manage application dependencies. We will cover all of that in the next chapter.