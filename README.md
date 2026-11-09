# aymanchafni.github.io

Personal portfolio and blog of **Ayman Chafni**, Data Engineer and Data Scientist.
Built with [Jekyll](https://jekyllrb.com/), which GitHub Pages builds automatically.
There's no theme dependency and no build step on your machine.

Live: <https://aymanchafni.github.io>

---

## Where things live

| What you want to change          | File                                   |
|----------------------------------|----------------------------------------|
| Name, email, links, SEO text     | `_config.yml`                          |
| Hero headline, intro, "open to"  | `_data/profile.yml`                    |
| Skills (pipeline stages)         | `_data/skills.yml`                     |
| Projects                         | `_data/projects.yml`                   |
| Work experience                  | `_data/experience.yml`                 |
| Education & certifications       | `_data/education.yml`                  |
| Articles                         | `_posts/`                              |
| Unpublished drafts               | `_drafts/`                             |
| CV (PDF) / photo                 | `assets/files/`, `assets/img/`         |
| Colors, fonts, layout            | `assets/css/main.css` (tokens at top)  |

## Writing a new article

1. Create a file in `_posts/` named `YYYY-MM-DD-short-title.md`, e.g.
   `_posts/2026-11-15-spark-partitioning-tips.md`.
2. Start it with this front matter, then write Markdown:

   ```markdown
   ---
   title: "Spark partitioning: 5 things I wish I knew"
   description: "One-sentence summary shown in lists and link previews."
   tags: [spark, data engineering]
   # optional:
   # image: /assets/img/posts/spark-cover.png   # cover + social preview
   # mermaid: true                              # enable ```mermaid diagrams
   # math: true                                 # enable $LaTeX$ math
   ---

   Your article in **Markdown**…
   ```

3. Commit and push. It shows up at `/blog/2026/spark-partitioning-tips/`,
   on the home page and in the RSS feed (`/feed.xml`).

Tips:
- Images: put them in `assets/img/posts/` and use `![alt text](/assets/img/posts/file.png)`.
- Code blocks get syntax highlighting and a copy button: ```` ```python ````, ```` ```sql ````, ```` ```bash ````…
- Code containing `{{ }}` (dbt, Jinja, Airflow templates) must be wrapped in
  `{% raw %}` … `{% endraw %}`, otherwise Jekyll tries to evaluate it.
- Want to work on something without publishing? Put it in `_drafts/` (no date in the name).
  See `_drafts/etl-vs-elt-pandas-vs-dbt.md` for an example using every feature.
- Writing in French? Add `lang: fr` to the front matter.

## Adding a project

Add an entry to `_data/projects.yml`:

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
