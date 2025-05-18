# Assembly Simulator

A **browser-based assembly language simulator** that lets you write, assemble, and simulate code in real time. Built for learners, hobbyists, and educators to visualize low-level programming concepts — no installation required.

> Runs 100% in the browser using Pyodide and WebAssembly.

---

## Preview

![Assembly Simulator UI](https://github.com/user-attachments/assets/51fa78ad-7782-421b-b92f-e746bccefaa1)
*Modern UI with register and memory visualization.*

---

## Features

* **In-Browser IDE** – Write, assemble, and simulate assembly code without any setup
* **Live Execution** – Instant code feedback with memory and register state updates
* **Modern Interface** – Clean, responsive layout with light/dark mode toggle
* **Sample Programs** – Load examples to get started quickly
* **Retro CRT Output** – Terminal-style output panel for nostalgia lovers
* **Powered by Pyodide** – Python interpreter compiled to WebAssembly for seamless browser performance

---

## 🛠Built With

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge\&logo=tailwind-css\&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)
![Pyodide](https://img.shields.io/badge/Pyodide-3776AB?style=for-the-badge\&logo=python\&logoColor=white)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Sambhav-Gautam/assembly-simulator.git
cd assembly-simulator
```

### 2. Open in Browser

Open the `index.html` file in any modern browser — no server setup needed.

### 3. Or Use Online

Explore the live version:
🔗 [assembly-simulator on GitHub](https://github.com/Sambhav-Gautam/assembly-simulator)

---

## How to Use

1. **Write Code** in the left-hand editor panel
2. Click **"Assemble"** to compile your code
3. Click **"Simulate"** to run the program
4. Use **"Try Sample"** to explore predefined examples

---

## 🔧 Supported Instructions

| Instruction | Description            | Example        |
| ----------- | ---------------------- | -------------- |
| `mov`       | Move value             | `mov R0 $10`   |
| `add`       | Add registers          | `add R0 R1 R2` |
| `sub`       | Subtract registers     | `sub R0 R1 R2` |
| `ld`        | Load value from memory | `ld R0 x`      |
| `st`        | Store value to memory  | `st R0 x`      |
| `hlt`       | Halt execution         | `hlt`          |

> Additional instructions and syntax can be found within the app.

---

## UI Highlights

* **Dark/Light Mode** toggle
* **Animated Gradient Background**
* **Retro CRT Output Panel**
* **Visual State Feedback** for registers, memory, and program counter
* **Mobile-Friendly** responsive design

---

## Contributing

We welcome your contributions to improve the simulator!

1. **Fork** this repository
2. **Create a new branch**

   ```bash
   git checkout -b feature/my-feature
   ```
3. **Commit** your changes

   ```bash
   git commit -m "Add new feature"
   ```
4. **Push** to GitHub

   ```bash
   git push origin feature/my-feature
   ```
5. **Open a Pull Request** — clearly describe your changes

> **Found a bug or issue?**
> Feel free to open a pull request for bug fixes or submit an issue with detailed reproduction steps.

---

## License

This project is licensed under the **MIT License**.
See [`LICENSE`](./LICENSE) for full details.

---

## Contact

**Author:** Sambhav Gautam
**GitHub:** [@Sambhav-Gautam](https://github.com/Sambhav-Gautam)
**Project Repository:** [assembly-simulator](https://github.com/Sambhav-Gautam/assembly-simulator)
