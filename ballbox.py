import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random, uniform, choice

mpl.use('TkAgg')


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
    def __init__(self, x, y, r, vx, vy):
        self.x, self.y, self.r, self.v = x, y, r, Vector2D(vx, vy)
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
                unit_normal_vector = Vector2D(other.x - self.x, other.y - self.y).get_unit_vector()
                unit_tangent_vector = Vector2D(-unit_normal_vector.y, unit_normal_vector.x)
                v1_scalar_normal_before = self.v.dot_product(unit_normal_vector)
                v1_tangent_scalar = self.v.dot_product(unit_tangent_vector)
                v2_normal_scalar_before = other.v.dot_product(unit_normal_vector)
                v2_tangent_scalar = other.v.dot_product(unit_tangent_vector)
                v1_normal_scalar_after = (
                    (v1_scalar_normal_before * (self.mass - other.mass)) + (2 * other.mass * v2_normal_scalar_before)
                ) / (self.mass + other.mass)
                v2_normal_scalar_after = (
                    (v2_normal_scalar_before * (other.mass - self.mass)) + (2 * self.mass * v1_scalar_normal_before)
                ) / (self.mass + other.mass)
                v1_normal_vector_after = v1_normal_scalar_after * unit_normal_vector
                v1_tangent_vector_after = v1_tangent_scalar * unit_tangent_vector
                v2_normal_vector_after = v2_normal_scalar_after * unit_normal_vector
                v2_tangent_vector_after = v2_tangent_scalar * unit_tangent_vector
                self.v = v1_normal_vector_after + v1_tangent_vector_after
                other.v = v2_normal_vector_after + v2_tangent_vector_after
                self.in_collision.append(other)
                other.in_collision.append(self)
        else:
            if other in self.in_collision:
                self.in_collision.remove(other)
                other.in_collision.remove(self)


class Box:
    def __init__(self, factor=1):
        self.factor = factor
        self.size_x, self.size_y = 1000 / factor, 1000 / factor
        self.balls = []
        self.fig, self.ax = plt.subplots()
        dpi = 100
        self.fig.set_size_inches(self.size_x / dpi, self.size_y / dpi)
        self.fig.set_dpi(dpi)
        self.ax.set_xlim(0, self.size_x), self.ax.set_xticks([])
        self.ax.set_ylim(0, self.size_y), self.ax.set_yticks([])
        self.artist_to_ball = {}
        self.fig.tight_layout()

    def add_ball(self, x, y, r, vx, vy):
        self.balls.append(ball := Ball(x, y, r, vx, vy))
        self.artist_to_ball[self.ax.add_artist(plt.Circle((x, y), r, color='b'))] = ball

    def add_balls(self, ball_list):
        for ball in ball_list:
            self.add_ball(*ball)

    def add_random_balls(self, num, random_sizes=True, random_colours=True):
        j = 0
        for i in range(num):
            if j > num * 5:
                break
            size = choice([25, 30, 35]) if random_sizes else 20
            size = size / self.factor
            color = [random() for _ in range(3)] if random_colours else 'b'
            ball = Ball(
                x := uniform(size, self.size_x-size), y := uniform(size, self.size_y-size),
                size, uniform(-7, 7) / self.factor, uniform(-7, 7) / self.factor
            )
            if any([ball.is_colliding(existing_ball) for existing_ball in self.balls]):
                i -= 1
            else:
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
        circles = []
        for artist in self.ax.get_children():
            ball = self.artist_to_ball.get(artist, None)
            if ball:
                artist.set_center((ball.x, ball.y))
                circles.append(artist)
        return circles

    def start_animation(self, gif_duration=None):
        if gif_duration:
            num_steps = 5
            frames = 60 * gif_duration
        else:
            num_steps = 5
            frames = None
        anim = animation.FuncAnimation(
            self.fig, self.update_fig, frames=frames, interval=5, fargs=(num_steps,), blit=True
        )
        if gif_duration:
            anim.save(
                'balls.gif', animation.ImageMagickWriter(fps=60, extra_args=['-layers', 'Optimize']),
            )
        else:
            plt.show()


if __name__ == '__main__':
    box = Box(3)
    box.add_random_balls(60, random_sizes=True, random_colours=True)
    box.start_animation(gif_duration=10)
