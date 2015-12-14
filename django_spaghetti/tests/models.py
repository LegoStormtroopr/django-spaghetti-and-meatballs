from django.db import models

class PoliceOfficer(models.Model):
    """
    An officer of the NYPD.
    E.g. "Jake Peralta"
    """
    badge_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    rank = models.CharField(max_length=200)
    
    arrests = models.ManyToManyField("Arrest",related_name="arresting_officers")
    station = models.ForeignKey("PoliceStation",related_name="officers")

class PoliceStation(models.Model):
    pass

class Precinct(PoliceStation):
    """
    A precinct of officers
    E.g. "Brookyln 99"
    """
    number = models.IntegerField(primary_key=True)
    burrough = models.CharField(max_length=20)
    captain = models.OneToOneField(PoliceOfficer)
    class Meta:
        unique_together = ("burrough","number")
    def natural_key(self):
        return (self.burrough,self.number)

class Division(PoliceStation):
    """
    A division of officers, not in the field.
    E.g. Major Crimes Unit
    """
    name = models.CharField(max_length=200)
    
class Arrest(models.Model):
    alleged_crime = models.CharField(max_length=20)
    perp = models.ForeignKey("Perpetrator")

class Perpetrator(models.Model):
    """
    A person who is accused of a crime.
    E.g. Doug Judy, aka. "The Pontiac Bandit"
    """
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
