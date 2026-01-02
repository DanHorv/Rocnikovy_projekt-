import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
from role_data import ROLE_DETAIL_GRIMOIRE, ROCNIK_TROUBLE_BREWING, NASTAVENI_PODLE_HRACU
import asyncio


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
discord.utils.setup_logging(level=logging.INFO, root=False, handler=handler)

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

HLAVNI_KANAL_NAZEV = "Náměstí"

game_state = {
    "players": [],
    "house_channels": {},
}

@bot.command(name="role")
async def role(ctx):
    member = ctx.author
    role_nazev = "Storyteller"
    target_role = discord.utils.get(ctx.guild.roles, name=role_nazev)

    if not target_role:
        await ctx.send(f"Chyba: Role {role_nazev} neexistuje.")
        return

    try:
        if target_role in member.roles:
            await member.remove_roles(target_role)
            await ctx.send(f"Role **{role_nazev}** byla odebrána.")
        else:
            await member.add_roles(target_role)
            await ctx.send(f"Role **{role_nazev}** byla přidělena.")
    except discord.Forbidden:
        await ctx.send(f"Chyba: Nemám oprávnění spravovat roli {role_nazev}.")

def je_vypravec():
    async def predicate(ctx):
        st_role = discord.utils.get(ctx.author.roles, name="Storyteller")
        if st_role is None:
            await ctx.send("Tento příkaz smí použít jen Vypravěč !")
            return False
        return True

    return commands.check(predicate)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} je online a připraven!')

@bot.command(name="starthry", aliases=["startgame", "start"])
async def start_hry(ctx):
    main_vc = discord.utils.get(ctx.guild.voice_channels, name=HLAVNI_KANAL_NAZEV)
    if not main_vc:
        await ctx.send(f"Chyba: Nemohu najít hlasový kanál s názvem `{HLAVNI_KANAL_NAZEV}`.")
        return

    players_in_game = [m for m in main_vc.members if m != ctx.author and not m.bot]
    player_count = len(players_in_game)
    game_state["players"] = players_in_game

    if player_count < 5:
        await ctx.send(f"Chyba: Pro hru je potřeba alespoň 5 hráčů (v kanálu je {player_count}).")
        return

    setup_counts = NASTAVENI_PODLE_HRACU.get(player_count)
    if not setup_counts:
        await ctx.send(f"**Chyba!** Počet hráčů ({player_count}) není podporován (podporujeme 5-15).")
        return

    tf_count, out_count, min_count, dem_count = setup_counts

    try:
        townsfolk_list = random.sample(ROCNIK_TROUBLE_BREWING["townsfolk"], tf_count)
        outsiders_list = random.sample(ROCNIK_TROUBLE_BREWING["outsiders"], out_count)
        minions_list = random.sample(ROCNIK_TROUBLE_BREWING["minions"], min_count)
        demons_list = random.sample(ROCNIK_TROUBLE_BREWING["demons"], dem_count)
    except ValueError as e:
        await ctx.send(
            f"**Chyba při sestavování rolí!** Pravděpodobně nemám v `role_data.py` dostatek unikátních rolí pro tento počet hráčů. Chyba: {e}")
        return

    drunk_token = None

    if "Opilec" in outsiders_list:
        all_townsfolk = set(ROCNIK_TROUBLE_BREWING["townsfolk"])
        used_townsfolk = set(townsfolk_list)
        available_tokens = list(all_townsfolk - used_townsfolk)

        if not available_tokens:
            drunk_token = random.choice(townsfolk_list)
        else:
            drunk_token = random.choice(available_tokens)

    final_role_list = townsfolk_list + outsiders_list + minions_list + demons_list
    random.shuffle(final_role_list)

    await ctx.send(f"🌙 **PRVNÍ Noc začíná!**")

    final_arrangement = list(zip(game_state["players"], final_role_list))
    st_grimoire_lines = [f"--- Tajný Grimoire (Hra #{ctx.message.id}) ---"]

    for i, (player, role) in enumerate(final_arrangement):

        levy_soused_index = (i - 1 + player_count) % player_count
        pravy_soused_index = (i + 1) % player_count

        levy_soused = final_arrangement[levy_soused_index][0].display_name
        pravy_soused = final_arrangement[pravy_soused_index][0].display_name

        role_to_send_player = role

        if role == "Opilec":
            role_to_send_player = drunk_token
            popis_role = ROLE_DETAIL_GRIMOIRE.get(drunk_token, "Popis role není k dispozici.")
            st_grimoire_lines.append(
                f"**{i + 1}. {player.display_name}** je **Opilec** (myslí si, že je **{drunk_token}**)")
        else:
            popis_role = ROLE_DETAIL_GRIMOIRE.get(role, "Popis role není k dispozici.")
            st_grimoire_lines.append(f"**{i + 1}. {player.display_name}** je **{role}**")

        dm_message = (
            f"**Tvoje pozice v kruhu:** **{i + 1}** z {player_count}\n"
            f"**Tvůj levý soused je:** **{levy_soused}**\n"
            f"**Tvůj pravý soused je:** **{pravy_soused}**\n\n"
            f"Tvoje role je: **{role_to_send_player}**\n"
            f"Popis role: {popis_role}\n"
        )

        try:
            await player.send(dm_message)
        except discord.Forbidden:
            await ctx.send(f"⚠️ Nemohu poslat DM hráči {player.display_name}. (Má zakázané DM?)")
        except Exception as e:
            await ctx.send(f"Chyba při posílání DM hráči {player.display_name}: {e}")

    try:
        final_grimoire_message = "\n".join(st_grimoire_lines)
        await ctx.author.send(final_grimoire_message)
    except discord.Forbidden:
        await ctx.send(f"⚠️ Nemohu ti poslat DM s Grimoirem, {ctx.author.mention}! (Máš zakázané DM?)")
    except Exception as e:
        await ctx.send(f"Chyba při posílání Grimoire DM: {e}")

    category = main_vc.category
    for player in game_state["players"]:
        try:
            house_vc = await ctx.guild.create_voice_channel(
                name=f" Dům - {player.display_name}",
                category=category
            )
            await house_vc.set_permissions(player, connect=True, speak=True, view_channel=True)
            await house_vc.set_permissions(ctx.guild.default_role, connect=False, view_channel=False)
            await house_vc.set_permissions(ctx.author, connect=True, speak=True, view_channel=True)

            game_state["house_channels"][player.id] = house_vc.id
            await player.move_to(house_vc)
        except Exception as e:
            await ctx.send(
                f"CHYBA PŘI PŘESUNU/TVORBĚ KANÁLU pro {player.display_name}: {e}\n(Chybí mi práva 'Manage Channels' nebo 'Move Members'?)")

    await ctx.send(f"Všichni hráči ({player_count}) byli přesunuti. Dobrou noc.")


