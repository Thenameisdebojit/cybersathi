@echo off
REM scripts\demo.bat
SET API_URL=%API_URL%
IF "%API_URL%"=="" SET API_URL=http://localhost:8000
SET ENDPOINT=%API_URL%/api/v1/complaints/

echo Creating demo complaint at %ENDPOINT%
curl -s -X POST "%ENDPOINT%" -H "Content-Type: application/json" -d ^
"{^
  \"name\": \"Demo User\",^
  \"phone\": \"+919900000000\",^
  \"language\": \"en\",^
  \"incident_type\": \"upi_scam\",^
  \"description\": \"Demo: lost money via UPI to a scammer\",^
  \"amount\": 2500^
}" > response.json

type response.json
del response.json
pause
