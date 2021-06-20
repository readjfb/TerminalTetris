# TerminalTetris
A basic but fun Tetris game played within your cli terminal, written with Python 3 and the [Blessed Library](https://pypi.org/project/blessed/). The game runs fully within the Terminal or console window, and should work accross Mac, Linus, and PC platforms. 

<img width="448" alt="Tetris Demo Image" src="https://user-images.githubusercontent.com/15671813/122665139-1ccf8500-d16b-11eb-9e6f-69eaffb0eac9.png">


## Program Setup
1. Install the needed libraries(s). The only one that is not installed in the default Python installation is blessed, which can be installed via `pip install blessed`
2. Navigate to the directory in your preferred terminal

## Program Use
1. Run the program with `python TetrisGame.py` or however you normally choose to run your Python files
2. Play the game! 
 - Use the Left and Right arrow keys to move the current tile back and forth
 - Use the Up Arrow Key to rotate the current tile clockwise
 - Use the Down Arrow Key to make the current block drop faster
 - Use the Return/ Enter Key to drop the current tile immediately
 - You can press `P` to pause the game, or `Q` to exit
3. Your score will be printed at the conclusion of the program, and the game will be cleaned up and hidden. Try to beat my high score of 10,900!

## Next Steps
Future features to include include:
- [ ] Display upcoming tiles
- [ ] Local saving of high scores
- [ ] Optimization to reduce CPU usage
- [ ] Refactoring to clean up code

## Contributing
Pull requests and reccomendations for changes are welcome. For major changes, please open an issue first to discuss what you would like to change, to avoid having multiple solutions to an issue.

## License 
[MIT License](LICENSE)
