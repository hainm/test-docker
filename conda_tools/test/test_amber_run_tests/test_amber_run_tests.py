import sys

sys.path.append('../../')
import amber_run_tests as ar


def test_get_tests_from_test_name():
    assert ar.get_tests_from_test_name('test.serial', 'Makefile.amber') == \
            ['test.serial.MM', 'test.serial.QMMM',
             'test.serial.sander.SEBOMD',
             'test.serial.emil', 'test.serial.sanderapi']
