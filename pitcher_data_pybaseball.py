import pybaseball
import pandas as pd
import json

# Commented out section will be used for machine learning data
def player(first_name, last_name, start_date, end_date):
    player_info = pybaseball.playerid_lookup(last_name, first_name)
    # if (player_info['mlb_played_last'][0] - player_info['mlb_played_first'][0]) < 10:
    #     start_year = int(player_info['mlb_played_first'][0])
    # else:
    #     start_year = int(player_info['mlb_played_last'][0] - 10)
        
    player_id = player_info['key_mlbam'][0]
    # player_info = [player_id,start_year,str(player_info['mlb_played_last'][0])]
    
    data = pybaseball.statcast_pitcher(start_dt = start_date, end_dt = end_date, player_id = player_info[0])
    data = data.reset_index(drop = True)
    return data

# Seperate the balls, stikes, and live balls in play
def ball_and_strike(game_data):
    balls = pd.DataFrame(columns = ['pitch_type', 'description'])
    strikes = pd.DataFrame(columns = ['pitch_type', 'description'])
    live = pd.DataFrame(columns = ['pitch_type', 'description'])
    for x in range(len(game_data)):
        if game_data['description'][x] == 'ball':
            details = game_data[['pitch_type','description', 'plate_x', 'plate_z']].iloc[[x]]
            balls = balls.append(details)
        elif game_data['description'][x] == 'hit_into_play':
            details = game_data[['pitch_type','description', 'plate_x', 'plate_z']].iloc[[x]]
            live = live.append(details)
        else:
            details = game_data[['pitch_type','description', 'plate_x', 'plate_z']].iloc[[x]]
            strikes = strikes.append(details)
    return balls, strikes, live

# Send data to a json file to be displayed in a scatter plot
def pitch_graph(pitching_breakdowns):
    pitch_ball = pitching_breakdowns[0]
    balls_xs = [x for x in pitch_ball['plate_x'].reset_index(drop = True)]
    balls_zs = [x for x in pitch_ball['plate_z'].reset_index(drop = True)]
    balls_type = [x for x in pitch_ball['pitch_type'].reset_index(drop = True)]
    balls_colors = ['blue' for x in range(len(balls_xs))]
    

    pitch_strike = pitching_breakdowns[1]
    strikes_xs = [x for x in pitch_strike['plate_x'].reset_index(drop = True)]
    strikes_zs = [x for x in pitch_strike['plate_z'].reset_index(drop = True)]
    strikes_type = [x for x in pitch_strike['pitch_type'].reset_index(drop = True)]
    strikes_colors = ['red' for x in range(len(strikes_xs))]

    pitch_hit = pitching_breakdowns[2]
    hit_xs = [x for x in pitch_hit['plate_x'].reset_index(drop = True)]
    hit_zs = [x for x in pitch_hit['plate_z'].reset_index(drop = True)]
    hit_type = [x for x in pitch_hit['pitch_type'].reset_index(drop = True)]
    hit_colors = ['green' for x in range(len(hit_xs))]


    xs = strikes_xs + balls_xs + hit_xs
    zs = strikes_zs + balls_zs + hit_zs
    pitch_type = strikes_type + balls_type + hit_type
    colors = strikes_colors + balls_colors + hit_colors

    values = {
        'plate_x': xs,
        'plate_z': zs,
        'pitch_type': pitch_type,
        'indicator': colors
    }

    jsonString =  json.dumps(values)
    jsonFile = open('data/pitcher_graph_data.json', 'w')
    jsonFile.write(jsonString)
    jsonFile.close()
    return jsonString

def main(first_name, last_name, start_date, end_date, team):
    first_name = first_name.lower()
    last_name = last_name.lower()
    start_date = str(start_date)
    end_date = str(end_date)

    player_data = player(first_name,last_name,start_date,end_date)
    pitch_breakdowns = ball_and_strike(player_data)
    pitch_graph(pitch_breakdowns)