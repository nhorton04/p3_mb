#  HTML Basics

### Step 1
Start by making a folder (outside of the Metis GitHub repo, to avoid git conflicts) called something like "website". This is where we'll put all of our website's **assets**. Inside this folder, start out with an empty HTML file, and call it `index.html`. The start of our website's folder should look like this

```
/website
    index.html
```

### Step 2
Now we start to create the HTML 'structure'. Inside the `index.html` file, include this "outline" to be filled in.

```html
<!DOCTYPE html>
<html>
<head>
    <title></title>
</head>
<body>

</body>
</html>
```

A few notes on this:

- The `<!DOCTYPE html>` tells the web server what to expect in syntax for this file
- The HTML tag (`<html>`) is the root node of the HTML doc, where `<head>` & `<body>` are the children (we always use indentation to illustrate the hierarchy).
- Within the `<head>` is all the metadata for the webpage (e.g., the `<title>` shows up in the tab in Chrome)

### Step 3
Now, we'll add a new section or division (`<div>`), containing a header (`<h1>`) and a paragraph (`<p>`). Remember, these tags represent elements within "boxes". HTML is very hierarchical, so everything is essentially a box, within another box, within another box.

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <div>
        <h1>Important Information</h1>
        <p>You are reading important information.</p>
    </div>
</body>
</html>
```

### Step 4

Now let's get creative, and include some fancy references to scripts and style sheets. Add another folder in our directory for JavaScript and CSS. So, we should have the directory looking like this:

```
/website
    /js
        main.js
    /css
        style.css
    index.html
```

Maybe you leave the JavaScript file empty, or maybe you don't! Up to you. As for the CSS, let's add some simple styling:

```css
/* Within the `body` tag, adjust the `background` with the value `lightblue`  */
body {
    background: lightblue;
}

/* Also, set a background for any Header 1 (h1) tag */
h1 {
    background: blue;
}
```

Regarding the `h1` tag, remember, we've got "boxes" in "boxes," so it's okay to think of the header with a background. **For this CSS to apply, you need to add `<link rel="stylesheet" href="css/style.css">` to the `<head>` section of your HTML file.** That is, your HTML file's head should look like:

```html
<head>
    <!-- The thing that shows up in the tab -->
    <title>Traffic Stopping Turtles</title>  

    <!-- Think of these as two different kinds of "import" statement -->
    <link rel="stylesheet" href="css/style.css">
</head>
```

### Step 5

Get creative. Check out all the other [elements](https://www.w3schools.com/html/html_elements.asp) you can include in your page, try some new [CSS](https://www.w3schools.com/html/html_css.asp), maybe even manipulate the DOM with some [JavaScript](https://www.w3schools.com/html/html_scripts.asp) code. If you can, add an [image](https://www.w3schools.com/html/html_images.asp) where the `src` attribute is some image URL from online (not saved locally).

Once you're all done, fire up a local server, and open the page in the Chrome development console. That is, follow these steps:

1. Make sure you navigate to the `website` folder where you created the `index.html`.
2. Run `python -m http.server`
3. You should get a response like

```
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Optional:

* Incorporate JavaScript into your front end design too.
* Use JQuery to change something else

A few words about:

* HTML (Hypertext Markup Language): provides the structure for our page
* CSS (Cascading Style Sheets) : provides the visual layout
* HTML & CSS are concerned with how the information is displayed, whereas Javascript allows us to manipulate this display (tags etc,) (more about javascript later!)
* jQuery is a collection of JavaScript libraries that are designed to simplify HTML document event handling, animation, & Ajax interactions (etc.)
