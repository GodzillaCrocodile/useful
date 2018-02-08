# ADUserCredentialsCheck.ps1 
# Script by Tim Buntrock 
# Run this script like ####PS C:\admin\Scripts\UserAccountAuthenticationCheck> .\ADUserCredentialsCheck.ps1 .\users.csv#### 
 
# users.csv look like -> 
# samaccountname,password 
# User1,PASSWORD1 
# User2,PASSWORD2 
 
param($UsersCsv) 
 
# specify function to test credentials 
Function Test-ADAuthentication { 
    param($samaccountname,$password) 
    (new-object directoryservices.directoryentry "",$samaccountname,$password).psbase.name -ne $null 
} 
 
# get domain infos 
$section = "search" 
import-module activedirectory 
$domobj = get-addomain 
$domain = $domobj.dnsroot # you can also specify another domain using $domain 
 
# import user data 
$data = import-csv $UsersCsv 
 
# verify all specified credentials, and output valid or invalid 
ForEach($rank in $data) { 
	$samaccountname = $rank.SamAccountName 
	$password = $rank.hash 
	if ($samaccountname -ne "") {
		if ($samaccountname -NotMatch ";") {
			if (Test-ADAuthentication "$domain\$samaccountname" "$password") { 
    			write-host "$samaccountname/$password >> CREDENTIALS VALID" -foregroundcolor "green" 
			} else { 
				write-host "$samaccountname/$password >> CREDENTIALS INVALID" -foregroundcolor "red" 
			} 
		} else {
			($samaccountname -split ";") | ForEach {
				if (Test-ADAuthentication "$domain\$_" "$password") {
					write-host "$_/$password >> CREDENTIALS VALID" -foregroundcolor "green" 
				} else {
					write-host "$_/$password >> CREDENTIALS INVALID" -foregroundcolor "red" 
				}
			}
			
		}
	}
}