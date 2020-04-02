# BallBox

<p align="center">
  <img width="400" height="400" src="https://github.com/dcragusa/BallBox/blob/master/balls.gif)">
</p>

A simulation of balls in a box, with inelastic collisions. Now argparse-ified!

The default behaviour is to open a 1000x1000px live animation with 60 balls. 

    usage: ballbox.py [-h] [-s SIZE SIZE] [-n NUM] [--random_sizes] [--random_colours] [--speed SPEED] [--fps FPS] [-f {gif,mp4}] [-d DURATION] [-o OUTPUT]
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SIZE SIZE, --size SIZE SIZE
                            The size of the box in pixels. Default: 1000x1000 px.
      -n NUM, --num NUM     The number of balls to simulate. Default: 60.
      --random_sizes        If present, balls will have random sizes.
      --random_colours, --random_colors
                            If present, balls will have random colours.
      --speed SPEED         The factor affecting the speed of balls in the simulation. Default: 1.
      --fps FPS             The frames per second of the animation. The maximum is 1000fps. Default: 60 fps.
      -f {gif,mp4}, --file_type {gif,mp4}
                            If present, the file type of the output animation. Default: a live window animation. ImageMagick must be installed for gif output. FFmpeg must be installed for video output.
      -d DURATION, --duration DURATION
                            The duration in seconds of the output animation. No effect on a live window. Default: 5 sec.
      -o OUTPUT, --output OUTPUT
                            The filename of the output animation. No effect on a live window. Default: balls.

More examples can be found below.

    python ballbox.py -s 400 400 -n 20 --fps 30 -f gif -d 10 -o balls_simple
    
<p align="center">
  <img width="400" height="400" src="https://github.com/dcragusa/BallBox/blob/master/balls_simple.gif)">
</p>

    python ballbox.py -s 400 400 -n 40 --random_sizes --random_colours --speed 1.5 -f gif -d 10 -o balls_complex

<p align="center">
  <img width="400" height="400" src="https://github.com/dcragusa/BallBox/blob/master/balls_complex.gif)">
</p>
