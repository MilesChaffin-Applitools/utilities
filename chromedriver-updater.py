from urllib.request import urlopen
import json
import zipfile
import re
import io
import os

platforms = {
	"linux" : "linux64",
	"mac-arm" : "mac-arm64",
	"mac-intel" : "mac-x64",
	"windows" : "win64",
	"windows32" : "win32"
}

plat_override = "windows"
plat = ""

latest_versions_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

response = urlopen(latest_versions_url)

version_data = json.loads(response.read())


if plat_override == "":
	plat = input("What platform would you like? Options: " + str(list(platforms.keys())) + '\n')
	while plat not in platforms.keys():
		plat = input("That's not an option. Options: " + str(list(platforms.keys())) + '\n')
else:
	plat = plat_override

dl_link = ""
for p in version_data["channels"]["Stable"]["downloads"]["chromedriver"]:
	if p["platform"] == platforms[plat]:
		dl_link = p["url"]
		break
new_version = version_data["channels"]["Stable"]["version"]

with zipfile.ZipFile(io.BytesIO(urlopen(dl_link).read())) as zipf:
	for z in zipf.infolist():
		if z.is_dir():
			continue
		z.filename = os.path.basename(z.filename)
		zipf.extract(z)

print("Updated chromedriver to version " + new_version + "!")