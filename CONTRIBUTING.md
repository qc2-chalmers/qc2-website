### Instructions for contributors

Below are some simple instructions for contributing to the website. Most contributions involve adding a new code block to the HTML pages. This is typically done by copying and pasting a code snippet and replacing the placeholder information (indicated by the capitalized text) with your own content.

#### People page

The "People" page features short biographies of our group members. To add a new member card, copy and paste the following code snippet:

```html
<div class="col">
    <div class="person-card text-center">
    <img src="images/people/NAME_LASTNAME.PNG" class="person-img shadow-sm" alt="NAME LASTNAME">
    <h5 class="fw-bold mb-1">NAME LASTNAME</h5>
    <div class="person-description text-body-secondary">
    A DESCRIPTION OF YOUR RESEARCH INTERESTS, E.G. "AI METHODS FOR PULSE OPTIMIZATION"
    </div>
    <a href="LINK-TO-YOUR-PERSONAL-PAGE" class="btn-profile">More About Me 🔍</a>
    </div>
</div>
```

#### Blog page

The blog page hosts news regarding papers, team members, and events. To create a new entry, copy and paste the HTML code for the card and update it with the new information. Here is an example:

```html
<div class="col">
    <div class="card blog-card h-100 p-3">
    <img src="images/blog/YOUR-IMAGE-NAME.png" class="blog-img shadow-sm" alt="Post 4">
    <div class="card-body p-0">
        <span class="badge badge-date">MONTH NUMBER, YEAR</span>
        <h4 class="card-title fw-bold h5">YOUR NEW TITLE</h4>
        <p class="card-text small text-body-secondary">
        A SHORT DESCRIPTION.
        </p>
        <a href="LINK-TO-YOUR-REFERENCE" class="btn btn-sm btn-link p-0 text-primary fw-bold text-decoration-none">Read more →</a>
    </div>
    </div>
</div>
```

**Regarding images**: All icons are generated using Gemini Nano Banana 2. To generate a new image, upload a reference image of our mascot (found at ./images/blog/mascot.png) to Gemini. When creating a new card, please ensure the style remains consistent: maintain the image proportions and remove the background so that the image renders correctly in both light and dark modes.


#### Publications page

As with the previous sections, there is a pre-formatted HTML block available for new publications:

```html
<article class="pub-card">
<div class="row g-4 align-items-start">
    <div class="col-md-8">
    <h3 class="fw-bold mb-3">PAPER TITLE</h3>
    <div class="d-flex flex-column gap-3">
        <p class="text-secondary fw-medium mb-0" style="color: #64748b !important;">
        AUTHOR 1, AUTHOR 2, ....
        </p>
        <div style="width: fit-content;">
        <a href="ARXIVE-LINK" target="_blank" class="btn btn-outline-primary btn-sm">
            <svg class="btn-icon"><use href="#journal-text"></use></svg> Read the Paper
        </a>
        </div>
    </div>
    </div>
    <div class="col-md-4">
    <img src="images/papers/MY-PAPER-FIGURE.PNG" class="pub-img" alt="Paper Image">
    </div>
</div>
</article>
```

Ciao