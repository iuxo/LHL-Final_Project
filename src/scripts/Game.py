class Game:
    """
    A class to represent a game of League of Legends at the 10 minute mark,
    or the end of the game if it ends before 10 minutes.

    ...

    Attributes:
    -----------
    id : str
        id of the game
    winning_team : int
        winner of the game where 100 = blue side wins, 200 = red side wins
    ------------
    The rest of the attributes are symmetrical for blue side and red side.
    ------------
    wards_placed : int
        total number of wards placed by blue/red side in the game
    wards_killed : int
        total number of wards killed by blue/red side in the game
    champions_killed : int
        total number of champions killed by blue/red side in the game
    elites_killed : int
        total number of elite monsters killed by blue/red side in the game
    plates_destroyed : int
        total number of turret plates destroyed by blue/red side in the game
    turrets_destroyed : int
        total number of turrets destroyed by blue/red side in the game
    total_gold : int
        total gold of blue/red side in the game
    average_level : float
        average level of blue/red side in the game
    jungle_monsters_killed : int
        total number of jungle monsters killed by blue/red side in the game
    minions_killed : int
        total number of minions killed by blue/red side in the game
    first_blood : int
        number of first bloods obtained by blue/red side in the game,
        can only be one of (0,1)
    """
    def __init__(self, match):
        """
        Initialize the attributes of the game, then get the match id, set the winning team,
        parse through the game and get team stats the 10 minute mark.

        Parameters
        ----------
        match : str
            the id of the game that is represented

        Returns
        -------
        None
        """
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
        """
        Set which team obtained first blood.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline

        Returns
        -------
        None
        """
        if event.get('killType') == 'KILL_FIRST_BLOOD':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_first_blood = 1
            else:
                self.red_first_blood = 1

    def count_wards_placed(self, event):
        """
        Increment number of wards placed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline

        Returns
        -------
        None
        """
        if event.get('type') == 'WARD_PLACED':
            participant = event.get('creatorId')
            if participant in range(1,6):
                self.blue_wards_placed += 1
            else:
                self.red_wards_placed += 1

    def count_ward_kills(self, event):
        """
        Increment number of wards killed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline
            
        Returns
        -------
        None
        """
        if event.get('type') == 'WARD_KILL':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_wards_killed += 1
            else:
                self.red_wards_killed += 1

    def count_champion_kills(self, event):
        """
        Increment number of champions killed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline
            
        Returns
        -------
        None
        """
        if event.get('type') == 'CHAMPION_KILL':
            participant = event.get('killerId')
            if participant in range(1,6):
                self.blue_champions_killed += 1
            else:
                self.red_champions_killed += 1

    def count_elite_kills(self, event):
        """
        Increment number of elite monsters killed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline
            
        Returns
        -------
        None
        """
        if event.get('type') == 'ELITE_MONSTER_KILL':
            participant = event.get('killerTeamId')
            if participant == 100:
                self.blue_elites_killed += 1
            else:
                self.red_elites_killed += 1

    def count_turret_plates_destroyed(self, event):
        """
        Increment number of turret plates destroyed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline
            
        Returns
        -------
        None
        """
        if event.get('type') == 'TURRET_PLATE_DESTROYED':
            team = event.get('teamId')
            if team == 200:
                self.blue_plates_destroyed += 1
            else:
                self.red_plates_destroyed += 1

    def count_turrets_destroyed(self, event):
        """
        Increment number of turrets destroyed depending on team.

        Parameters
        ----------
        event : dictionary
            event obtained from match timeline
            
        Returns
        -------
        None
        """
        if event.get('type') == 'BUILDING_KILL':
            team = event.get('teamId')
            if team == 200:
                self.blue_turrets_destroyed += 1
            else:
                self.red_turrets_destroyed += 1

    def parse_events(self, frames):
        """
        For the first 10 frames of a game, parse through each event.
        Counting wards placed, wards killed, champions killed, elites killed,
        turret plates destroyed, turrets destroyed, and which side obtained first blood.

        Parameters
        ----------
        frames : list
            list of frames obtained from match timeline
            
        Returns
        -------
        None
        """
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
        """
        Get the gold a player holds at 10 minutes and add them together depending
        on team.

        Parameters
        ----------
        participants : list
            list of players in a game where blue team is (1-5), red is (6-10)
        
        Return
        ------
        None
        """
        for p in range(1,6):
            self.blue_total_gold += participants.get(f'{p}').get('totalGold')
        for p in range(6,11):
            self.red_total_gold += participants.get(f'{p}').get('totalGold')
    
    def team_average_level(self, participants):
        """
        Get player level at 10 minutes and calculate the two teams averages.

        Parameters
        ----------
        participants : list
            list of players in a game where blue team is (1-5), red is (6-10)

        Return
        ------
        None
        """
        blue_levels = 0
        red_levels = 0
        for p in range(1,6):
            blue_levels += participants.get(f'{p}').get('level')
        for p in range(6,11):
            red_levels += participants.get(f'{p}').get('level')
        self.blue_average_level = blue_levels / 5
        self.red_average_level = red_levels / 5

    def count_team_cs(self, participants):
        """
        Count how many jungle creeps and minions players have killed, and add them together
        depending on the team.

        Parameters
        ----------
        participants: list
            list of players in a game where blue team is (1-5), red is (6-10)
        
        Return
        ------
        None
        """
        for p in range(1,6):
            self.blue_jungle_monsters_killed += participants.get(f'{p}').get('jungleMinionsKilled')
            self.blue_minions_killed += participants.get(f'{p}').get('minionsKilled')
        for p in range(6,11):
            self.red_jungle_monsters_killed += participants.get(f'{p}').get('jungleMinionsKilled')
            self.red_minions_killed += participants.get(f'{p}').get('minionsKilled')
    
    def get_team_info(self, frame):
        """
        Helper function to get team gold, average level, and team creep score.

        Parameters
        ----------
        frame : dictionary
            information from a match time line at each minute of the game

        Return
        ------
        None
        """
        participants = frame.get('participantFrames')

        self.count_team_gold(participants)
        self.team_average_level(participants)
        self.count_team_cs(participants)

    def get_match_id(self, match):
        """
        Set the match id attribute.

        Parameters
        ----------
        match : MatchTimeLineDTO
            timeline object from RiotGames API

        Return
        ------
        None
        """
        self.id = match.get('metadata').get('matchId')

    def set_winning_team(self, match):
        """
        Set the winning team of a game

        Parameters
        ----------
        match : MatchTimeLineDTO
            timeline object from RiotGame API
        
        Return
        ------
        None
        """
        self.winning_team = match.get('info').get('frames')[-1].get('events')[-1].get('winningTeam')
