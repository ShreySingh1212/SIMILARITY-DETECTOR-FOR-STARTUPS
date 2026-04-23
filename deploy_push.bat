@echo off
echo Committing memory optimizations...
git add .
git commit -m "Optimize memory for Render free tier by replacing PyTorch with HuggingFace API"

echo Pushing to GitHub...
git push -u origin main

echo Done! The code has been successfully pushed.
