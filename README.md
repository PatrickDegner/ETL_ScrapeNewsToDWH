# ScrapeNewsToDWH
<br>
This tool scrapes (Extracts) Liveblog News, puts them into a "Fake" Staging-DWH,<br>
(Transforms) the data and (Loads) it into the Core DWH <br>
Fully run on Docker Container


# ETL Python Script
## Extract:
The data is extracted with beautifulsoup4 webscraping. <br>
Pushed into a "Fake" Staging-DWH to be Transformed.
<br>

## Transform:
Cleaned up with the help of regex.
<br>

## Load:
Loaded into the Core DWH fact<br>
![image](https://user-images.githubusercontent.com/108484798/182218304-f1573340-2d8b-48a6-9b0c-bf0f8cce9470.png) <br>
Also into its News_dimension<br>
![image](https://user-images.githubusercontent.com/108484798/182218524-c3f46712-9e32-414b-aadc-daf88000a600.png) <br>
As well the Date_dimension is created<br>
![image](https://user-images.githubusercontent.com/108484798/182218919-2930a20f-7ec9-4836-9fd1-87127ad2e5a9.png)

