import unittest
from typing import List

import file_manager
import settings_manager


def add_default(guild_id: str) -> None:
    settings_manager.set_default(guild_id)


def remove_settings(guild_id: str) -> bool:
    if not settings_manager.in_settings(guild_id):
        return True
    settings_manager.remove_settings(guild_id)
    return False


def in_settings(guild_id: str) -> bool:
    return settings_manager.in_settings(guild_id)


def change_setting_controller(guild_id: str, setting: str, new_setting: str) \
        -> bool:
    if new_setting == settings_manager.fetch_setting(guild_id, setting):
        return False
    settings_manager.change_setting(guild_id, setting, new_setting)
    return True


def fetch_setting(guild_id: str, setting: str) -> str:
    return settings_manager.fetch_setting(guild_id, setting)


def get_all_setting_options(setting: str) -> List[str]:
    all_settings = file_manager.load('json/allSettings.json')
    return all_settings[setting]


def get_all_settings() -> List[str]:
    all_settings = file_manager.load('json/allSettings.json')
    return list(all_settings.keys())


# UNITTESTS
class TestSettingsManager(unittest.TestCase):

    def test_set_default(self):
        # resetting the file
        file_manager.save('json/settings.json', {})
        self.assertEqual(
            file_manager.load('json/settings.json'),
            {}
        )
        settings_manager.set_default('1007966523')
        test_dict = file_manager.load('json/settings.json')
        self.assertEqual(
            test_dict,
            {
                '1007966523': {
                    'Adapt profile picture': 'Yes'
                }
            }
        )
        self.assertFalse(change_setting_controller('1007966523',
                                                   'Adapt profile picture',
                                                   'Yes'))
        self.assertTrue(change_setting_controller('1007966523',
                                                  'Adapt profile picture',
                                                  'No'))
        test_dict_2 = file_manager.load('json/settings.json')
        self.assertEqual(
            test_dict_2,
            {
                '1007966523': {
                    'Adapt profile picture': 'No'
                }
            }
        )

    def test_get_all_settings(self):
        file_manager.save('json/allSettings.json', {})
        self.assertEqual(
            file_manager.load('json/allSettings.json'),
            {}
        )
        file_manager.save(
            'json/allSettings.json',
            {
                "Adapt profile picture": ["Yes", "No"]
            }
        )
        all_settings = get_all_settings()
        self.assertEqual(all_settings, ["Adapt profile picture"])

    def test_get_all_setting_options(self):
        self.test_get_all_settings()
        self.assertEqual(get_all_setting_options('Adapt profile picture'),
                         ["Yes", "No"])


if __name__ == '__main__':
    unittest.main()
