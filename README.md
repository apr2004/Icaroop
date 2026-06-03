# Icaroop

A Flappy Bird style game developed in Python using the Pygame library. In this game, players control Icarus, navigating him through a series of dynamically generated column obstacles. Can you keep him from flying too close to the sun or crashing into the sea?

## Key Features

* **Custom Physics & Movement:** Realistic gravity implementation, terminal velocity limits, and snappy jumps.
* **Dynamic Sprite Animations:** Multi-frame flapping animations controlled by a cooldown system, combined with real-time rotation based on vertical velocity.
* **Procedural Obstacle Generation:** Columns are dynamically built using separated base and body components, spawning at random heights while keeping a consistent gap.
* **Pixel-Perfect Collisions:** Utilizes `pygame.mask` instead of simple bounding boxes to calculate exact per-pixel collisions between Icarus and the columns.
* **Infinite Environment Scrolling:** Seamlessly repeating ground and ceiling layers that scroll automatically to simulate forward movement.
* **Custom UI & Typography:** Integrated a custom font (`Icarop.ttf`) to render the start screen, live score tracker, and game over overlays cleanly.

## Controls

* **Fly / Jump:** Press the **Spacebar** or **Left Mouse Click**.
* **Start / Restart:** Press the **Spacebar** or **Left Mouse Click** on the "PLAY" or "GAME OVER" screens.

## Requirements & Installation

1. Ensure you have **Python 3** installed on your system.
2. Clone this repository to your local machine.
3. Install the required dependency:
```bash
pip install pygame

```


4. Run the main game script:
```bash
python flappy_icarus.py

```



---

## To-Do List

* [ ] **Implement Scoring Logic:** Connect the obstacle clearance to the `score` variable so it increments dynamically when safely passing columns.
* [ ] **Repository Cleanup:** Remove the `discarded_classes/` directory and the unused `columns.py` script to keep the production codebase clean.
* [ ] **Audio Integration:** Add sound effects for jumping, scoring, and crashing, alongside a retro background music track.
* [ ] **High Score System:** Implement a local storage system (using a simple `.txt` or `.json` file) to save and display the player's all-time high score.
* [ ] **Dynamic Difficulty:** Gradually increase the `SCROLL_SPEED` or narrow the column gap as the player's score increases to make the game more challenging.