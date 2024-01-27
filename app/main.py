#!/usr/bin/env python3
import os
import time

import discord as d
import dotenv
from google.cloud import compute_v1

dotenv.load_dotenv()


def pip_freeze():
    import subprocess

    proc = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
    print(proc.stdout.decode("utf-8"))
    exit(0)


def get_pal2_instance_status():
    project = os.getenv("GCP_PROJECT")
    zone = os.getenv("GCP_ZONE")
    instance_name = os.getenv("GCE_INSTANCE_NAME")

    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(project=project, zone=zone, instance=instance_name)

    return instance.status


def get_pal2_instance_externalip():
    project = os.getenv("GCP_PROJECT")
    zone = os.getenv("GCP_ZONE")
    instance_name = os.getenv("GCE_INSTANCE_NAME")

    instance_client = compute_v1.InstancesClient()
    instance = instance_client.get(project=project, zone=zone, instance=instance_name)

    return instance.network_interfaces[0].access_configs[0].nat_i_p


def start_pal2():
    project = os.getenv("GCP_PROJECT")
    zone = os.getenv("GCP_ZONE")
    instance_name = os.getenv("GCE_INSTANCE_NAME")

    instance_client = compute_v1.InstancesClient()
    operation = instance_client.start(
        project=project, zone=zone, instance=instance_name
    )
    operation.result()
    return operation.result()


def stop_pal2():
    project = os.getenv("GCP_PROJECT")
    zone = os.getenv("GCP_ZONE")
    instance_name = os.getenv("GCE_INSTANCE_NAME")

    instance_client = compute_v1.InstancesClient()
    operation = instance_client.stop(project=project, zone=zone, instance=instance_name)
    operation.result()
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

        if message.content == "/PalServer bot-test":
            await message.channel.send("bot-test だよ. Hello!")

        if message.content == "/PalServer help":
            await message.channel.send(bot_help)

        if message.content == "/PalServer start":
            await message.channel.send("PalServer を起動するよ。１分ぐらい待ってね。")
            # 起動処理
            start_pal2()
            time.sleep(60)
            # IP アドレスを取得して表示する
            res = get_pal2_instance_status()
            if res == "RUNNING":
                nat_ip = get_pal2_instance_externalip()
                await message.channel.send(f"{nat_ip}:8211")
            else:
                time.sleep(60)
                if res == "RUNNING":
                    nat_ip = get_pal2_instance_externalip()
                    await message.channel.send(f"{nat_ip}:8211")
                else:
                    await message.channel.send(
                        "PalServer を起動しようとしたけどうまくできてないかも。 \nもう1分待って `/PalServer status` を確認してみて。それでもだめならなんか問題が起きてるかも。"
                    )

        if message.content == "/PalServer stop":
            await message.channel.send("PalServer を停止するよ")
            # 停止処理
            stop_pal2()
            time.sleep(60)
            res = get_pal2_instance_status()
            if res == "TERMINATED":
                await message.channel.send("PalServer を停止したよ。また遊んでね。")
            else:
                await message.channel.send(
                    "PalServer はまだ停止していないみたい。ほっといていいよ。"
                )

        if message.content == "/PalServer restart":
            await message.channel.send("PalServer を再起動するよ。ちょっとまっててね。")
            status = get_pal2_instance_status()
            if status == "RUNNING":
                stop_pal2()
                time.sleep(60)

            start_pal2()
            time.sleep(60)
            status = get_pal2_instance_status()
            if status == "RUNNING":
                nat_ip = get_pal2_instance_externalip()
                await message.channel.send(f"{nat_ip}:8211")
            else:
                time.sleep(60)
                if status == "RUNNING":
                    nat_ip = get_pal2_instance_externalip()
                    await message.channel.send(f"{nat_ip}:8211")
                else:
                    await message.channel.send(
                        "PalServer を起動しようとしたけどうまくできてないかも。 \nもう1分待って `/PalServer status` を確認してみて。それでもだめならなんか問題が起きてるかも。"
                    )

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
