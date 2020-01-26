from .Pointa import Pointa, Player
from .DynamicEventLoop import DynamicEventLoop
import asyncio
import time

'''Pointa! PlayableClientDemo
Pointa Client workflow in a loop
Get The Game Log -> Excute The Diffierences to Sync -> Wait for Input
'''


splitLine = '------------------------------'

# Setting up Enviroment
p1, p2 = Player('player1'), Player('player2')
ps = {
    'player1': p1,
    'player2': p2
}
Pointa = Pointa(p1, p2)
Loop = asyncio.get_event_loop()
Del = DynamicEventLoop(loop=Loop)
Del.append(Pointa, Pointa.main())

# Run Task Thread
Del.run()

local_log = []

local_var = {
    'Round': 0,
    'Phase': 0
}


Switch = True


def Write():
    global Switch
    Switch = False

    for k, p in ps.items():
        print(p.key, repr(p.properties))

    p1a = input(
        'Actions for player1("atk,def,hel")> '
        ).split(',')
    p2a = input(
        'Actions for player2("atk,def,hel")> '
        ).split(',')

    print('waiting!')

    p1.action(
        {
            0: int(p1a[0]),
            1: int(p1a[1]),
            2: int(p1a[2])
        }
    )

    p2.action(
        {
            0: int(p2a[0]),
            1: int(p2a[1]),
            2: int(p2a[2])
        }
    )


def Read():
    global Switch
    # Syncing
    temp = Pointa.getLog()  # If it's a web client, get
    diff = [i for i in temp if i not in local_log]
    # Excute diff
    for cmd in diff:
        if cmd['action'] == 'roundBegin':
            print(splitLine)
            local_var['Round'] = cmd['value']
            print('Round ', str(cmd['value'] - 1), ' Settled!')
            Switch = True
        if cmd['action'] == 'pointRolled':
            print(f'{ps[cmd["actor"]].key} Rolled {cmd["value"]} Pts!')
        if cmd['action'] == 'phaseBegin':
            local_var['Phase'] = cmd['value']['phase']
        if cmd['action'] == 'atkJudge':
            print(
                f'{ps[cmd["actor"]].key} Rolled {cmd["value"]} for atk judge!'
                )
        local_log.append(cmd)
    if local_var['Phase'] == 2 and Switch:
        Write()


# Main Game Loop
while True:
    # Sync latency
    time.sleep(0.5)
    Read()
