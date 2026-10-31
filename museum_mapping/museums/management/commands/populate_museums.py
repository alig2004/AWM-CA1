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

        """
        need to figure out how many we'll have before putting this in
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of cities to create (default: 100)",
        )
        """

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing museums...")
            Museum.objects.all().delete()

        count = options["count"]

        #European museum data with coordinates and information
        european_museum_data = [
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
            ("Name", "City", "Country", 53.3355, 6.2346, 45831, 0.00, 1996, "type", "00:00", "00:00"),
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
        """
        if created_count < count:
            additional_needed = count - created_count
            self.stdout.write(f"Generating {additional_needed} additional cities...")

            # Check what fields actually exist in the model
            model_fields = [field.name for field in City._meta.get_fields()]
            self.stdout.write(f"Available model fields: {model_fields}")

            countries = ["Germany", "France", "Italy", "Spain", "Poland", "United Kingdom", 
                        "Netherlands", "Belgium", "Czech Republic", "Hungary", "Austria", 
                        "Sweden", "Denmark", "Finland", "Norway", "Portugal", "Greece"]

            city_types = ["regional", "town", "major"]

            for i in range(additional_needed):
                country = random.choice(countries)
                city_name = f"City_{random.randint(1000, 9999)}"

                # Generate realistic European coordinates
                lat = random.uniform(35.0, 70.0)  # European latitude range
                lng = random.uniform(-10.0, 30.0)  # European longitude range

                population = random.randint(50000, 1500000)
                area = random.uniform(20, 800)

                try:
                    # Use get_or_create and only include fields that exist
                    city_data = {
                        'population': population,
                        'latitude': lat,
                        'longitude': lng,
                        'location': Point(lng, lat, srid=4326),
                        'city_type': random.choice(city_types),
                    }

                    # Only add fields if they exist in the model
                    if 'urban_area_km2' in model_fields:
                        city_data['urban_area_km2'] = area
                    if 'population_density' in model_fields:
                        city_data['population_density'] = population / area
                    if 'gdp_per_capita' in model_fields:
                        city_data['gdp_per_capita'] = random.randint(20000, 70000)
                    if 'unemployment_rate' in model_fields:
                        city_data['unemployment_rate'] = random.uniform(2.0, 15.0)
                    if 'green_space_percentage' in model_fields:
                        city_data['green_space_percentage'] = random.uniform(8.0, 45.0)
                    if 'elevation' in model_fields:
                        city_data['elevation'] = random.randint(0, 800)
                    if 'region_code' in model_fields:
                        city_data['region_code'] = f"{country[:2].upper()}{random.randint(10, 99)}"
                    if 'population_year' in model_fields:
                        city_data['population_year'] = random.choice([2022, 2023])
                    if 'data_source' in model_fields:
                        city_data['data_source'] = 'Generated Data'

                    city, created = City.objects.get_or_create(
                        name=city_name,
                        country=country,
                        defaults=city_data
                    )

                    if created:
                        created_count += 1
                        if created_count % 10 == 0:
                            self.stdout.write(f"Generated {created_count}/{count} cities...")
                    else:
                        self.stdout.write(f"City {city_name} already exists")

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f" Error generating city {city_name}: {e}")
                    )
        """

        self.stdout.write(self.style.SUCCESS(
            f"\nMuseum population complete 
            \nCreated: {created_count} 
            \nExisting: {updated_count} 
            \nTotal museums in database: {Museum.object.count()}"
        ))