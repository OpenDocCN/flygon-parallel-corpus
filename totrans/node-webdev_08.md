Implementing the Mobile-First Paradigm

Now that our first Express application is usable, we should act on the mantra of this age of software development: mobile-first. Mobile devices, whether they be smartphones, tablet computers, automobile dashboards, refrigerator doors, or bathroom mirrors, are taking over the world. 

The primary considerations in designing for mobiles are the small screen sizes, the touch-oriented interaction, the fact that there's no mouse, and the somewhat different **User Interface** (**UI**) expectations. In 1997-8, when streaming video was first developed, video producers had to learn how to design video experiences for a viewport the size of a fig newton (an American snack food). Today, application designers have to contend with an application window the size of a playing card.

With the *Notes* application, our UI needs are modest, and the lack of a mouse doesn't make any difference to us. 

In this chapter, we won't do much Node.js development. Instead, we'll do the following:

*   Modify the Notes application templates for better mobile presentation.
*   Edit Bootstrap SASS files to customize application theming.
*   Install a third-party Bootstrap theme.
*   Learn about Bootstrap 4.5, a popular framework for responsive UI design.

As of the time of writing, Bootstrap v5 has just entered the alpha phase. That makes it premature to adopt at this time, but we may wish to do so in the future. Going by the migration guide, much of Bootstrap will stay the same, or very similar, in version 5\. However, the biggest change in version 5 is the dropping of the requirement for jQuery. Because we use jQuery fairly heavily in [Chapter 9](3d687da9-7857-4c79-915b-b5b79873748c.xhtml), *Dynamic Client/Server Interaction with Socket.IO*, this is a significant consideration.

By completing the tasks in the preceding list, we'll dip our toes in the water of what it means to be a full-stack web engineer. The goal of this chapter is to gain an introduction to an important part of application development, namely the UI, and one of the leading toolkits for web UI development.

Rather than just do mobile-first development because it's the popular thing, let's first try to understand the problem being solved.

# Understanding the problem – the Notes app isn't mobile-friendly

Let's start by quantifying the problem. We need to explore how well (or not) the application behaves on a mobile device. This is simple to do:

1.  Start the *Notes* application. Determine the IP address of the host system.
2.  Using your mobile device, connect to the service using the IP address, and browse around the *Notes* application, putting it through its paces and noting any difficulties.

Another way to approach this is to use your desktop browser, resizing it to be very narrow. The Chrome DevTools also includes a mobile device emulator. Either way, you can mimic the small screen size of a smartphone on your desktop.

To see a real UI problem on a mobile screen, edit `views/noteedit.hbs` and make this change:

[PRE0]js\1

The first segment of the stylesheet configures the page layout for all devices. Next, for any browser viewport at least `600px` wide, it reconfigures the page to display on the larger screen. Then, for any browser viewport at least `960px` wide, it is reconfigured again. The stylesheet has a final media query to cover print devices.

These widths are what's called a **breakpoint**. Those threshold viewport widths are the points where the design changes itself around. You can see breakpoints in action by going to any responsive website, then resizing the browser window. Watch how the design jumps at certain sizes. Those are the breakpoints chosen by the author of that website.

There's a wide range of differing opinions about the best strategy to choose your breakpoints. Do you target specific devices or do you target general characteristics? The Twenty Twelve theme did fairly well on mobile devices using only two viewport-size media queries. The CSS-Tricks blog has posted an extensive list of specific media queries for every known device, which is available at [https://css-tricks.com/snippets/css/media-queries-for-standard-devices/](https://css-tricks.com/snippets/css/media-queries-for-standard-devices/).

We should at least target these devices:

*   **Small**: This includes iPhone 5 SE.
*   **Medium**: This can refer to tablet computers or larger smartphones.
*   **Large**: This includes larger tablet computers or smaller desktop computers.
*   **Extra-large**: This refers to larger desktop computers and other large screens.
*   **Landscape/portrait**: You may want to create a distinction between landscape mode and portrait mode. Switching between the two of course changes viewport width, possibly pushing it past a breakpoint. However, your application may need to behave differently in the two modes.

That's enough theory of responsive web design to get us started. In our *Notes* application, we'll work on using touch-friendly UI components and using Bootstrap to scale the user experience based on screen size. Let's get started.

# Using Twitter Bootstrap on the Notes application

Bootstrap is a mobile-first framework consisting of HTML5, CSS3, and JavaScript code providing a comprehensive set of world-class, responsive web design components. It was developed by engineers at Twitter and then released to the world in August 2011.

The framework includes code to retrofit modern features onto older browsers, a responsive 12-column grid system, and a long list of components (some using JavaScript) for building web applications and websites. It's meant to provide a strong foundation on which to build your application.

