# PowerShell script to test the Ingestion API

Write-Host "Testing DevSecOps AI Agent Ingestion API..." -ForegroundColor Cyan
Write-Host ""

$uri = "http://127.0.0.1:5000/api/traffic"

$body = @{
    method = "POST"
    url = "https://example.com/api/login"
    headers = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer weak-token-123"
    }
    body = '{"username":"admin","password":"password123"}'
    response_status = 200
    response_headers = @{
        "Content-Type" = "application/json"
    }
    response_body = '{"token":"abc123","user_id":1}'
} | ConvertTo-Json

try {
    Write-Host "Sending test traffic data to API..." -ForegroundColor Yellow
    Write-Host "URL: $uri" -ForegroundColor Gray
    Write-Host ""
    
    $response = Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/json" -Body $body
    
    Write-Host "Success!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Cyan
    $response | ConvertTo-Json | Write-Host
    
    Write-Host ""
    Write-Host "Check the Flask API terminal for the workflow execution..." -ForegroundColor Yellow
    
} catch {
    Write-Host "Error!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the Flask API is running on http://127.0.0.1:5000" -ForegroundColor Yellow
    Write-Host "Run: python ingestion_api.py" -ForegroundColor Gray
}
