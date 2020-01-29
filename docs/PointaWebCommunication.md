# PointaWebCommunication

**Pointa uses HTTP in communication, these are some conventions in Pointa web communication.** 

## ClientSide

### Ingame

Sync (GET)

```json
.../inGame/<key>/?fts=<Time>&r=<LocalRound>&p=<LocalPhase>
```

Insert (POST TO `.../inGame/<key>`)

```json
{Action: [<ATK>, <DEF>, <HEL>]}
```

### Outside Game

POST TO `.../outGame/<key>`

```json
{
    Action: <'Ready' or 'Invite'>,
    Target: <Target player's key>
}
```

***

## ServerSide

### Ingame

Sync Response

```json
{
    UpdatedLog: [...] // According to the 'finalTimeStamp'
    playerStats: [...]
}
```
