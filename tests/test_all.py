import pytest

from padelpy import from_sdf, from_smiles


def test_from_smiles():
    descriptors = from_smiles('CCC')
    assert len(descriptors) == 1875
    assert float(descriptors['MW']) == pytest.approx(44.0626, 1e-4)
    assert int(descriptors['nC']) == 3


def test_multiple_smiles():
    smiles = ['CCC', 'CCCC']
    descriptors = from_smiles(smiles)
    assert len(descriptors) == 2
    assert len(descriptors[0]) == 1875


def test_errors():
    bad_smiles = 'SJLDFGSJ'
    with pytest.raises(RuntimeError):
        _ = from_smiles(bad_smiles)
    bad_smiles = ['SJLDFGSJ', 'CCC']
    with pytest.raises(RuntimeError):
        _ = from_smiles(bad_smiles)


def test_from_sdf():
    descriptors = from_sdf('tests/aspirin_3d.sdf')[0]
    assert len(descriptors) == 1875
    assert float(descriptors['MW']) == pytest.approx(180.04225, 1e-4)
    assert float(descriptors['SsCH3']) == pytest.approx(1.2209, 1e-4)
    assert int(descriptors['nC']) == 9
