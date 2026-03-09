# 🖥️ VALE Command Center — Concept (Phase 3)

> ⚠️ Parked intentionally. Build after N8n is learned in Phase 3.

## What It Is
A centralized life context dashboard that aggregates personal 
data and feeds it to Lucien so he's aware of your life state 
before conversations begin.

## The Vision
You wake up. Discord shows your Oura score, AI news, and any 
overnight errors. You open OpenWebUI. Before you say anything 
Lucien already knows how you slept, what broke, and what's 
relevant to your day.

## Architecture
- **N8n** — orchestrates all data collection workflows
- **Discord** — visual dashboard (for you)
- **Qdrant** — searchable context store (for Lucien)
- **OpenWebUI** — conversation engine that queries Qdrant

## Data Sources Planned
- Oura ring (sleep, HRV, recovery)
- Apple Health (activity, steps)
- GitHub (commits, project status)
- RSS feeds (AI/ML news filtered by interest)
- Docker/OpenWebUI error logs

## Why It's Parked
N8n is the backbone of this entire system and is Phase 3 
scope. Building this before the memory system exists would 
be decorating a house before the foundation is poured.

## Own Repo When Ready
Repo name: `vale-command-center`
Public framing: life context aggregation system, data 
engineering, automation pipeline. Stands alone as a 
portfolio piece independent of VALE.

## First Steps When Phase 3 Begins
1. Learn N8n basics
2. Build first workflow — GitHub commits → Discord
3. Add health data source
4. Wire into Qdrant
5. Test Lucien referencing context unprompted