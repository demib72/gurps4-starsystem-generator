import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace
import sys
import run

class TestRun(unittest.TestCase):
    @patch.dict(
        'sys.modules',
        {
            'stargen.utils.gifout': SimpleNamespace(render_system_gif=MagicMock()),
            'stargen.utils.mapmaker': SimpleNamespace(generate_world_map=MagicMock()),
        },
    )
    @patch('run.StarSystem')
    @patch('run.LatexWriter')
    @patch('run.generate_random_name', return_value='testname')
    def test_main(self, gen_name, LatexWriterMock, StarSystemMock):
        world = MagicMock()
        world.get_name.return_value = 'A4'
        world.get_type.return_value = 'Garden'
        world.get_hydrographic_cover.return_value = 30
        ps = MagicMock()
        ps.get_orbitcontents.return_value = {'a': world}
        star = MagicMock(planetsystem=ps)
        StarSystemMock.return_value.stars = [star]
        instance = StarSystemMock.return_value
        tex_instance = LatexWriterMock.return_value

        run.main()

        StarSystemMock.assert_called_once()
        LatexWriterMock.assert_called_once_with(instance, 'testname.tex')
        tex_instance.write.assert_called()
        sys.modules['stargen.utils.gifout'].render_system_gif.assert_called_once_with(instance, 'gifs/testname.gif')
        sys.modules['stargen.utils.mapmaker'].generate_world_map.assert_called_once_with('maps/testname_A4.png', 30)

if __name__ == '__main__':
    unittest.main()
