# philipagain.com

Personal site of Philip Müller. Plain HTML and CSS, served by GitHub Pages.
No framework, no tracking, no third-party requests.

**All the words on the site live in [`content.md`](content.md).** Edit that file,
commit, and a GitHub Action rebuilds `index.html` from it within a couple of minutes.
Don't edit `index.html` by hand: the next rebuild overwrites it.

## Structure

```
content.md            all the text: hero, So far, Now, Things I build, About, Get in touch
template.html         the page layout, with {{placeholders}} for the text
build.py              turns content.md + template.html into index.html (python3 build.py)
.github/workflows/    runs build.py on every push that changes the three files above
index.html            the generated page (don't edit by hand)
404.html              page shown for broken links
favicon.svg           the logo: three overlapping leaves
assets/css/site.css   all styles: colours, fonts, layout, interactions
assets/js/site.js     the "again..." button and the moving "So far" path
assets/img/           images (tool icons; later hero.jpg and portrait.jpg)
assets/fonts/         self-hosted fonts (Comfortaa, Jost) and their licences
```

## Everyday changes

Every change pushed to `main` is live within about a minute.

| What | Where |
| :- | :- |
| Hero text | `content.md`, section `# Hero` |
| A career step | `content.md`, section `# So far`: copy a `##` entry |
| "Now" lines | `content.md`, section `# Now` |
| Add a tool | `content.md`, section `# Things I build`: copy a `##` entry |
| About text | `content.md`, section `# About` |
| Contact email | `content.md`, the `email:` line at the top (used by every button and link) |
| Page title and search description | `content.md`, the lines between `---` at the top |
| Hero photo | save as `assets/img/hero.jpg`, then follow the comment above `<header class="hero">` in `template.html` |
| Portrait | replace `assets/img/portrait.jpg` |
| Colours | `assets/css/site.css`, the variables under `:root` (light) and the dark-mode block below |

Text edits work directly on github.com: open `content.md`, click the pencil
icon, edit, and commit. The comment at the top of `content.md` explains its format.

To preview locally, run `python3 build.py` and open `index.html` in a browser.
To change layout or markup, edit `template.html`, then run `python3 build.py`.

## Before the public launch

- Fill in all placeholders shown in `[square brackets]`.
- Remove `<meta name="robots" content="noindex">` from `template.html`, so search engines can find the site.
- Make sure `hello@philipagain.com` receives email (the domain needs mail records).

## Design

- **Palette:** [Prova](https://docs.google.com/spreadsheets/d/1VUufIwgOt2PKE-Hl9khhqfq5y1BKrQf6): plaster, blush, charcoal, terracotta (actions), sky and olive (accents only). Dark mode follows the visitor's system setting.
- **Logo:** three see-through leaves in terracotta, sky and charcoal (`.logo` in `site.css`, behaviour in `site.js`). They gather in on load and every 9 to 14 seconds; a click turns the mark a third.
- **Type:** Comfortaa 700 for headlines, Jost for text, both under the SIL Open Font License, self-hosted so no visitor data goes to Google.
- **Accessibility:** text contrast at least 4.5:1, tap targets at least 44 px, visible keyboard focus, animations off when the visitor prefers reduced motion.

## Custom domain

Once DNS is ready: add a `CNAME` file containing `philipagain.com`, set the custom domain in the repository's Pages settings, and enforce HTTPS.

## After changing CSS or JavaScript

`template.html` loads `site.css?v=…` and `site.js?v=…`. Change the `v=` value
(for example to the current date and time) whenever you edit those files, so
browsers fetch the new version instead of a cached old one.
