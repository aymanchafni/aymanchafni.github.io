source "https://rubygems.org"

# Same Jekyll version + plugins that GitHub Pages uses in production.
gem "github-pages", group: :jekyll_plugins

# Needed to run `jekyll serve` on Ruby 3+
gem "webrick"

# Windows / JRuby don't ship zoneinfo files
platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
gem "wdm", "~> 0.1", platforms: [:windows]
