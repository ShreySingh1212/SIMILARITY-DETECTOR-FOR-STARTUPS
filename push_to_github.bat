@echo off
echo Fixing Git Configuration...
git config user.name "Shrey Singh"
git config user.email "shreysingh1212@github.com"

echo Committing files...
git commit -m "Initial commit: Complete Startup Similarity Detector"

echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo Done! Press any key to exit.
pause
