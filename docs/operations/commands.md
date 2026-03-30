# 📋 VALE Command Reference
> *The Docker commands you'll actually use (not the 500 you won't).*

---

## 🎯 Philosophy

This isn't a complete Docker manual. This is **the 20 commands that solve 80% of your problems** when working with VALE.

Organized by task, not alphabetically, because that's how humans think.

---

## 🚀 Starting & Stopping Things

### Start Your Entire VALE Stack
```bash
cd ~/Documents/project-vale/infra/compose
docker-compose up -d
```
**What it does:** Starts postgres, qdrant, and any other services in your compose file  
**The `-d` flag:** "Detached" mode (runs in background)

---

### Stop Everything
```bash
cd ~/Documents/project-vale/infra/compose
docker-compose down
```
**What it does:** Stops and removes containers (but keeps your data volumes safe)

---

### Restart a Single Container
```bash
docker restart <container-name>

# Examples:
docker restart open-webui
docker restart vale_qdrant
```

---

### Start/Stop Individual Services
```bash
# Start just one service
docker-compose start qdrant

# Stop just one service
docker-compose stop postgres
```

---

## 🔍 Checking Status (Your Daily Bread)

### See What's Running
```bash
docker ps
```
**Shows:** Container ID, image, status, ports, names

---

### See ALL Containers (Including Stopped Ones)
```bash
docker ps -a
```
**Use when:** You're looking for a container that should be running but isn't

---

### Check If a Specific Container Is Running
```bash
docker ps | grep <name>

# Examples:
docker ps | grep qdrant
docker ps | grep open-webui
```

---

### See Container Resource Usage
```bash
docker stats
```
**Shows:** CPU, memory, network I/O in real-time  
**Exit:** Press `Ctrl+C`

---

## 📖 Reading Logs (Debugging Your Life)

### View Recent Logs
```bash
docker logs <container-name>

# Show last 50 lines
docker logs <container-name> --tail=50

# Examples:
docker logs open-webui --tail=100
docker logs vale_qdrant --tail=30
```

---

### Follow Logs in Real-Time
```bash
docker logs -f <container-name>

# Example:
docker logs -f open-webui
```
**Use when:** Debugging in real-time, watching something start up  
**Exit:** Press `Ctrl+C`

---

### Search Logs for Specific Text
```bash
docker logs <container-name> | grep "error"
docker logs <container-name> | grep -i "qdrant"  # case-insensitive
```

---

## 🗄️ Managing Volumes (Your Data Lives Here)

### List All Volumes
```bash
docker volume ls
```

---

### Inspect a Volume
```bash
docker volume inspect <volume-name>

# Example:
docker volume inspect open-webui
```
**Shows:** Where the volume actually lives on your disk, when it was created

---

### See How Much Space Volumes Are Using
```bash
docker system df -v
```

---

### Remove Unused Volumes (DANGER ZONE)
```bash
# Shows what would be removed (safe)
docker volume ls -f dangling=true

# Actually removes them (CAREFUL!)
docker volume prune
```
**⚠️ WARNING:** Only run this if you're 100% sure you don't need those volumes

---

## 🔧 Working Inside Containers

### Open a Shell Inside a Running Container
```bash
docker exec -it <container-name> bash

# If bash doesn't work, try sh:
docker exec -it <container-name> sh

# Example:
docker exec -it open-webui bash
```
**Use when:** You need to poke around inside the container  
**Exit:** Type `exit` or press `Ctrl+D`

---

### Run a One-Off Command Inside a Container
```bash
docker exec <container-name> <command>

# Examples:
docker exec open-webui ls /app/backend/data
docker exec vale_postgres psql -U vale -d vale_db -c "SELECT COUNT(*) FROM chats;"
```

---

### Check Environment Variables Inside a Container
```bash
docker exec <container-name> env

# Filter for specific variables:
docker exec open-webui env | grep QDRANT
```

---

## 🌐 Networking (Making Containers Talk)

### See All Networks
```bash
docker network ls
```

---

### Inspect a Network (See What's Connected)
```bash
docker network inspect <network-name>

# Example:
docker network inspect compose_default
```

---

### Connect a Container to a Network
```bash
docker network connect <network-name> <container-name>

# Example:
docker network connect compose_default open-webui
```

---

## 🧹 Cleanup Commands

### Remove a Stopped Container
```bash
docker rm <container-name>

# Force remove even if running:
docker rm -f <container-name>
```

---

### Remove Multiple Containers
```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker rm $(docker ps -aq)
```

---

### Clean Up Everything Docker Isn't Using
```bash
# Shows what would be removed (safe)
docker system prune --dry-run

# Actually removes it
docker system prune

# Nuclear option (removes EVERYTHING unused including volumes)
docker system prune -a --volumes
```
**⚠️ EXTREME DANGER:** The `--volumes` flag **WILL DELETE YOUR DATA** if volumes aren't in use

