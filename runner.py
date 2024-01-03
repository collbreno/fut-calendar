import argparse

from scripts import get_teams_from_competition, create_calendars, get_markdown, make_calendars_public


def __run_script(script_name: str):
    if script_name == 'get_serie_a':
        get_teams_from_competition.get_serie_a()

    elif script_name == 'create_calendars':
        create_calendars.create_all()

    elif script_name == 'get_markdown':
        get_markdown.print_all()
    
    else:
        print(f'Invalid script: {script_name}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('script', help='Name of the script to run')
    args = parser.parse_args()

    __run_script(args.script)