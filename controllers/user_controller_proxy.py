from __future__ import absolute_import, division, print_function, unicode_literals


class UserControllerProxy(object):

    def __init__(self, user_controller):
        self.user_controller = user_controller

    @property
    def creature(self):
        return self.user_controller.creature

    @property
    def level(self):
        return self.user_controller.game_actions.creature.level

    @property
    def io(self):
        return self.user_controller.io

    @property
    def game_actions(self):
        return self.user_controller.game_actions
