import unittest
import json
import os
from src.file_manager import ConfigManager
    
class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config_file = 'test_config.json'
        with open(self.config_file, 'w') as f:
            json.dump({"items": ["item1", "item2"]}, f)
        self.config_manager = ConfigManager(self.config_file)

    def tearDown(self):
        os.remove(self.config_file)

    def test_load_config(self):
        config = self.config_manager.load_config()
        self.assertEqual(config, ["item1", "item2"])

    def test_save_config(self):
        new_config = ["item3", "item4"]
        self.config_manager.save_config(new_config)
        with open(self.config_file, 'r') as f:
            data = json.load(f)
        self.assertEqual(data["items"], new_config)

if __name__ == "__main__":
    unittest.main()