@bot.command(name="noc")
@je_vypravec()
async def noc(ctx):
    main_vc = discord.utils.get(ctx.guild.voice_channels, name=HLAVNI_KANAL_NAZEV)
    if not main_vc:
        await ctx.send(f"Chyba: Nemohu najít hlasový kanál s názvem `{HLAVNI_KANAL_NAZEV}`.")
        return

    if not game_state["players"]:
        await ctx.send("Chyba: Seznam aktivních hráčů je prázdný. Spusť nejprve `!starthry`.")
        return

    if game_state["house_channels"]:
        await ctx.send("Chyba: Noc již běží! Nejprve musíš ukončit noc pomocí `!den`.")
        return

    await ctx.send(f"🌙 **Noc začíná!** Přesouvám hráče do jejich domů...")

    category = main_vc.category
    player_count = 0

    for player in game_state["players"]:
        player_member = ctx.guild.get_member(player.id)
        if not player_member:
            print(f"Hráč {player.name} nebyl nalezen na serveru, přeskakuji.")
            continue

        try:
            house_vc = await ctx.guild.create_voice_channel(
                name=f"🏡 Dům - {player_member.display_name}",
                category=category
            )
            await house_vc.set_permissions(player_member, connect=True, speak=True, view_channel=True)
            await house_vc.set_permissions(ctx.guild.default_role, connect=False, view_channel=False)
            await house_vc.set_permissions(ctx.author, connect=True, speak=True, view_channel=True)

            game_state["house_channels"][player_member.id] = house_vc.id

            if player_member.voice and player_member.voice.channel == main_vc:
                await player_member.move_to(house_vc)

            player_count += 1

        except Exception as e:
            await ctx.send(
                f"CHYBA PŘI PŘESUNU/TVORBĚ KANÁLU pro {player_member.display_name}: {e}\n(Chybí mi práva 'Manage Channels' nebo 'Move Members'?)")

    await ctx.send(f"Všichni hráči ({player_count}) byli přesunuti. Dobrou noc.")


@bot.command(name="den", aliases=["konecnoci", "day"])
@je_vypravec()
async def den(ctx):
    main_vc = discord.utils.get(ctx.guild.voice_channels, name=HLAVNI_KANAL_NAZEV)
    if not main_vc:
        await ctx.send(f"Chyba: Nemohu najít hlasový kanál s názvem `{HLAVNI_KANAL_NAZEV}`.")
        return

    if not game_state["house_channels"]:
        await ctx.send("Chyba: Žádné domy k úklidu nebyly nalezeny. Hra zřejmě neběží v noci.")
        return

    await ctx.send("☀️ **Noc končí!** Svolávám všechny zpět na Náměstí a uklízím domy...")

    for player_id, channel_id in game_state["house_channels"].items():
        player = ctx.guild.get_member(player_id)
        house_vc = bot.get_channel(channel_id)

        if not house_vc:
            continue

        if player and player.voice and player.voice.channel == house_vc:
            try:
                await player.move_to(main_vc)
            except Exception as e:
                print(f"Nepodařilo se přesunout {player.display_name} do Náměstí: {e}")

        try:
            await house_vc.delete(reason="Konec noci/start dne.")
        except Exception as e:
            print(f"Nepodařilo se smazat kanál {house_vc.name}: {e}")

    game_state["house_channels"] = {}

    await ctx.send("✅ Všichni hráči jsou zpět na Náměstí. **Den začíná.**")


