import unittest
from app.services.mcq_bank import get_all_mcqs, get_mcq_by_id

class TestMCQBank(unittest.TestCase):

    def test_mcq_retrieval(self):
        mcqs = get_all_mcqs()
        self.assertGreater(len(mcqs), 0)
        
        q = get_mcq_by_id(mcqs[0].id)
        self.assertEqual(q.id, mcqs[0].id)
        self.assertGreater(len(q.options), 0)

    def test_mcq_has_correct_options(self):
        mcqs = get_all_mcqs()
        for q in mcqs:
            correct_opts = [opt for opt in q.options if opt.is_correct]
            self.assertGreater(len(correct_opts), 0, f"MCQ {q.id} must have at least 1 correct option")

if __name__ == "__main__":
    unittest.main()
