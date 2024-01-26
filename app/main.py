#!/usr/bin/env python3
import os

import discord as d
import dotenv

dotenv.load_dotenv()


def pip_freeze():
    import subprocess

    proc = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
    print(proc.stdout.decode("utf-8"))
    exit(0)


def gcp_show_instances():
    # https://cloud.google.com/compute/docs/api/libraries?hl=ja
    from google.cloud import compute_v1

    project = "mollinaca-development"
    zone = "asia-east1-b"

    instance_client = compute_v1.InstancesClient()
    instance_list = instance_client.list(project=project, zone=zone)

    print(f"Instances found in zone {zone}:")
    for instance in instance_list:
        print(f" - {instance.name} ({instance.machine_type})")

    return instance_list


def get_pal2_instance_status():
    # https://cloud.google.com/compute/docs/api/libraries?hl=ja
    from google.cloud import compute_v1

    project = "mollinaca-development"
    zone = "asia-east1-b"
    instance_name = "pal2"

    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(project=project, zone=zone, instance=instance_name)

    return instance.status


def get_pal2_instance_externalip():
    # https://cloud.google.com/compute/docs/api/libraries?hl=ja
    from google.cloud import compute_v1

    project = "mollinaca-development"
    zone = "asia-east1-b"
    instance_name = "pal2"

    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(project=project, zone=zone, instance=instance_name)

    return instance.network_interfaces[0].access_configs[0].nat_i_p


def start_pal2():
    # https://cloud.google.com/compute/docs/api/libraries?hl=ja
    from google.cloud import compute_v1

    project = "mollinaca-development"
    zone = "asia-east1-b"
    instance_name = "pal2"

    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(
        project=project, zone=zone, instance=instance_name
    )
    operation.result()
    print(operation.result())
    return operation.result()


def stop_pal2():
    # https://cloud.google.com/compute/docs/api/libraries?hl=ja
    from google.cloud import compute_v1

    project = "mollinaca-development"
    zone = "asia-east1-b"
    instance_name = "pal2"

    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(project=project, zone=zone, instance=instance_name)
    operation.result()
    print(operation.result())
    return operation.result()


def discord_bot():
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    client = d.Client(intents=d.Intents.all())

    bot_help = (
        "/PalServer BOT の使い方だよ\n"
        "```"
        "/PalServer start   : PalServer を起動します。１～２分待ってね。 \n"
        "/PalServer stop    : PalServer を終了します。遊び終わったら止めてね。\n"
        "/PalServer status  : PalServer の稼働状態を確認します。動いてたなら、IPアドレスも確認するよ。 \n"
        "/PalServer restart : PalServer を再起動します。稼働中なのに繋がらないとかなんかおかしかったら試してね。 \n"
        "/PalServer costs   : 今月現時点での費用を出力するよ。使いすぎ注意！ \n"
        "/PalServer help    : このテキストを表示するよ。 \n"
        "```"
    )

    # 起動時に動作する処理
    @client.event
    async def on_ready():
        print("bot login to channel")

    # メッセージ受信時に動作する処理
    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content == "/bot-test":
            await message.channel.send("Hello!")
        if message.content == "/PalServer help":
            await message.channel.send(bot_help)
        if message.content == "/PalServer start":
            await message.channel.send(
                "PalServer を起動するよ ※この機能はまだ実装されていません"
            )
            # 起動処理
            # start_pal2
            # IP アドレスを取得して表示する
        if message.content == "/PalServer stop":
            await message.channel.send(
                "PalServer を停止するよ ※この機能はまだ実装されていません"
            )
            # 停止処理
        if message.content == "/PalServer restart":
            await message.channel.send(
                "PalServer を再起動するよ ※この機能はまだ実装されていません"
            )
            # 停止処理
            # 起動処理
            # IP アドレスを取得して表示する

        if message.content == "/PalServer status":
            res = get_pal2_instance_status()
            await message.channel.send(f"PalServer の稼働状態 : {res}")
            if res == "RUNNING":
                nat_ip = get_pal2_instance_externalip()
                await message.channel.send(f"{nat_ip}:8211")

        if message.content == "/PalServer costs":
            await message.channel.send(
                "今月現時点での月額請求額は : <> だよ ※この機能はまだ実装されていません"
            )

        if message.content == "/PalServer ipaddress":
            res = get_pal2_instance_externalip()
            await message.channel.send(f"PalServer IPAddress : {res}")

    # Botの起動とDiscordサーバーへの接続
    client.run(TOKEN)


if __name__ == "__main__":
    # pip_freeze()
    discord_bot()
    exit(0)
