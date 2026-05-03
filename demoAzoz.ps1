# demo.ps1

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("destroy", "restore")]
    [string]$Action
)

if ($Action -eq "destroy") {
    Write-Host "<<>> DESTROYING all AWS resources..." 
    cd C:\Users\azooo\mycodes\part2\url-processor-serverless\infrastructure
    terraform destroy -auto-approve
    Write-Host "✅ Everything destroyed!" 
}

if ($Action -eq "restore") {
    Write-Host "<<>> 1 Terraform init and apply..." 
    cd C:\Users\azooo\mycodes\part2\url-processor-serverless\infrastructure
    terraform init
    terraform apply -auto-approve

    Write-Host "<<>> 2 Login to ECR..." 
    $password = aws ecr get-login-password --region us-east-1
    $password | docker login --username AWS --password-stdin 530467655445.dkr.ecr.us-east-1.amazonaws.com

    Write-Host "<<>> 3 Build and push API image..." 
    cd C:\Users\azooo\mycodes\part2\url-processor-serverless\api-service
    docker buildx build --platform linux/amd64 --provenance=false `
        -t 530467655445.dkr.ecr.us-east-1.amazonaws.com/url-processor-api:latest `
        --push .

    Write-Host "<<>> 4 Build and push Worker image..." 
    cd C:\Users\azooo\mycodes\part2\url-processor-serverless\worker-service
    docker buildx build --platform linux/amd64 --provenance=false `
        -t 530467655445.dkr.ecr.us-east-1.amazonaws.com/url-processor-worker:latest `
        --push .

    Write-Host "<<>> 5 Update Lambda functions..." 
    aws lambda update-function-code `
        --function-name url-processor-api `
        --image-uri 530467655445.dkr.ecr.us-east-1.amazonaws.com/url-processor-api:latest

    aws lambda update-function-code `
        --function-name url-processor-worker `
        --image-uri 530467655445.dkr.ecr.us-east-1.amazonaws.com/url-processor-worker:latest

    Write-Host ">><< Everything restored and live!" 
    cd C:\Users\azooo\mycodes\part2\url-processor-serverless\infrastructure
    terraform output
}