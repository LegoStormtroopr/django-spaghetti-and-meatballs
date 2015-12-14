from django.db import models

class PoliceOfficer(models.Model):
    """
    An officer of the NYPD
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
    number = models.IntegerField(primary_key=True)
    burrough = models.CharField(max_length=20)
    captain = models.OneToOneField(PoliceOfficer)
    class Meta:
        unique_together = ("burrough","number")
    def natural_key(self):
        return (self.burrough,self.number)

class Division(PoliceStation):
    name = models.CharField(max_length=200)
    
class Arrest(models.Model):
    alleged_crime = models.CharField(max_length=20)
    perp = models.ForeignKey("Perpetrator")

class Perpetrator(models.Model):
    first_name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
