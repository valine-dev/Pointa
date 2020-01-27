### ClientSide
When in game, Clients send requests in short time period in json with the format like.
```json
{
    lastTimestamp: ..., // Confirming last command
    localVar: {
        round: 0,
        phase: 0
    }
    
}
```

```json
{
    Action: [Ready / Invite],
    Target: TargetKey
}
```