@Echo Off
setlocal enabledelayedexpansion

for /r %%a in (*.py) do (
  set FILENAME=%%a
  
  set check=!FILENAME:~-6,-3!
  if  not "!check!" == "sql" (
	if  not "!check!" == "t__" (
		if  not "!check!" == "ger" (echo ===========================  Search in !FILENAME! ===========================') 
	)



  )

)
pause
