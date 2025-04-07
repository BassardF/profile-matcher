from app import app, db
from models import Player, Item, Device, Clan
from datetime import datetime

PLAYER_ID = '97983be2-98b7-11e7-90cf-082e5f28d836'

def init_db():
    """Initialize the database and create tables"""
    db.create_all()

    # Check if sample data already exists
    if not Player.query.filter_by(player_id=PLAYER_ID).first():
        # Create sample clan
        clan = Clan(clan_id='123456', name='Hello world clan')
        db.session.add(clan)

        # Create sample player
        player = Player(
            player_id=PLAYER_ID,
            credential='apple_credential',
            created=datetime.strptime('2021-01-10 13:37:17Z', '%Y-%m-%d %H:%M:%SZ'),
            modified=datetime.strptime('2021-01-23 13:37:17Z', '%Y-%m-%d %H:%M:%SZ'),
            last_session=datetime.strptime('2021-01-23 13:37:17Z', '%Y-%m-%d %H:%M:%SZ'),
            total_spent=400,
            total_refund=0,
            total_transactions=5,
            last_purchase=datetime.strptime('2021-01-22 13:37:17Z', '%Y-%m-%d %H:%M:%SZ'),
            level=3,
            xp=1000,
            total_playtime=144,
            country='CA',
            language='fr',
            birthdate=datetime.strptime('2000-01-10 13:37:17Z', '%Y-%m-%d %H:%M:%SZ'),
            gender='male',
            custom_field='mycustom',
            clan=clan
        )
        db.session.add(player)
        db.session.flush()  # Flush to get the player ID

        # Create sample items
        items = [
            Item(key='cash', name='Cash', description='In-game cash'),
            Item(key='coins', name='Coins', description='In-game coins'),
            Item(key='item_1', name='Item 1', description='Sample item 1'),
            Item(key='item_34', name='Item 34', description='Sample item 34'),
            Item(key='item_55', name='Item 55', description='Sample item 55'),
        ]
        player.items.extend(items)

        # Create sample device
        device = Device(
            device_id=1,
            model='apple iphone 11',
            carrier='vodafone',
            firmware='123'
        )
        player.devices.append(device)

        # Commit all changes
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        init_db()
        print('Database successfully initialized with sample data.')