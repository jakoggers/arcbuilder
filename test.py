import json
from team_handler import team_handler
import time
"""error_list = ["a", "b", "c"]
with open("test.txt", 'w', encoding="utf-8") as test:
	if len(error_list) == 0:
		print("No empty cells!")
	else:
		for given_error in error_list:
			test.write(given_error)
		print(f"Wrote {len(error_list)} error(s).")"""

wat_time = time.time()
team_handler("https://pokepast.es/75f244f48321cd63", str(0))
print(f"Completed Write Time in {(time.time() - wat_time) / 60}")

# my team: https://pokepast.es/d4061070550b4255
# https://pokepast.es/24004544bf17ccfc