#!/bin/bash

# PUSH_TO_GITHUB.sh - Manual push script with token support
# Usage: ./PUSH_TO_GITHUB.sh [GITHUB_TOKEN]

echo "🚀 Pushing to GitHub Repository..."
echo ""

# Check if token is provided as argument
if [ -n "$1" ]; then
    echo "📝 Using provided GitHub token..."
    git remote set-url origin "https://$1@github.com/abhaymanikanti1/KataTestingFramework.git"
else
    echo "⚠️  No token provided. Using existing credentials."
    echo "   If push fails, run: ./PUSH_TO_GITHUB.sh YOUR_GITHUB_TOKEN"
    echo ""
fi

# Show current remote
echo "📍 Remote URL configured:"
git remote get-url origin | sed 's/https:\/\/.*@/https:\/\/[TOKEN]@/'
echo ""

# Push to GitHub
echo "📤 Pushing to main branch..."
if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🔗 Repository: https://github.com/abhaymanikanti1/KataTestingFramework"
    echo ""
    echo "📋 Next steps:"
    echo "1. Configure GitHub Secrets: https://github.com/abhaymanikanti1/KataTestingFramework/settings/secrets/actions"
    echo "2. Add the 6 required secrets (see GITHUB_SECRETS.md)"
    echo "3. Test the workflow: https://github.com/abhaymanikanti1/KataTestingFramework/actions"
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "🔧 To fix authentication, try:"
    echo "1. Create token: https://github.com/settings/tokens/new (with 'repo' scope)"
    echo "2. Run: ./PUSH_TO_GITHUB.sh YOUR_GITHUB_TOKEN"
    echo "   OR"
    echo "3. Run: gh auth login (and select abhaymanikanti1 account)"
    echo "   Then: git push -u origin main"
    exit 1
fi
