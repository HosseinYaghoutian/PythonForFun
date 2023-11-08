import random
import arcade
import sys
import os

PATH = os.path.dirname(__file__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Platformer Game"

MOVEMENT_SPEED = 5
SPRITE_SCALING = 0.05


class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    """
    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
           self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
          self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
        self.texture = self.idle_texture_pair[self.character_face_direction]
        return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
        self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]
      
    """


class Apple(arcade.Sprite):
    pass


class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.sound = arcade.load_sound(PATH + "/file/sound.wav")

        self.player_list = None
        self.player = None

        self.apple_list = None
        self.apple = None

    def setup(self):
        self.score = 0
        self.end = False

        self.player_setup()
        self.apple_setup()

    def player_setup(self):
        #player
        self.player_list = arcade.SpriteList()
        self.player = Player(PATH + "/file/snake.png", SPRITE_SCALING)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

    def apple_setup(self):
        #apple
        self.apple_list = arcade.SpriteList()
        self.apple = Apple(PATH + "/file/apple.png", SPRITE_SCALING)

        flag = True
        while flag:
            self.apple.center_x = random.randint(5, SCREEN_WIDTH - 5)
            self.apple.center_y = random.randint(5, SCREEN_HEIGHT - 5)
            flag = False
            if (self.apple.center_x
                    == self.player.center_x) and (self.apple.center_y
                                                  == self.player.center_y):
                flag = True

        self.apple_list.append(self.apple)

    def on_update(self, delta_time):
        self.player_list.update()
        self.apple_list.update()

        if arcade.check_for_collision_with_list(self.player, self.apple_list):
            self.apple.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.sound)

            self.apple_setup()

        if self.score == 20:
            sys.exit("You Win")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.apple_list.draw()

        self.s = "score: " + str(self.score)
        arcade.draw_text(self.s, 8, 15, arcade.color.BLACK, 15)


def main():
    """ Main function """
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()