# High level choices

* Pretty small service -> Flask
* RDB but easy to use -> SQLite
* ORM to avoid hand-made SQL -> SQLAlchemy
* JSON serialization for the fun (overkill here) -> Marshmallow

## DB

[DB Schema](https://i.ibb.co/ZRgFkQfC/Screenshot-2025-04-05-at-1-38-39-PM.png)

* The DB model for Campaigns has been made simple (name only) to respect the rule, but doesn't match the shape of the one mocked (unusual, hence the awkward APICampaignSchema)
* Devices should be split in various sub tables, but as they are not central to the task, they are left as one

## Questionable elements

* My usage of SQLAlchemy is probably unoptimized, we are likely over-fetching data.
* A lot of logic is still done in app.js. If the application was meant to be a bit more complex, this would be moved to an in-between layer (separation of concerns).
* The approach to matchers is manual, would not scale with with a large number of matchers
* Config managment is inexistent, to keep things simple. Not an option in a "real" project.


## How to use

* This is a standard Flask:
    * Create & Activate a Venv
    * Install dependencies (make install)
    * Initialize the database (make init-db)
    * Run the server (make run)
    * Test endpoints (make test-config)
    * Run unit tests (make test)
    