import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
import sys
import run

class TestRun(unittest.TestCase):
    @patch.dict('sys.modules', {'stargen.utils.gifout': SimpleNamespace(render_system_gif=MagicMock())})
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
        sys.modules['stargen.utils.gifout'].render_system_gif.assert_called_once_with(instance, 'gifs/testname.gif')

if __name__ == '__main__':
    unittest.main()
