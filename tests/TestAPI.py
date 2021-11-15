import json
import pandas as pd
import unittest
import requests
import jsonschema
from jsonschema import validate


def validateJson(jsonData, jsonSchema):
    try:
        validate(instance=jsonData, schema=jsonSchema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True


class TestAPI(unittest.TestCase):
    content = pd.read_csv('../Data/content.csv')

    def test_RegisterLoginUser(self):
        """Checks the appropriate user creation and ability to log in by this user"""
        register_data = {'id': 6, 'name': 'test_API', 'is_admin': False, 'password': 'string'}
        requests.post('http://localhost:8000/user',
                      json=register_data)
        r = requests.get('http://localhost:8000/user', params={'login': 6, 'password': 'string'})
        get_data = r.json()
        self.assertEqual(register_data, get_data)

    def test_InsertGetWatchHistory(self):
        """Checks the API function of insertion and getting user Watch History"""
        insert_watch_history_data = {
            'history': [{'user_uid': 6, 'content_uid': 25329, 'name': 'Хоть раз в жизни', 'duration': 0.56,
                         'type': 'movie'}]}
        requests.post('http://localhost:8000/watch_history/6', json=insert_watch_history_data)
        r = requests.get('http://localhost:8000/watch_history/6')
        get_watch_history_data = r.json()
        self.assertEqual(insert_watch_history_data, get_watch_history_data)

    def test_GetContent(self):
        """Checks the appropriate information on selected content"""
        actual_content_data = self.content[self.content.content_uid == 25329].to_dict('records')
        r = requests.get('http://localhost:8000/content/25329')
        get_content_data = r.json()
        self.assertEqual(actual_content_data[0]['content_name'], get_content_data['name'])
        self.assertEqual(actual_content_data[0]['duration_seconds'], get_content_data['duration'])
        self.assertEqual(actual_content_data[0]['content_uid'], get_content_data['content_id'])
        self.assertEqual(actual_content_data[0]['genres'], get_content_data['genres'][0])

    def test_ValidateTypeRecommendationSchema(self):
        """Checks the valid view of json output for recommendation based on content type"""
        type_recommendation_schema = {
            "type": "object",
            "properties": {
                "serial_with_season": {
                    "type": "object"
                },
                "movie": {
                    "type": "object"
                }
            },
            "required": [
                "serial_with_season",
                "movie"
            ]
        }
        r = requests.get('http://localhost:8000/recommendation/type')
        get_recommendation_type_data = r.json()
        self.assertTrue(validateJson(get_recommendation_type_data, type_recommendation_schema))

    def test_ValidateGenreRecommendationSchema(self):
        """Checks the valid view of json output for recommendation based on content genre"""
        genre_recommendation_schema = {
            "type": "object",
            "properties": {
                "genres": {
                    "type": "array",
                },
                "content": {
                    "type": "array",
                    "items": [
                        {
                            "type": "object",
                            "properties": {
                                "content_id": {
                                    "type": "integer"
                                },
                                "name": {
                                    "type": "string"
                                },
                                "type": {
                                    "type": "string"
                                },
                                "serial_id": {
                                    "type": "integer"
                                },
                                "genres": {
                                    "type": "array",
                                    "items": {}
                                },
                                "duration": {
                                    "type": "integer"
                                }
                            },
                            "required": [
                                "content_id",
                                "name",
                                "type",
                                "serial_id",
                                "genres",
                                "duration"
                            ]
                        }
                    ]
                }
            },
            "required": [
                "genres",
                "content"
            ]
        }
        r = requests.get('http://localhost:8000/recommendation/genre', params={'user_id': 4})
        get_recommendation_genre_data = r.json()
        self.assertTrue(validateJson(genre_recommendation_schema, get_recommendation_genre_data))

    def test_ValidateHistoryRecommendationSchema(self):
        """Checks the valid view of json output based on user's watch history"""
        history_recommendation_schema = {
            "type": "array",
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        },
                        "type": {
                            "type": "string"
                        },
                        "serial_id": {
                            "type": "integer"
                        },
                        "genres": {
                            "type": "array",
                            "items": [
                                {
                                    "type": "string"
                                },
                                {
                                    "type": "string"
                                }
                            ]
                        },
                        "duration": {
                            "type": "integer"
                        }
                    },
                    "required": [
                        "content_id",
                        "name",
                        "type",
                        "serial_id",
                        "genres",
                        "duration"
                    ]
                }
            ]
        }
        r = requests.get('http://localhost:8000/recommendation/base', params={'user_id': 4})
        get_recommendation_history_data = r.json()
        self.assertTrue(validateJson(get_recommendation_history_data, history_recommendation_schema))
