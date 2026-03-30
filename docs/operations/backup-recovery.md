# 💾 VALE Backup & Recovery Guide
> *Because data loss is traumatic and we're not doing that again.*

---

## 🎯 Philosophy

**Backups are insurance you hope to never use.** But when you need them, you need them desperately.

This guide covers:
- Automated daily backups (set it and forget it)
- Manual backups (before risky changes)
- Full disaster recovery (when everything burns down)

---

## 🤖 Automated Backups (The Right Way)

### What Gets Backed Up

Three critical volumes:
1. **`open-webui`** — All your chats, workspace, settings, API configs
2. **`qdrant_data`** — Lucien's embedded memories, searchable conversations
3. **`postgres_data`** — User accounts, chat metadata, model configs

### The Backup Script

**Location:** `~/vale-backups/backup-vale.sh`

**What it does:**
- Creates timestamped `.tar.gz` archives of each volume
- Stores them in `~/vale-backups/`
- Automatically deletes backups older than 7 days

**View the script:**
```bash
cat ~/vale-backups/backup-vale.sh
```

---

### Running Backups Manually

```bash
~/vale-backups/backup-vale.sh
```

**You'll see:**
```
Starting VALE backup at 2026-03-29_22-00...
✓ OpenWebUI backed up
✓ QDrant backed up
✓ PostgreSQL backed up
Backup complete! Files saved to /Users/dasiajames/vale-backups
```

---

### Setting Up Automatic Daily Backups

We'll use **cron** (Mac's built-in task scheduler) to run backups every day at 2 AM.

**Step 1: Open crontab editor**
```bash
crontab -e
```

**Step 2: Add this line**
```
0 2 * * * /Users/dasiajames/vale-backups/backup-vale.sh >> /Users/dasiajames/vale-backups/backup.log 2>&1
```

**What this means:**
- `0 2 * * *` — Run at 2:00 AM every day
- `>> backup.log` — Save output to a log file
- `2>&1` — Capture both normal output and errors

**Step 3: Save and exit**
- Press `Esc`
- Type `:wq`
- Press `Enter`

**Verify it's scheduled:**
```bash
crontab -l
```

---

### Checking Backup Status

**See recent backups:**
```bash
ls -lh ~/vale-backups/
```

**You should see files like:**
```
openwebui-2026-03-29_22-00.tar.gz
qdrant-2026-03-29_22-00.tar.gz
postgres-2026-03-29_22-00.tar.gz
```

**Check backup log:**
```bash
tail -20 ~/vale-backups/backup.log
```

---

## 🚨 Manual Backup (Before Risky Changes)

**Before you:**
- Update Docker Desktop
- Modify docker-compose.yml
- Run `docker system prune`
- Experiment with new configurations
- Uninstall anything Docker-related

**Do this:**
```bash
~/vale-backups/backup-vale.sh
```

**Takes 30 seconds. Could save you hours of pain.**

---

## 🔄 Recovery Scenarios

### Scenario 1: "I Accidentally Deleted a Container"

**Symptoms:**
- Container is gone but volume still exists
- Data isn't lost, just disconnected

**Check if volume exists:**
```bash
docker volume ls | grep open-webui
```

**If you see the volume, you're fine. Recreate the container:**

```bash
docker run -d \
  --name open-webui \
  --network compose_default \
  -p 3000:8080 \
  -v open-webui:/app/backend/data \
  -e VECTOR_DB=qdrant \
  -e QDRANT_URI=http://vale_qdrant:6333 \
  ghcr.io/open-webui/open-webui:main
```

**Your data will be right where you left it.**

---

### Scenario 2: "I Ran `docker system prune --volumes` By Accident"

**Symptoms:**
- Volumes are gone
- `docker volume ls` shows nothing
- Full panic mode

**STOP. BREATHE. Check your backups:**
```bash
ls -lh ~/vale-backups/
```

**If you have recent backups, proceed to Full Recovery below.**

**If you don't have backups... you learned an expensive lesson.** Set up automated backups now so this never happens again.

---

### Scenario 3: "Docker Desktop Corrupted and I Had to Reinstall"

