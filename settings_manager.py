import unittest

import file_manager


def set_default(guild_id: str) -> None:
    settings_dict = file_manager.load('json/settings.json')
    settings_dict[guild_id] = {
        "Adapt profile picture": "On"
    }
    file_manager.save('json/settings.json', settings_dict)


def remove_settings(guild_id: str) -> None:
    settings_dict = file_manager.load('json/settings.json')
    del settings_dict[guild_id]


def in_settings(guild_id: str) -> bool:
    settings_dict = file_manager.load('json/settings.json')
    return guild_id in settings_dict


def fetch_setting(guild_id: str, setting: str) -> str:
    settings_dict = file_manager.load('json/settings.json')
    return settings_dict[guild_id][setting]


def change_setting(guild_id: str, setting: str, new_setting: str) -> None:
    settings_dict = file_manager.load('json/settings.json')
    settings_dict[guild_id][setting] = new_setting
    file_manager.save('json/settings.json', settings_dict)


# UNITTESTS
class TestSettingsManager(unittest.TestCase):

    def test_set_default(self):
        # resetting the file
        file_manager.save('json/settings.json', {})
        self.assertEqual(
            file_manager.load('json/settings.json'),
            {}
        )
        set_default('1007966523')
        test_dict = file_manager.load('json/settings.json')
        self.assertEqual(
            test_dict,
            {
                '1007966523': {
                    'Adapt profile picture': 'Yes'
                }
            }
        )
        set_default('9000000')
        test_dict = file_manager.load('json/settings.json')
        self.assertEqual(
            test_dict,
            {
                '1007966523': {
                    'Adapt profile picture': 'Yes'
                },
                '9000000': {
                    'Adapt profile picture': 'Yes'
                }
            }
        )

    def test_change_settings(self):
        self.test_set_default()
        change_setting('1007966523', 'Adapt profile picture', 'No')
        test_dict = file_manager.load('json/settings.json')
        self.assertEqual(
            test_dict,
            {
                '1007966523': {
                    'Adapt profile picture': 'No'
                },
                '9000000': {
                    'Adapt profile picture': 'Yes'
                }
            }
        )

    def test_fetch_setting(self):
        self.test_change_settings()
        self.assertEqual(
            fetch_setting('1007966523', 'Adapt profile picture'),
            'No'
        )
        self.assertEqual(
            fetch_setting('9000000', 'Adapt profile picture'),
            'Yes'
        )


if __name__ == '__main__':
    unittest.main()
