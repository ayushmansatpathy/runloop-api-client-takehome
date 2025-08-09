# Runloop API Client Takehome Assignment

Thank you for taking the time to take this assessment. This is intended to test how quickly you can learn a new framework, your understanding of Runloop/container primitives, and finally give you a sense of what work might look like when using our product. 

You objective is to complete as many of the following tasks, as correctly as possible. Task #3 is an extension and it directly mirrors what everyday work onboarding benchmarks will feel like.

We will grade this assignment for completion > code quality and organization = speed (based on final commit timestamp). You will be contacted at your email for any follow-up actions.

## Setup
Sign-up @ [platform.runloop.pro](https://platform.runloop.pro) & [with your google/github using test card numbers](https://stripe.com/docs/testing#cards). If using email, you do not need to verify your email. Generate an api key for this project.

SDK setup (Pointing to our development servers)
```python
from runloop_api_client import Runloop

client = Runloop(base_url="https://api.runloop.pro", bearer_token=os.environ.get("RUNLOOP_API_KEY"))
```

```typescript
import { Runloop } from "@runloop/api-client";

const client = new Runloop({
  bearerToken: process.env.RUNLOOP_API_KEY,
  baseURL: "https://api.runloop.pro",
});
```

## Tasks

For each task, make a separate script that completes the stated task. Organize your project however you wish, but please keep in mind standard software engineering convention and best practices.

### 1.a Create Devbox
- Use Runloop SDK (Python or TypeScript) to create a devbox
    - https://github.com/runloopai/runloop-examples
- Name it your email address
- Record `api-key`, `devbox-name`, and `devbox-id` in `answers.json`

### 1.b Operations on the devbox
- Copy the provided `resources` folder into the new devbox
- Edit `me.txt` and replace the email with your own
- Execute either `test.js` or `test.py` on the devbox

### 1.c Create snapshot
- Snapshot your devbox after step 2
- Record `snapshot-id` in `answers.json`

### 2. Create blueprint
- Make a blueprint
  - Install `cowsay` in the blueprint
  - Create and save `blueprint-name` and `blueprint-id` to `answers.json`
  - Boot a devbox from the created blueprint and save a screenshot of `cowsay` running
  - Commit the screenshot as `blueprint.png`
  - Record `blueprint-name` and `blueprint-id` in `answers.json`
  
### 3. Extension - Create a Custom Scenario
- Make a scenario with a custom scorer that checks for the presence of `resources`
  - Copy scenario folder `resources` to devbox
  - Custom Scorer (Can be any type they want)
    - returns 1 if folder and files exist
    - returns 0 if not
  - Run scenario, creating a scenario run
  - Execute the script from step 1.b to load edit `me.txt` and one of the test scripts
  - Score and complete the scenario run
  - Record `ext-scenario-run-id` in `answers.json`

## Code Requirements
- Repository structure after assignment completion:

```
├── devbox.py (or .ts) #1
├── blueprint.py (or .ts) #2
├── blueprint.png (or jpeg) #2
├── scenario.py (or .ts) #2
├── resources/
├──── me.txt
├──── test.js
├──── test.py
├── answers.json
├── language setup for python or typescript
└── README.md
```

## answers.json Format
Do not change the format of this file. We will use this to score your submission.

```json
{
  "api-key": "YOUR_RUNLOOP_API_KEY",
  "devbox-name": "YOUR_DEVBOX_NAME",
  "devbox-id": "YOUR_DEVBOX_ID",
  "snapshot-id": "YOUR_SNAPSHOT_ID",
  "blueprint-name": "YOUR_BLUEPRINT_NAME",
  "blueprint-id": "YOUR_BLUEPRINT_ID",
  "devbox-from-blueprint-id": "YOUR_BLUEPRINT_DEVBOX_ID", 
  "devbox-from-blueprint-name": "YOUR_BLUEPRINT_DEVBOX_NAME",
  "ext-scenario-run-id": "YOUR_SCENARIO_RUN_ID"
}
```