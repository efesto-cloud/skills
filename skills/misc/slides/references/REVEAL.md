
## Base Elements

### Body Structure
```html
	<body>
		<div class="reveal">
      <div class="slides">
      // Slides go here
      </div>
    </div>
  </body>
```

### Slide Structure
```html
<section>
  <h1>Title</h1>
  <h3>SubTitle</h3>
  <p>
  Some Text here
  </p>
</section>
```
### Multi-Slide (Vertical) Structure
```html
<section>
    <section>
      <h1>First Slide</h1>
    </section>
    <section>
      <h1>Second Slide</h1>
    </section>    
</section>
```

### Multi-Slide (Vertical) Structure
```html
<section>
    <section>
      <h1>First Slide</h1>
    </section>
    <section>
      <h1>Second Slide</h1>
    </section>    
</section>
```

### Multi-Slide (Vertical) Structure
```html
<section>
    <section>
      <h1>First Slide</h1>
    </section>
    <section>
      <h1>Second Slide</h1>
    </section>    
</section>
```

### Markdown Slide
```html
<section data-markdown>
  <script type="text/template">
    ## Markdown Slide Title
    Content here.
  </script>
</section>
```

## Fragmentation (Displaying progressively)
```html
<section id="fragments">
  <p>Visible By default</p>
  <p class="fragment">after hitting next</p>
  <p class="fragment">then again</p>
  <p class="fragment">and again</p>
  </aside>
</section>
```
Animations and Highlighting:
```html
<p class="fragment grow">Grow Current Selected</p>
<p class="fragment shrink">Shrink Current Selected</p>
<p class="fragment fade-out">Hide Current Selected</p>
<p class="fragment fade-up">Fade and Grow Up</p>
<p class="fragment fade-down">Fade and Grow Down</p>
<p class="fragment fade-left">Fade and Grow Left</p>
<p class="fragment fade-right">Fade and Grow Right</p>
<p class="fragment current-visible">Display only when selected</p>
<p> Highlight Colors
  <span class="fragment highlight-red">red</span>
  <span class="fragment highlight-blue">blue</span>
  <span class="fragment highlight-green">green</span>
</p>
```

## Transitions
Append to the URL:
* `?transition=none#/transitions` : No transition
* `?transition=slide#/transitions` : Slide transition
* `?transition=convex#/transitions` : Convex Slide transition
* `?transition=concave#/transitions` : Concave Slide transition
* `?transition=zoom#/transitions` : Zoom transition

## Backgrounds
* `<section data-background="#dddddd">` Colored Background
* `<section data-background="image.png">` Image background
* `<section data-background="image.png" data-background-repeat="repeat" data-background-size="100px">` Tiled Image
* `<section data-background-video="video.mp4,video.webm">` Video Background

## Code Highlighting
```
<pre><code class="hljs" data-trim contenteditable>

function linkify( selector ) {
  if( supports3DTransforms ) {

    var nodes = document.querySelectorAll( selector );

    for( var i = 0, len = nodes.length; i &lt; len; i++ ) {
      var node = nodes[i];

      if( !node.className ) {
        node.className += ' roll';
      }
    }
  }
}

</code></pre>```