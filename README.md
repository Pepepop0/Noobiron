# NoobIron

NoobIron is an online dashboard designed for balancing matches between friends in the Company of Heroes game.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)

## Features

- **Player Management:** Easily visualize, edit, and create player profiles. The dashboard connects to an SQL database, facilitating management of registered players.
  <p align="center">
  <img src="assets\git\Print_Edição.png" alt="Edition Page">
  </p>
- **Match Generation:** Assign players to matches ranging from 1v1 to 4v4. The dashboard balances matches by considering the skill levels of registered players.
  <p align="center">
  <img src="assets\git\Print_Geração de Partida.png" alt="Generation Page">
  </p>

## Getting Started
To begin using NoobIron, follow these steps:

1. **Download and Install MySQL and SQL Workbench:** Ensure you have MySQL and SQL Workbench installed on your system.
2. **Database Setup:** Create a database using the provided .SQL script located in "db_setup\create_schema.sql".
3. **Clone or Download the Repository:** Obtain the source code by cloning the repository or downloading it directly.
4. **Install Dependencies:** Execute `pip install -r requirements.txt` to install all necessary dependencies.
5. **Run the Dashboard:** Launch the dashboard by running `streamlit run home.py` in your terminal or command prompt.

