# BallBox

A simulation of balls in a box, with inelastic collisions.

![ball simulation](balls.gif)

The default behaviour is to open a 1000x1000px animation with 60 randomly sized and coloured balls.

The parameter to `Box()` controls the scale factor. If you want a smaller image, and you probably do if you want to 
output gifs, set this to some value. For example, setting 5 will produce a 200x200px animation.

The parameters to `add_random_balls` are the number of balls, whether the balls should be random sizes, and whether 
they should be random colours (the default is blue).

The parameter to `start_animation` is the gif duration in seconds. A duration of `None` produces an indefinite
matplotlib window animation.