@bot.command(name="volno")
@je_vypravec()
async def volno(ctx, seconds: int):
    main_vc = discord.utils.get(ctx.guild.voice_channels, name=HLAVNI_KANAL_NAZEV)
    if not main_vc:
        await ctx.send(f"Chyba: Nemohu najít hlasový kanál s názvem `{HLAVNI_KANAL_NAZEV}`.")
        return

    if not game_state["players"]:
        await ctx.send("Chyba: Seznam aktivních hráčů je prázdný. Spusť nejprve `!starthry`.")
        return

    if seconds <= 0:
        await ctx.send("Čas volného času musí být větší než nula sekund.")
        return

    duration_str = f"{seconds // 60} minut a {seconds % 60} sekund" if seconds >= 60 else f"{seconds} sekund"
    await ctx.send(
        f"🟢 **Volno ({duration_str}) spuštěno!** Můžete se volně přesouvat mezi kanály. Za {duration_str} budete přesunuti zpět do `{HLAVNI_KANAL_NAZEV}`.")

    await asyncio.sleep(seconds)

    await ctx.send(f"🔴 **Volno skončilo!** Čas vypršel. Všichni hráči jsou přesouváni zpět do `{HLAVNI_KANAL_NAZEV}`.")

    recalled_count = 0
    for player in game_state["players"]:

        try:
            player_member = ctx.guild.get_member(player.id)
            if player_member and not player_member.bot and player_member.voice and player_member.voice.channel != main_vc:
                await player_member.move_to(main_vc)
                recalled_count += 1
        except Exception as e:
            print(f"Nepodařilo se přesunout {player.display_name} zpět: {e}")

    await ctx.send(f"✅ Všichni hráči ({recalled_count} přesunuto) jsou zpět v `{HLAVNI_KANAL_NAZEV}`. Hra pokračuje.")


@bot.command(name="offline")
@je_vypravec()
async def offline_rozpis(ctx, player_count: int):

    if player_count < 5 or player_count > 15:
        await ctx.send(
            f"**Chyba!** Počet hráčů ({player_count}) musí být mezi 5 a 15.")
        return

    setup_counts = NASTAVENI_PODLE_HRACU.get(player_count)
    if not setup_counts:
        await ctx.send(f"**Chyba!** Počet hráčů ({player_count}) není podporován (podporujeme 5-15).")
        return

    tf_count, out_count, min_count, dem_count = setup_counts

    try:
        townsfolk_list = random.sample(ROCNIK_TROUBLE_BREWING["townsfolk"], tf_count)
        outsiders_list = random.sample(ROCNIK_TROUBLE_BREWING["outsiders"], out_count)
        minions_list = random.sample(ROCNIK_TROUBLE_BREWING["minions"], min_count)
        demons_list = random.sample(ROCNIK_TROUBLE_BREWING["demons"], dem_count)
    except ValueError as e:
        await ctx.send(
            f"**Chyba při sestavování rolí!** Pravděpodobně nemám v `role_data.py` dostatek unikátních rolí pro tento počet hráčů. Chyba: {e}")
        return

    final_role_list = townsfolk_list + outsiders_list + minions_list + demons_list
    random.shuffle(final_role_list)

    drunk_token = None
    if "Opilec" in outsiders_list:
        all_townsfolk = set(ROCNIK_TROUBLE_BREWING["townsfolk"])
        used_townsfolk = set(townsfolk_list)
        available_tokens = list(all_townsfolk - used_townsfolk)

        if not available_tokens:
            drunk_token = random.choice(townsfolk_list)
        else:
            drunk_token = random.choice(available_tokens)

    st_output_lines = [
        f"--- 📝 **Offline Grimoire** ({player_count} hráčů) ---",
        f"**Rozdělení rolí:**"
    ]

    for i, role in enumerate(final_role_list):
        display_role = role
        note = ""

        if role == "Opilec":
            display_role = f"Opilec (myslí si, že je: {drunk_token})"
            note = f" -> Skutečná role Opilce: **{drunk_token}**"

        st_output_lines.append(f"**Pozice {i + 1}.** | Role: **{display_role}** {note}")

    try:
        final_message = "\n".join(st_output_lines)
        await ctx.author.send(final_message)
        await ctx.send(f"✅ Rozpis rolí pro {player_count} hráčů byl odeslán do tvého DM.")
    except discord.Forbidden:
        await ctx.send(f"⚠️ Nemohu ti poslat DM, {ctx.author.mention}! Zkontroluj nastavení soukromí.")
    except Exception as e:
        await ctx.send(f"Chyba při posílání DM s rozpisem: {e}")



@bot.command(name="cislo")
async def command_cislo(ctx):
    spravne_cislo = random.randint(1, 5)
    await ctx.send("uhodni cislo")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    zprava = await bot.wait_for('message', check=check, timeout=30.0)


    odpoved_string = zprava.content

    uhadnute_cislo = int(odpoved_string)


    if uhadnute_cislo == spravne_cislo:
        await ctx.send("správná odpověď! 🎉")
    else:
        await ctx.send(f"špatně, číslo bylo {spravne_cislo}")



bot.run(token)
