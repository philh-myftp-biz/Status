# Server Status

---

### Installation

1. Clone repository to *C* drive \
    `git clone https://github.com/philh-myftp-biz/Status C:\Scripts`
<br>

2. Add Console Profile to Windows Terminal \
    `& "C:\Scripts\Utils\Console\install.ps1"`
<br>

3. Activate Scheduled Tasks \
    TODO

---
### Configuration

1. Find your hostname without any dashes \
    `$hostname = ($env:COMPUTERNAME -replace '-', '')`
<br>

2. Open the *Items* folder in Explorer \
    `Set-Location "C:\Scripts\Items\"`
<br>

3. Copy the *PC1* configuration folder \
    `Copy-Item PC1 $hostname\ -Force -Recurse`
<br>

4. Open the copied folder in your chosen browser \
    `code $hostname` \
    `explorer $hostname`
<br>

5. Modify the configuration files \
    *(You can safely delete any files that contain empty lists)*

---