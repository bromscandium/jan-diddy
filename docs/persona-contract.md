# Persona contract (bot side)

Bot owns: WHEN to reply (triggers), WHICH context to send, and the success SIGNAL
(scoring + per-user profiles). Engine owns: WHAT to reply (prompt, model, RAG).

## Triggers — two independent tracks

`core/llm.py`:

```
TrackConfig:  min_messages, min_minutes, probability, cooldown_minutes
TriggerConfig:
    active_hours, reply_probability, prewarm_messages, prewarm_minutes
    spontaneous: TrackConfig
    addressed:   TrackConfig

PROD  spont(20, 30, 0.15, 20)  addr(2, 0, 0.7, 3)
DEBUG spont(2,  0,  1.0,  0)   addr(1, 0, 1.0, 0)
```

- spontaneous: random injection under prior conditions.
- addressed: fires when the bot is pinged (@mention) or replied-to. Own counter,
  more permissive; DEBUG ~ always.

## Redis keys (prefix `p = jd:{chat_id}:{thread|none}`)

```
{p}:buf                       list  message buffer
{p}:spont                     hash  count, last_response_ts, cooldown_until, prewarmed
{p}:addr                      hash  count, last_response_ts, cooldown_until
jd:pending:{chat}:{bot_msg}   str   json{context, reply, target_user_id, score, saved}
jd:lastbot:{chat}:{thread}    str   bot_message_id
jd:profile:{user_id}          hash  engagement cache (source of truth = Postgres)
```

## services/state.py

```
record_incoming(chat_id, thread_id, user_id, username, text, message_id, ts)
get_context(chat_id, thread_id) -> list[dict]
get_track(chat_id, thread_id, track) -> dict
register_reply(chat_id, thread_id, track, now, cooldown_minutes)
mark_prewarmed(chat_id, thread_id)
```

## services/triggers.py

```
should_reply(track, state, cfg, bias=1.0) -> bool
should_prewarm(state_spont, cfg) -> bool
```

## services/scoring.py (graded)

```
REACTION_WEIGHTS: dict[str,int]   APPROVAL_KEYWORDS: set[str]   SCORING_WINDOW=120
register_pending(chat_id, thread_id, bot_message_id, context, reply, target_user_id)
last_bot_message(chat_id, thread_id) -> int | None
apply_reaction(chat_id, bot_message_id, emoji)
apply_reply_signal(chat_id, bot_message_id, text)
```

Score accumulates in the pending payload; SuccessfulDialogs.score = running total;
each signal also calls profiles.record(target_user_id, delta).

## services/profiles.py (new)

```
record(user_id, username, delta) -> None
get(user_id) -> dict
bias(user_id) -> float
```

## models — UserProfiles (LLMModel, schema llm)

```
user_id (BigInt, unique), username (Text null), engagement_score (Int=0),
replies_to_them (Int=0), successes (Int=0), last_seen (Datetime null)
```

## persona_client.generate

```
generate(messages, chat_id, thread_id, mode, target) -> str | None
mode: "spontaneous" | "addressed"
target: {"user_id","username","text"} | None
```

## Handlers pull from Update

listener: addressed = mention "@<bot username>" OR reply to last_bot_message;
track = addr|spont; target = this message; bias = profiles.bias(user_id).
reactions: emoji = message_reaction.new_reaction[-1].emoji -> scoring.apply_reaction.

## Engine GenerateRequest (frozen now, handled later)

```
mode: "spontaneous" | "addressed" | None
target: {user_id, username, text} | None
```
