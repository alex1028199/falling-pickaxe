import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path to allow for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from youtube import validate_live_stream_id, get_live_streams, get_live_stream, get_live_chat_id, get_new_live_chat_messages, get_subscriber_count

class TestYouTube(unittest.TestCase):

    def test_validate_live_stream_id(self):
        self.assertEqual(validate_live_stream_id("https://www.youtube.com/watch?v=uvubgYqg9VQ"), "uvubgYqg9VQ")
        self.assertEqual(validate_live_stream_id("https://www.youtube.com/live/uvubgYqg9VQ?si=dfmI1IOGu4NRlxtM"), "uvubgYqg9VQ")
        self.assertEqual(validate_live_stream_id("https://youtu.be/uvubgYqg9VQ"), "uvubgYqg9VQ")
        self.assertEqual(validate_live_stream_id("uvubgYqg9VQ"), "uvubgYqg9VQ")
        self.assertIsNone(validate_live_stream_id("not_a_valid_id"))
        self.assertIsNone(validate_live_stream_id(None))
        self.assertIsNone(validate_live_stream_id(""))

    @patch('youtube.youtube')
    def test_get_live_streams(self, mock_youtube):
        mock_youtube.search().list().execute.return_value = {
            "items": [
                {"id": {"videoId": "video1"}, "snippet": {"title": "Title 1"}},
                {"id": {"videoId": "video2"}, "snippet": {"title": "Title 2"}},
            ]
        }
        streams = get_live_streams("channel_id")
        self.assertEqual(len(streams), 2)
        self.assertEqual(streams[0]['video_id'], "video1")

    @patch('youtube.youtube')
    def test_get_live_stream(self, mock_youtube):
        mock_youtube.videos().list().execute.return_value = {"items": ["stream1"]}
        stream = get_live_stream("livestream_id")
        self.assertEqual(stream, "stream1")

    @patch('youtube.youtube')
    def test_get_live_chat_id(self, mock_youtube):
        mock_youtube.videos().list().execute.return_value = {
            "items": [{"liveStreamingDetails": {"activeLiveChatId": "chat_id"}}]
        }
        chat_id = get_live_chat_id("live_stream_id")
        self.assertEqual(chat_id, "chat_id")

    @patch('youtube.youtube')
    def test_get_new_live_chat_messages(self, mock_youtube):
        mock_youtube.liveChatMessages().list().execute.return_value = {
            "items": [
                {
                    "id": "msg1",
                    "snippet": {"publishedAt": "2024-01-01T12:00:00Z", "displayMessage": "Hello"},
                    "authorDetails": {"displayName": "User1", "channelId": "user1_id", "profileImageUrl": "url1"}
                }
            ]
        }
        messages = get_new_live_chat_messages("chat_id")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]['author'], "User1")

    @patch('youtube.youtube')
    def test_get_subscriber_count(self, mock_youtube):
        mock_youtube.channels().list().execute.return_value = {
            "items": [{"statistics": {"subscriberCount": "123"}}]
        }
        count = get_subscriber_count("channel_id")
        self.assertEqual(count, 123)

if __name__ == '__main__':
    unittest.main()
