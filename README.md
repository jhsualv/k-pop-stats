# kpop stats

A Flask web application that analyzes a user's Spotify listening habits and identifies their favorite K-pop groups, eras, and tracks.

## Overview

kpop stats connects to Spotify through OAuth, ingests the user's top tracks and saved tracks, and uses a relational PostgreSQL database to analyze listening patterns across groups, eras, albums, and tracks.

The application calculates era affinity from the user's Spotify top-track rankings and aggregates those scores to determine group rankings.

## Features

* Spotify OAuth authentication
* Spotify profile information
* Top tracks ingestion across three Spotify time ranges:
  * 4 weeks
  * 6 months
  * all time
* Saved tracks ingestion
* Group ranking based on combined era affinity
* Favorite era for each group
* Favorite track for each group
* Era-level listening breakdown
* Group profile images
* Expandable group analysis
* PostgreSQL-backed relational data model
* Flask/Jinja server-rendered interface

## How the analysis works

Each track in a user's Spotify top-track results has a ranking position. The application assigns greater weight to higher-ranked tracks using an inverse-position score:

`1 / position`

Tracks are connected through the relational model:

`tracks → albums → eras → groups`

The application first aggregates these weighted track scores by era. It then combines the scores of eras belonging to the same group to produce a group affinity score.

This allows the application to show both:

* which group the user listens to most
* which era within that group contributes most to the result

## Tech stack

* Python
* Flask
* PostgreSQL
* SQL
* Jinja templates
* HTML / CSS
* Spotify Web API

## Setup

Spotify API credentials and other secrets are provided through environment variables and are not stored in the repository.

The application requires:

* Python 3
* PostgreSQL
* Spotify Developer API credentials

After configuring the environment and database, run the Flask application with:

```bash
python app.py
```

## Project status

The core Spotify ingestion and listening-analysis functionality is implemented. The application is currently focused on K-pop groups and eras, with additional groups and analysis features planned for future development.
