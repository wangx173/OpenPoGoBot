# -*- coding: utf-8 -*-

from pokemongo_bot import logger
from pokemongo_bot.human_behaviour import sleep
from pokemongo_bot.utils import distance, format_dist


class WalkTowardsFortWorker(object):
    def __init__(self, fort, bot):
        self.fort = fort
        self.api_wrapper = bot.api_wrapper
        self.bot = bot
        self.position = bot.position
        self.config = bot.config
        self.item_list = bot.item_list
        self.rest_time = 50
        self.stepper = bot.stepper

    def work(self):
        lat = self.fort.latitude
        lng = self.fort.longitude
        unit = self.config.distance_unit  # Unit to use when printing formatted distance

        fort_id = self.fort.fort_id
        dist = distance(self.position[0], self.position[1], lat, lng)

        self.api_wrapper.fort_details(fort_id=fort_id,
                                      latitude=lat,
                                      longitude=lng)
        response_dict = self.api_wrapper.call()
        if response_dict is None:
            return
        fort_details = response_dict["fort"]
        fort_name = fort_details.fort_name

        self.bot.fire("fort_found", fort_name=fort_name, fort_distance=format_dist(dist, unit))

        if dist > 0:
            self.bot.fire("fort_moving", fort_name=fort_name)
            position = (lat, lng, 0.0)

            if self.config.walk > 0:
                self.stepper.walk_to(self.config.walk, *position)
            else:
                self.api_wrapper.set_position(*position)
            self.api_wrapper.player_update(latitude=lat, longitude=lng)
            sleep(2)

        self.bot.fire("fort_arrived", fort_name=fort_name)
