import json
import tempfile
import unittest
from pathlib import Path

from task_tracker import add_task, complete_task, delete_task, load_tasks


class TaskTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_task_assigns_id_and_persists(self):
        task = add_task(self.data_path, "  Learn SQL  ")
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Learn SQL")
        self.assertEqual(load_tasks(self.data_path), [task])

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            add_task(self.data_path, "   ")

    def test_complete_task(self):
        task = add_task(self.data_path, "Write tests")
        self.assertTrue(complete_task(self.data_path, task["id"]))
        self.assertTrue(load_tasks(self.data_path)[0]["done"])

    def test_missing_task_returns_false(self):
        self.assertFalse(complete_task(self.data_path, 999))
        self.assertFalse(delete_task(self.data_path, 999))

    def test_delete_task(self):
        task = add_task(self.data_path, "Temporary task")
        self.assertTrue(delete_task(self.data_path, task["id"]))
        self.assertEqual(load_tasks(self.data_path), [])


if __name__ == "__main__":
    unittest.main()
