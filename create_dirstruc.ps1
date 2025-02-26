# PowerShell Script to Create Project Directory Structure for Vendor Shop Management System
# This script creates only the directories, no files

# Set the root directory name
$rootDir = "vendor_shop_management"

# Create the root directory if it doesn't exist
if (-not (Test-Path $rootDir)) {
    New-Item -Path $rootDir -ItemType Directory | Out-Null
    Write-Host "Created root directory: $rootDir"
}

# Define all directories to create
$directories = @(
    "src",
    "src\api",
    "src\core",
    "src\crud",
    "src\db",
    "src\models",
    "src\schemas",
    "src\services",
    "static",
    "migrations",
    "migrations\versions",
    "tests",
    "tests\test_api",
    "tests\test_crud",
    "tests\test_services"
)

# Create directories
foreach ($dir in $directories) {
    $path = Join-Path -Path $rootDir -ChildPath $dir
    if (-not (Test-Path $path)) {
        New-Item -Path $path -ItemType Directory | Out-Null
        Write-Host "Created directory: $path"
    }
}

Write-Host "`nDirectory structure for $rootDir has been created successfully!"