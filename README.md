# philipagain.com

Personal site of Philip Müller. Plain HTML and CSS, served by GitHub Pages.
No build step, no framework, no tracking, no third-party requests.

## Structure

```
index.html            the page: hero, Now, Things I build, About, Follow along
404.html              page shown for broken links
favicon.svg           the three Bauhaus marks
assets/css/site.css   all styles: colours, fonts, layout, interactions
assets/js/site.js     signup form behaviour (no data is stored yet)
assets/img/           images (tool icons; later hero.jpg and portrait.jpg)
assets/fonts/         self-hosted fonts (Comfortaa, Jost) and their licences
```

## Everyday changes

Every change pushed to `main` is live within about a minute.

| What | Where |
| :- | :- |
| "Now" lines | `index.html`, section `NOW` |
| Add a tool | `index.html`, section `THINGS I BUILD`: copy a `card` block |
| About text | `index.html`, section `ABOUT` |
| Hero photo | save as `assets/img/hero.jpg`, then follow the comment above `<header class="hero">` |
| Portrait | save as `assets/img/portrait.jpg`, then follow the comment in `ABOUT` |
| Colours | `assets/css/site.css`, the variables under `:root` (light) and the dark-mode block below |

Small text edits also work directly on github.com: open the file, click the
pencil icon, edit, and commit.

## Before the public launch

- Fill in all placeholders shown in `[square brackets]`.
- Remove `<meta name="robots" content="noindex">` from `index.html`, so search engines can find the site.
- Connect a newsletter service in `assets/js/site.js`, and add a privacy notice page.

## Design

- **Palette:** Prova, iterated: plaster, blush, charcoal, burnt sienna (actions), sky and ochre (accents only). Dark mode follows the visitor's system setting.
- **Type:** Comfortaa 700 for headlines, Jost for text, both under the SIL Open Font License, self-hosted so no visitor data goes to Google.
- **Accessibility:** text contrast at least 4.5:1, tap targets at least 44 px, visible keyboard focus, animations off when the visitor prefers reduced motion.

## Custom domain

Once DNS is ready: add a `CNAME` file containing `philipagain.com`, set the custom domain in the repository's Pages settings, and enforce HTTPS.

## After changing CSS or JavaScript

`index.html` loads `site.css?v=…` and `site.js?v=…`. Change the `v=` value
(for example to the current date and time) whenever you edit those files, so
browsers fetch the new version instead of a cached old one.
