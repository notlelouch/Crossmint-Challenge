import requests
import time


class CrossmintAPI:
    def __init__(self, candidate_id):
        self.base_url = "https://challenge.crossmint.com/api"
        self.candidate_id = candidate_id

    def create_polyanet(self, row, column):
        url = f"{self.base_url}/polyanets"
        payload = {
            "candidateId": self.candidate_id,
            "row": row,
            "column": column
        }

        response = requests.post(url, json=payload)
        # Add delay to avoid rate limiting
        time.sleep(1)
        return response


def create_x_pattern(api):
    size = 11
    positions = []

    for i in range(2, 9):
        positions.append((i, i))
        positions.append((i, size - i - 1))

    # Create POLYanets
    for row, col in positions:
        print(f"Creating POLYanet at position ({row}, {col})")
        response = api.create_polyanet(row, col)

        if response.status_code == 200:
            print(f"Successfully created POLYanet at ({row}, {col})")
        else:
            print(f"Failed to create POLYanet at ({row}, {
                  col}). Status: {response.status_code}")
            print(f"Response: {response.text}")


def main():
    candidate_id = "6a1c24e3-d2d3-4936-bf58-a49c1eeec715"
    api = CrossmintAPI(candidate_id)

    create_x_pattern(api)


if __name__ == "__main__":
    main()
