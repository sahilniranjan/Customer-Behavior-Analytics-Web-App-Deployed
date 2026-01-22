#!/bin/bash

# Quick deployment script for GitHub
echo "🚀 Preparing Customer Behavior Analytics for deployment..."

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git branch -M main
fi

# Check for GitHub username
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username is required!"
    exit 1
fi

# Create repository name
repo_name="customer-behavior-analytics"

echo ""
echo "📝 Next steps:"
echo "1. Create a new repository on GitHub: https://github.com/new"
echo "   - Repository name: $repo_name"
echo "   - Keep it PUBLIC (required for free tier hosting)"
echo "   - Don't initialize with README"
echo ""
echo "2. After creating the repository, press Enter to continue..."
read -p ""

# Add all files
echo "Adding files to git..."
git add .

# Commit
echo "Creating commit..."
git commit -m "Initial commit - Customer Behavior Analytics App ready for deployment"

# Add remote
echo "Adding GitHub remote..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "📋 Repository URL: https://github.com/$github_username/$repo_name"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com (recommended) or https://railway.app"
echo "2. Sign up and connect your GitHub account"
echo "3. Deploy both services (API and Dashboard)"
echo "4. See DEPLOYMENT.md for detailed instructions"
echo ""
echo "🌟 Good luck with your deployment!"
