from datetime import datetime
from .models import Room
#from .models import Memory


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
        
'''
class MemoryService:
    @staticmethod
    def create_memory(data):
        """
        Create a new Memory instance.
        :param data: Dictionary containing memory details.
        :return: Created Memory instance.
        """
        return Memory.objects.create(**data)

    @staticmethod
    def get_memory_by_id(memory_id):
        """
        Retrieve a Memory instance by ID.
        :param memory_id: Memory ID.
        :return: Memory instance or None.
        """
        try:
            return Memory.objects.get(id=memory_id)
        except Memory.DoesNotExist:
            return None

    @staticmethod
    def update_memory(memory_id, data):
        """
        Update a Memory instance.
        :param memory_id: Memory ID.
        :param data: Dictionary of updated fields.
        :return: Updated Memory instance or None.
        """
        memory = MemoryService.get_memory_by_id(memory_id)
        if memory:
            for field, value in data.items():
                setattr(memory, field, value)
            memory.save()
            return memory
        return None

    @staticmethod
    def delete_memory(memory_id):
        """
        Delete a Memory instance.
        :param memory_id: Memory ID.
        """
        memory = MemoryService.get_memory_by_id(memory_id)
        if memory:
            memory.delete()
            return True
        return False
'''