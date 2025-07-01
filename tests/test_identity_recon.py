import requests
import json

BASE_URL = "http://localhost:8000/identify"

test_cases = [
    {
        "name": "Case 1: New Contact — Alice",
        "data": {"email": "alice@domain.com", "phoneNumber": "9991110001"},
        "expected": {
            "emails": ["alice@domain.com"],
            "phoneNumbers": ["9991110001"],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 2: Same Phone as Alice (phone only)",
        "data": {"email":"", "phoneNumber": "9991110001"},
        "expected": {
            "emails": ["alice@domain.com"],
            "phoneNumbers": ["9991110001"],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 3: New Email + Alice’s Phone — Bob",
        "data": {"email": "bob@domain.com", "phoneNumber": "9991110001"},
        "expected": {
            "emails": ["alice@domain.com", "bob@domain.com"],
            "phoneNumbers": ["9991110001"],
            "secondaryContactIds": [2]
        }
    },
    {
        "name": "Case 4: Bob again — same email, new phone",
        "data": {"email": "bob@domain.com", "phoneNumber": "9992223333"},
        "expected": {
            "emails": ["alice@domain.com", "bob@domain.com"],
            "phoneNumbers": ["9991110001", "9992223333"],
            "secondaryContactIds": [2, 3]
        }
    },
    {
        "name": "Case 5: Charlie — new contact",
        "data": {"email": "charlie@domain.com", "phoneNumber": "7777777777"},
        "expected": {
            "emails": ["charlie@domain.com"],
            "phoneNumbers": ["7777777777"],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 6: David — new contact",
        "data": {"email": "david@domain.com", "phoneNumber": "8888888888"},
        "expected": {
            "emails": ["david@domain.com"],
            "phoneNumbers": ["8888888888"],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 7: Merge Charlie + David",
        "data": {"email": "charlie@domain.com", "phoneNumber": "8888888888"},
        "expected": {
            "emails": ["charlie@domain.com", "david@domain.com"],
            "phoneNumbers": ["7777777777", "8888888888"],
            "secondaryContactIds": [6]
        }
    }
    # {
    #     "name": "Case 8: Invalid — No email or phone",
    #     "data": {},
    #     "expected_error": "At least one of email or phoneNumber must be provided."
    # }
]

def validate_response(actual, expected):
    def normalize(lst): return sorted(list(set(lst)))

    assert normalize(actual["emails"]) == normalize(expected["emails"]), f"Emails mismatch: {actual['emails']} != {expected['emails']}"
    assert normalize(actual["phoneNumbers"]) == normalize(expected["phoneNumbers"]), f"Phone numbers mismatch: {actual['phoneNumbers']} != {expected['phoneNumbers']}"

    if "secondaryContactIds" in expected:
        expected_count = len(expected["secondaryContactIds"])
        actual_count = len(actual["secondaryContactIds"])
        assert actual_count == expected_count, f"Expected {expected_count} secondary IDs, got {actual_count}"


def run_tests():
    for idx, case in enumerate(test_cases, start=1):
        print(f"\n🔹 Test {idx}: {case['name']}")
        response = requests.post(BASE_URL, json=case["data"])

        if "expected_error" in case:
            assert response.status_code == 422, f"Expected 422 error, got {response.status_code}"
            error_msg = response.json()["detail"][0]["msg"]
            assert case["expected_error"] in error_msg, f"Unexpected error message: {error_msg}"
            print("✅ Passed (Error case as expected)")
            continue

        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        res_json = response.json()
        assert "contact" in res_json, "Missing 'contact' key in response"
        validate_response(res_json["contact"], case["expected"])
        print("✅ Passed")

if __name__ == "__main__":
    run_tests()
