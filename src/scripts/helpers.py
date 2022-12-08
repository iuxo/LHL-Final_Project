
def get_file_contents(filename):
    """ Given a filename, return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


class Game:

    def __init__(self, match):
        self.id = ""

        self.winning_team = 0

        self.blue_wards_placed = 0
        self.blue_wards_killed = 0
        self.blue_champions_killed = 0
        self.blue_elites_killed = 0
        self.blue_plates_destroyed = 0
        self.blue_turrets_destroyed = 0
        self.blue_total_gold = 0
        self.blue_average_level = 1
        self.blue_jungle_monsters_killed = 0
        self.blue_minions_killed = 0
        self.blue_first_blood = 0

        self.red_wards_placed = 0
        self.red_wards_killed = 0
        self.red_champions_killed = 0
        self.red_elites_killed = 0
        self.red_plates_destroyed = 0
        self.red_turrets_destroyed = 0
        self.red_total_gold = 0
        self.red_average_level = 1
        self.red_jungle_monsters_killed = 0
        self.red_minions_killed = 0
        self.red_first_blood = 0

        self.get_match_id(match)
        self.set_winning_team(match)
        self.parse_events(match.get('info').get('frames'))

        # some games end before 10 minutes
        try:
            self.get_team_info(match.get('info').get('frames')[10])
        except:
            self.get_team_info(match.get('info').get('frames')[-1])

    def first_blood(self, event):
        if event.get('killType') == 'KILL_FIRST_BLOOD':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_first_blood = 1
            else:
                self.red_first_blood = 1

    def count_wards_placed(self, event):
        if event.get('type') == 'WARD_PLACED':
            participant = event.get('creatorId')
            if participant in range(1,6):
                self.blue_wards_placed += 1
            else:
                self.red_wards_placed += 1

    def count_ward_kills(self, event):
        if event.get('type') == 'WARD_KILL':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_wards_killed += 1
            else:
                self.red_wards_killed += 1

    def count_champion_kills(self, event):
        if event.get('type') == 'CHAMPION_KILL':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_champions_killed += 1
            else:
                self.red_champions_killed += 1

    def count_elite_kills(self, event):
        if event.get('type') == 'ELITE_MONSTER_KILL':
            participant = event.get('killerTeamId')
            if participant == 100:
                self.blue_elites_killed += 1
            else:
                self.red_elites_killed += 1

    def count_turret_plates_destroyed(self, event):
        if event.get('type') == 'TURRET_PLATE_DESTROYED':
            team = event.get('teamId')
            if team == 200:
                self.blue_plates_destroyed += 1
            else:
                self.red_plates_destroyed += 1

    def count_turrets_destroyed(self, event):
        if event.get('type') == 'BUILDING_KILL':
            team = event.get('teamId')
            if team == 200:
                self.blue_turrets_destroyed += 1
            else:
                self.red_turrets_destroyed += 1

    def parse_events(self, frames):
        for frame in frames[0:11]:
            for event in frame.get('events'):
                self.count_wards_placed(event)
                self.count_ward_kills(event)
                self.count_champion_kills(event)
                self.count_elite_kills(event)
                self.count_turret_plates_destroyed(event)
                self.count_turrets_destroyed(event)
                self.first_blood(event)

    def count_team_gold(self, participants):
        for p in range(1,6):
            self.blue_total_gold += participants.get(f'{p}').get('totalGold')
        for p in range(6,11):
            self.red_total_gold += participants.get(f'{p}').get('totalGold')
    
    def team_average_level(self, participants):
        blue_levels = 0
        red_levels = 0
        for p in range(1,6):
            blue_levels += participants.get(f'{p}').get('level')
        for p in range(6,11):
            red_levels += participants.get(f'{p}').get('level')
        self.blue_average_level = blue_levels / 5
        self.red_average_level = red_levels / 5

    def count_team_cs(self, participants):
        for p in range(1,6):
            self.blue_jungle_monsters_killed += participants.get(f'{p}').get('jungleMinionsKilled')
            self.blue_minions_killed += participants.get(f'{p}').get('minionsKilled')
        for p in range(6,11):
            self.red_jungle_monsters_killed += participants.get(f'{p}').get('jungleMinionsKilled')
            self.red_minions_killed += participants.get(f'{p}').get('minionsKilled')
    
    def get_team_info(self, frame):
        participants = frame.get('participantFrames')

        self.count_team_gold(participants)
        self.team_average_level(participants)
        self.count_team_cs(participants)

    def get_match_id(self, match):
        self.id = match.get('metadata').get('matchId')

    def set_winning_team(self, match):
        self.winning_team = match.get('info').get('frames')[-1].get('events')[-1].get('winningTeam')