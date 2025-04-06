# High level choices

* Pretty small service -> Flask
* RDB but easy to use -> SQLite
* ORM to avoid hand made SQL -> SQLAlchemy
* JSON serialization for the fun (overkill here) -> Marshmallow

## DB

![DB Schema](https://i.ibb.co/ZRgFkQfC/Screenshot-2025-04-05-at-1-38-39-PM.png)

* The DB model for Campaigns has been made simple (name only) to respect the rule, but doesn't match the shape of the one mocked (unusual)
* Devices should clearly be split in various sub tables, but as they are not central to the task, they are left as one