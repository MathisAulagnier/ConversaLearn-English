import unittest
from srcLLM.com2LLM_Offline import loadModel, question_answer

class TestCom2LLM(unittest.TestCase):
    def test_loadModel(self):
        model = loadModel()
        self.assertIsNotNone(model)

    def test_question_answer(self):
        model = loadModel()
        prompt = "What is the capital of Paris?"
        response = question_answer(prompt, model)
        self.assertEqual("Paris" in response, True)
        

if __name__ == '__main__':
    unittest.main()