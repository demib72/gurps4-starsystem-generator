import unittest
from unittest.mock import patch, MagicMock
import run

class TestRun(unittest.TestCase):
    @patch('run.StarSystem')
    @patch('run.LatexWriter')
    @patch('run.generate_random_name', return_value='testname')
    def test_main(self, gen_name, LatexWriterMock, StarSystemMock):
        instance = StarSystemMock.return_value
        tex_instance = LatexWriterMock.return_value
        run.main()
        StarSystemMock.assert_called_once()
        LatexWriterMock.assert_called_once_with(instance, 'testname.tex')
        tex_instance.write.assert_called()

if __name__ == '__main__':
    unittest.main()
