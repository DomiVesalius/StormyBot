"""
Commands:
    - OW <platform|region|battletag|(Hero)>: Fetches player info for the overwatch account with specified battle_tag
"""

import os, discord, asyncio, json, requests, random
from discord.ext import commands
from urllib import request
country_list = ['AFGHANISTAN', 'ALBANIA', 'ALGERIA', 'ANDORRA', 'ANGOLA', 'ANTIGUA AND BARBUDA', 'ARGENTINA', 'ARMENIA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN', 'BAHAMAS', 'BAHRAIN', 'BANGLADESH', 'BARBADOS', 'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BHUTAN', 'BOLIVIA', 'BOSNIA AND HERZEGOVINA', 'BOTSWANA', 'BRAZIL', 'BRUNEI DARUSSALAM', 'BULGARIA', 'BURKINA FASO', 'BURUNDI', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAPE VERDE', 'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'CHILE', 'CHINA', 'COLOMBIA', 'COMOROS', 'CONGO (BRAZZAVILLE)', 'CONGO (KINSHASA)', 'COSTA RICA', 'CROATIA', 'CUBA', 'CYPRUS', 'CZECH REPUBLIC', "CÔTE D'IVOIRE", 'DENMARK', 'DJIBOUTI', 'DOMINICA', 'DOMINICAN REPUBLIC', 'ECUADOR', 'EGYPT', 'EL SALVADOR', 'EQUATORIAL GUINEA', 'ERITREA', 'ESTONIA', 'ETHIOPIA', 'FIJI', 'FINLAND', 'FRANCE', 'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GREECE', 'GRENADA', 'GUATEMALA', 'GUINEA', 'GUINEA-BISSAU', 'GUYANA', 'HAITI', 'HOLY SEE (VATICAN CITY STATE)', 'HONDURAS', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN, ISLAMIC REPUBLIC OF', 'IRAQ', 'IRELAND', 'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KOREA (SOUTH)', 'KUWAIT', 'KYRGYZSTAN', 'LAO PDR', 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 'LIBYA', 'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MACEDONIA, REPUBLIC OF', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES', 'MALI', 'MALTA', 'MAURITANIA', 'MAURITIUS', 'MEXICO', 'MOLDOVA', 'MONACO', 'MONGOLIA', 'MONTENEGRO', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 'NAMIBIA', 'NEPAL', 'NETHERLANDS', 'NEW ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 'NORWAY', 
'OMAN', 'PAKISTAN', 'PALESTINIAN TERRITORY', 'PANAMA', 'PAPUA NEW GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'POLAND', 'PORTUGAL', 'QATAR', 'REPUBLIC OF KOSOVO', 'ROMANIA', 'RUSSIA', 'RWANDA', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA', 'SAINT VINCENT AND GRENADINES', 'SAN MARINO', 'SAO TOME AND PRINCIPE', 'SAUDI ARABIA', 'SENEGAL', 'SERBIA', 'SEYCHELLES', 'SIERRA LEONE', 'SINGAPORE', 'SLOVAKIA', 'SLOVENIA', 'SOMALIA', 'SOUTH AFRICA', 'SOUTH SUDAN', 'SPAIN', 'SRI LANKA', 'SUDAN', 'SURINAME', 'SWAZILAND', 'SWEDEN', 'SWITZERLAND', 'SYRIAN ARAB REPUBLIC (SYRIA)', 'TAIWAN, REPUBLIC OF CHINA', 'TAJIKISTAN', 'TANZANIA, UNITED REPUBLIC OF', 'THAILAND', 'TIMOR-LESTE', 'TOGO', 'TRINIDAD AND TOBAGO', 'TUNISIA', 'TURKEY', 'UGANDA', 'UKRAINE', 'UNITED ARAB EMIRATES', 'UNITED KINGDOM', 'UNITED STATES OF AMERICA', 'URUGUAY', 'UZBEKISTAN', 'VENEZUELA (BOLIVARIAN REPUBLIC)', 'VIET NAM', 'WESTERN SAHARA', 'YEMEN', 'ZAMBIA', 'ZIMBABWE']
colors = ["greyple", "light_grey", "lighter_grey", "magenta", "mro", "orange", "purple", "r", "red", "teal", "to_rgb"]

