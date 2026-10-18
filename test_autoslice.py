import unittest
from autoslice import candidates, align, metrics
import tempfile
from pathlib import Path
class PlannerTests(unittest.TestCase):
    def test_matrix(self):
        for nozzle in (.2,.25,.4,.6,.8):
            machine={'nozzle_diameter':[str(nozzle)],'min_layer_height':[str(nozzle*.1)],'max_layer_height':[str(nozzle*.8)]}
            for purpose in ('everyday','finish','strong','draft'):
                result=candidates(machine,{}, {'filament_max_volumetric_speed':['12']},(40,40,50),purpose)
                for mode,trials in result['modes'].items():
                    self.assertLessEqual(len(trials),3)
                    self.assertTrue(trials)
                    for trial in trials:
                        self.assertLessEqual(trial['height']*trial['infill_every'],nozzle*.8+1e-8)
                        self.assertGreaterEqual(float(trial['process']['wall_loops']),2)
    def test_grid(self):
        self.assertAlmostEqual(align(.32,.08,.64,.001875),.31875)
        self.assertAlmostEqual(align(.32,.08,.64,0),.32)
    def test_reject_multi(self):
        with self.assertRaises(ValueError): candidates({'nozzle_diameter':['.4','.6']},{},{},(1,1,1))
    def test_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample.gcode';p.write_text('; estimated printing time (normal mode) = 1h 2m 3s\n;LAYER_CHANGE\n;LAYER_CHANGE\n')
            self.assertEqual(metrics(p)['seconds'],3723)
            self.assertEqual(metrics(p)['total_layers'],2)
if __name__=='__main__':unittest.main()
