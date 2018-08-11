from __future__ import print_function
import requests


EXPECTED_COUNTS = {
    "Expedia": 1199,
    "Orbitz": 300,
    "Priceline": 600,
    "Travelocity": 400,
    "United": 1799,
}


def test_flight_search():
    resp = requests.get("http://localhost:8000/flights/search")
    results = resp.json()["results"]

    provider_counts = {}
    for provider in EXPECTED_COUNTS.keys():
        provider = provider.lower()
        for result in results:
            if result["provider"] == provider:
                provider_counts[provider] += 1
        if len(provider_counts) < 1:
            print("WARNING: Results do not include {}".format(provider))

    for provider, count in provider_counts:
        expected = EXPECTED_COUNTS[provider]
        assert count == expected, "{} results incomplete for {}".format(
            expected - count,
            provider,
        )

    sorted_results = sorted(results, key=lambda r: r["agony"])
    assert results == sorted_results, "Results aren't sorted properly!"

    took = resp.elapsed.total_seconds()

    msg = "Took %.2f seconds." % took
    if took > 3:
        msg += " Kinda slow..."
    else:
        msg += " Looks good!"

    print(msg)


if __name__ == "__main__":
    test_flight_search()
