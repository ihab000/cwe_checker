import unittest
import cwe_checker_testlib


class TestCwe415(unittest.TestCase):

    def setUp(self):
        self.target = '415'
        self.string = b'Double Free'

    @unittest.skip("FIXME: broken on Ubuntu 18.04 with the corresponding gcc version")
    def test_cwe415_01_x64_gcc(self):
        expect_res = 9
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'x64', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    @unittest.skip("FIXME: broken on Ubuntu 18.04 with the corresponding clang version")
    def test_cwe415_01_x64_clang(self):
        expect_res = 9
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'x64', 'clang', self.string)
        self.assertEqual(res, expect_res)

    @unittest.skip("FIXME: yields different results on Ubuntu 16.04 and 18.04")
    def test_cwe415_01_x86_gcc(self):
        expect_res = 5
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'x86', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_x86_clang(self):
        expect_res = 5
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'x86', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_arm_gcc(self):
        expect_res = 5
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'arm', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_arm_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'arm', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_aarch64_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'aarch64', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_aarch64_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'aarch64', 'clang', self.string)
        self.assertEqual(res, expect_res)

    @unittest.skip("Depends on proper MIPS support in BAP")
    def test_cwe415_01_mips_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mips_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mipsel_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mipsel', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mipsel_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mipsel', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mips64_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips64', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mips64_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips64', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mips64el_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips64el', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_mips64el_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'mips64el', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_ppc_gcc(self):
        expect_res = 3
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'ppc', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_ppc64_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'ppc64', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_ppc64_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'ppc64', 'clang', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_ppc64le_gcc(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'ppc64le', 'gcc', self.string)
        self.assertEqual(res, expect_res)

    def test_cwe415_01_ppc64le_clang(self):
        expect_res = 1
        res = cwe_checker_testlib.execute_and_check_occurence(
            self.target, self.target, 'ppc64le', 'clang', self.string)
        self.assertEqual(res, expect_res)
