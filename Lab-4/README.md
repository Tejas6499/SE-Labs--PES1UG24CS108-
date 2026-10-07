# Lab 4 - VibeCoding

- Name: B V TEJAS
- SRN: PES1UG24CS108
- Section: B

## Links

- Assigned repository: https://github.com/SETAPESU26/41_fruit-ninja
- Updated code (my fork, one commit per task): https://github.com/Tejas6499/41_fruit-ninja
- LLM chat history: https://claude.ai/share/de226c97-b7b7-4bd0-80b1-868cdf862069

## Tasks

| Task | Change | Commit |
| --- | --- | --- |
| 1 | Slice detection tests the line segment between the previous and current mouse positions, so fast swipes register. | Task 1: fix slice detection for fast swipes |
| 2 | On-screen game-over screen with the final score replaces the console print. Slicing stops once the game is over. | Task 2: add on-screen game-over screen |
| 3 | From the game-over screen, E / M / H restarts on Easy / Medium / Hard and Q quits. | Task 3: add replay with Easy/Medium/Hard and quit |
| 4 | Sound effects for slicing a fruit, slicing a bomb and game over, generated in code. The game runs silently if no audio device is available. | Task 4: add generated sound effects |

## Files in this folder

- `before.mp4` - the original game: fast swipes pass through fruit and there is no game-over screen.
- `after.mp4` - the updated game: fast swipes slice, game-over screen, restart on Hard.
- `chat_history.pdf` - the LLM chat used for the four tasks.
- `Lab4_PES1UG24CS108_B.pdf` - submission document with the deliverables and prompts.
- `main.py`, `requirements.txt`, `game/` - the updated code.

## Running the game

```
pip install -r requirements.txt
python main.py
```