---

## 🔄 Updating & Rebuilding

### Pull Latest Image
```bash
docker pull <image-name>

# Example:
docker pull ghcr.io/open-webui/open-webui:main
```

---

### Rebuild and Restart a Service
```bash
cd ~/Documents/project-vale/infra/compose
docker-compose up -d --build <service-name>

# Example:
docker-compose up -d --build open-webui
```

---

## 💾 Backup & Data Commands

### Backup a Volume to a .tar.gz File
```bash
docker run --rm \
  -v <volume-name>:/data \
  -v ~/vale-backups:/backup \
  alpine tar czf /backup/<filename>.tar.gz -C /data .

# Example:
docker run --rm \
  -v open-webui:/data \
  -v ~/vale-backups:/backup \
  alpine tar czf /backup/openwebui-backup.tar.gz -C /data .
```

---

### Restore a Volume from Backup
```bash
docker run --rm \
  -v <volume-name>:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/<filename>.tar.gz -C /data"

# Example:
docker run --rm \
  -v open-webui:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/openwebui-2026-03-29.tar.gz -C /data"
```

---

### Copy Files Between Host and Container
```bash
# From container to your Mac:
docker cp <container-name>:/path/in/container /path/on/mac

# From your Mac to container:
docker cp /path/on/mac <container-name>:/path/in/container

# Example:
docker cp open-webui:/app/backend/data/config.json ~/Desktop/
```

---

## 🎛️ Docker Compose Specific

### Start Services Defined in Compose File
```bash
cd ~/Documents/project-vale/infra/compose
docker-compose up -d
```

---

### View Status of Compose Services
```bash
docker-compose ps
```

---

### View Logs for All Compose Services
```bash
docker-compose logs

# Follow in real-time:
docker-compose logs -f

# Just one service:
docker-compose logs open-webui
```

---

### Rebuild and Restart Everything
```bash
docker-compose down
docker-compose up -d --build
```

---

### Run a One-Off Command in a Compose Service
```bash
docker-compose exec <service-name> <command>

# Example:
docker-compose exec postgres psql -U vale
```

---

## 🆘 Emergency Commands (When Everything's On Fire)

### Kill All Running Containers
```bash
docker kill $(docker ps -q)
```

---

### Restart Docker Daemon (Mac)
```bash
killall Docker && open /Applications/Docker.app
```

---

### Check If Docker Daemon Is Even Running
```bash
docker info
```
**If this errors, Docker isn't running**

---

### Free Up Disk Space Fast
```bash
# Remove unused images
docker image prune -a

# Remove build cache
docker builder prune
```

---

## 📝 Aliases (Make Your Life Easier)

Add these to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Quick status check
alias dps='docker ps'
alias dpsa='docker ps -a'

# Logs
alias dlogs='docker logs'
alias dlogsf='docker logs -f'

# Compose shortcuts
alias dcup='docker-compose up -d'
alias dcdown='docker-compose down'
alias dcps='docker-compose ps'
alias dclogs='docker-compose logs -f'

# VALE specific
alias vale-start='cd ~/Documents/project-vale/infra/compose && docker-compose up -d'
alias vale-stop='cd ~/Documents/project-vale/infra/compose && docker-compose down'
alias vale-backup='~/vale-backups/backup-vale.sh'
```

**To activate after adding:**
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

---

## 🧠 Mental Models (How to Think About This)

### Containers vs Images
- **Image:** The blueprint (like a recipe)
- **Container:** A running instance (like the actual cake you baked)
- You can have multiple containers from the same image

### Containers vs Volumes
- **Container:** The process that's running (temporary)
- **Volume:** Where the data lives (permanent)
- Deleting a container ≠ deleting the data (unless you use `--volumes` flag)

### Networks
- Think of them like VLANs or subnets
- Containers on the same network can talk to each other by name
- Containers on different networks are isolated

---

## 💡 Pro Tips

1. **Always use `docker-compose` for multi-container setups** — it's way easier to manage than individual `docker run` commands

2. **Name your containers explicitly** — `vale_qdrant` is way better than `romantic_turing`

3. **Use volumes for anything you want to keep** — container filesystems are ephemeral

4. **Check logs first** — 90% of problems reveal themselves in the logs

5. **When in doubt, restart the container** — it's the Docker equivalent of "turn it off and on again"

6. **Before running destructive commands, do a dry run or backup** — `docker system prune --dry-run` before `docker system prune`

---

**Remember:** You don't need to memorize all of this. Bookmark this file. Reference it when you need it. That's what senior engineers do.

---

*Last updated: March 2026*
*Maintained by: Dasia James*
