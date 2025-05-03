# Flappy Bird

Create a clone of the flappy bird game. 

First, you can review a  [web version of the game online](https://flappybird.io/) to see how the game works, or run the example in `examples/flappy_bird`. 

![example](images/example.png)

 The basic game play is:

1. The player plays a bird that is constantly flapping its wings to maintain flight. 
2. The bird moves up and down, but not left or right. Instead. the pipes move toward the player from the right side of the screen.
3. The player must navigate the bird through the gaps in the pipes without hitting them. 

The bird's motion is like jumping: flapping provides a small increase in upward
velocity, while gravity is pulling the bird down. 

If you'd like some serious inspiration, and some code to help you get started, we have a very nice version 
of the game in the `examples/flappy_bird` directory.

## Development Process

You can create the game in whatever way you'd like, but this process may make your development smoother. 

### 1. Moving pipes

Start by creating the background, by displaying the background image, which must be repeated to fill the screen.

Use code like this to get the background:

```python from pathlib import Path
assets = Path(__file__).parent / 'assets'
background = pygame.image.load(assets/'background.png')
```

See ``06_Surfaces/01_tile_background.py`` for an example of how to tile the background image.

This code will open the the 'assets' director in the same parent directory as
the file that is being executed.  When using the Path() object, the `/` operator
has a different meaning than the normal division operator.  Instead, it is used
to join the path with a string, so it is like writing `"assets" + "/" + "background.png"`. 


### 2. Add the Bird

Add the bird. Pressing the space bar should give the bird a small upward
velocity, but gravity should be pulling the bird down.

Try to animate the bird by swaping the image of the bird between two or three of
the bird images in the `images/` directory

### 2. Add collisions

Implement collisions so the game ends when the bird hits the pipes.

### 3. Scoring

Add a score that increases as the bird passes through the pipes.