class Statistics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = 'ow', aliases=[ "overwatch"])
    async def ow(self, ctx, *, parameters):
        # Parsing parameters
        param_list = parameters.split('|')
        
        # Checking for whitespaces
        for n in range(0, len(param_list)):
            if ' ' in param_list[n]:
                param_list[n] = param_list[n].replace(' ', '')
            if '#' in param_list[n]:
                param_list[n] = param_list[n].replace('#', '-')

            

        # Assigning each parameter to its variable
        for par in param_list:
            if par == 'us' or par == 'eu' or par == 'asia':
                region = par
            elif '-' in par:
                battle_tag = par
            if par == 'pc':
                platform = par
            elif par == 'xbox':
                platform = par
            elif par == 'ps4':
                platform = par

        if len(param_list) < 3:
            await ctx.send("You are missing at least one parameter.\n```>ow platform(pc etc) | region(us, eu, asia) | battletag(Domi#11705) | optional(heroes: ana,bastion,junkrat etc```")
            return
        
        # General Lookup
        if len(param_list) == 3:
            r = requests.get(f"https://ow-api.com/v1/stats/{platform}/{region}/{battle_tag}/profile")
            ow_stats = dict(r.json())
            if ow_stats.get("error") is not None:
                await ctx.send("That player does not exist.")
                return
            
            if bool(ow_stats.get("private")) == False:
                # Assigning Variables
                # General Information
                player_name = ow_stats.get('name')
                pfp_icon = ow_stats.get('icon')
                endorsement = ow_stats.get('endorsement')
                total_games_won = ow_stats.get('gamesWon')
                level = int(ow_stats.get('prestige')) * 100 + int(ow_stats.get('level'))


                # QP Awards
                qp_cards = ow_stats.get('quickPlayStats').get('awards').get('cards')
                qp_b_medals = ow_stats.get('quickPlayStats').get('awards').get('medalsBronze')
                qp_s_medals = ow_stats.get('quickPlayStats').get('awards').get('medalsSilver')
                qp_g_medals = ow_stats.get('quickPlayStats').get('awards').get('medalsGold')

                # QP Games
                qp_games_won = ow_stats.get('quickPlayStats').get('games').get('won')
                qp_gen_sr = ow_stats.get('rating')
                

                # Comp Awards
                cards = ow_stats.get("competitiveStats").get("awards").get("cards")
                b_medals = ow_stats.get("competitiveStats").get("awards").get("medalsBronze")
                s_medals = ow_stats.get("competitiveStats").get("awards").get("medalsSilver")
                g_medals = ow_stats.get("competitiveStats").get("awards").get("medalsGold")

                # Comp Games 
                games_played = ow_stats.get("competitiveStats").get("games").get("played")
                games_won = ow_stats.get("competitiveStats").get("games").get("won")
                games_lost = games_played - games_won

                # Comp Ratings
                comp_srs = {}
                if type(ow_stats.get("ratings")) == list:
                    for dct in ow_stats.get("ratings"):
                        comp_srs[dct.get('role')] = dct.get('level')

                if "damage" not in comp_srs:
                    comp_srs["damage"] = "N/A"
                if "tank" not in comp_srs:
                    comp_srs["tank"] = "N/A"
                if "support" not in comp_srs:
                    comp_srs["support"] = "N/A"
                role_sr_str = ""
                x = 0
                for role, sr in comp_srs.items():
                    if x != len(comp_srs):
                        role_sr_str += f"{role.capitalize()} SR: {sr}\n"
                    else:
                        role_sr_str += f"{role.capitalize()}: SR: {sr}"
                    x += 1

                embed = discord.Embed(
                    title = player_name,
                    description = 'Account Statistics',
                    color = 0xFA9C1D
                    )
                embed.set_image(url="https://webstockreview.net/images/overwatch-logo-png-4.png")
                embed.set_thumbnail(url=pfp_icon)
                
                embed.add_field(name = '**General Information**', value = f"Level: {level}\nEndorsment Level: {endorsement}\n Total Games Won: {total_games_won}", inline = False)
                embed.add_field(name = "**Competitive Play**", value = f"{role_sr_str}", inline=True)
                embed.add_field(name = "⠀", value = f"Games Played: {games_played}\nGames Won: {games_won}\nGames Lost: {games_lost}", inline=True)
                
                embed.add_field(name = "⠀", value = f"Cards: {cards}\nBronze Medals: {b_medals}\nSilver Medals: {s_medals}\nGold Medals: {g_medals}", inline=False)
                embed.add_field(name = '**Quick Play**', value = f"Games Won: {qp_games_won}\nSkill Rating (SR): {qp_gen_sr}\nCards: {qp_cards}", inline=True)
                embed.add_field(name = "⠀", value = f"Bronze Medals: {qp_b_medals}\nSilver Medals: {qp_s_medals}\nGold Medals: {qp_g_medals}" ,inline=True)

                await ctx.send(embed=embed)
            else:
                await ctx.send("Cannot fetch data of a private profile.")
        # Hero Lookup
        elif len(param_list) == 4:
            pass

    @commands.command(name = "covid", aliases=["Coronavirus"])
    async def covid(self, ctx, *, country=None):
        """
        API: https://covid19api.com
        """
        url_link = f"https://api.covid19api.com/summary"
        resp = requests.get(url_link)
        covid_stats = dict(resp.json())
        
        if country is None:
            global_stats = covid_stats["Global"]
            covid_embed = discord.Embed(
                title = "Global COVID-19 Statistics",
                description = f"Valid as of {covid_stats['Date'][:10]}",
                color = 0x99ccff
            )
            covid_embed.add_field(name="New Confirmed Cases", value=format(global_stats["NewConfirmed"], ',d'), inline=True)
            covid_embed.add_field(name="Total Confirmed Cases", value=format(global_stats['TotalConfirmed'], ',d'), inline=True)
            covid_embed.add_field(name="New Deaths", value=format(global_stats['NewDeaths'], ',d'), inline=True)
            covid_embed.add_field(name="Total Deaths", value=format(global_stats['TotalDeaths'], ',d'), inline=True)
            covid_embed.add_field(name="Newly Recovered Cases", value=format(global_stats['NewRecovered'], ',d'), inline=True)
            covid_embed.add_field(name="Total Recovered Cases", value=format(global_stats['TotalRecovered'], ',d'), inline=True)
            covid_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/EarthFlag1.svg/350px-EarthFlag1.svg.png")
            
        else:
            if "USA" in country.upper():
                country = "UNITED STATES OF AMERICA"
            if country.upper() in country_list:
                per_country_stats = covid_stats["Countries"]
                country_index =  country_list.index(country.upper())
                country_stats = per_country_stats[country_index]
                
                covid_embed = discord.Embed(
                    title=f"({country_stats['CountryCode']}) {country_stats['Country']}'s COVID-19 Statistics",
                    description=f"Valid as of {country_stats['Date'][:10]}",
                    color=0x99ccff
                )
                covid_embed.add_field(name="New Confirmed Cases", value=format(country_stats["NewConfirmed"], ',d'), inline=True)
                covid_embed.add_field(name="Total Confirmed Cases", value=format(country_stats['TotalConfirmed'], ',d'), inline=True)
                covid_embed.add_field(name="New Deaths", value=format(country_stats['NewDeaths'], ',d'), inline=True)
                covid_embed.add_field(name="Total Deaths", value=format(country_stats['TotalDeaths'], ',d'), inline=True)
                covid_embed.add_field(name="Newly Recovered Cases", value=format(country_stats['NewRecovered'], ',d'), inline=True)
                covid_embed.add_field(name="Total Recovered Cases", value=format(country_stats['TotalRecovered'], ',d'), inline=True)
                covid_embed.set_thumbnail(url=f"https://www.countryflags.io/{country_stats['CountryCode']}/flat/64.png")
            else:
                await ctx.send("I can't find the stats for that country. Sorry!")
                return
        await ctx.send(embed=covid_embed)

def setup(client):
    client.add_cog(Statistics(client))
