from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tweedle.util import archive, cliview, fs, sh


def test_shell_run(mocker):
    mocker.patch('tweedle.util.sh.run')
    sh.run('ls -l')
    sh.run.assert_called_once_with('ls -l')


def test_shell_to_args():
    expected = ['ls', '-l']
    result = sh.to_args('ls -l')
    assert result == expected


@pytest.mark.skip('Should have at least one assertion statement,but not')
def test_terminal_printx():
    from tweedle.util.clickx import Colors
    some_log = [('This is Red ', Colors.Magenta), ('This is Blue', Colors.Blue)]
    cliview.display(some_log)


def test_achieveutil():
    with TemporaryDirectory() as this_dir, TemporaryDirectory() as dest_dir:
        this_dir, dest_dir = Path(this_dir), Path(dest_dir)
        with sh.change_dir_temporarily_to(this_dir):
            basenames = "12345"
            for i in basenames:
                Path(f'{i}.txt').touch()

            new_test1 = archive.compress('test', 'zip', Path('1.txt'), this_dir)
            assert Path('test.zip').exists()
            archive.extract_all(new_test1, dest_dir)
            assert (dest_dir / '1.txt').exists()

            new_test2 = archive.compress('test2', 'zip', Path.cwd(), dest_dir)
            assert (dest_dir / 'test2.zip').exists()
            archive.extract_all(new_test2, this_dir)
            actual_extracted = {fs.strip_ext(str(path.name)) for path in this_dir.glob('*.txt')}

            expected = set(basenames)
            assert actual_extracted & expected
