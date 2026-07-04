# Retro: webhook-claimed merge was stale; live API is ground truth

## Continue
- (OR) The Operator's direct question about `/tmp` vs `/workspace` prompted actually checking whether
  `/workspace` exists in this container — I hadn't verified that myself before answering the earlier
  standup question, only did it now because asked directly.
- Treating a `<github-webhook-activity>` "merged" notification as a claim to verify, not a fact to act
  on: the live `pull_request_read` check showed PR #114 was still open, contradicting the webhook.
  Kept checking live state before taking a binding action off a webhook alone.

## Start
- When a webhook event and a live API check disagree, trust the live check and say so explicitly in
  the record (done in the rescheduled check-in message for #114) rather than silently picking one and
  moving on.

## Stop
- Deleting a scheduled check-in trigger on a webhook's word alone, with no live confirmation first —
  did exactly this for PR #114's "merged" event a few turns ago, and it was premature (the PR was still
  open). Re-armed once the live state was confirmed, but the near-miss is worth naming so it isn't
  repeated on the next merge notification.