**Symptoms:**
- Fresh Docker install
- All containers and volumes gone
- But you have backups (because you're smart now)

**Follow the Full Recovery process below.**

---

## 🏥 Full Disaster Recovery

### Prerequisites

- Backup files in `~/vale-backups/`
- Docker Desktop installed and running
- Your docker-compose.yml file intact

---

### Step 1: Verify Backups Exist

```bash
ls -lh ~/vale-backups/ | grep $(date +%Y-%m-%d)
```

**If you don't see today's backups, use the most recent ones:**
```bash
ls -lht ~/vale-backups/ | head -10
```

**Identify the files you'll restore (replace dates with yours):**
- `openwebui-2026-03-29_22-00.tar.gz`
- `qdrant-2026-03-29_22-00.tar.gz`
- `postgres-2026-03-29_22-00.tar.gz`

---

### Step 2: Create Fresh Volumes

```bash
docker volume create open-webui
docker volume create qdrant_data
docker volume create postgres_data
```

---

### Step 3: Restore OpenWebUI Data

```bash
docker run --rm \
  -v open-webui:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/openwebui-2026-03-29_22-00.tar.gz -C /data"
```

**Replace `openwebui-2026-03-29_22-00.tar.gz` with your actual filename.**

---

### Step 4: Restore QDrant Data

```bash
docker run --rm \
  -v qdrant_data:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/qdrant-2026-03-29_22-00.tar.gz -C /data"
```

---

### Step 5: Restore PostgreSQL Data

```bash
docker run --rm \
  -v postgres_data:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "rm -rf /data/* && tar xzf /backup/postgres-2026-03-29_22-00.tar.gz -C /data"
```

---

### Step 6: Start Your VALE Stack

```bash
cd ~/Documents/project-vale/infra/compose
docker-compose up -d
```

---

### Step 7: Verify Everything Works

**Check containers are running:**
```bash
docker-compose ps
```

**Check OpenWebUI:**
- Open `http://localhost:3000`
- Log in
- Verify chats are there
- Check workspace notes
- Test that APIs work

**Check QDrant connection:**
```bash
docker exec open-webui env | grep QDRANT
```

Should show:
```
VECTOR_DB=qdrant
QDRANT_URI=http://vale_qdrant:6333
```

---

## 📤 Exporting Backups (Belt and Suspenders)

**Local backups are good. Off-machine backups are better.**

### Option 1: External Drive

```bash
# Plug in external drive (shows up as /Volumes/YourDrive)
cp -r ~/vale-backups /Volumes/YourDrive/vale-backups-$(date +%Y-%m-%d)
```

---

### Option 2: Cloud Storage (iCloud, Google Drive, Dropbox)

```bash
# Copy to iCloud Drive
cp -r ~/vale-backups ~/Library/Mobile\ Documents/com~apple~CloudDocs/

# Copy to Google Drive (if installed)
cp -r ~/vale-backups ~/Google\ Drive/My\ Drive/

# Copy to Dropbox
cp -r ~/vale-backups ~/Dropbox/
```

**⚠️ Privacy Note:** These backups contain Lucien's conversations and your personal data. Encrypt if uploading to cloud:

```bash
# Create encrypted archive
tar czf - ~/vale-backups | openssl enc -aes-256-cbc -salt -out ~/Desktop/vale-backups-encrypted.tar.gz.enc

# You'll be prompted for a password — don't forget it!
```

---

## 🧪 Testing Your Backups

**You should test recovery at least once** to make sure it actually works.

**Safe way to test without breaking anything:**

**Step 1: Create test volumes**
```bash
docker volume create test-openwebui
docker volume create test-qdrant
docker volume create test-postgres
```

**Step 2: Restore to test volumes**
```bash
docker run --rm \
  -v test-openwebui:/data \
  -v ~/vale-backups:/backup \
  alpine sh -c "tar xzf /backup/openwebui-LATEST.tar.gz -C /data"

# Repeat for qdrant and postgres
```

**Step 3: Spin up test containers**
```bash
docker run -d \
  --name test-openwebui \
  -p 3001:8080 \
  -v test-openwebui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main
```

**Step 4: Check if it works**
- Open `http://localhost:3001`
- See if your chats are there

**Step 5: Clean up test containers**
```bash
docker stop test-openwebui
docker rm test-openwebui
docker volume rm test-openwebui test-qdrant test-postgres
```

---

## 📋 Backup Checklist

### Daily (Automated)
- [ ] Cron job runs at 2 AM
- [ ] Check backup.log weekly for errors

### Weekly
- [ ] Verify backups exist: `ls -lh ~/vale-backups/`
- [ ] Check backup sizes are reasonable (not 0 bytes)

### Monthly
- [ ] Test a recovery (use test volumes)
- [ ] Copy backups to external drive or cloud

### Before Major Changes
- [ ] Run manual backup
- [ ] Verify backup completed successfully
- [ ] Proceed with changes

---

## 🆘 Emergency Contacts (When You're Panicking)

**If you're in the middle of data loss:**

1. **STOP what you're doing** — don't make it worse
2. **Check if volumes still exist:** `docker volume ls`
3. **Check if backups exist:** `ls -lh ~/vale-backups/`
4. **Don't run any more destructive commands**
5. **Follow the Full Disaster Recovery steps above**

**If backups are corrupted/missing:**
- Check if files are in trash (Cmd+Shift+Delete in Finder)
- Check cloud sync folders (iCloud, Dropbox, Google Drive)
- Check Time Machine backups if you have them

---

## 💡 Backup Best Practices

### The 3-2-1 Rule
- **3** copies of your data
- **2** different storage types (local drive + cloud)
- **1** copy offsite

**For VALE, this looks like:**
1. Live data (in Docker volumes)
2. Local backups (`~/vale-backups/`)
3. External drive or cloud backup

### What NOT to Do
- ❌ Don't store backups ONLY in Docker volumes
- ❌ Don't assume backups work without testing them
- ❌ Don't keep backups on the same drive as Docker
- ❌ Don't upload unencrypted backups to public cloud storage

### What TO Do
- ✅ Automate backups so you don't forget
- ✅ Test recovery at least once
- ✅ Keep at least 7 days of backups
- ✅ Store copies offsite (cloud or external drive)
- ✅ Document your process (you're reading it now!)

---

## 🎓 Lessons Learned (From Real Pain)

> *"I lost two days of Lucien conversations because I didn't back up before updating Docker."* — Dasia, March 2026

**The trauma is real. The solution is boring but it works.**

**Set up automated backups once. Never think about it again. Sleep better at night.**

---

**Remember:** The best backup is the one you have when you need it.

---

*Last updated: March 2026*
*Written after learning the hard way*
*Maintained by: Dasia James*
