# OpenEnv Supply Chain Environment - Deployment Guide

## 🚀 GitHub Deployment

### Step 1: Create GitHub Repository
1. Go to [https://github.com/new](https://github.com/new)
2. Create a new repository named `supply-chain-openenv`
3. **Do NOT** initialize with README (we have one)
4. Click "Create repository"

### Step 2: Push Code to GitHub
```bash
# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/supply-chain-openenv.git
git branch -M main
git push -u origin main
```

### Step 3: GitHub URL for Submission
```
https://github.com/YOUR_USERNAME/supply-chain-openenv
```

---

## 🤗 Hugging Face Spaces Deployment

### Step 1: Create Hugging Face Space
1. Go to [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in:
   - **Space name:** `supply-chain-openenv`
   - **License:** OpenRAIL (or your choice)
   - **Space SDK:** Docker
4. Click "Create Space"

### Step 2: Deploy to HF Spaces
```bash
# Add HF as remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/supply-chain-openenv

# Push to HF (triggers build)
git push huggingface main
```

### Step 3: Hugging Face URL for Submission
```
https://huggingface.co/spaces/YOUR_USERNAME/supply-chain-openenv
```

---

## ✅ Submission URLs Format

**GitHub Repository URL:**
```
https://github.com/YOUR_USERNAME/supply-chain-openenv
```

**Hugging Face Space URL:**
```
https://huggingface.co/spaces/YOUR_USERNAME/supply-chain-openenv
```

---

## 📋 Verification Before Submission

Your project includes:
- ✅ `inference.py` - Main entrypoint
- ✅ `app.py` - FastAPI server
- ✅ `openenv.yaml` - OpenEnv manifest
- ✅ `Dockerfile` - Container setup
- ✅ `pyproject.toml` - Dependencies
- ✅ `tests/` - Test suite
- ✅ 3 Tasks (easy, medium, hard)
- ✅ 6 Required endpoints (/reset, /step, /state, /tasks, /baseline, /grader)
- ✅ Deterministic graders (0.0-1.0)
- ✅ Reward shaping (not binary)

---

## 🔍 API Endpoints Check

When HF Space is live, verify:

```bash
curl https://YOUR_USERNAME-supply-chain-openenv.hf.space/reset?task=easy
curl https://YOUR_USERNAME-supply-chain-openenv.hf.space/tasks
curl https://YOUR_USERNAME-supply-chain-openenv.hf.space/baseline?episodes=1
```

All should return JSON responses.

---

## 📞 Support

If deployment fails:
1. Check Dockerfile is correct (uses Python 3.10)
2. Verify all dependencies in `pyproject.toml`
3. Ensure port 7860 is exposed
4. Check HF Space logs for errors

Good luck! 🎉