Refer to [http://getbootstrap.com](http://getbootstrap.com) for more details about Bootstrap.

With this introduction to Bootstrap, let's proceed to set it up.

## Setting up Bootstrap

The first step is to duplicate the code you created in the previous chapter. If, for example, you created a directory named `chap05/notes`, then create one named `chap06/notes` from the content of `chap05/notes`.

Now, we need to go about adding Bootstrap's code in the *Notes* application. The Bootstrap website suggests loading the required CSS and JavaScript files out of the Bootstrap (and jQuery) public CDN. While that's easy to do, we won't do this for two reasons:

*   It violates the principle of keeping all dependencies local to the application and not relying on global dependencies.
*   It makes our application dependent on whether the CDN is functioning.
*   It prevents us from generating a custom theme.

Instead, we'll install a local copy of Bootstrap. There are several ways to install Bootstrap locally. For example, the Bootstrap website offers a downloadable TAR/GZIP archive (tarball). The better approach is an automated dependency management tool, and fortunately, the npm repository has all the packages we need. 

The most straightforward choice is to use the Bootstrap ([https://www.npmjs.com/package/bootstrap](https://www.npmjs.com/package/bootstrap)), Popper.js ([https://www.npmjs.com/package/popper.js](https://www.npmjs.com/package/popper.js)), and jQuery ([https://www.npmjs.com/package/jquery](https://www.npmjs.com/package/jquery)) packages in the npm repository. These packages provide no Node.js modules and instead are frontend code distributed through npm. Many frontend libraries are distributed through the npm repository.

We install the packages using the following command:

[PRE1]js\1

Within each of these directories are the CSS and JavaScript files that are meant to be used in the browser. More importantly, these files are located in a given directory whose pathname is known—specifically, the directories we just inspected.

Let's see how to configure our Notes app to use those three packages on the browser side, as well as set up Bootstrap support in the page layout templates.

## Adding Bootstrap to the Notes application

In this section, we'll first load Bootstrap CSS and JavaScript in the page layout templates, and then we'll ensure that the Bootstrap, jQuery, and Popper packages are available to be used. We have made sure those libraries are installed in `node_modules`, so we need to make sure Notes knows to serve the files as static assets to web browsers.

On the Bootstrap website, they give a recommended HTML structure for pages. We'll be interpolating from their recommendation to instead use the local copies of Bootstrap, jQuery, and Popper that we just installed.

Refer to the *Getting Started* page at [https://getbootstrap.com/docs/4.5/getting-started/introduction/](https://getbootstrap.com/docs/4.5/getting-started/introduction/).

What we'll do is modify `views/layout.hbs` to match the template recommended by Bootstrap, by making the changes shown in bold text:

[PRE2]js\1

We're again using the `express.static` middleware to serve asset files to browsers visiting the *Notes* application. Each of these pathnames is where npm installed the Bootstrap, jQuery, and Popper libraries.

There is a special consideration for the Popper.js library. In the `popper.js/dist` directory, the team distributes a library in the ES6 module syntax. At this time, we cannot trust all browsers to support ES6 modules. In `popper.js/dist/umd` is a version of the Popper.js library that works in all browsers. We have therefore set the directory appropriately.

Within the `public` directory, we have a little house-keeping to do. When `express-generator` set up the initial project, it generated `public/images`, `public/javascripts`, and `public/stylesheets` directories. Hence the URLs for each start with `/images`, `/javascripts`, and `/stylesheets`. It's cleaner to give such files a URL starting with the `/assets` directory. To implement that change, start by moving the files around as follows:

[PRE3]js\1

The onscreen differences are minor, but this is the necessary proof that the CSS and JavaScript files for Bootstrap are being loaded. We have accomplished the first major goal—using a modern, mobile-friendly framework to implement a mobile-first design.

Before going on to modify the look of the application, let's talk about other available frameworks.

## Alternative layout frameworks

Bootstrap isn't the only JavaScript/CSS framework providing a responsive layout and useful components. Of course, all the other frameworks have their own claims to fame. As always, it is up to each project team to choose the technologies they use, and of course, the marketplace is always changing as new libraries become available. We're using Bootstrap in this project because of its popularity. These other frameworks are worthy of a look:

*   Pure.css ( [https://purecss.io/](https://purecss.io/)): A responsive CSS framework with an emphasis on a small code footprint.
*   Picnic CSS ([https://picnicss.com/](https://picnicss.com/)): A responsive CSS framework emphasizing small size and beauty.
*   Bulma ([https://bulma.io/](https://bulma.io/)): A responsive CSS framework that's self-billed as very easy to use.
*   Shoelace ([https://shoelace.style/](https://shoelace.style/)): A CSS framework emphasizing using future CSS, meaning it uses CSS constructs at the bleeding edge of CSS standardization. Since most browsers don't support those features, cssnext ([http://cssnext.io/](http://cssnext.io/)) is used to retrofit that support. Shoelace uses a grid layout system based on Bootstrap's grid.
*   PaperCSS ([https://www.getpapercss.com/](https://www.getpapercss.com/)): An informal CSS framework that looks like it was hand-drawn.
*   Foundation ([https://foundation.zurb.com/](https://foundation.zurb.com/)): Self-described as the most advanced responsive frontend framework in the world.
*   Base ([http://getbase.org/](http://getbase.org/)): A lightweight modern CSS framework.

HTML5 Boilerplate ([https://html5boilerplate.com/](https://html5boilerplate.com/)) is an extremely useful basis from which to code the HTML and other assets. It contains the current best practices for the HTML code in web pages, as well as tools to normalize CSS support and configuration files for several web servers.

Browser technologies are also improving rapidly, with layout techniques being one area. The Flexbox and CSS Grid layout systems are a significant advance in making HTML content layout much easier than older techniques.

# Flexbox and CSS Grids

Two new technologies impacting web application development are these new CSS layout methodologies. The CSS3 committee has been working on several fronts, including page layout. 

In the distant past, we used nested HTML tables for page layout. That is a bad memory that we don't have to revisit. More recently, we've been using a box model using `<div>` elements, and even at times using absolute or relative placement techniques. All these techniques have been suboptimal in several ways, some more than others.

One popular layout technique is to divide the horizontal space into columns and assign a certain number of columns to each thing on the page. With some frameworks, we can even have nested `<div>` elements, each with their own set of columns. Bootstrap 3, and other modern frameworks, used that layout technique. 

The two new CSS layout methodologies, Flexbox ([https://en.wikipedia.org/wiki/CSS_flex-box_layout](https://en.wikipedia.org/wiki/CSS_flex-box_layout)) and CSS Grids ([https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)), are a significant improvement over all previous methodologies. We are mentioning these technologies because they're both worthy of attention. 

With Bootstrap 4, the Bootstrap team chose to go with Flexbox. Therefore, under the hood are Flexbox CSS constructs. 

Having set up Bootstrap, and having learned some background to responsive web design, let's dive right in and start implementing responsive design in *Notes*.

# Mobile-first design for the Notes application

When we added CSS and JavaScript for Bootstrap et al., that was only the start. To implement a responsive mobile-friendly design, we need to modify every template to use Bootstrap components. Bootstrap's features, in version 4.x, are grouped into four areas:

*   **Layout**: Declarations to control the layout of HTML elements, supporting different layouts based on device size
*   **Content**: For regularizing the look of HTML elements, typography, images, tables, and more
*   **Components**: A comprehensive set of UI elements including navigation bars, buttons, menus, popups, forms, carousels, and more to make it easy to implement applications
*   **Utilities**: Additional tools to aid in tweaking the presentation and layout of HTML elements

The Bootstrap documentation is full of what we might call *recipes*, to implement the structure of HTML elements for certain Bootstrap components or effects. A key to the implementation is that Bootstrap effects are triggered by adding the correct HTML class declaration to each HTML component.

Let's start with page layout using Bootstrap.

## Laying the Bootstrap grid foundation

Bootstrap uses a 12-column grid system to control layout, giving applications a responsive mobile-first foundation on which to build. When correctly set up, a layout using Bootstrap components can automatically rearrange components for different sized screens between extra small up to large desktop computers. The method relies on `<div>` elements with classes to describe the role each `<div>` plays in the layout.

The basic layout pattern in Bootstrap is as follows:

[PRE4]js\1

This declares three different layouts, one for extra-small devices, another for medium devices, and the last for large devices. 

The grid system can do a lot more. For details, see the documentation at [https://getbootstrap.com/docs/4.5/layout/overview/](https://getbootstrap.com/docs/4.5/layout/overview/).

This introduction gives us enough knowledge to start modifying the *Notes* application. Our next task is to better understand the structure of the application pages.

## Responsive page structure for the Notes application

We could go through a whole user experience analysis of *Notes*, or get designers involved, and get the perfect page design for each screen of the *Notes* application. But the current *Notes* application design is the result of a developer coding up page designs that are functional and not ugly. Let's start by discussing the logic behind the structure of the page designs we have. Consider the following structure:

[PRE5]js\1

You can then inspect the downloaded package and see that `./node_modules/feather-icons/dist/feather.js` contains browser-side code, making it easy to use the icons.

We make that directory available by mounting it in `app.mjs`, just as we did for the Bootstrap and jQuery libraries. Add this code to `app.mjs`:

[PRE6]js\1

This loads the browser-side library and then invokes that library to cause the icons to be used. 

To use one of the icons, use a `data-feather` attribute specifying one of the icon names, like so:

[PRE7]js\1

Adding `class="page-header"` informs Bootstrap that this is, well, the page header. Within that, we have the `<h1>` header as before, providing the page title, and then a responsive Bootstrap `navbar`.

By default, the `navbar` is expanded—meaning the components inside the `navbar` are visible—because of the `navbar-expand-md` class. This `navbar` uses a `navbar-toggler` button that governs the responsiveness of the `navbar`. By default, this button is hidden and the body of the `navbar` is visible. If the screen is small enough, the `navbar-toggler` is switched so it's visible and the body of the `navbar` becomes invisible, and when clicking on the now-visible `navbar-toggler`, a menu drops down containing the body of the `navbar`:

![](img/9e463059-e746-40ad-8de7-86722783d8d1.png)

We chose the Feather Icons' *home* icon because that link goes to the *home page*. It's intended that the middle portion of the `navbar` will contain a breadcrumb trail as we navigate around the *Notes* application. 

The ADD Note button is glued to the right-hand side with a little Flexbox magic. The container is a Flexbox, meaning we can use the Bootstrap classes to control the space consumed by each item. The breadcrumb area is the blank spot between the home icon and the ADD Note button. It is empty in this case, but the `<div>` element that would contain it is there and declared with `class="col"`, meaning that it takes up a column unit. The ADD Note button is, on the other hand, declared with `class="col-auto"`, meaning it takes up only the room required for itself. Therefore, the empty breadcrumb area that will expand to fill the available space, while the ADD Note button fills only its own space, and is therefore pushed over to the side.

Because it's the same application, the functionality all works; we're simply working on the presentation. We've added a few notes but the presentation of the list on the front page leaves a lot to be desired. The small size of the title is not very touch-friendly since it doesn't present a large target area for a fingertip. And can you explain why the `notekey` value has to be displayed on the home page? With that in mind, let's move on to fixing up the front page.

## Improving the Notes list on the front page

The current home page has some simple text list that's not terribly touch-friendly, and showing the *key* at the front of the line might be inexplicable to the user. Let's fix this.

Edit `views/index.hbs` as follows, with the changed lines shown in bold:

[PRE8]js\1

This removes the `<h1>` tag at the top of the header area, immediately tightening up the presentation. 

Within the `navbar-collapse` area, we've replaced what had been intended as the breadcrumb with a simple `navbar-text` component containing the page title. To keep the ADD Note button glued to the right, we're maintaining the `class="col"` and `class="col-auto"` settings:

![](img/f36a31a8-1cbd-4018-a2a6-2ca910157907.png)

Which header area design is better? That's a good question. Since beauty is in the eye of the beholder, both designs are probably equally good. What we have demonstrated is the ease with which we can update the design by editing the template files.

Let's now take care of the page for viewing notes.

## Cleaning up the note viewing experience

Viewing a note isn't bad, but the user experience can be improved. For example, the user does not need to see the `notekey`, meaning we might remove that from the display. Additionally, Bootstrap has nicer-looking buttons we can use.

In `views/noteview.hbs`, make these changes:

[PRE9]js\1

There's a lot going on here. What we've done is reorganize the `form` so Bootstrap can do the right things with it. The first thing to note is that we have several instances of this:

[PRE10]js\1

We've reworked it to use similar Bootstrap form markup. The question about deleting the note is wrapped with `class="form-text"` so that Bootstrap can display it properly.

The buttons are wrapped with `class="btn-group"` as before. The buttons have exactly the same styling as on other screens, giving a consistent look across the application:

![](img/8f9abc52-09b0-4df4-b231-afb832a45aee.png)

There is an issue in that the title text in the navbar does not use the word `Delete`. In `routes/notes.mjs`, we can make this change:

[PRE11]js\1

This will automatically download and unpack the Bootstrap source distribution, and then the `postdownload` step will run `npm install` to install the dependencies declared by the Bootstrap project. This gets the source tree all set up and ready to modify and build.

Type this command:

[PRE12]js\1

Obviously, you'll need to adjust these directory names when a new Bootstrap release is issued.

In the Bootstrap source tree, running `npm run dist` builds Bootstrap using a process recorded in the Bootstrap `package.json` file. Likewise, `npm run watch` sets up an automated process to scan for changed files and rebuilds Bootstrap upon changing any file. Running `npm run clean` will delete the Bootstrap source tree. By adding these lines to our `theme/package.json` file, we can start this in the Terminal and we can now rerun the build as needed without having to scratch our heads, struggling to remember what to do.

To avoid having the Bootstrap source code checked into your Git repository, add a `theme/.gitignore` file:

[PRE13]js\1

The built files land in the `theme/bootstrap-4.5.0/dist` directory. The content of that directory will match the contents of the npm package for Bootstrap.

Before proceeding, let's take a look around the Bootstrap source tree. The `scss` directory contains the SASS source that will be compiled into the Bootstrap CSS files. To generate a customized Bootstrap build will require a few modifications in that directory.

The `bootstrap-4.5.0/scss/bootstrap.scss` file contains `@import` directives to pull in all Bootstrap components. The file `bootstrap-4.5.0/scss/_variables.scss` contains definitions used in the remainder of the Bootstrap SASS source. Editing or overriding these values will change the look of websites using the resulting Bootstrap build.

For example, these definitions determine the main color values:

[PRE14]js\1

This reverses the values for the `$body-bg` and `$body-color` settings in `_variables.scss`. The Notes app will now use white text on a dark background, rather than the default white background with dark text. Because these declarations do not use `!default`, they'll override the values in `_variables.scss`.

Then, make a copy of `scss/bootstrap.scss` in the `theme` directory and modify it like so:

[PRE15]js\1

With these scripts, before building Bootstrap, these two files will be copied in place, and afterward, the built files will be copied to a directory named `dist`. The `prebuild` step lets us commit our copy of the `_custom.scss` and `bootstrap.scss` files into our source repository, while being free to delete the Bootstrap source at any time. Likewise, the `postbuild` step lets us commit the custom theme we built to the source repository.

Next, rebuild Bootstrap:

[PRE16]js\1

What we've done is switch from the Bootstrap configuration in `node_modules` to what we just built in the `theme` directory. 

Then reload the application, and you'll see the coloring change.

There are two changes required to get this exact presentation. The button elements we used earlier have the `btn-outline-dark` class, which works well on a light background. Because the background is now dark, these buttons need to use light coloring. 

To change the buttons, in `views/index.hbs`, make this change:

[PRE17]js\1

That's cool, we can now rework the Bootstrap color scheme any way we want. Don't show this to your user experience team, because they'll throw a fit. We did this to prove the point that we can edit `_custom.scss` and change the Bootstrap theme.

The next thing to explore is using a pre-built, third-party Bootstrap theme.

## Using third-party custom Bootstrap themes

If all this is too complicated for you, several websites provide pre-built Bootstrap themes, or else simplified tools to generate a Bootstrap build. To get our feet wet, let's download a theme from Bootswatch ([https://bootswatch.com/](https://bootswatch.com/)). This is both a collection of free and open source themes and a build system for generating custom Bootstrap themes ([https://github.com/thomaspark/bootswatch/](https://github.com/thomaspark/bootswatch/)).

Let's use the **Minty** theme from Bootswatch to explore the needed changes. You can download the theme from the website or add the following to the `scripts` section of `package.json`:

[PRE18]js\1

In `app.mjs` we will need to change the Bootstrap mounts to separately mount the JavaScript and CSS files. Use the following:

[PRE19]js\1

We selected the `text-dark` and `btn-dark` classes to provide some contrast against the background.

Re-run the application and you'll see something like this:

![](img/bb10d8cb-6641-48f4-a1dd-961043e0e675.png)

With that, we have completed our exploration of customizing the look and feel of a Bootstrap-based application. We can now wrap up the chapter.

# Summary

The possibilities for using Bootstrap are endless. While we covered a lot of material, we have only touched the surface, and we could have done much more with our *Notes* application. But since our focus in this book is not on the UI, but on the backend Node.js code, we purposely limited ourselves to making the application work acceptably well on mobile devices.

You learned what the Twitter Bootstrap framework can do by using it to implement a simple responsive website design. Even the little changes we made improved the way the *Notes* app looks and feels. We also created a customized Bootstrap theme, along with using a third-party theme, to explore how easy it is to make a Bootstrap build look unique.

Now, we want to get back to writing Node.js code. We left off [Chapter 5](582d3898-0135-430c-8b6e-8326f287e18b.xhtml), *Your First Express Application*, with the problem of persistence, where the *Notes* application could be stopped and restarted without losing our notes. In [Chapter 7](ae8529e5-3a08-45cc-89e9-82895eb45641.xhtml), *Data Storage and Retrieval*, we'll dive into using several database engines to store our data.