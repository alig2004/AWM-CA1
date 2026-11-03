# Application description and features

# Set-up instructions
1. Clone this repository<br>
   `git clone https://github.com/alig2004/AWM-CA1.git`
2. Navigate to the clone
3. Navigate into museums_mapping folder
4. Launch docker
5. Build the container<br>
   `docker compose build`<br>
   `docker compose up`
6. Check that all aspects are running<br>
   `docker compose ps`
   This should return something like the following:
   <img width="1890" height="147" alt="image" src="https://github.com/user-attachments/assets/1e69ba3a-12c1-43b3-bd17-38e2b705fe1a" />

7. Add to database <br>
   To add to the database the first time or add further entries:<br>
   `docker compose run --rm web python manage.py populate_museums --count [c]`<br>
     Where [c] is the number of museums to be added to the database

   To clear the database and re-add entries:<br>
   `docker compose run --rm web python manage.py populate_museums --clear --count [c]`<br>
     Where [c] is the number of museums to be added to the database
   
8. Launch the site<br>
   Open your browser and input the following URL:<br>
   `localhost:8000`

# Technology stack
Python<br>
Django<br>
Django REST framework<br>
Django REST framework GIS<br>
PostGreSQL<br>
PostGIS<br>
HTML<br>
CSS<br>
JavaScript<br>
Bootstrap<br>
GeoJSON<br>
Docker<br>
Git/Github<br>
PGAdmin<br>
Leaflet<br>
Django Environ<br>
drf-spectacular<br>
pytest<br>

# Screenshots
Within the following screenshots, a database of 100 museums has been loaded in. 21 of these are based of pre-input details from populate_museums.py, the other 79 are randomised.

## Dashboard
### Upon first load
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/dcdd5abd-2dba-4e26-ba69-f309d23454d9" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/afbca2de-7de7-459f-842f-d65f87f3a6ce" />

### With OSM map toggled
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/34b2e1be-ed50-49a4-aa0b-6a64fe7c8306" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/6f0068ac-7271-41bd-875a-d9f5977ced79" />

### Untoggling Map Layers - Show All Museums
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/b159af3a-ca71-4c9d-ad2b-dca56c190edf" />

### Clicking on a museum
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/ddc0b15f-851a-44ed-8b64-d625132a8c64" />

## Filtering 
### Filtering by visitor count
#### Visitor count greater than 150,000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/4f16ff54-4cb1-4df5-9551-ac09cfffcddd" />

#### Visitor count less than 150,000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/d3f0461a-6568-451f-9459-d702a03d0a42" />

#### Visitor count between 10,000 and 100,000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/9591a51f-97b8-457a-afbd-b383bd835b58" />

### Filtering by admission price
#### Admission greater than €15
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/c6d6e058-d24c-48f9-90c2-089939cb9810" />

#### Admission less than €15
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/3af426ce-64f4-418e-99ec-e092e73a2e29" />

#### Admission between €5 and €15
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/6c3b0c17-232e-4812-b20d-5b51f2610629" />

### Filtering by year of establishment
#### Established after 2000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/badf8457-431f-4c69-9bd7-8ca8581c7797" />

#### Established before 2000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/658dab07-d5ce-4ee3-ba8b-051081183638" />

#### Established between 1900 and 2000
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/e23a24c0-abf3-475c-a6be-6cc32a8b75c7" />

### Filtering by city - Dublin
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/061393fc-0fbd-4682-8b58-2031ffbee371" />

### Filtering by museum type - Natural History
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/210f0071-2fdc-47ed-979b-8d71bfeb849a" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/a2fb485b-ee7c-4754-80e0-d6938cbd1c09" />

### Spatial query - Museums nearby Famine Warhouse 1848
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/233863f0-10f0-4e13-bc93-d03ee5c323db" />
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/b258bcef-984b-4d9a-bfeb-c7f6843ff938" />

# Issues and limitations
1. Unable to read opening and closing hours <br>
   <img width="303" height="47" alt="image" src="https://github.com/user-attachments/assets/ea136a43-6e7b-4802-84b2-5b60fd4d0fee" /><br>
   Opening and closing hours don't appear, instead showing as Unknown

2. Only one spatial query - nearby() <br>
   I was unable to find enough time to get multiple spatial queries working, therefore only one exists. Given more time I was going to implement a way to set a bounding box and find museums within this space, but this idea had to be scrapped.

3. Minimal real data <br>
   Due to a lack of datasets, the only real museum data I was able to add to populate_museums.py were 21 Irish museums, with the rest being randomly generated. Given enough time I would have liked to do other European museums, but the lack or pre-formatted data made this difficult and ultimately not worth the time.
