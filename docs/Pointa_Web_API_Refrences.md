# Pointa Web API Refrences


## Requests

Sync (GET)

```
.../inGame/<key>/?fts=<Time>&r=<LocalRound>&p=<LocalPhase> // Time's length must be 13 bytes
```

Insert (POST TO `.../inGame/<key>`)

```json
{Action: [<ATK>, <DEF>, <HEL>]}
```

POST TO `.../outGame/<key>`

```json
{
    Action: <'Ready' or 'Invite'>, // Use Ready to Login, Invite to Send Invite request
    Target: <Target player's key>
}
```

***

## Responses

#### Sync Response
```json
{
    UpdatedLog: [ // According to the 'finalTimeStamp'
        {
            "time": int, // 13 bytes length
            "action": str,  // Cases will be shown later
            "actor": str,
            "value": // Depends on action
        }
    ] 
    playerStats: []
}
```
And possible actions are:

> |Action|Values|
> |:----:|:----:|
> |roundBegin|actor="game", value=int ServerRound|
> |phaseBegin|actor="game", value={"num":int ServerRound, "phase":ServerPhase}|
> |pointRolled|actor=str player'sKey, value=int RolledPoint|
> |atkJudged|actor=str player'sKey, value=int RolledPoints|
> |playerKilled|actor="game", value=str player'sKey|
> |gameEnd|actor="game"|





