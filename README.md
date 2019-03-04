Assignment 1: Grid World
=========

Your task is to implement the following search strategies in `methods.py`:

- BFS (2 points)
- Uniform Cost Search (4 points)
- A\* Search (6 points)

The code for DFS is given to make it easy for you to understand the code. (Expect to spend much more time on reading the code in future assignments.) 

The parts that you need to fill in are left blank as "pass". There are some hints here and there (you don't have to take them seriously). Do not make major changes to the other parts of the code, but you can add more auxiliary functions. 

In class I briefly explained the meaning of the different colors of the nodes -- check podcast and read the code to figure things out. 

Due date
-----
Jan-20 11pm Pacific Time.

Grading
-----
- Functionality (12 points)

The output should look like what the movie file shows (it shows what happens after pressing from 1 to 4 for the four different search methods). For UCS and AStar, always print (in the terminal) the final cost of the path that is found in the end.

- Documentation (2 points)

Write comments that make it easy for other people, which includes the version of yourself one week from now, to understand your code. In particular, fill in the lines with "#..." in the DFS code with your comments. 

Note
------
- You need to install the pygame library to make things work. I'm sure you can figure out how. The code is supposed to work for both Python2 and Python3, but it is possible (especially on mac) that pygame only works smoothly Python2. 
- On my mac, loading pygame for the first time can take quite some time, be patient and wait till the game is fully load. After that it should always load quickly. 
- You can click mouse to put down more puddles when search is not running.
