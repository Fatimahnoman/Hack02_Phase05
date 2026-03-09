$ErrorActionPreference = "Stop"
Set-Location "C:\Users\LENOVO\Downloads\Hackhtahon2-Phase-5-main\Hackhtahon2-Phase-5-main"
git add .
git commit --amend -m "Initial commit: Todo app with Dapr, Kafka, and OKE deployment"
git push -u origin master --force
