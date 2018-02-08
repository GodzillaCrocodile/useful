$domains = "domain1.test.net","domain2.test.net"
ForEach ($domain in $domains) {
	Import-csv -Path input.csv -delimiter "," | ForEach {
		$details = @{
			email = $_.email
			status = ''
			hash = ''
			DisplayName = ''
			SamAccountName = ''
			Department = ''
			Title = ''
			telephoneNumber = ''
			domain = ''
		}
		$result = Get-ADUser -Filter "EmailAddress -eq '$($_.email)'" -Server $domain -Properties DisplayName, EmailAddress, SamAccountName, Department, Title, telephoneNumber
		if ($result -ne $Null) {
			Write-Host "User exists:$($_.email) in $domain" -fore green
			$details.domain = $domain
			$details.status = 'Found'
			$details.hash = $_.hash
			$details.SamAccountName = $result.SamAccountName-Join ';'
			$details.DisplayName = $result.DisplayName-Join ';'
			$details.Department = $result.Department-Join ';'
			$details.Title = $result.Title-Join ';'
			$details.telephoneNumber = $result.telephoneNumber-Join ';'
		}
		else {
				#Write-Warning "User $($_.email) not found"
				$details.status = 'Not Found'
		}
		New-Object PsObject -Property $details
	} | Export-Csv out.csv -NoTypeInformation -Encoding Unicode -Append
}

#$a = out.csv
#(Get-Content $a) | Foreach-Object {$_ -replace '"', ''} | Out-File $a