"""The sector→keyword router that decides what the Jobs agent searches."""
from core.agents.jobs import _keyword
from core.types import WorkerProfile

P = WorkerProfile()


def test_caregiving_maps_to_caregiver():
    assert _keyword("Caregiving / Nursing care", P) == "caregiver"


def test_software_maps_to_engineer():
    assert _keyword("Software development", P) == "software engineer"


def test_unknown_sector_falls_back_to_first_token():
    assert _keyword("Basket weaving / artisan", P) == "basket weaving"


def test_empty_sector_falls_back_to_skilled_worker():
    assert _keyword("", P) == "skilled worker"
