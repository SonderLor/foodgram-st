import csv
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Load ingredients from JSON or CSV file"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="Path to the data file")
        parser.add_argument(
            "--format",
            type=str,
            default="json",
            choices=["json", "csv"],
            help="Format of the data file (json or csv)",
        )

    def handle(self, *args, **options):
        path = options.get("path")
        if not path:
            path = (
                Path(__file__).resolve().parent.parent.parent.parent
                / "data"
                / "ingredients.json"
            )

        file_format = options.get("format")

        try:
            if file_format == "json":
                self.load_from_json(path)
            elif file_format == "csv":
                self.load_from_csv(path)

            self.stdout.write(
                self.style.SUCCESS("Ingredients were successfully loaded")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error loading ingredients: {str(e)}")
            )

    def load_from_json(self, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                Ingredient.objects.get_or_create(
                    name=item["name"],
                    measurement_unit=item["measurement_unit"],
                )

    def load_from_csv(self, path):
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1]
                    )
