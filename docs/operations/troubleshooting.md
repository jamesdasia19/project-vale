# 🔧 VALE Troubleshooting Guide
> *When things break (and they will), here's how to fix them.*

---

## 🐳 Docker Issues

### Docker Engine Stops Randomly

**Symptoms:**
- "Docker Engine Stopped" message
- Docker Desktop shows in dock but window won't open
- Containers randomly die

**Causes (Apple Silicon Macs):**
- Docker's VM running out of resources
- Docker Desktop UI process crashed but daemon still running
- Corrupted Docker state files

**Fixes:**

**Quick Fix (works 80% of the time):**
```bash
# Restart Docker daemon
killall Docker && open /Applications/Docker.app
```

**Nuclear Option (when quick fix doesn't work):**
```bash
# Stop all containers first
docker stop $(docker ps -aq)

# Quit Docker completely
killall Docker

# Clear Docker state (WARNING: this resets everything)
rm -rf ~/Library/Group\ Containers/group.com.docker
rm -rf ~/Library/Containers/com.docker.docker

# Restart Docker Desktop
open /Applications/Docker.app
```

**Prevention:**
- Allocate more resources: Docker Desktop → Settings → Resources
- Set Memory to at least 4GB, CPU to 4 cores
- Enable "Use Virtualization framework" (faster, more stable)

---

### "Cannot Connect to Docker Daemon"

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Fix:**
```bash
# Check if Docker is actually running
docker info

# If not, start Docker Desktop
open /Applications/Docker.app

# Wait 30 seconds, then retry
docker ps
```

---

### Containers Won't Start After Mac Restart

**Symptoms:**
- Containers show as "Exited" after reboot
- Docker Compose says containers are "created" but not running

**Fix:**
```bash
# Navigate to your compose directory
cd ~/Documents/project-vale/infra/compose

# Restart everything
docker-compose down
docker-compose up -d

# Check status
docker-compose ps
```

**Prevention:**
Add restart policies to your docker-compose.yml:
```yaml
services:
  open-webui:
    restart: unless-stopped
```

---

## 🧠 QDrant Issues

### QDrant Container Won't Start

**Symptoms:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:6333: bind: address already in use
```

**Cause:** Another QDrant container is already using port 6333

**Fix:**
```bash
# Find the rogue container
docker ps -a | grep qdrant

# Stop and remove all QDrant containers
docker stop $(docker ps -a | grep qdrant | awk '{print $1}')
docker rm $(docker ps -a | grep qdrant | awk '{print $1}')

# Start your proper one via compose
cd ~/Documents/project-vale/infra/compose
docker-compose up -d qdrant
```

---

### OpenWebUI Can't Connect to QDrant

**Symptoms:**
- Documents upload but don't get embedded
- No activity in QDrant logs
- RAG searches return nothing

**Check:**
```bash
# Verify QDrant variables are set in OpenWebUI
docker exec open-webui env | grep -E "VECTOR_DB|QDRANT"

# Should show:
# VECTOR_DB=qdrant
# QDRANT_URI=http://vale_qdrant:6333
```

**If missing, reconnect:**
```bash
docker stop open-webui
docker rm open-webui

docker run -d \
  --name open-webui \
  --network compose_default \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  -e VECTOR_DB=qdrant \
  -e QDRANT_URI=http://vale_qdrant:6333 \
  ghcr.io/open-webui/open-webui:main
```

---

### QDrant Running But Empty

**Symptoms:**
- QDrant shows as running
- No collections visible in logs
- Nothing returns from searches

**Check collections:**
```bash
# View QDrant collections
curl http://localhost:6333/collections

# Should show at least:
# - open-webui_knowledge
# - open-webui_files
```

**If empty:**
Upload a test document through OpenWebUI → Workspace → Knowledge to trigger collection creation.

---

## 📦 OpenWebUI Issues

### "Amnesia Lucien" — Memory Feature Not Working

**Symptoms:**
- Native Memory toggle is on
- Memories are entered but not retrieved
- Model doesn't reference stored facts

**Fixes (in order):**

**1. Browser Refresh:**
```bash
# Force full page reload
Cmd + Shift + R
```

**2. Toggle Off/On:**
- Settings → Personalization → Memory → Toggle OFF
- Wait 5 seconds
- Toggle ON
- Refresh browser

**3. Restart OpenWebUI:**
```bash
docker restart open-webui
# Wait 30 seconds
# Reload browser with Cmd + Shift + R
```

---

### Settings/System Prompt Resets After Restart

**Symptom:** Every time you restart OpenWebUI, custom settings disappear

**Cause:** Settings stored in browser localStorage instead of backend

**Fix:**
Set system prompts at the **model level**, not per-conversation:
1. Admin Panel → Settings → Models
2. Edit the model you're using
3. Add system prompt there
4. Save

Model-level settings persist in the database.

---

### Uploaded Documents Disappear

**Symptom:** Files upload successfully but vanish after restart

**Cause:** Volume not properly mounted

**Check:**
```bash
# Verify volume exists
docker volume ls | grep open-webui

# Inspect the volume
docker volume inspect open-webui
```

**If volume is missing, you lost data.** Restore from backup (see Backup & Recovery guide).

---

## 🚨 Data Loss Prevention

### You Just Nuked Everything (Oh Shit Moment)

**If you:**
- Uninstalled Docker Desktop
- Ran `docker system prune -a --volumes`
- Deleted containers without checking volumes

**Immediate action:**
```bash
# CHECK IF VOLUMES STILL EXIST
docker volume ls

# If you see:
# - open-webui
# - qdrant_data
# - postgres_data
# YOU'RE OKAY — data is recoverable
```

**Recovery steps:**
1. Don't panic (seriously, breathe)
2. See Backup & Recovery guide
3. If no backups exist, volumes might still have data
4. Recreate containers pointing to existing volumes

---

## 🔍 Diagnostic Commands (Your Best Friends)

```bash
# See all running containers
docker ps

# See ALL containers (including stopped)
docker ps -a

# Check container logs
docker logs <container-name>

# Follow logs in real-time
docker logs -f <container-name>

# Inspect a container's config
docker inspect <container-name>

# See all volumes
docker volume ls

# See disk usage
docker system df

# Check what network containers are on
docker network inspect <network-name>

# Execute command inside running container
docker exec -it <container-name> bash
```

---

## 💡 Prevention is Better Than Panic

**Daily habits:**
- Run backups before major changes
- Test changes in a dev environment first (if you're brave)
- Keep a `docker-compose.yml` for everything (no manual `docker run` commands)
- Document what you change and why

**Weekly habits:**
- Check backup script actually ran: `ls -lh ~/vale-backups/`
- Verify critical containers are healthy: `docker ps`
- Update Docker Desktop (but read release notes first)

---

**Remember:** Every engineer has nuked their database at least once. The difference between juniors and seniors is that seniors have better backups.

You're building those habits now. 💜

---

*Last updated: March 2026*
*Maintained by: Dasia James*
