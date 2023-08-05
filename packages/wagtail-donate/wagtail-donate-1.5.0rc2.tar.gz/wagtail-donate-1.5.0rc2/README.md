# Wagtail Donate

A pluggable donations app for Wagtail sites.

## Staging site

Staging site is available at https://wagtaildonate-staging.herokuapp.com/.

## Development

See the
[internal/wagtaildonatesite](https://git.torchbox.com/internal/wagtaildonatesite)
repo for instructions on how to get this running locally. This is the codebase
that is used on staging site and that project's CI is used for deployments.

## Technical documentation

Docs can be viewed at https://internal.pages.torchbox.com/wagtail-donate/ or in `./docs`.

## Storybook

This project uses [Storybook](https://storybook.js.org/).

A static version is available at: https://internal.pages.torchbox.com/wagtail-donate/storybook

Storybook can be executed locally by running `npm run storybook`.

## Running tests

Running tests requires `tox`

```[python]
pip install tox
```

To run test just run `tox` at the root.
