# aymanchafni.github.io

Personal portfolio of Ayman Chafni, in English (`/`), French (`/fr/`) and Arabic (`/ar/`, right-to-left).

## Editing

All text lives in `content/site.json`:

- `shared`: links, projects (repo URL and stack), skill lists and certifications, used by every language.
- `langs.en`, `langs.fr`, `langs.ar`: everything that's translated, including project descriptions and experience.

Styles are in `assets/site.css`. The page template and the hero pipeline diagram are in `build.py`.

## Building and previewing

Python 3 only, no dependencies:

```bash
python3 build.py
python3 -m http.server -d _site 8000
```

Then open http://localhost:8000.

## Deploying

Pushing to `master` runs `.github/workflows/deploy.yml`, which builds the site and publishes `_site/` to the `gh-pages` branch that GitHub Pages serves. Pull requests run the build as a check without publishing.
