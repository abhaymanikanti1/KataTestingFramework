#!/bin/bash
# Deploy KATA Testing Framework to GitHub

REPO_URL="https://github.com/abhaymanikanti1/KataTestingFramework.git"

echo "================================================================"
echo "🚀 Deploying KATA Testing Framework to GitHub"
echo "================================================================"
echo ""

cd "$(dirname "$0")"

# Initialize git
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
    git branch -M main
fi

# Configure remote
echo "🔗 Configuring remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "✅ Remote configured: $REPO_URL"

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Create commit
echo "💾 Creating commit..."
git commit -m "feat: Add KATA Testing Framework with API integration

- Integrated test comparison system with benchmark validation
- FastAPI server for serving degraded responses as JSON
- Azure Blob Storage integration for data persistence
- Microsoft Teams webhook alerts for test results
- GitHub Actions workflows for automated daily testing
- Complete documentation for frontend team and deployment
- Docker support for containerized deployment
" || echo "Already committed or no new changes"

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
echo "This may prompt for GitHub credentials..."
git push -u origin main --force

PUSH_STATUS=$?

echo ""
if [ $PUSH_STATUS -eq 0 ]; then
    echo "================================================================"
    echo "✅ Deployment Successful!"
    echo "================================================================"
    echo ""
    echo "🌐 Repository: https://github.com/abhaymanikanti1/KataTestingFramework"
    echo ""
    echo "📋 Next Steps:"
    echo ""
    echo "1. Configure GitHub Secrets:"
    echo "   https://github.com/abhaymanikanti1/KataTestingFramework/settings/secrets/actions"
    echo "   (See GITHUB_SECRETS.md for values)"
    echo ""
    echo "2. Test the Workflow:"
    echo "   https://github.com/abhaymanikanti1/KataTestingFramework/actions"
    echo "   → Click 'Daily API Testing & Deployment'"
    echo "   → Click 'Run workflow'"
    echo ""
    echo "3. Share with Frontend Team:"
    echo "   API URL: https://kata-api-v2.azurewebsites.net"
    echo "   Documentation: FRONTEND_QUICKSTART.md"
    echo ""
    echo "================================================================"
else
    echo "================================================================"
    echo "⚠️  Push failed or requires authentication"
    echo "================================================================"
    echo ""
    echo "If you need to authenticate:"
    echo "1. GitHub CLI: gh auth login"
    echo "2. Or use GitHub Desktop"
    echo "3. Or push manually: git push -u origin main"
    echo ""
    echo "================================================================"
fi
