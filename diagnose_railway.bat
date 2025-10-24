@echo off
REM Railway Diagnosis Script for Windows
REM Run this and share the output

echo ==========================================
echo RAILWAY DEPLOYMENT DIAGNOSIS
echo ==========================================
echo.

echo 1. Checking Railway CLI...
railway --version
echo.

echo 2. Checking Railway Status...
railway status
echo.

echo 3. Checking Environment Variables...
railway variables
echo.

echo 4. Checking Recent Logs (last 100 lines)...
railway logs --lines 100
echo.

echo 5. Testing Django Check...
railway run python manage.py check
echo.

echo 6. Checking Migrations...
railway run python manage.py showmigrations
echo.

echo ==========================================
echo DIAGNOSIS COMPLETE
echo ==========================================
pause
