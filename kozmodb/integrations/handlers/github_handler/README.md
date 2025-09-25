# GitHub Handler

GitHub handler for KozmoDB provides interfaces to connect to GitHub via APIs and pull repository data into KozmoDB.

---

## Table of Contents

- [GitHub Handler](#github-handler)
  - [Table of Contents](#table-of-contents)
  - [About GitHub](#about-github)
  - [GitHub Handler Implementation](#github-handler-implementation)
  - [GitHub Handler Initialization](#github-handler-initialization)
  - [Implemented Features](#implemented-features)
  - [Example Usage](#example-usage)

---

## About GitHub

GitHub is a web-based hosting service for version control using Git. It is mostly used for computer code.
It offers all the distributed version control and source code management (SCM) functionality
of Git as well as adding its own features. It provides access control and several collaboration
features such as bug tracking, feature requests, task management, and wikis for every project.

## GitHub Handler Implementation

This handler was implemented using the [pygithub](https://github.com/PyGithub/PyGithub) library.
PyGithub is a Python library that wraps GitHub API v3.

## GitHub Handler Initialization

The GitHub handler is initialized with the following parameters:

- `repository`: a required name of a GitHub repository to connect to
- `api_key`: an optional GitHub API key to use for authentication
- `github_url`: an optional GitHub URL to connect to a GitHub Enterprise instance

Read about creating a GitHub API key [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

## Implemented Features

- [x] GitHub Issues Table for a given Repository
  - [x] Support SELECT
    - [x] Support LIMIT
    - [x] Support WHERE
    - [x] Support ORDER BY
    - [x] Support column selection
  - [x] Support INSERT
    - [x] Support title, body, assignee, milestone, and labels columns
- [x] GitHub Pull Requests Table for a given Repository
- [x] GitHub Commits Table for a given Repository
- [x] GitHub Releases Table for a given Repository
- [x] GitHub Branches Table for a given Repositorytory
- [x] GitHub Projects Table for a given Repository
  - [x] Support SELECT
    - [x] Support LIMIT
    - [x] Support WHERE
    - [x] Support ORDER BY
    - [x] Support column selection

## Example Usage

The first step is to create a database with the new `github` engine. The `api_key` parameter is optional,
however, GitHub aggressively rate limits unauthenticated users. Read about creating a GitHub API key [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

~~~~sql
CREATE DATABASE kozmodb_github
WITH ENGINE = 'github',
PARAMETERS = {
  "repository": "digitranslab/kozmodb",
  "api_key": "your_api_key"    -- optional GitHub API key
};
~~~~

Use the established connection to query your database:

~~~~sql
SELECT * FROM kozmodb_github.issues
~~~~

~~~~sql
SELECT * FROM kozmodb_github.branches
~~~~

~~~~sql
SELECT * FROM kozmodb_github.contributors
~~~~

~~~~sql
SELECT * FROM kozmodb_github.projects
~~~~

Run more advanced queries:

~~~~sql
SELECT number, state, creator, assignee, title, labels
  FROM kozmodb_github.issues
  WHERE state="all"
  ORDER BY created ASC, creator DESC
  LIMIT 10
~~~~

~~~~sql
SELECT number, state, title, creator, head, commits
  FROM kozmodb_github.pull_requests
  WHERE state="all"
  ORDER BY long_running DESC, commits DESC
  LIMIT 10
~~~~


