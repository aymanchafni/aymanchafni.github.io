# aymanchafni.github.io

Personal portfolio and blog of **Ayman Chafni**, Data Engineer and Data Scientist.
Built with [Jekyll](https://jekyllrb.com/), which GitHub Pages builds automatically.
There's no theme dependency and no build step on your machine.

Live: <https://aymanchafni.github.io>

---

## Bilingual (EN / FR)

The site exists in English at `/` and in French at `/fr/`. Every content file
has an English and a French copy:

| English                    | Français                     | URL (EN → FR)                 |
|----------------------------|------------------------------|-------------------------------|
| `index.html`               | `fr/index.html`              | `/` → `/fr/`                  |
| `projects.html`            | `fr/projets.html`            | `/projects/` → `/fr/projets/` |
| `blog/index.html`          | `fr/blog/index.html`         | `/blog/` → `/fr/blog/`        |
| `_posts/`                  | `fr/_posts/`                 | `/blog/2026/x/` → `/fr/blog/2026/y/` |
| `_data/en/*.yml`           | `_data/fr/*.yml`             |                               |

- The **EN / FR button** in the header goes to the translated version of the
  current page. Pages are paired by a shared `ref:` in their front matter.
  If a page has no translation, the button goes to the other language's home page.
- **Articles don't have to be translated.** An article written in only one
  language also appears in the other language's list, with a small `EN` / `FR` badge.
  To link an article to its translation, give both the same `ref:`.
- Interface labels (menu, buttons, section titles, month names) are in `_data/i18n.yml`.
- French typography: use a non-breaking space (U+00A0, or `&nbsp;` in Markdown) before `:` so
  the colon never wraps to the start of a line.

## Where things live

| What you want to change          | File                                         |
|----------------------------------|----------------------------------------------|
| Name, email, links, SEO text     | `_config.yml`                                |
| Menu, buttons, section titles    | `_data/i18n.yml`                             |
| Hero headline, intro, "open to"  | `_data/en/profile.yml`, `_data/fr/profile.yml` |
| Skills (pipeline stages)         | `_data/{en,fr}/skills.yml`                   |
| Projects                         | `_data/{en,fr}/projects.yml`                 |
| Work experience                  | `_data/{en,fr}/experience.yml`               |
| Education & certifications       | `_data/{en,fr}/education.yml`                |
| Articles                         | `_posts/` (EN), `fr/_posts/` (FR)            |
| Unpublished drafts               | `_drafts/` (EN), `fr/_drafts/` (FR)          |
| CV (PDF) / photo                 | `assets/files/`, `assets/img/` (CV link per language: `cv_url` in `_data/i18n.yml`) |
| Colors, fonts, layout            | `assets/css/main.css` (tokens at top)        |

## Writing a new article

1. Create a file named `YYYY-MM-DD-short-title.md` in `_posts/` for English or
   `fr/_posts/` for French, e.g. `_posts/2026-11-15-spark-partitioning-tips.md`.
2. Start it with this front matter, then write Markdown:

   ```markdown
   ---
   title: "Spark partitioning: 5 things I wish I knew"
   description: "One-sentence summary shown in lists and link previews."
   tags: [spark, data engineering]
   # optional:
   # ref: spark-partitioning                    # same value in the translation

   # image: /assets/img/posts/spark-cover.png   # cover + social preview
   # mermaid: true                              # enable ```mermaid diagrams
   # math: true                                 # enable $LaTeX$ math
   ---

   Your article in **Markdown**…
   ```

3. Commit and push. It shows up at `/blog/2026/spark-partitioning-tips/`
   (or `/fr/blog/...`), on the home page and in the RSS feed (`/feed.xml`).

Tips:
- Images: put them in `assets/img/posts/` and use `![alt text](/assets/img/posts/file.png)`.
- Code blocks get syntax highlighting and a copy button: ```` ```python ````, ```` ```sql ````, ```` ```bash ````…
- Code containing `{{ }}` (dbt, Jinja, Airflow templates) must be wrapped in
  `{% raw %}` … `{% endraw %}`, otherwise Jekyll tries to evaluate it.
- Want to work on something without publishing? Put it in `_drafts/` or `fr/_drafts/` (no date in the name).
  See `_drafts/etl-vs-elt-pandas-vs-dbt.md` and its French twin
  `fr/_drafts/etl-vs-elt-pandas-contre-dbt.md` for an example using every feature.

## Adding a project

Add an entry to **both** `_data/en/projects.yml` and `_data/fr/projects.yml`
(translate `title`, `category`, `summary`, `highlights`; the rest stays the same):

```yaml
- title: My New Pipeline
  category: Data Engineering
  featured: true            # show on the home page
  repo: my-new-pipeline     # repo name on github.com/aymanchafni (or a full URL)
  article: /blog/2026/my-new-pipeline/   # optional link to a write-up
  summary: One or two sentences on the problem and the result.
  highlights:
    - What you built, with numbers if you have them
  stack: [Python, Spark, Airflow]
```

## Deploying

GitHub Pages builds the site on every push:

1. Push this folder to `github.com/aymanchafni/aymanchafni.github.io`.
2. In the repo, go to **Settings → Pages → Build and deployment**:
   *Source: Deploy from a branch*, *Branch: `main` / `(root)`*.
3. The site is live at <https://aymanchafni.github.io> about a minute later.

## Previewing locally (optional)

**With Docker** (no Ruby needed):

```bash
docker compose up
# open http://localhost:4000 (add --drafts to the command in docker-compose.yml to see drafts)
```

**With Ruby** (3.x):

```bash
bundle install
bundle exec jekyll serve --livereload --drafts
```
