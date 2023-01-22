import delayexe
from mcdreforged.info_reactor.info import Info
from mcdreforged.plugin.server_interface import PluginServerInterface

global is_all_left


def on_load(server: PluginServerInterface, prev_module):
    global is_all_left
    is_all_left = True
    server.logger.info('Registering events')
    server.register_event_listener(delayexe.ON_LAST_PLAYER_LEAVE, lambda *args: all_left(server))


def on_unload(_server: PluginServerInterface):
    delayexe.clear_delay_task()


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    global is_all_left
    if is_all_left:
        server.logger.info('A player has returned, resuming server')
        server.register_event_listener(delayexe.ON_LAST_PLAYER_LEAVE, lambda *args: all_left(server))
        server.execute('tick rate 20')
        server.execute('gamerule doDaylightCycle true')
        is_all_left = False


def all_left(server: PluginServerInterface):
    server.logger.info('All players has left, freezing server')
    global is_all_left
    is_all_left = True
    server.execute('tick rate 0.1')
    server.execute('gamerule doDaylightCycle false')
