def build_payload(ctx: list[dict], reply_to_id: int | None, msg, ts: int) -> list[dict]:
    by_id = {m.get("message_id"): m for m in ctx if m.get("message_id")}
    chain_ids: list[int] = []
    rid = reply_to_id
    while rid is not None and rid in by_id and rid not in chain_ids and len(chain_ids) < 5:
        chain_ids.append(rid)
        rid = by_id[rid].get("reply_to")
    chain_ids.reverse()
    ordered = [m for m in ctx if m.get("message_id") not in set(chain_ids)] + [by_id[i] for i in chain_ids]
    payload = [
        {
            "username": m["username"],
            "text": m["text"],
            "ts": m.get("ts"),
            "user_id": m.get("user_id"),
            "message_id": m.get("message_id"),
            "reply_to": m.get("reply_to"),
        }
        for m in ordered
    ]
    rep = msg.reply_to_message
    rep_text = (rep.text or rep.caption) if rep else None
    if rep and rep.message_id not in by_id and rep_text and rep_text not in [m["text"] for m in payload]:
        rep_user = rep.from_user
        payload.append({
            "username": rep_user.full_name if rep_user else "anon",
            "text": rep_text,
            "ts": int(rep.date.timestamp()) if rep.date else ts,
            "user_id": rep_user.id if rep_user else None,
            "message_id": rep.message_id,
            "reply_to": None,
        })
    return payload
