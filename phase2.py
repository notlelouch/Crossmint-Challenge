import requests
import time
from typing import List, Dict, Any


class CrossmintAPI:
    def __init__(self, candidate_id: str):
        self.base_url = "https://challenge.crossmint.com/api"
        self.candidate_id = candidate_id

    def _make_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        payload["candidateId"] = self.candidate_id

        response = requests.request(method, url, json=payload)
        # Adding delay to avoid rate limiting
        time.sleep(0.5)
        return response

    def get_goal_map(self) -> List[List[str]]:
        response = requests.get(
            f"{self.base_url}/map/{self.candidate_id}/goal")
        return response.json()["goal"]

    def create_polyanet(self, row: int, column: int) -> requests.Response:
        return self._make_request("POST", "polyanets", {
            "row": row,
            "column": column
        })

    def create_soloon(self, row: int, column: int, color: str) -> requests.Response:
        return self._make_request("POST", "soloons", {
            "row": row,
            "column": column,
            "color": color.lower()
        })

    def create_cometh(self, row: int, column: int, direction: str) -> requests.Response:
        return self._make_request("POST", "comeths", {
            "row": row,
            "column": column,
            "direction": direction.lower()
        })


class MegaverseBuilder:
    def __init__(self, api: CrossmintAPI):
        self.api = api

    def parse_cell(self, cell: str) -> Dict[str, str]:
        """Parse a cell from the goal map and return its type and attributes."""
        if cell == "SPACE":
            return {"type": "SPACE"}
        elif cell == "POLYANET":
            return {"type": "POLYANET"}
        elif "SOLOON" in cell:
            color = cell.split("_")[0].lower()
            return {"type": "SOLOON", "color": color}
        elif "COMETH" in cell:
            direction = cell.split("_")[0].lower()
            return {"type": "COMETH", "direction": direction}
        else:
            raise ValueError(f"Unknown cell type: {cell}")

    def create_object(self, row: int, column: int, cell_info: Dict[str, str]) -> None:
        """Create the appropriate astral object based on cell information."""
        obj_type = cell_info["type"]

        if obj_type == "SPACE":
            return

        try:
            if obj_type == "POLYANET":
                response = self.api.create_polyanet(row, column)
            elif obj_type == "SOLOON":
                response = self.api.create_soloon(
                    row, column, cell_info["color"])
            elif obj_type == "COMETH":
                response = self.api.create_cometh(
                    row, column, cell_info["direction"])

            if response.status_code == 200:
                print(f"Successfully created {obj_type} at ({row}, {column})")
            else:
                print(f"Failed to create {obj_type} at ({row}, {
                      column}). Status: {response.status_code}")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"Error creating {obj_type} at ({row}, {column}): {str(e)}")

    def build_megaverse(self) -> None:
        """Build the entire megaverse according to the goal map."""
        try:
            goal_map = self.api.get_goal_map()
            print("Successfully fetched goal map")

            for row in range(len(goal_map)):
                for col in range(len(goal_map[row])):
                    cell = goal_map[row][col]
                    cell_info = self.parse_cell(cell)
                    if cell_info["type"] != "SPACE":
                        self.create_object(row, col, cell_info)

        except Exception as e:
            print(f"Error building megaverse: {str(e)}")


def main():
    candidate_id = "6a1c24e3-d2d3-4936-bf58-a49c1eeec715"
    api = CrossmintAPI(candidate_id)
    builder = MegaverseBuilder(api)
    builder.build_megaverse()


if __name__ == "__main__":
    main()
