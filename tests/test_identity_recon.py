import requests
import json
import random
import string

BASE_URL = ""
BASE_URL += "identify" if BASE_URL[-1] == "/" else "/identify"

NAME1 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
PHNO1 = ''.join(random.choices(string.digits, k=10))
NAME2 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
NAME3 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
NAME4 = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
PHNO2 = ''.join(random.choices(string.digits, k=10))
PHNO3 = ''.join(random.choices(string.digits, k=10))
PHNO4 = ''.join(random.choices(string.digits, k=10))

test_cases = [
    {
        "name": "Case 1: New Contact — Alice",
        "data": {"email": f"{NAME1}@domain.com", "phoneNumber": PHNO1},
        "expected": {
            "emails": [f"{NAME1}@domain.com"],
            "phoneNumbers": [PHNO1],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 2: Same Phone as Alice (phone only)",
        "data": {"email":"", "phoneNumber": PHNO1},
        "expected": {
            "emails": [f"{NAME1}@domain.com"],
            "phoneNumbers": [PHNO1],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 3: New Email + Alice’s Phone — Bob",
        "data": {"email": f"{NAME2}@domain.com", "phoneNumber": PHNO1},
        "expected": {
            "emails": [f"{NAME1}@domain.com", f"{NAME2}@domain.com"],
            "phoneNumbers": [PHNO1],
            "secondaryContactIds": [2]
        }
    },
    {
        "name": "Case 4: Bob again — same email, new phone",
        "data": {"email": f"{NAME2}@domain.com", "phoneNumber": PHNO2},
        "expected": {
            "emails": [f"{NAME1}@domain.com", f"{NAME2}@domain.com"],
            "phoneNumbers": [PHNO1, PHNO2],
            "secondaryContactIds": [2, 3]
        }
    },
    {
        "name": "Case 5: Charlie — new contact",
        "data": {"email": f"{NAME3}@domain.com", "phoneNumber": PHNO3},
        "expected": {
            "emails": [f"{NAME3}@domain.com"],
            "phoneNumbers": [PHNO3],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 6: David — new contact",
        "data": {"email": f"{NAME4}@domain.com", "phoneNumber": PHNO4},
        "expected": {
            "emails": [f"{NAME4}@domain.com"],
            "phoneNumbers": [PHNO4],
            "secondaryContactIds": []
        }
    },
    {
        "name": "Case 7: Merge Charlie + David",
        "data": {"email": f"{NAME3}@domain.com", "phoneNumber": PHNO4},
        "expected": {
            "emails": [f"{NAME3}@domain.com", f"{NAME4}@domain.com"],
            "phoneNumbers": [PHNO3, PHNO4],
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
