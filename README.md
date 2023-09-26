# hexamind
AI game application

The program allows users to play against an artificial intelligence system to create edges between vertices in a graph with the main aim of avoiding the creation of a triangle. The AI player works by finding the best move to be made that would lessen the chances of creating a triangle in the future and would increase this chance for the other player based on the current state of the graph (minimax algorithm).

To run the code use command:
python3 main.py

Please ensure the networkx package is installed which can be done using the below command:
pip3 install networkx
