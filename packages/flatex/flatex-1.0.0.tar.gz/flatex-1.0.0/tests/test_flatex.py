import unittest
from flatex.main import parse_args, get_included_file_name


class TestParse(unittest.TestCase):
    def test_verbose(self):
        args = parse_args(["-v", "test.txt"])
        self.assertTrue(args.verbose)

        args = parse_args(["test.txt"])
        self.assertFalse(args.verbose)


class TestIncludedFileName(unittest.TestCase):
    def test_simple_case(self):
        res = get_included_file_name(r"\input{file}")
        self.assertEqual("file.tex", res)

        res = get_included_file_name(r"    \input{file}")
        self.assertEqual("file.tex", res)

        res = get_included_file_name(r"    \input{file} %comment")
        self.assertEqual("file.tex", res)

    def test_error_case(self):
        res = get_included_file_name(r"file")
        self.assertEqual("", res)


if __name__ == "__main__":
    unittest.main()
