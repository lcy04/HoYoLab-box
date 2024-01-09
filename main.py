import requests
import os

hoyo_uid = 114797891
hoyo_token = 3QVqmzK3t9e0ObpDcR1hwT3PohtlYAtU5wJycZeW
game_code = '26'

# Game Code
# 2 : Genshin Impact
# 6 : Honkai: Star Rail

gh_api_url = 'https://api.github.com'
gh_token =  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
gist_id = lcy04

def get_data_from_hoyolab(hoyo_uid, hoyo_token) :

    headers = {
        'x-rpc-language': 'en-us',
        'Cookie': f'ltuid={hoyo_uid}; ltoken={hoyo_token};'
    }

    requestData = requests.get(
        url=f'https://bbs-api-os.hoyolab.com/game_record/card/wapi/getGameRecordCard?uid={hoyo_uid}',
        headers=headers
    )

    return_list = []
    if requestData.status_code == 200 :
        jsonData = requestData.json()
        for eachGame in jsonData['data']['list'] :
            if eachGame['game_id'] == 2 :
                return_list.append(['Genshin Impact'])
            elif eachGame['game_id'] == 6 :
                return_list.append(['Honkai: Star Rail'])
            return_list[-1].append(str(eachGame['level']))
            for eachData in eachGame['data'] :
                if 'Active' in eachData['name'] :
                    return_list[-1].append(eachData['value'])
                elif 'Characters' in eachData['name'] :
                    return_list[-1].append(eachData['value'])
                elif 'Achievements' in eachData['name'] :
                    return_list[-1].append(eachData['value'])
        return return_list
    else : return 'Error occured'

def update_gist(gh_api_url, gh_token, gist_id, hoyo_data) :

    padding = ' '
    for i in range(1, len(hoyo_data[0])) :
        len_for_padding = max(len(hoyo_data[0][i]), len(hoyo_data[1][i]))
        hoyo_data[0][i] = hoyo_data[0][i].rjust(len_for_padding, padding)
        hoyo_data[1][i] = hoyo_data[1][i].rjust(len_for_padding, padding)

    str_hoyo_data = ''
    for game in hoyo_data :
        str_hoyo_data += '🎮 ' + game[0] + '\n'\
            + ('⚔️ Lv.' + game[1]).ljust(13, padding)\
            + ('🤝 ' + game[3] + ' chars').ljust(12, padding)\
            + ('🕹️ ' + game[2] + ' days').ljust(13, padding)\
            + ('🏆 ' + game[4] + ' achvmnts').ljust(12, padding)\
            + '\n\n'

    data = {
        'description' : '🎮 HoYoverse gameplay stats',
        'files' : {'🎮 HoYoverse gameplay stats' : {'content' : str_hoyo_data}}
    }

    request = requests.patch(
        url=f'{gh_api_url}/gists/{gist_id}',
        headers={
            'Authorization': f'token {gh_token}',
            'Accept': 'application/json'
        },
        json=data
    )

    try :
        request.raise_for_status()
    except requests.exceptions.HTTPError as e :
        print(e)
        return 'Error retrieving data'

if __name__ == '__main__' :
    hoyo_data = get_data_from_hoyolab(hoyo_uid, hoyo_token)
    update_gist(gh_api_url, gh_token, gist_id, hoyo_data)
