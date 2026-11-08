---
layout: post
title: "Building an Internal SMS Verification Code Manager"
author: KimKitae
date: 2024-09-12 12:00:00 +0900
last_modified_at: 2026-11-08
lang: en
permalink: /en/posts/sms-management-system/
translation_url: /posts/sms-management-system/
description: An internal tool that shares SMS codes from test devices through FastAPI, Redis, WebSocket, Slack, and an automation API, including the source's TTL discrepancy and a parallel-run race.
categories: [Automation, TestPlatform]
tags: [Testing, TestPlatform]
---

Checking SMS verification codes during test automation is tedious. You may have to find a test phone or ask the person holding it. This article describes the internal tool built to reduce that work, and two problems found when rereading it. One is that the original records two different retention periods. The other is that when several tests share a phone, nothing identifies which run a code belongs to.

![Synthetic timeline where two runs share one phone number and the latest value becomes another run's code](/assets/img/posts/renewal/sms-management-system.svg)

*Figure 1. SMS arrival order need not match request order. Redis keeps one latest value per phone number, so the earlier code is overwritten.*

## Problem and scope

When several scenarios share a number, it is hard to know who received a code and when. Giving each number an owner creates a different bottleneck: someone must be available whenever authentication is needed. The goal was to let the team see the arrival and the code in one place for a short period.

The tool had three parts:

- **Android app**: detects SMS on a test phone and sends it to the internal server.
- **Web server**: registers devices, serves recent codes, and updates the UI in real time.
- **Automation API**: lets test scripts fetch the most recent code.

## Retention: a contradiction in the source

The original prose says codes stay in Redis for **10 minutes**. Its `send_code` implementation uses these two calls.

```python
await _redis.set_key(key=sms_entry.phone_number, value=json.dumps(sms_data), ttl=300)
await _redis.set_key(f"sms:{sms_entry.phone_number}", value=str(sms_entry.code), ttl=300)
```

`ttl=300` corresponds to five minutes, not ten. That does not prove production used five minutes. `set_key` is a wrapper with no definition in the article, and whether `ttl` is seconds or milliseconds is not visible in the code. The wrapper may have converted it. The verifiable fact is that **the prose and the call arguments disagree**.

If writing this today, express the policy as one explicit constant and use Redis units directly. `EX` is seconds.

```python
# Policy: keep the code for ten minutes
await redis.set(f"sms:{phone_number}", code, ex=600)
```

To learn what a deployment actually used, do not guess; inspect the key.

```bash
redis-cli TTL sms:01000000000     # seconds left; -1 no expiry, -2 no key
redis-cli PTTL sms:01000000000    # milliseconds
redis-cli GET sms:01000000000
```

Comparing `TTL` right after sending a message and again six minutes later reveals the effective policy even when the wrapper and deployment configuration are unknown.

## Only the latest value per phone survives

The original stores the latest value under the phone number. It is not a list or a history. The two `send_code` calls above overwrite the same keys through `_redis.set_key`, so a second message for the same number overwrites the first. History would need a list or a separate table, which the source does not have. So an “old messages pile up and never expire” problem cannot be claimed from this code. What can be observed is that **only the latest value remains and the previous one is gone**.

The lookup code deserves attention too. `get_code` reads `sms:{phone_number}` and calls `json.loads`, but the write stores only the code string in that key.

```python
data_json = await _redis.get_key(f"sms:{phone_number}")
data = json.loads(data_json)
return data
```

In Python, `json.loads('1234')` returns the integer `1234`, and `json.loads('0123')` is not a valid JSON number, so parsing raises. A code of `"1234"` therefore returns a non-object value, and a code with a leading zero such as `"0123"` fails lookup. This is inferred from the code and `json.loads` behavior; the article cannot show whether production received such a message. If rebuilding, store the code string and metadata separately and pin the lookup response shape with a test.

## When parallel runs share a phone

When several runs share one number, “latest value” does not say which run it belongs to. The timeline below is **synthetic**, for explaining the structure, not a recorded incident.

| Time | Run A | Run B | Redis `sms:{phone}` |
|---|---|---|---|
| T+0s | Sends auth request | | none |
| T+5s | | Sends auth request | none |
| T+8s | | Receives code 1111 | 1111 |
| T+9s | Receives code 2222 | | 2222 |
| T+10s | | Reads 2222 | 2222 |
| T+12s | Reads 2222 | | 2222 |

SMS arrival order need not match request order. Here B reads A's code, not its own. If codes are valid only for the request that triggered them, B fails authentication. If they are valid per number, B might pass using A's code. Either way, the test result depends on another run's code.

Three ways to reduce it:

1. **Lease the number.** Lock a phone per run and release it at the end. This is the simplest way to serialize concurrent runs.
2. **Record correlation data.** Receive time and expected sender narrow freshness, but when two runs request nearly simultaneously on the same number, “arrived after my request” cannot decide which run the code belongs to. The source has no such condition either.
3. **Use a provider-supported correlation identifier.** This is the most precise when the SMS body or provider API can carry a run ID. Do not assume every SMS contains one; sender, timing, and body format depend on the provider and template. When parallel runs share one number, prefer lease-based serialization or a provider correlation identifier.

## Four lifetimes and boundaries

| Item | What it protects | Original value or state |
|---|---|---|
| Redis TTL | Exposure time of the code | Prose says 10 minutes; call passes 300 |
| WebSocket session | How long the screen stays connected | Maximum 30 minutes, cleared on refresh |
| Access control | Who may register or read | No implementation recorded |
| Run correlation | Which code belongs to which run | No implementation recorded |

Shortening retention does not fix reading another run's code. Shortening a session does not fix authorization. These are separate problems, and setting one does not solve the others.

## If publishing this today

The original highlighted the convenience of sharing a test SIM: if the phone sits in a drawer, anyone who can install the app can share its number. That convenience assumed anyone who can install the app may share the number. Approved devices, sender allowlists, and internal network access control are not recorded in the source; they are boundaries to establish first today.

One Android correction: the source uses `SmsMessage.createFromPdu((byte[]) pdu)`. The single-argument method was deprecated in API 23; use `createFromPdu(byte[] pdu, String format)` ([official reference](https://developer.android.com/reference/android/telephony/SmsMessage)). General SMS receipt and SMS Retriever behave differently, and apps distributed through Google Play are subject to its SMS permission policy.

The original lookup function writes `data_json` to an info log. That key contains the authentication code, so the code may remain in log storage after its Redis TTL expires. Shortening the TTL alone does not control its exposure lifetime. I would log the request ID, outcome, and latency instead of the value.

Operational recommendations:

- Read the sender allowlist and Slack channel IDs from configuration, not code.
- Keep message bodies and codes out of logs.
- Limit who can register or remove a device, and record registrations.
- Give test code a timeout and retry limit, and record the receive time alongside the code.

## Summary

What this tool reduced was the time spent finding a person to read a message. What it adds is the need to manage phone leasing, correlation, and access control. The TTL contradiction was invisible without rereading the code, and the parallel-run race can corrupt results even when every component works. Check the deployed TTL with `TTL`, and decide on leasing or correlation before sharing one number across concurrent runs.
