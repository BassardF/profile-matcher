# High level choices

* Pretty small service -> Flask
* RDB but easy to use -> SQLite
* ORM to avoid hand made SQL -> SQLAlchemy
* JSON serialization for the fun (overkill here) -> Marshmallow

## DB

[DB Schema](https://i.ibb.co/ZRgFkQfC/Screenshot-2025-04-05-at-1-38-39-PM.png)

* The DB model for Campaigns has been made simple (name only) to respect the rule, but doesn't match the shape of the one mocked (unusual, hence the awkward APICampaignSchema)
* Devices should clearly be split in various sub tables, but as they are not central to the task, they are left as one

## Questionable elements

* My usage of SQLAlchemy is probably unoptimized, we are probably fetching way too much data to do the checks.
* A lot of logic is still done at the View level in app.js. If the application was meant to be a bit more complex, this would be moved to an in-between layer.