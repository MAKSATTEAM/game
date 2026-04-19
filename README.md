# 🐞 Mia's Bug Garden Adventure
### 8-Bit Terminal Game — Pet Project by Mia & Papa

```
 ____  _   _  ____      ___   ____  ____  ____  _   _
|  _ \| | | |/ ___|    / _ \ |  _ \|  _ \| ___|| \ | |
| |_) | | | | |  _    / /_\ \| |_) | | | |  _|  \  | |
|  _ <| |_| | |_| |  /  ___  \  _ <| |_| | |___ |  \ |
|_| \_\\___/ \____|  /_/     \_\___/|____/|_____||_| \_|
         * M A G I C   G A R D E N *
```

---

## 🌸 The Story

Little ladybug **Mia** woke up one morning and discovered all her friends had disappeared!

- 🐝 **Bee Buzzy** is lost in the Sunny Meadow
- 🦋 **Butterfly Bella** flew into the Flower Garden
- 🦗 **Cricket Charlie** is hiding in the Evening Garden

Help Mia find all three friends and bring them home!

---

## 🎮 How to Play

### Start the game
```bash
python3 bug_adventure.py
```

### Controls
| Key | Action |
|-----|--------|
| ⬆️ Arrow Up | Move up |
| ⬇️ Arrow Down | Move down |
| ⬅️ Arrow Left | Move left |
| ➡️ Arrow Right | Move right |
| `ENTER` | Confirm / Next screen |
| `Q` | Quit |

### Map symbols
| Symbol | Meaning |
|--------|---------|
| `@` | Mia the ladybug (you!) |
| `*` | Flower — collect for +10 points! |
| `#` | Hedge wall — can't walk through |
| `T` | Tree — can't walk through |
| `W` | Spider web — slows you down! |
| `B` | Bee Buzzy — find him! |
| `F` | Butterfly Bella — find her! |
| `C` | Cricket Charlie — find him! |

---

## 🏆 Levels

1. **Sunny Meadow** — Easy. Find Bee Buzzy!
2. **Flower Garden** — Medium. Find Butterfly Bella!
3. **Evening Garden** — Hard. Find Cricket Charlie!

---

## 📋 Requirements

- Python 3.6 or newer
- Works on: Linux, macOS, Windows (via WSL or Windows Terminal)
- No extra packages needed — uses Python's built-in `curses` library

---

## 🛠️ Project structure

```
bug-garden/
├── bug_adventure.py    ← The whole game (one file!)
└── README.md           ← This file
```

---

## 💡 Ideas for future updates

Mia can request new features by typing them here! Ideas so far:

- [ ] Add more levels
- [ ] Add a spider enemy that moves!
- [ ] Add sound effects (terminal beeps)
- [ ] Add a high score table
- [ ] Add a map editor so Mia can design her own levels
- [ ] Add a day/night cycle

---

*Made with ❤️ by Mia & Papa*
