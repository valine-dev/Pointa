## ClientSide
### **Ingame**
Sync (GET)
```
.../inGame/<key>/?finalTimeStamp=<Time>&round=<LocalRound>&phase=<LocalPhase>
```

Insert (POST TO `.../inGame/<key>`)
```json
{Action: [<ATK>, <DEF>, <HEL>]}
```

### **Outside Game**
POST TO `.../outGame/<key>`
```json
{
    Action: <'Ready' or 'Invite'>,
    Target: <Target player's key>
}
```

***

## ServerSide
### **Ingame**
Sync Response
```json
{
    UpdatedLog: [...] // According to the 'finalTimeStamp'
    playerStats: [...]
}
```