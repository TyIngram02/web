from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def display_output():
    import requests
    import json
    import tls_client
    from tabulate import tabulate


    w = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    requests = tls_client.Session(
        client_identifier="chrome112",
    )

    response1 = requests.get('https://api.prizepicks.com/projections').json()
    prizepicks = response1
    underdog_req = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines").json()
    underdog = underdog_req

    udlist = [] #underdog players name
    pplist = [] #underdog players name
    matchingnames = [] #seperate list for matching ud names == prizepicks names
    tabled_data = []

    #looping over the array
    for appearances in underdog["over_under_lines"]:
        #filtering for sport type
        underdog_sport = ''.join(appearances["over_under"]["title"].split()[0:1])
        #title is equal to players name/// using split method to only get first name
        underdog_title = ''.join(appearances["over_under"]["title"].split()[1:2])
        #display stat is equal to prop// ex map 1 kills
        UDdisplay_stat = f"{appearances['over_under']['appearance_stat']['display_stat']}"
        #stat value is equal to the prop value ex 5.5 /// so on
        UDstat_value = appearances['stat_value']
        #filter out names for esports only
        if UDdisplay_stat == 'Kills on Map 1+2' and underdog_sport == 'CS:GO':
            csgokills = UDdisplay_stat = 'CSGO MAPS 1-2 KILLS'
        if UDdisplay_stat == 'Headshots on Maps 1+2' and underdog_sport == 'CS:GO':
            csgohs = UDdisplay_stat = 'CSGO MAPS 1-2 HEADSHOTS'
        if UDdisplay_stat == 'Kills on Map 1' and underdog_sport == 'LoL:':
            lolkills = UDdisplay_stat = 'LOL MAP 1 KILLS'
        if UDdisplay_stat == 'Kills on Map 1+2' and underdog_sport == 'LoL:':
            lolkills = UDdisplay_stat = 'LOL MAP 1-2 KILLS'
        if UDdisplay_stat == 'Kills on Map 3' and underdog_sport == 'CoD:':
            codmap3 = UDdisplay_stat = 'COD MAP 3 K'
        if UDdisplay_stat == 'Kills on Maps 1+2+3' and underdog_sport == 'CoD:':
            codallmaps = UDdisplay_stat = 'COD MAPS 1-3 KILLS'
        if UDdisplay_stat == 'Kills on Map 1' and underdog_sport == 'CoD:':
            codmap1 = UDdisplay_stat = 'COD MAP 1 KILLS'
        if UDdisplay_stat == 'Kills on Maps 1+2+3' and underdog_sport == 'Val:':
            valo = UDdisplay_stat = 'VAL MAPS 1-3 KILLS'
        if UDdisplay_stat == 'Kills in Game 1+2' and underdog_sport == 'Dota':
            DotaPP = UDdisplay_stat = 'DOTA MAPS 1-2 KILLS'
        if UDdisplay_stat == 'CSGO MAPS 1-2 KILLS' or UDdisplay_stat == 'CSGO MAPS 1-2 HEADSHOTS' or UDdisplay_stat == 'LOL MAP 1 KILLS' or UDdisplay_stat == 'COD MAP 3 KILLS' or UDdisplay_stat == 'COD MAPS 1-3 KILLS' or UDdisplay_stat == 'COD MAP 1 KILLS' or UDdisplay_stat == 'VAL MAPS 1-3 KILLS' or UDdisplay_stat =='DOTA MAPS 1-2 KILLS' or UDdisplay_stat =='LOL MAP 1-2 KILLS':
        #creating a dictionary
            uinfo = {"Name": underdog_title.lower(), "Stat": UDdisplay_stat, "Line": UDstat_value}
            udlist.append(uinfo)
            
    #start if prizepicks//loop array

    for included in prizepicks['included']:
        #get id we will match this later o
        PPname_id = included['id']
        #getting prizepicks prop name
        PPname = included['attributes']['name']
        if 'team' in included['attributes']:
                teamname = included['attributes']['team']
        
        #nested loop must go thru data
        for data1 in prizepicks['data']:
            #ppid will match this to id to get correct information
            PPid = data1['relationships']['new_player']['data']['id']
            #getting pp line //ex map 1-2 kills
            PPprop_value = data1['attributes']['line_score']
            #gettting value// ex 7.5 kills
            PPprop_type = data1['attributes']['stat_type']
            
            if 'league' in included['attributes']:
                Sport_type = included['attributes']['league']
            #filtering esports props only
            if PPprop_type == 'MAPS 1-2 Kills' and PPname_id == PPid and Sport_type =='CSGO':
                ppcsgokills = PPprop_type= 'CSGO MAPS 1-2 KILLS'
            if PPprop_type == 'MAPS 1-2 Headshots' and PPname_id == PPid and Sport_type == 'CSGO':
                ppcsheadshots = PPprop_type = 'CSGO MAP 1-2 HEADSHOTS'
            if PPprop_type == 'MAP 1 Kills' and PPname_id == PPid and Sport_type =='LoL':
                lolpp = PPprop_type = 'LOL MAP 1 KILLS'
            if PPprop_type == 'MAPS 1-2 Kills' and PPname_id == PPid and Sport_type =='LoL':
                lolpp = PPprop_type = 'LOL MAP 1-2 KILLS'
            if PPprop_type == 'MAP 3 Kills' and PPname_id == PPid and Sport_type =='COD':
                codmp3pp = PPprop_type = 'COD MAP 3 KILLS'
            if PPprop_type == 'MAPS 1-3 Kills' and PPname_id == PPid and Sport_type =='COD':
                codallkills = PPprop_type = 'COD MAPS 1-3 KILLS'
            if PPprop_type == 'MAP 1 Kills' and PPname_id == PPid and Sport_type == 'COD':
                codmp1pp = PPprop_type = 'COD MAP 1 KILLS'
            if PPprop_type == 'MAPS 1-2 Kills' and PPname_id == PPid and Sport_type == 'VAL':
                valallmp = PPprop_type = 'VAL MAPS 1-2 KILLS'
            if PPprop_type == 'MAPS 1-3 Kills' and PPname_id == PPid and Sport_type == 'VAL':
                valallmp = PPprop_type = 'VAL MAPS 1-3 KILLS'
            if PPprop_type == 'Maps 1-2 First Blood' and PPname_id == PPid and Sport_type == 'VAL':
                valallmpFB = PPprop_type = 'VAL MAPS 1-2 First Blood'
            if PPprop_type == 'MAP 3 Kills' and PPname_id == PPid and Sport_type == 'VAL':
                valallmpMP3 = PPprop_type = 'VAL MAP 3 KILLS'
            if PPprop_type == 'MAPS 1-2 Kills' and PPname_id == PPid and Sport_type== 'Dota2':
                DotaPP = PPprop_type = 'DOTA MAPS 1-2 KILLS'
            if PPprop_type == 'CSGO MAPS 1-2 KILLS' or PPprop_type == 'CSGO MAPS 1-2 HEADSHOTS' or PPprop_type == 'LOL MAP 1 KILLS' or PPprop_type == 'COD MAP 3 KILLS' or PPprop_type == 'COD MAPS 1-3 KILLS' or PPprop_value == 'COD MAP 1 KILLS' or PPprop_type == 'VAL MAPS 1-2 KILLS' or PPprop_value == 'DOTA MAPS 1-2 KILLS' or PPprop_type == 'LOL MAP 1-2 KILLS' or PPprop_type == 'VAL MAPS 1-3 KILLS':
                ppinfo ={"Name": PPname.lower(), "Team": teamname, "Stat": PPprop_type, "Line": PPprop_value}
                pplist.append(ppinfo)
                

    for udn in udlist:
        for ppn in pplist:
            if udn["Name"] == ppn["Name"] and udn['Stat'] == ppn['Stat']:
                final = {"Name": udn["Name"] ,"Stat":udn["Stat"], "Team": ppn["Team"], "UD": float(udn["Line"]), "PP": float(ppn["Line"]), "Dif": abs(float(udn["Line"]) - float(ppn["Line"]))}
                if final['Dif'] >=1.0 or final['Dif'] <=-1.0:
                    tabled_data.append(final)
                    def sort_key(d):
                        return d["Dif"]
                    tabled_data.sort(key=sort_key, reverse=True)
    headings = ("Name","Stat","Team","PP","UD","DIF")
    tabled_data1 = tabled_data
       
    return render_template('index.html',headings=headings, tabled_data=tabled_data1)
if __name__ == '__main__':
    app.run()
    print()
