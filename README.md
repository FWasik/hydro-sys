# Hydroponic System Management
## Introduction


Hydroponic System Management (or hydro-sys) was developed as part of the recruitment process. The main goal was to create an application to manage various hydroponic systems by creating, reading, updating and deleting them. The application also allows users to manage measurements for various hydroponic systems stored in a database.

## How to run and use the application

First, rename the `env_example.txt` file to `.env` and update the environment variables as needed. After that, start Docker Compose by running the following command:
```
docker compose up
```

Next, you need to create a superuser. To do this, attach to the running container using:
```
docker exec -it <name_of_container> sh
```

Then, run:
```
python manage.py createsuperuser
```

In my case, `<name_of_container>` is `hydro-sys-backend`.

No need to worry about migrations - they are applied automatically when the container starts. Also, if you want to create new users, you must do so via the admin panel.

You can debug the application, there is already the configuration for vscode in `.vscode/launch.json`. In Visual Studio Code switch to `Run and Debug` view, change to `Python Debugger: Remote Attach` and press F5 button.

And that’s it! You can now use the application freely.


## How the application is built

There are two main models for this application: 

- HydroponicSystem:
    ```python
    class HydroponicSystem(models.Model):
        types = [
            ("NFT", "Nutrient Film Technique"),
            ("DWC", "Deep Water Culture"),
            ("Ebb and Flow", "Ebb and Flow"),
            ("Aeroponics", "Aeroponics"),
            ("Drip", "Drip System"),
            ("Wick", "Wick System"),
        ]

        name = models.CharField(max_length=125, unique=True)
        timestamp = models.DateTimeField(auto_now_add=True)
        owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systems")
        type = models.CharField(max_length=50, choices=types)
        description = models.TextField(blank=True, null=True)

        def __str__(self):
            return self.name
    ```

- Measurement:
  ```python
    class Measurement(models.Model):
        system = models.ForeignKey(
            HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
        )
        ph = models.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(14)],
            help_text="In the pH scale (0-14)",
        )
        temperature = models.FloatField(
            validators=[MinValueValidator(-1000), MaxValueValidator(1000)],
            help_text="In Celcius (°C)",
        )
        tds = models.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(1000000)],
            help_text="Parts per million (ppm)",
        )
        timestamp = models.DateTimeField(auto_now_add=True)
        description = models.TextField(blank=True, null=True)
  ```

The app supports pagination, ordering, and filtering of data. The data is paginated when listing `HydroponicSystem` and `Measurement` records. Assigned `Measurement` records are also returned and paginated when a user retrieves a single `HydroponicSystem` record. There are 10 values per page.

`HydroponicSystem` can be ordered by:
- timestamp
- name
- type

`Measurement` by:
- ph
- tds
- temperature
- timestamp
- system


Filtering is handled by the following classes:
```python
    class BaseFilter(django_filters.FilterSet):
    datetime_from = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="gte", label="From Datetime"
    )
    datetime_to = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="lte", label="To Datetime"
    )

    class Meta:
        abstract = True


class MeasurementFilter(BaseFilter):
    ph_min = django_filters.NumberFilter(
        field_name="ph", lookup_expr="gte", label="Min pH"
    )
    ph_max = django_filters.NumberFilter(
        field_name="ph", lookup_expr="lte", label="Max pH"
    )
    tds_min = django_filters.NumberFilter(
        field_name="tds", lookup_expr="gte", label="Min TDS"
    )
    tds_max = django_filters.NumberFilter(
        field_name="tds", lookup_expr="lte", label="Max TDS"
    )
    temperature_min = django_filters.NumberFilter(
        field_name="temperature", lookup_expr="gte", label="Min Temperature"
    )
    temperature_max = django_filters.NumberFilter(
        field_name="temperature", lookup_expr="lte", label="Max Temperature"
    )

    class Meta:
        model = Measurement
        fields = ("ph", "tds", "temperature", "timestamp")


class HydroponicSystemFilter(BaseFilter):
    type = django_filters.ChoiceFilter(choices=HydroponicSystem.types)

    class Meta:
        model = HydroponicSystem
        fields = ("type", "timestamp")
  ```

Each field can be used in the URL to filter data based on your preferences. Remember, the application supports JWT, so to perform any action across the app, you must first obtain an access token. The app includes features that prevent users from performing any actions on records they do not own.

Here are a few examples of endpoints:

- http://localhost:8000/systems/measurements/?datetime_to=2025-02-06T12:24:22.976956Z&datetime_from=2025-02-06T10:22:05.771700Z
- http://localhost:8000/systems/measurements/?ph_min=7&tds_max=500.10&temperature_min=1&ordering=ph
- http://localhost:8000/systems/hydroponic/?type=DWC&ordering=-timestamp


Swagger is also included in the app. Swagger is also included in the app. I am aware that the Swagger configuration is quite basic, but I wanted to keep it as simple as possible. Here are the links (remember to start the app first):

- [Swagger](http://localhost:8000/swagger/)
- [REDOC delivered by Swagger](http://localhost:8000/redoc/)


## How you can run unittests
To run unittests, you need to attach to the running container exactly as shown in the second paragraph. Then, run the following command:

```
python manage.py test
```

And that’s all!