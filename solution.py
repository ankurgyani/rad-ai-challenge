#! /usr/bin/python
import argparse
import fileinput
import locale
import re
import sys

class TeamInfo(object):
    """Class to store team info"""
    def __init__(self, name):
        self.name = name
        self.points = 0

    def increment_points(self, pts):
        self.points += pts
    
    def __eq__(self, other):
        if isinstance(other, TeamInfo):   
            return self.name == other.name
        return False

    ## sorting function    
    def __lt__(self, other):
        if(self.points == other.points):
            return self.name < other.name  ## since the names have to be sorted alphabetically in ascending order
        return self.points > other.points ## since the points have to be sorted descending order

    
class LeaderBoard(object):
    def __init__(self):
        self.teams = []
    
    def _record_win(self, team):
        team.increment_points(3)

    def _record_tie(self, team1, team2):
        team1.increment_points(1)
        team2.increment_points(1)
    
    def _record_result(self, match):
        """Read match details and record result
        
        Args:
            match: match details - teams played and scores of each team
        """
        name1, name2, score1, score2 = self._parse_input(match)
        team1 = TeamInfo(name1)
        team2 = TeamInfo(name2)
        if team1 not in self.teams:
            self.teams.append(team1) 
        if team2 not in self.teams:
            self.teams.append(team2) 
        if score1 == score2:
            self._record_tie(self.teams[self.teams.index(team1)], self.teams[self.teams.index(team2)])  #if tie increment points for both teams
        else:
            self._record_win(self.teams[self.teams.index(team1)] if score1 > score2 else self.teams[self.teams.index(team2)])
        
        
    def _parse_input(self, match):
        """Parse input match details

        Args:
            match: details of match team names and scores 

        Returns:
            teams names and score by each team
        """
        teams = []
        scores = []
        for record in match.split(','):
            teams.append(re.search("(\S+.*?)\s+\d+\s*$", record).group(1))
            scores.append(int(re.search("(\d+)\s*$", record).group(1)))
        return teams[0], teams[1], scores[0], scores[1]
    
            
    def print_rankings(self):
        """Print ranking of teams"""
        self.teams.sort()
        rank = 1
        tmp = 0
        for i in range(0, len(self.teams)-1):
            curr_team = self.teams[i]
            next_team = self.teams[i+1]
            print("%d. %s, %d pts" % (rank, curr_team.name, curr_team.points))
            if (curr_team.points == next_team.points):
                tmp += 1
            else:
                rank += tmp + 1
                tmp = 0
        print("%d. %s, %d pts" % (rank, self.teams[-1].name, self.teams[-1].points))


def get_input():
    """Do arg parsing"""
    parser = argparse.ArgumentParser(description='Ranking for soccer')
    parser.add_argument(
        'file', nargs='?', help=(
            "File containing match results. If not specified, "
            "the same format is expected via standard input pipe. "
            "See README.md for format details."
        ))
    args = parser.parse_args()
    if args.file:
        def line_generator():
            with open(args.file) as f:
                for line in f:
                    yield line
        return line_generator()
    elif not sys.stdin.isatty():
        return (line for line in fileinput.input())
    else:
        parser.print_help()
        exit()


def main():
    leader_board = LeaderBoard()
    for line in get_input():
        leader_board._record_result(line)
    leader_board.print_rankings()


if __name__ == '__main__':
    main()