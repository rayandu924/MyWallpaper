import unittest
from unittest.mock import Mock
from watchdog.events import FileModifiedEvent
from src.file_system_handler import FileSystemHandler
from src.file_manager import ConfigManager
from src.hash_manager import HashManager

class TestFileSystemHandler(unittest.TestCase):
    def setUp(self):
        # Set up mock config and hash managers
        self.config_manager = Mock(spec=ConfigManager)
        self.hash_manager = Mock(spec=HashManager)
        self.hash_manager.list_items.return_value = ['item1', 'item2']
        self.reinjection_callback = Mock()
        self.handler = FileSystemHandler(self.config_manager, self.hash_manager, self.reinjection_callback)

    def test_on_modified_item(self):
        event = FileModifiedEvent("item1")
        self.handler.on_modified(event)
        self.reinjection_callback.assert_called()

    def test_on_modified_config(self):
        event = FileModifiedEvent(self.config_manager.config_file)
        self.handler.on_modified(event)
        self.reinjection_callback.assert_called()

if __name__ == "__main__":
    unittest.main()