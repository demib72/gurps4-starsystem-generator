import unittest
from unittest.mock import patch, MagicMock
import json
from types import SimpleNamespace
import sys

# Provide stub modules to avoid heavy optional dependencies during import
sys.modules.setdefault('stargen.utils.gifout', SimpleNamespace(render_system_gif=MagicMock()))
sys.modules.setdefault('stargen.utils.mapmaker', SimpleNamespace(generate_world_map=MagicMock()))

import run

class TestRun(unittest.TestCase):
    @patch('run.StarSystem')
    @patch('run.DokuwikiWriter')
    @patch('run.LatexWriter')
    @patch('run.generate_random_name', return_value='testname')
    @patch('builtins.input', side_effect=['y', 'y'])
    def test_main_latex(self, input_mock, gen_name, LatexWriterMock, DokuwikiMock, StarSystemMock):
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

    @patch('run.StarSystem')
    @patch('run.DokuwikiWriter')
    @patch('run.LatexWriter')
    @patch('run.generate_random_name', return_value='testname')
    @patch('builtins.input', side_effect=['n', 'n'])
    def test_main_dokuwiki(self, input_mock, gen_name, LatexWriterMock, DokuwikiMock, StarSystemMock):
        world = MagicMock()
        world.get_name.return_value = 'A4'
        world.get_type.return_value = 'Garden'
        world.get_hydrographic_cover.return_value = 30
        ps = MagicMock()
        ps.get_orbitcontents.return_value = {'a': world}
        star = MagicMock(planetsystem=ps)
        StarSystemMock.return_value.stars = [star]
        instance = StarSystemMock.return_value
        wiki_instance = DokuwikiMock.return_value

        run.main(['--format', 'dokuwiki'])

        StarSystemMock.assert_called_once()
        DokuwikiMock.assert_called_once_with(instance, 'testname.txt')
        wiki_instance.write.assert_called()

    @patch('run.StarSystem')
    @patch('run.DokuwikiWriter')
    @patch('run.LatexWriter')
    @patch('run.generate_random_name', return_value='testname')
    @patch('builtins.input', side_effect=['n', 'n'])
    def test_main_json(self, input_mock, gen_name, LatexWriterMock, DokuwikiMock, StarSystemMock):
        star_system = StarSystemMock.return_value
        star_system.stars = []
        star_system.get_age.return_value = 1
        star_system.is_open_cluster.return_value = False
        star_system.get_orbits.return_value = []
        star_system.get_period.return_value = []

        run.main(['--json', 'out.json'])

        StarSystemMock.assert_called_once()
        with open('out.json') as f:
            data = json.load(f)
        self.assertIn('stars', data)

if __name__ == '__main__':
    unittest.main()
