import sys, io
import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        fake_out = io.StringIO()
        print_orig = sys.stdout
        with Redirect(stdout=fake_out):
            print("test stdout")
            self.assertIs(sys.stdout, fake_out)
        self.assertIs(sys.stdout, print_orig)
        self.assertEqual(fake_out.getvalue(), "test stdout\n")

    def test_redirect_stderr(self):
        fake_err = io.StringIO()
        err_orig = sys.stderr
        with Redirect(stderr=fake_err):
            sys.stderr.write("error msg\n")
            self.assertIs(sys.stderr, fake_err)
        self.assertIs(sys.stderr, err_orig)
        self.assertEqual(fake_err.getvalue(), "error msg\n")

    def test_redirect_both(self):
        fake_out = io.StringIO()
        fake_err = io.StringIO()
        out_orig = sys.stdout
        err_orig = sys.stderr
        with Redirect(stdout=fake_out, stderr=fake_err):
            print("out msg")
            sys.stderr.write("err msg\n")
            self.assertIs(sys.stdout, fake_out)
            self.assertIs(sys.stderr, fake_err)
        self.assertIs(sys.stdout, out_orig)
        self.assertIs(sys.stderr, err_orig)
        self.assertEqual(fake_out.getvalue(), "out msg\n")
        self.assertEqual(fake_err.getvalue(), "err msg\n")

    def test_no_redirect(self):
        # Если не переданы ни stdout, ни stderr, ничего не меняется
        out_orig = sys.stdout
        err_orig = sys.stderr
        with Redirect():
            self.assertIs(sys.stdout, out_orig)
            self.assertIs(sys.stderr, err_orig)
        self.assertIs(sys.stdout, out_orig)
        self.assertIs(sys.stderr, err_orig)

    def test_nested_redirects(self):
        fake_out1 = io.StringIO()
        fake_out2 = io.StringIO()
        out_orig = sys.stdout
        with Redirect(stdout=fake_out1):
            print("level 1")
            with Redirect(stdout=fake_out2):
                print("level 2")
                self.assertIs(sys.stdout, fake_out2)
            # после вложенного контекста должен восстановиться fake_out1
            self.assertIs(sys.stdout, fake_out1)
        self.assertIs(sys.stdout, out_orig)
        self.assertEqual(fake_out1.getvalue(), "level 1\n")
        self.assertEqual(fake_out2.getvalue(), "level 2\n")




if __name__ == '__main__':
    #unittest.main()
    with open('test_results.txt', 'w') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner, exit=False)
