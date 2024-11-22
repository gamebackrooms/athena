from datetime import datetime
from .models import Room

class RoomService:
    @staticmethod
    def save_room(external_id: str, external_date_created: str):
        try:
            # Convert the external_date_created string to a datetime object
            external_date_created = datetime.strptime(external_date_created, "%Y-%m-%d %H:%M:%S")

            # Create a new Room instance
            room = Room(external_id=external_id, external_date_created=external_date_created)
            room.save()  # Save the instance to the database

            return room  # Return the saved room instance

        except Exception as e:
            raise ValueError(f"Error saving Room: {e}")
