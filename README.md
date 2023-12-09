# Pacman_game
 
Jaysen Gomez- includes the following:
1.1 Scope
In its traditional form, Pacman has deterministic and predictable ghost behaviors. This project aims to enhance the Pacman game by introducing various algorithms for the ghosts' behaviors,
transforming it into an educational tool. Users can select from different algorithms, observing in
real time how each impacts ghost strategy and movement. This visualization will aid in
comprehending the underlying principles of these algorithms, using the familiar Pacman
environment as a dynamic canvas. Additionally, the project will develop an AI that can
autonomously play the game, offering another layer of understanding as users observe AI
strategies in navigating the maze and evading the ghosts.


2: Game parts. 
2.1 main.py file
The main.py file in the project serves as the entry point for the game. It is a script that gets executed to start the game, its primary role is to initialize and link together the major components of the game.

2.2 start.py
The start.py file in the Pacman project is primarily responsible for setting up and displaying the game's start screen, which includes the functionality for the player to select different algorithms that potentially influence the game's behavior. The player can choose between the following algorithms: Random, Breadth-first search, A*, Dijkstra’s, Greedy 
2.3 game.py
The game.py file in the Pacman project initializes the game environment. This includes the screen setup and character instantiation. The game loop function, game_loop, is central to this script, handling essential tasks like rendering graphics, capturing and processing user inputs, and updating game states. Within this loop, the movements of Pac-Man and the ghosts are managed, including their interactions, such as Pac-Man eating pellets and power-ups, and ghosts chasing Pac-Man. The script also takes care of drawing all game elements on the screen, including the maze and UI components like scores. It also includes logic for different game states. 
2.4 maze.py
The maze.py file primarily deals with the layout and representation of the maze. It simply defines the maze’s structure using a 2D array, where each element represents a specific type of tile, such as walls, paths, pellets, and power pellets. 
2.5 pacman.py
The pacman.py files specifically handles the implementation and mechanics of the pacman character. It includes the Pacman class which defines various attributes such as the score, lives, and powered-up states. This class also manages Pac-Man's movement within the game, responding to player inputs and interacting with the game environment (like eating pellets). The file is equipped with functionality for loading and managing Pac-Man's images, supporting animations to represent different actions and states (e.g., moving, eating, dying). Additionally, it handles collision detection, scoring mechanics, and life management.

2.5.1 pacman.py ai
In the AI design for Pac-Man, the system prioritizes evasion and strategic movement based on the positions of ghosts and the maze layout. Upon each move, the AI evaluates the nearest ghost's proximity, determining the primary escape direction. Simultaneously, it considers the last successful move and avoids reverse directions to prevent backtracking. The AI then selects from potential escape routes, balancing between continuing in a successful direction and changing course when blocked. If a ghost is deemed too close, the AI escalates evasion tactics, overriding other considerations. This approach ensures that Pac-Man moves intelligently, avoiding ghosts and navigating the maze efficiently, thereby enhancing gameplay dynamics and challenging the player's strategic planning skills.

2.6 ghosts.py
In the ghosts.py file each ghost character, derived from a base Ghost class, exhibits distinct behaviors using Pygame. Blinky, the red ghost, straightforwardly chases Pac-Man's current position. Pinky, the pink ghost, primarily targets a few tiles ahead of Pac-Man but switches to a scatter mode, moving between specific points when close to Pac-Man. Inky, the cyan ghost, calculates its target based on a reference point two tiles ahead of Pac-Man's current direction, without considering Blinky's position. Clyde, the orange ghost, combines chasing Pac-Man when far and scattering to a corner when close, with a behavior switch determined by a set tile distance. These behaviors are controlled by various pathfinding algorithms (A*, Dijkstra's, BFS, Greedy Best-First) and state changes, like frightened mode or scatter mode, influencing the ghosts' movement and targeting logic within the game's maze environment.





2.6.1
Random Search:

The ghost moves step by step towards the goal. At each step, it randomly shuffles the possible moves (up, down, left, right) and selects the first move that leads to a valid, non-blocked space in the maze. This process continues until the ghost reaches the goal or cannot find a valid move to proceed.


Greedy best-first search:

This algorithm utilizes a PriorityQueue to manage the exploration of nodes, prioritizing them based solely on a heuristic function that estimates the distance to the goal. Unlike A*, it does not account for the traveled distance to the current node, focusing only on the potential distance to the goal. The algorithm iterates through adjacent nodes, avoiding obstacles and previously visited nodes, and continuously updates the priority queue with these new nodes based on their heuristic values. If the goal is reached, it reconstructs the path from the goal to the start.

Breadth-First Search (BFS):

This algorithm employs a queue to systematically explore all possible paths from the start point, expanding outward in all directions. Each path is extended one step at a time, and if a step leads to the goal, the algorithm returns that path. BFS is known for its effectiveness in finding the shortest path in terms of the number of steps, as it explores all possible paths in a level-wise manner. The algorithm also keeps track of visited nodes to prevent revisiting and looping. If the goal is unreachable, the algorithm eventually exhausts all paths and returns an empty list, indicating that no path exists.

Dijkstra's Algorithm:

Starts with a start_node and iteratively explores its neighbors (or children), updating their distance from the start (tracked as g value). The algorithm uses two lists: open_list for nodes to be explored and closed_list for nodes already explored. The key step is selecting the node with the smallest g value from the open_list for exploration, which ensures that the algorithm always proceeds along the shortest known path to the next node. If a node is revisited, it updates the path if a shorter one is found. The process continues until the goal (end_node) is reached, and then it reconstructs the path from the goal back to the start. Unlike A*, Dijkstra's algorithm does not use a heuristic; it methodically explores all possible paths based on the actual shortest distance traveled from the start, making it highly effective for finding the shortest path in a graph with non-negative edge weights.
.

A Search:*

This heuristic-based algorithm efficiently finds the shortest path from a start node to a goal node by maintaining two lists: open and closed. Nodes are evaluated based on their 'f' score, calculated as the sum of the actual distance from the start node ('g') and the estimated distance to the goal node ('h'), using squared Euclidean distance as a heuristic. The algorithm continues to assess adjacent nodes, avoiding already evaluated or blocked paths, until it reaches the goal, effectively ensuring an optimal route in the game's maze.

