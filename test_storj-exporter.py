import json

import pytest
import responses

import storj_exporter

## Global varibles
STORJ_HOST = "192.168.1.10"
STORJ_PORT = 14002
API_RESPONSES_CONF = [
    {"uri": "/api/sno/", "response_file": "./test_files/sno.json"},
    {"uri": "/api/sno/satellite/118UWpMCHzs6CvSgWd9BfFVjw5K9pZbJjkfZJexMtSkmKxvvAW",
     "response_file": "./test_files/sno.satellite.118UWpMCHzs6CvSgWd9BfFVjw5K9pZbJjkfZJexMtSkmKxvvAW.json"},
    {"uri": "/api/sno/satellite/1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE",
     "response_file": "./test_files/sno.satellite.1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE.json"},
    {"uri": "/api/sno/satellite/121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6",
     "response_file": "./test_files/sno.satellite.121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6.json"},
    {"uri": "/api/sno/satellite/12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S",
     "response_file": "./test_files/sno.satellite.12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S.json"},
    {"uri": "/api/sno/satellite/12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs",
     "response_file": "./test_files/sno.satellite.12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs.json"},
    {"uri": "/api/sno/satellite/12rfG3sh9NCWiX3ivPjq2HtdLmbqCrvHVEzJubnzFzosMuawymB",
     "response_file": "./test_files/sno.satellite.12rfG3sh9NCWiX3ivPjq2HtdLmbqCrvHVEzJubnzFzosMuawymB.json"},
]


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


def mock_responses_ok(mocked_responses):
    base_url = f"http://{STORJ_HOST}:{STORJ_PORT}"
    for r in API_RESPONSES_CONF:
        with open(r["response_file"]) as f:
            response_json = json.load(f)
            mocked_responses.add(responses.GET, base_url + r["uri"], json=response_json)


# this test validate that requests mocking is working
def test_api(mocked_responses):
    mock_responses_ok(mocked_responses)
    api = storj_exporter.StorjApi(STORJ_HOST, STORJ_PORT)
    sno_data = api.get_sno_data()
    assert "nodeID" in sno_data, "sno_data Should be dict contains nodeID"
    assert sno_data["nodeID"] == "123456abc", "nodeID Should be 123456abc"
    assert len(sno_data["satellites"]) == 6, "Should have 6 satellites defined"
    for satellite in sno_data["satellites"]:
        satellite_data = api.get_satellite_data(satellite["id"])
        assert satellite_data["id"] == satellite["id"], "Should fetch satellite data"


def test_satellite_creation(mocked_responses):
    mock_responses_ok(mocked_responses)
    collector = storj_exporter.StorjCollector(STORJ_HOST, STORJ_PORT)
    sat = collector.get_or_create_satellite("118UWpMCHzs6CvSgWd9BfFVjw5K9pZbJjkfZJexMtSkmKxvvAW","satellite.stefan-benten.de:7777")
    assert sat.id == "118UWpMCHzs6CvSgWd9BfFVjw5K9pZbJjkfZJexMtSkmKxvvAW" , "Should get sat with correct id"
    assert sat.node_joined_at == "2019-09-01T08:59:04.123456Z" , "Should sat has joined at date 2019-09-01T08:59:04.123456Z"
    

