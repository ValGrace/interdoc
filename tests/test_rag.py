import unittest
from unittest.mock import patch

from app import rag


class RagResponseTests(unittest.TestCase):
    def test_generate_response_uses_message_content_and_source_metadata(self):
        fake_response = type(
            'FakeResponse',
            (),
            {
                'choices': [
                    type('Choice', (), {'message': type('Message', (), {'content': 'hello'})()})
                ]
            }
        )()

        search_results = {
            'documents': [['chunk one']],
            'metadatas': [[{'source': 'doc.txt', 'chunk_index': 2}]],
        }

        with patch.object(rag.client.chat.completions, 'create', return_value=fake_response):
            result = rag.generate_response('what?', search_results)

        self.assertEqual(result['answer'], 'hello')
        self.assertEqual(result['sources'][0]['source'], 'doc.txt')
        self.assertEqual(result['sources'][0]['chunk_index'], 2)

    def test_generate_response_returns_fallback_when_groq_is_unavailable(self):
        search_results = {
            'documents': [['chunk one']],
            'metadatas': [[{'source': 'doc.txt', 'chunk_index': 0}]],
        }

        with patch.object(rag, 'client', None):
            result = rag.generate_response('what?', search_results)

        self.assertIn('GROQ_API_KEY', result['answer'])
        self.assertEqual(result['sources'][0]['source'], 'doc.txt')


if __name__ == '__main__':
    unittest.main()
