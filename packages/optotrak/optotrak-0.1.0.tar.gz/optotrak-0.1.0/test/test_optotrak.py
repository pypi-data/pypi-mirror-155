from pathlib import Path

from numpy.testing import assert_array_equal

from optotrak import load_optotrak

TESTROOT = Path(__file__).parent


def test_load_optotrak():
    data = load_optotrak(TESTROOT / 'test_optotrak.tsv', delimiter='\t')
    assert_array_equal(data.loc[7, 'Beam2'],
                       [349.382965088, -561.469482422, -2551.994140625])
    assert data.attrs['Count'] == 10
    assert data.attrs['Frequency'] == 50.0
    assert data.attrs['Units'] == 'mm'
