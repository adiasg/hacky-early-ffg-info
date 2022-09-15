Get to know about Ethereum finality faster!

## Prerequisites

Lighthouse with HTTP endpoint enabled. 

## Installation

Clone the repo. Venv if you want. Then `pip install httpx`.

## Usage

- Fill in your Lighthouse HTTP endpoint in `LIGHTHOUSE_API_ENDPOINT` in the file `monitor-unrealized-checkpoints.py`.
- Then `python monitor-unrealized-checkpoints.py`.

The script queries the consensus client every 6 seconds, and outputs in the terminal like this:

![image](https://user-images.githubusercontent.com/25324105/190313363-e5b9b5fe-e0b9-4f60-a022-8c2193129a8e.png)

Explanation of output:
- The first 2 lines give information about current time, slot, slot in epoch, epoch etc.
- The next 2 lines provide information about realized (R) and unrealized (U) checkpoints. Unrealized checkpoints are expected to lead the realized ones by 1 epoch in the 22nd slot of every epoch.
- The next 3 JSON objects are:
  - Current FFG checkpoints
  - Lowest block that contains the unrealized justified checkpoint
  - Lowest block that contains the unrealized finalized checkpoint
  
Enjoy!
