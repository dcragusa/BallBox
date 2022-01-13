import math
import argparse
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random, uniform, choice

mpl.use('TkAgg')
BASE_SPEED = 10


class Vector2D:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f'Vector2D(x={self.x}, y={self.y})'

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    @property
    def magnitude(self):
        return 1 if not (divisor := math.sqrt(self.x**2 + self.y**2)) else divisor

    def get_unit_vector(self):
        return Vector2D(self.x / self.magnitude, self.y / self.magnitude)

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)


class Ball:
    def __init__(self, x, y, r, vx, vy, e):
        self.x, self.y, self.r, self.v, self.e = x, y, r, Vector2D(vx, vy), e
        self.in_collision = []

    @property
    def mass(self):
        return self.r**2

    def time_step(self, num_steps):
        self.x += self.v.x / num_steps
        self.y += self.v.y / num_steps

    def check_wall_collision(self, size_x, size_y):
        if self.x <= self.r:
            self.x = self.r
            self.v.x = -self.v.x
        elif self.x >= (x2_bound := (size_x - self.r)):
            self.x = x2_bound
            self.v.x = -self.v.x
        elif self.y <= self.r:
            self.y = self.r
            self.v.y = -self.v.y
        elif self.y >= (y2_bound := (size_y - self.r)):
            self.y = y2_bound
            self.v.y = -self.v.y

    def is_colliding(self, other):
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2) <= self.r + other.r

    def check_ball_collision(self, other):
        if self.is_colliding(other):
            if other not in self.in_collision:
                e = min(self.e, other.e)
                unit_normal_vector = Vector2D(other.x - self.x, other.y - self.y).get_unit_vector()
                unit_tangent_vector = Vector2D(-unit_normal_vector.y, unit_normal_vector.x)
                v1_scalar_normal_before = self.v.dot_product(unit_normal_vector)
                v1_tangent_scalar = self.v.dot_product(unit_tangent_vector)
                v2_normal_scalar_before = other.v.dot_product(unit_normal_vector)
                v2_tangent_scalar = other.v.dot_product(unit_tangent_vector)
                v1_normal_scalar_after = (
                    (v1_scalar_normal_before * (self.mass - e * other.mass)) + ((e + 1) * other.mass * v2_normal_scalar_before)
                ) / (self.mass + other.mass)
                v2_normal_scalar_after = (
                    (v2_normal_scalar_before * (other.mass - e * self.mass)) + ((e + 1) * self.mass * v1_scalar_normal_before)
                ) / (self.mass + other.mass)
                v1_normal_vector_after = v1_normal_scalar_after * unit_normal_vector
                v1_tangent_vector_after = v1_tangent_scalar * unit_tangent_vector
                v2_normal_vector_after = v2_normal_scalar_after * unit_normal_vector
                v2_tangent_vector_after = v2_tangent_scalar * unit_tangent_vector
                self.v = v1_normal_vector_after + v1_tangent_vector_after
                other.v = v2_normal_vector_after + v2_tangent_vector_after
                self.in_collision.append(other)
                other.in_collision.append(self)
        elif other in self.in_collision:
            self.in_collision.remove(other)
            other.in_collision.remove(self)


