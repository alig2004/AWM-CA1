from itertools import count
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from museums.models import Museum
import random

class Command(BaseCommand):
    help = "Populate the database with European museum data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing museums before populating",
        )

        
        #need to figure out how many we'll have before putting this in
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of cities to create (default: 100)",
        )
        

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing museums...")
            Museum.objects.all().delete()

        count = options["count"]

        #European museum data with coordinates and information
        european_museum_data = [
            #irish museums
            ("National Print Museum", "Dublin", "Ireland", 53.3355, -6.2346, 45831, 0.00, 1996, "art", "12:00", "16:00"),
            ("Crawford Art Gallery", "Cork", "Ireland", 51.9889, -8.4733, 265428, 0.00, 1850, "art", "10:00", "17:00"),
            ("Hunt Museum", "Limerick", "Ireland", 52.6663, -8.6245, 144942, 12.50, 1978, "art", "10:00", "17:00"),
            ("James Mitchell Geology Museum", "Galway", "Ireland", 53.2773, -9.0617, 18617, 0.00, 1852, "natural history", "10:00", "16:00"),
            ("Pearse Museum", "Dublin", "Ireland", 53.2829, -6.2816, 45831, 0.00, 1979, "natural history", "09:30", "17:30"),
            ("National Museum of Ireland - Natural History", "Dublin", "Ireland", 53.3398, -6.2530, 387412, 0.00, 1856, "natural history", "09:00", "17:00"),
            ("Hook Lighthouse", "Wexford", "Ireland", 52.1238, -6.9292, 8497, 15.00, 2001, "maritime", "09:30", "16:00"),
            ("Arklow Heritage Museum", "Arklow", "Ireland", 52.7985, -6.2346, 45831, 7.00, 1976, "maritime", "10:00", "17:00"),
            ("National Maritime Museum of Ireland", "Dublin", "Ireland", 53.2921, -6.1317, 18647, 10.00, 1978, "maritime", "11:00", "17:00"),
            ("Country Carlow Military Museum", "Carlow", "Ireland", 52.5036, -6.5543, 11829, 4.00, 1995, "military", "12:00", "16:00"),
            ("Duncannon Fort", "Wexford", "Ireland", 52.2208, -6.9367, 26782, 10.00, 1993, "military", "10:00", "16:45"),
            ("Elizabeth Fort", "Cork", "Ireland", 51.8945, -8.4776, 68427, 0.00, 1996, "military", "10:00", "17:00"),
            ("Blackrock Castle Observatory", "Cork", "Ireland", 51.5400, -8.2409, 97294, 0.00, 2007, "science", "10:00", "20:00"),
            ("Birr Castle Demesne", "Offaly", "Ireland", 53.0954, -7.9148, 14816, 14.00, 1996, "science", "09:00", "17:30"),
            ("Science Gallery", "Dublin", "Ireland", 53.3443, -6.2502, 286948, 0.00, 2008, "science", "12:00", "16:00"),
            ("National Transport Museum of Ireland", "Dublin", "Ireland", 53.3868, -6.0810, 26758, 5.50, 1949, "transport", "14:00", "17:00"),
            ("Cobh Heritage Centre", "Cobh", "Ireland", 51.8488, -8.2994, 187643, 15.00, 1993, "history", "09:30", "17:30"),
            ("Famine Warhouse 1848", "Ballingarry", "Ireland", 52.6193, -7.5229, 1818, 0.00, 2004, "history", "14:00", "16:00"),
            ("Glasnevin Cemetary", "Dublin", "Ireland", 53.2220, -6.1640, 187946, 17.00, 2010, "history", "09:00", "17:00"),
            ("Cork Waterworks", "Cork", "Ireland", 51.8951, -8.5092, 16078, 5.00, 2006, "technology", "09:00", "17:00"),
            ("Ye Olde Hurdy Gurdy Museum of Vintage Radio", "Howth", "Ireland", 53.3877, -6.0637, 3572, 5.00, 2003, "technology", "11:00", "17:00"),
            #("name", "city", "country", lat, lng, vis, price, yr, "type", "00:00", "00:00"),
        ]

        created_count = 0
        updated_count = 0

        #add the european museums
        for name, city, country, lat, lng, visitors, admission, established, museum_type, time_opened, time_closed in european_museum_data:
            if created_count >= count:
                break
            
            try:
                museum, created = Museum.objects.get_or_create(
                    name = name,
                    city = city, 
                    defaults = {
                        'country': country,
                        'latitude': lat, 
                        'longitude': lng, 
                        'location': Point(lng, lat, srid=4326), 
                        'elevation': random.randint(0,500), 
                        'visitors': visitors, 
                        'admission': admission, 
                        'established': established, 
                        'museum_type': museum_type, 
                        'time_opened': time_opened,
                        'time_closed': time_closed
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Created: {name}, {city}"))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"Already exists: {name}, {city}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating {name}: {e}"))


        #for random generation, will need to be edited
        
        if created_count < count:
            additional_needed = count - created_count
            self.stdout.write(f"Generating {additional_needed} additional museums...")

            # Check what fields actually exist in the model
            model_fields = [field.name for field in Museum._meta.get_fields()]
            self.stdout.write(f"Available model fields: {model_fields}")

            cities = ["Munich", "Strassbourg", "Florence", "Bilbao", "Krakow", "London", 
                    "Zwolle", "Antwerp", "Prague", "Budapest", "Vienna", 
                    "Gothenburg", "Copenhagen", "Helsinki", "Oslo", "Lisbon", "Athens"]

            countries = ["Germany", "France", "Italy", "Spain", "Poland", "United Kingdom", 
                        "Netherlands", "Belgium", "Czech Republic", "Hungary", "Austria", 
                        "Sweden", "Denmark", "Finland", "Norway", "Portugal", "Greece"]

            museum_types = ["art", "natural history", "maritime", "military", "science", "transport", "history", "technology"]

            for i in range(additional_needed):
                city = random.choice(cities)
                country = random.choice(countries)
                museum_name = f"Museum_{random.randint(1000, 9999)}"

                # Generate realistic European coordinates
                lat = random.uniform(35.0, 70.0)  # European latitude range
                lng = random.uniform(-10.0, 30.0)  # European longitude range

                visitors = random.randint(5000, 300000)

                try:
                    # Use get_or_create and only include fields that exist
                    museum_data = {
                        'visitors': visitors,
                        'latitude': lat,
                        'longitude': lng,
                        'location': Point(lng, lat, srid=4326),
                        'museum_type': random.choice(museum_types),
                    }

                    # Only add fields if they exist in the model
                    if 'elevation' in model_fields:
                        museum_data['elevation'] = random.randint(0, 800)
                    if 'admission' in model_fields:
                        museum_data['admission'] = random.uniform(0.00, 25.00)
                    if 'established' in model_fields:
                        museum_data['established'] = random.randint(1800, 2026)

                    museum, created = Museum.objects.get_or_create(
                        name=museum_name,
                        city=city,
                        country=country,
                        defaults=museum_data
                    )

                    if created:
                        created_count += 1
                        if created_count % 10 == 0:
                            self.stdout.write(f"Generated {created_count}/{count} museums...")
                    else:
                        self.stdout.write(f"Museum {museum_name} already exists")

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error generating city {museum_name}: {e}")
                    )
        

        self.stdout.write(self.style.SUCCESS(
            f"\nMuseum population complete \nCreated: {created_count} \nExisting: {updated_count} \nTotal museums in database: {Museum.objects.count()}"
        ))