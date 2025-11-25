Kata Testing Framework

Overview
--------
This repo runs scheduled KATA API tests, compares results with a benchmark (`compare.xlsx`), generates a degraded responses Excel report, uploads the report to SharePoint via a Power Automate webhook, and posts a Teams MessageCard alert with the SharePoint link.

What I changed locally
----------------------
- Removed generated artifacts and caches (see .gitignore)
- Added `.gitignore` to exclude venv, caches, logs and generated Excel files
- Ensured `integrated_test_comparison.py` is configured to run full tests (`TEST_LIMIT = None`)
- Added GitHub Actions workflow: `.github/workflows/daily-kata-test.yml` (runs daily at 8:00 AM IST)

How to push these changes to GitHub (run locally)
-------------------------------------------------
Replace the origin URL if needed and run:

```bash
# ensure you are in the project root
git remote add origin https://github.com/abhaymanikanti1/KataTestingFramework.git  # only if not set
git branch -M main
git add .
git commit -m "chore: cleanup, add .gitignore, add GitHub Actions workflow and README"
git push -u origin main
```

Set repository secrets (GitHub → Settings → Secrets and variables → Actions):
- `TEAMS_WEBHOOK_URL` - Teams Incoming Webhook URL
- `SHAREPOINT_UPLOAD_URL` - Power Automate HTTP trigger URL

How the workflow runs
---------------------
- Workflow file: `.github/workflows/daily-kata-test.yml`
- Schedule: daily at 8:00 AM IST (cron: `30 2 * * *` UTC runs at 2:30 UTC = 8:00 IST)
- It checks out the repo, installs dependencies from `requirements.txt`, and runs `python integrated_test_comparison.py`.

Run locally (immediate full run)
-------------------------------
To run all 300 questions locally now (takes time):

```bash
# activate your venv if you use one
. .venv/bin/activate
python integrated_test_comparison.py
```

Troubleshooting & notes
-----------------------
- The script may make HTTPS requests to a staging endpoint; you may see InsecureRequestWarning due to verify=False. Consider adding certificate verification in production.
- If Excel files are corrupted when uploading via Power Automate, check the Power Automate expression: `base64ToBinary(triggerBody()['fileContent'])` in the SharePoint Create File action.

Contact / Next steps
--------------------
Once you push, open Actions → Daily KATA Test and either wait for the scheduled run or click "Run workflow" to test immediately. If you want, paste the `git push` output here and I can help verify the workflow run and parse logs.
