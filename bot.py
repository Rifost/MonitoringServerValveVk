import config
import a2s
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token=config.token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, config.group_id)


def get_server_info(message):
    info = a2s.info(config.address)
    players = a2s.players(config.address)
    vac_status = "Включен" if info.vac_enabled else "Выключен"

    all_players, count = "", 0
    for player in players:
        count += 1
        if count == 1:
            all_players += f"Список игроков:\n{count}. {player.name} | {player.score}\n"
        else:
            all_players += f"{count}. {player.name} | {player.score}\n"

    send_message = f"Информация о сервере:\n"\
                   f"Название: {info.server_name}\n"\
                   f"Игра: {info.game}\n"\
                   f"Карта: {info.map_name}\n"\
                   f"Игроки: {info.player_count}/{info.max_players} ({info.bot_count} боты)\n"\
                   f"VAC: {vac_status}\n\n"\
                   f"{all_players}"
    
    vk.messages.send(peer_id=message['peer_id'], message=send_message, random_id=0)


def get_online_players(message):
    players = a2s.players(config.address)

    all_players, count = "", 0
    for player in players:
        count += 1
        if count == 1:
            all_players += f"Игроки онлайн:\n{count}. {player.name} | {player.score}\n"
        else:
            all_players += f"{count}. {player.name} | {player.score}\n"

    if count == 0:
        all_players += "В данный момент на сервере отсутствуют игроки"

    vk.messages.send(peer_id=message['peer_id'], message=all_players, random_id=0)


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message
                text = message['text'].lower()

                if text == "!сервер":
                    get_server_info(message)
                elif text == "!онлайн":
                    get_online_players(message)
    except Exception as e:
        print(f"LongPoll Exception: {e}")