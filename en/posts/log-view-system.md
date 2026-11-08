---
layout: post
title: "Building and Operating a Small Log Viewer"
author: KimKitae
date: 2024-09-15 12:00:00 +0900
last_modified_at: 2026-11-08
lang: en
permalink: /en/posts/log-view-system/
translation_url: /posts/log-view-system/
description: A small internal log viewer built with FastAPI, Kafka, Redis, and MariaDB, and what I would simplify today.
categories: [Automation, TestPlatform]
tags: [TestPlatform]
---

When the number of automation tools grows, finding out where a failure happened becomes a bottleneck. Full observability platforms such as New Relic, Datadog, or Grafana already exist, but attaching one just to read a single log line can be excessive. This article summarizes a small LogViewer built on an existing API server with Kafka and Redis.

![Clients to FastAPI, Kafka, MariaDB, Redis pub/sub, WebSocket, and web UI](/assets/img/posts/renewal/log-view-system.svg)

*Figure 1. Ingestion and live delivery are separated. MariaDB stores history; Redis pub/sub carries the live stream.*

## Why Kafka

The first idea was for the API server to write logs directly to the database. As volume grew, database writes could slow down request handling. So the API published to a Kafka topic, and a separate consumer handled persistence and live delivery.

Kafka was chosen for scalability and bottleneck concerns, and also because it was a technology I was interested in applying to this project. Current advice is separate: a simpler queue may be enough for a small internal tool, so match the tool to the problem size and the operational capacity.

## Components

- **Clients**: automation tools send a `LogEntry`.
- **FastAPI**: stores service names in a Redis set and publishes logs to the `log` topic.
- **Kafka consumer**: persists messages to MariaDB and publishes them to the Redis `log` channel.
- **WebSocket**: subscribes to Redis and pushes logs to connected browsers.
- **Web UI**: filters by service, tag, and level, and can pause the live stream.

## FastAPI lifespan

The earlier version used `@app.on_event("startup")`. Current FastAPI recommends the `lifespan` context, which keeps connection setup and cleanup in one place and is easier to test.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    app.state.redis = await create_redis()
    app.state.kafka = await create_kafka()
    try:
        yield
    finally:
        await app.state.kafka.close()
        await app.state.redis.close()
```

Move old code to the current recommended pattern instead of copying it unchanged.

## Persistence and live delivery

The save API performs minimal validation and hands the log to Kafka. Service names are collected in Redis for the filter list. The consumer dispatches by topic; for the `log` topic it writes to the database and publishes to Redis.

```python
async for message in consumer:
    data = json.loads(message.value.decode("utf-8"))
    await save_log(data)
    await redis.publish("log", json.dumps(data))
```

The live UI subscribes to Redis pub/sub and forwards messages over WebSocket. On refresh, the browser loads recent logs from the database and then switches to the live stream. This avoids querying the database on every update.

## What to decide in operation

The first decision is about what not to log. Verification codes, tokens, and order details should be masked at the client before they ever reach the viewer. A retention period per service is also needed.

The UI should stay small: service selection, tag and level filters, pause, pagination, and connection status are enough. A useful test is whether a reader can tell why a log is missing. Showing reconnection state when the WebSocket drops, and reporting a failed database query explicitly, belong to the same principle.

## Summary

This is not a full observability platform, only a way to check logs from small internal tools quickly. As volume grows, it should move to a dedicated log system. Until then, one API call to emit a log and one screen to read it removes a surprising amount of communication overhead. The code here is an abbreviated explanation of the implementation, not a version tested against current library releases.