class Box:
    def __init__(self, x, y):
        self.size_factor = min(x, y) / 1000
        self.size_x, self.size_y = x, y
        self.balls = []
        self.fig, self.ax = plt.subplots()
        dpi = 100
        self.fig.set_size_inches(self.size_x / dpi, self.size_y / dpi)
        self.fig.set_dpi(dpi)
        self.ax.set_xlim(0, self.size_x), self.ax.set_xticks([])
        self.ax.set_ylim(0, self.size_y), self.ax.set_yticks([])
        self.artist_to_ball = {}
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    def add_ball(self, x, y, r, vx, vy, e):
        self.balls.append(ball := Ball(x, y, r, vx, vy, e))
        self.artist_to_ball[self.ax.add_artist(plt.Circle((x, y), r, color='b'))] = ball

    def add_balls(self, ball_list):
        for ball in ball_list:
            self.add_ball(*ball)

    def add_random_balls(self, num, random_sizes=True, random_colours=True, speed_factor=1.0, e=1.0):
        i, j = 0, 0
        while i < num:
            if j > num * 5:
                break
            size = choice([25, 30, 35]) if random_sizes else 20
            size = size * self.size_factor
            color = [random() for _ in range(3)] if random_colours else 'b'
            speed = BASE_SPEED * speed_factor * self.size_factor
            ball = Ball(
                x := uniform(size, self.size_x-size), y := uniform(size, self.size_y-size),
                size, uniform(-speed, speed), uniform(-speed, speed), e
            )
            if not any([ball.is_colliding(existing_ball) for existing_ball in self.balls]):
                i += 1
                self.balls.append(ball)
                self.artist_to_ball[self.ax.add_artist(plt.Circle((x, y), size, color=color))] = ball
            j += 1

    def time_step(self, num_steps):
        for ball_idx, ball in enumerate(self.balls):
            ball.time_step(num_steps)
            ball.check_wall_collision(self.size_x, self.size_y)
            for other_ball in self.balls[ball_idx+1:]:
                ball.check_ball_collision(other_ball)

    def update_fig(self, _, num_steps):
        for _ in range(num_steps):
            self.time_step(num_steps)
        for artist in self.ax.get_children():
            ball = self.artist_to_ball.get(artist, None)
            if ball:
                artist.set_center((ball.x, ball.y))

    def start_animation(self, file_type, fps, duration, filename):

        frames = fps * duration if file_type else None
        interval = 1000 / fps
        if file_type:
            # annoyingly required as file animations don't respect the interval set in FuncAnimation, so the balls
            # bounce around at sanic speed at high fps.
            factor = 60 / fps
            for ball in self.balls:
                ball.v *= factor

        anim = animation.FuncAnimation(
            self.fig, self.update_fig, frames=frames, interval=interval, fargs=(5,)
        )
        if file_type == 'gif':
            anim.save(
                f'{filename}.gif', animation.ImageMagickWriter(fps=fps, extra_args=['-layers', 'Optimize'])
            )
        elif file_type == 'mp4':
            anim.save(f'{filename}.mp4', animation.FFMpegWriter(fps=fps))
        else:
            plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--size', nargs=2, default=[1000, 1000], type=int,
        help='The size of the box in pixels. Default: 1000x1000 px.'
    )
    parser.add_argument(
        '-n', '--num', default=60, type=int,
        help='The number of balls to simulate. Default: 60.'
    )
    parser.add_argument(
        '-e', '--elasticity', default=1.0, type=float,
        help='Coefficient of restitution.  Default: 1.0, i.e. perfectly elastic'
    )
    parser.add_argument(
        '--random_sizes', action='store_true',
        help='If present, balls will have random sizes.'
    )
    parser.add_argument(
        '--random_colours', '--random_colors', action='store_true', dest='random_colours',
        help='If present, balls will have random colours.'
    )
    parser.add_argument(
        '--speed', default=1.0, type=float,
        help='The factor affecting the speed of balls in the simulation. Default: 1.'
    )
    parser.add_argument(
        '--fps', default=60, type=int,
        help='The frames per second of the animation. The maximum is 1000fps. Default: 60 fps.'
    )
    parser.add_argument(
        '-f', '--file_type', choices=['gif', 'mp4'],
        help='If present, the file type of the output animation. Default: a live window animation. '
             'ImageMagick must be installed for gif output. FFmpeg must be installed for video output.'
    )
    parser.add_argument(
        '-d', '--duration', default=5, type=int,
        help='The duration in seconds of the output animation. No effect on a live window. Default: 5 sec.'
    )
    parser.add_argument(
        '-o', '--output', default='balls',
        help='The filename of the output animation. No effect on a live window. Default: balls.'
    )
    args = parser.parse_args()

    box = Box(args.size[0], args.size[1])
    box.add_random_balls(
        args.num, random_sizes=args.random_sizes, random_colours=args.random_colours, speed_factor=args.speed, e=args.elasticity
    )
    box.start_animation(file_type=args.file_type, fps=args.fps, duration=args.duration, filename=args.output)
